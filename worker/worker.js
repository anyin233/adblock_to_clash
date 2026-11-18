/**
 * Cloudflare Worker for Adblock to Clash/Stash rule conversion
 * Usage: https://worker.cf.com/easylist-downloads.adblockplus.org/easylist.txt
 *        https://worker.cf.com/https://easylist-downloads.adblockplus.org/easylist.txt?format=domain
 *
 * Supported formats:
 * - clash (default): Clash YAML format with DOMAIN-SUFFIX rules
 * - domain: Stash domain format, one domain per line
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.slice(1); // Remove leading slash
    const format = url.searchParams.get('format') || 'clash'; // Get format parameter

    // Require a path
    if (!path) {
      return new Response('Usage: Append rule source URL to this worker URL\nExample: https://worker.example.com/easylist-downloads.adblockplus.org/easylist.txt\nSupported formats: ?format=clash (default) or ?format=domain', {
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
        status: 400,
      });
    }

    // Validate format parameter
    if (format !== 'clash' && format !== 'domain') {
      return new Response(JSON.stringify({
        error: 'Invalid format parameter. Use "clash" or "domain"',
        format: format,
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    try {
      // Normalize the rule source URL
      const ruleUrl = normalizeUrl(path);

      // Download rules from the source
      console.log(`Fetching rules from: ${ruleUrl}`);
      const ruleContent = await downloadRules(ruleUrl);

      // Parse Adblock rules
      const domains = parseAdblockRules(ruleContent);

      // Convert based on requested format
      let convertedRules;
      let contentType;

      if (format === 'domain') {
        convertedRules = convertToDomain(domains);
        contentType = 'text/plain; charset=utf-8';
      } else {
        convertedRules = convertToClash(domains);
        contentType = 'text/yaml; charset=utf-8';
      }

      // Return the converted rules
      return new Response(convertedRules, {
        headers: {
          'Content-Type': contentType,
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
        },
      });

    } catch (error) {
      return new Response(JSON.stringify({
        error: error.message,
        path: path,
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }
  }
};

/**
 * Normalize URL or domain to a valid URL
 */
function normalizeUrl(urlOrDomain) {
  let url = urlOrDomain.trim();
  
  // If it already starts with http:// or https://, return as is
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }
  
  // Otherwise, prepend https://
  return `https://${url}`;
}

/**
 * Download rules from URL
 */
async function downloadRules(url) {
  const response = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to download rules: ${response.status} ${response.statusText}`);
  }
  
  return await response.text();
}

/**
 * Parse Adblock format rules and extract domains
 */
function parseAdblockRules(content) {
  const domains = new Set();
  const lines = content.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // Skip empty lines
    if (!trimmed) continue;
    
    // Skip comments and metadata
    if (trimmed.startsWith('!') || trimmed.startsWith('[')) continue;
    
    // Skip exception rules
    if (trimmed.startsWith('@@')) continue;
    
    // Extract domain from ||domain.com^ format
    const domain = extractDomain(trimmed);
    if (domain) {
      domains.add(domain.toLowerCase());
    }
  }
  
  return Array.from(domains).sort();
}

/**
 * Extract domain from an Adblock rule
 */
function extractDomain(rule) {
  // Match ||domain.com^ pattern
  if (!rule.startsWith('||')) {
    return null;
  }
  
  // Remove || prefix
  let domain = rule.slice(2);
  
  // Remove ^ suffix and any options
  if (domain.includes('^')) {
    domain = domain.split('^')[0];
  }
  
  // Remove any path after domain
  if (domain.includes('/')) {
    domain = domain.split('/')[0];
  }
  
  // Remove any port number
  if (domain.includes(':')) {
    domain = domain.split(':')[0];
  }
  
  // Validate domain format
  if (isValidDomain(domain)) {
    return domain;
  }
  
  return null;
}

/**
 * Check if string is a valid domain
 */
function isValidDomain(domain) {
  if (!domain || domain.length > 253) {
    return false;
  }
  
  const parts = domain.split('.');
  if (parts.length < 2) {
    return false;
  }
  
  // Check each label
  for (const part of parts) {
    if (!part || part.length > 63) {
      return false;
    }
    if (!/^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$/.test(part)) {
      return false;
    }
  }
  
  return true;
}

/**
 * Convert domains to Clash YAML format
 */
function convertToClash(domains) {
  const rules = domains.map(domain => `  - DOMAIN-SUFFIX,${domain}`);
  return `payload:\n${rules.join('\n')}\n`;
}

/**
 * Convert domains to Stash domain format (one domain per line)
 * Uses leading dot notation for wildcard matching
 */
function convertToDomain(domains) {
  // Add leading dot to each domain for wildcard matching
  const domainList = domains.map(domain => `.${domain}`);
  return domainList.join('\n') + '\n';
}
