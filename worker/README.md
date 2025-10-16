# Cloudflare Worker - Adblock to Clash Converter

A Cloudflare Worker that converts Adblock format rules to Clash ruleset format on-demand.

## Features

- 🚀 On-demand conversion via HTTP requests
- 🔄 Automatic rule downloading and parsing
- ✨ Domain deduplication
- 📦 Clash DOMAIN-SUFFIX format output
- ⚡ 1-hour cache for performance
- 🌐 CORS enabled for API usage
- 📝 Interactive HTML interface

## Deployment

### Prerequisites

- [Node.js](https://nodejs.org/) (v16 or later)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- Cloudflare account

### Installation

1. Install Wrangler CLI:
```bash
npm install -g wrangler
```

2. Login to Cloudflare:
```bash
wrangler login
```

3. Deploy the worker:
```bash
cd worker
wrangler deploy
```

The worker will be deployed to a `*.workers.dev` subdomain.

## Usage

### Method 1: Domain Only

Append a domain name to the worker URL:

```
https://your-worker.workers.dev/easylist-downloads.adblockplus.org/easylist.txt
```

### Method 2: Full URL

Append a complete URL to the worker URL:

```
https://your-worker.workers.dev/https://easylist-downloads.adblockplus.org/easylist.txt
```

## Integration with Clash

Use the worker in your Clash configuration:

```yaml
rule-providers:
  easylist:
    type: http
    behavior: domain
    url: "https://your-worker.workers.dev/easylist-downloads.adblockplus.org/easylist.txt"
    interval: 86400
    path: ./rulesets/easylist.yaml

rules:
  - RULE-SET,easylist,REJECT
```

## API Response

The worker returns rules in Clash YAML format:

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
  - DOMAIN-SUFFIX,test.org
  - DOMAIN-SUFFIX,sample.net
```

## Configuration

Edit `wrangler.toml` to customize:

- `name`: Worker name
- `compatibility_date`: Cloudflare compatibility date
- `routes`: Custom domain routes (optional)

### Custom Domain (Optional)

To use a custom domain:

1. Add a route in `wrangler.toml`:
```toml
routes = [
  { pattern = "worker.example.com/*", zone_name = "example.com" }
]
```

2. Configure DNS in Cloudflare dashboard:
   - Add a CNAME record pointing to your worker

## Performance

- **Caching**: Responses are cached for 1 hour
- **Timeout**: 50 seconds (Cloudflare Worker limit)
- **Memory**: Optimized for large rule sets (tested with 400K+ domains)

## Supported Rule Formats

The worker parses Adblock domain-based rules:

- `||example.com^` → `DOMAIN-SUFFIX,example.com`
- `||subdomain.example.com^` → `DOMAIN-SUFFIX,subdomain.example.com`

**Filtered out:**
- Comments (lines starting with `!` or `[`)
- Exception rules (lines starting with `@@`)
- Invalid domains

## Error Handling

If the conversion fails, the worker returns a JSON error:

```json
{
  "error": "Failed to download rules: 404 Not Found",
  "path": "invalid-domain.com"
}
```

## Development

### Local Testing

Use Wrangler to test locally:

```bash
wrangler dev
```

Then access at `http://localhost:8787/`

### Testing the Worker

```bash
# Test with a domain
curl https://your-worker.workers.dev/easylist-downloads.adblockplus.org/easylist.txt

# Test with a full URL
curl "https://your-worker.workers.dev/https://easylist-downloads.adblockplus.org/easylist.txt"
```

## Monitoring

Monitor your worker in the Cloudflare dashboard:
- Request count
- Error rate
- CPU time
- Bandwidth usage

## Limitations

- Cloudflare Worker CPU time: 50ms per request (can be extended)
- Response size: 10MB (sufficient for most rule sets)
- Only supports domain-based Adblock rules

## Security

- No data is stored permanently
- CORS enabled for public API access
- All requests are logged in Cloudflare dashboard

## License

Same as the parent project (MIT License).

## Troubleshooting

### Worker not responding
- Check Cloudflare dashboard for errors
- Verify the worker is deployed: `wrangler deployments list`

### Conversion errors
- Ensure the source URL is accessible
- Check if the source provides valid Adblock rules
- Review worker logs: `wrangler tail`

### Cache issues
- Cache is set to 1 hour by default
- To force refresh, redeploy the worker or wait for cache expiration

## Support

For issues and questions, refer to:
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Project Repository](https://github.com/yourusername/rule_converter)
