"""Adblock rule parser module."""
import re
from typing import List, Set


class AdblockParser:
    """Parses Adblock format rules."""
    
    def __init__(self):
        """Initialize the parser."""
        # Common Adblock rule patterns
        self.domain_pattern = re.compile(r'^\|\|([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\^?')
        self.comment_pattern = re.compile(r'^[!\[]')
        
    def parse(self, content: str) -> Set[str]:
        """Parse Adblock rules and extract domains.
        
        Args:
            content: Raw Adblock rules content
            
        Returns:
            Set of domain strings
        """
        domains = set()
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip comments and metadata
            if self.comment_pattern.match(line):
                continue
            
            # Skip exception rules (start with @@)
            if line.startswith('@@'):
                continue
            
            # Extract domain from ||domain.com^ format
            domain = self._extract_domain(line)
            if domain:
                domains.add(domain)
        
        return domains
    
    def _extract_domain(self, rule: str) -> str:
        """Extract domain from an Adblock rule.
        
        Args:
            rule: Single Adblock rule line
            
        Returns:
            Extracted domain or empty string if not a domain rule
        """
        # Match ||domain.com^ pattern
        if rule.startswith('||'):
            # Remove || prefix
            rule = rule[2:]
            
            # Remove ^ suffix and any options
            if '^' in rule:
                rule = rule.split('^')[0]
            
            # Remove any path after domain
            if '/' in rule:
                rule = rule.split('/')[0]
            
            # Remove any port number
            if ':' in rule:
                rule = rule.split(':')[0]
            
            # Validate domain format
            if self._is_valid_domain(rule):
                return rule.lower()
        
        return ''
    
    def _is_valid_domain(self, domain: str) -> bool:
        """Check if string is a valid domain.
        
        Args:
            domain: Domain string to validate
            
        Returns:
            True if valid domain, False otherwise
        """
        if not domain or len(domain) > 253:
            return False
        
        # Basic domain validation
        parts = domain.split('.')
        if len(parts) < 2:
            return False
        
        # Check each label
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', part):
                return False
        
        return True
