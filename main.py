"""Adblock to Clash rule converter main application."""
import sys
from pathlib import Path
from typing import Set

from config import Config
from downloader import RuleDownloader
from parser import AdblockParser
from converter import ClashConverter


def main():
    """Main application entry point."""
    config_path = "config.yaml"
    output_path = "output/clash_rules.yaml"
    
    print("=" * 60)
    print("Adblock to Clash Rule Converter")
    print("=" * 60)
    
    try:
        # Load configuration
        print(f"\n[1/5] Loading configuration from {config_path}...")
        config = Config(config_path)
        config.load()
        print(f"✓ Loaded {len(config.rules)} rule sources")
        print(f"✓ Target format: {config.target}")
        
        # Initialize components
        downloader = RuleDownloader()
        parser = AdblockParser()
        converter = ClashConverter()
        
        # Download and parse rules
        print(f"\n[2/5] Downloading rules from {len(config.rules)} sources...")
        all_domains: Set[str] = set()
        
        for idx, rule_source in enumerate(config.rules, 1):
            try:
                print(f"  [{idx}/{len(config.rules)}] Fetching: {rule_source}")
                content = downloader.download(rule_source)
                
                # Parse Adblock rules
                domains = parser.parse(content)
                all_domains.update(domains)
                print(f"      → Found {len(domains)} domains")
                
            except Exception as e:
                print(f"      ✗ Error: {e}")
                continue
        
        downloader.close()
        
        # Deduplication
        print(f"\n[3/5] Deduplicating rules...")
        original_count = sum(1 for _ in all_domains)  # Already deduplicated via set
        print(f"✓ Total unique domains: {len(all_domains)}")
        
        # Convert to Clash format
        print(f"\n[4/5] Converting to Clash ruleset format...")
        converter.convert(all_domains, output_path)
        print(f"✓ Converted {len(all_domains)} domains")
        
        # Generate statistics
        print(f"\n[5/5] Generating output...")
        stats = converter.get_stats(all_domains)
        print(f"✓ Output saved to: {output_path}")
        
        # Summary
        print("\n" + "=" * 60)
        print("Conversion Summary")
        print("=" * 60)
        print(f"Total domains processed: {stats['total_domains']}")
        print(f"Output file: {output_path}")
        print(f"Format: Clash ruleset (DOMAIN-SUFFIX)")
        print("\n✓ Conversion completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print(f"\nPlease create a configuration file at '{config_path}'")
        print("\nExample config.yaml:")
        print("---")
        print("rules:")
        print("  - nsfw.oisd.nl")
        print("  - https://example.com/rules.txt")
        print("target: clash")
        sys.exit(1)
        
    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n✗ Conversion cancelled by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
