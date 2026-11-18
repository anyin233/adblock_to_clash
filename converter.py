"""Clash rule converter module."""
import yaml
from typing import Set, List
from pathlib import Path


class ClashConverter:
    """Converts domains to Clash ruleset format."""
    
    def __init__(self, rule_type: str = "domain-suffix"):
        """Initialize the converter.
        
        Args:
            rule_type: Type of Clash rule (domain-suffix, domain, domain-keyword)
        """
        self.rule_type = rule_type.upper().replace("-", "-")
    
    def convert(self, domains: Set[str], output_path: str = "output.yaml", rule_type: str = "domain-suffix") -> None:
        """Convert domains to Clash ruleset format and save to file.
        
        Args:
            domains: Set of domain strings
            output_path: Path to save the output file
            rule_type: Type of Clash rule (domain-suffix, domain, domain-keyword)
        """
        # Deduplicate by using set (already done) and sort for consistency
        sorted_domains = sorted(domains)
        
        # Build Clash ruleset structure based on rule type
        rule_prefix = rule_type.upper().replace("-", "-")
        payload = [f"{rule_prefix},{domain}" for domain in sorted_domains]
        
        # Create the ruleset structure
        ruleset = {
            'payload': payload
        }
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(ruleset, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def get_stats(self, domains: Set[str]) -> dict:
        """Get statistics about the domains.
        
        Args:
            domains: Set of domain strings
            
        Returns:
            Dictionary with statistics
        """
        return {
            'total_domains': len(domains),
            'unique_domains': len(domains),  # Already deduplicated via set
        }
