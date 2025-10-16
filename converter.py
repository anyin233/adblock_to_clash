"""Clash rule converter module."""
import yaml
from typing import Set, List
from pathlib import Path


class ClashConverter:
    """Converts domains to Clash ruleset format."""
    
    def __init__(self):
        """Initialize the converter."""
        pass
    
    def convert(self, domains: Set[str], output_path: str = "output.yaml") -> None:
        """Convert domains to Clash ruleset format and save to file.
        
        Args:
            domains: Set of domain strings
            output_path: Path to save the output file
        """
        # Deduplicate by using set (already done) and sort for consistency
        sorted_domains = sorted(domains)
        
        # Build Clash ruleset structure
        # Clash uses DOMAIN-SUFFIX for domain matching
        payload = [f"DOMAIN-SUFFIX,{domain}" for domain in sorted_domains]
        
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
