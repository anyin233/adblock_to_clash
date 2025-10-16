# Adblock to Clash Rule Converter

A Python tool that converts Adblock format rules to Clash ruleset format with automatic deduplication. Available as both a CLI tool and a Cloudflare Worker for on-demand conversion.

## Features

- ✅ Download rules from multiple sources (URLs or domains)
- ✅ Parse Adblock format rules (domain-based)
- ✅ Convert to Clash ruleset format (DOMAIN-SUFFIX)
- ✅ Automatic deduplication
- ✅ Comprehensive error handling
- ✅ Progress tracking and statistics
- ✅ **Cloudflare Worker for on-demand conversion** (see [worker/README.md](worker/README.md))

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
cd rule_converter

# Install dependencies
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file in the project root:

```yaml
rules:
  - easylist-downloads.adblockplus.org/easylist.txt
  - https://easylist-downloads.adblockplus.org/easylist.txt
target: clash
```

### Configuration Options

- **rules**: List of rule sources (URLs or domains to download from)
- **target**: Output format (currently only `clash` is supported)

## Deployment Options

### Option 1: CLI Tool (Batch Conversion)

For batch processing multiple rule sources locally.

### Option 2: Cloudflare Worker (On-Demand Conversion)

Deploy as a serverless API for on-demand conversion. See [worker/README.md](worker/README.md) for details.

Usage example:
```
https://your-worker.workers.dev/easylist-downloads.adblockplus.org/easylist.txt
```

## Usage (CLI Tool)

Run the converter:

```bash
# Using uv
uv run python main.py

# Using standard Python
python main.py
```

The converter will:
1. Load configuration from `config.yaml`
2. Download rules from all specified sources
3. Parse Adblock format rules
4. Deduplicate domains
5. Convert to Clash format
6. Save output to `output/clash_rules.yaml`

## Output Format

The generated Clash ruleset follows the standard format:

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
  - DOMAIN-SUFFIX,test.org
  - DOMAIN-SUFFIX,sample.net
```

This file can be directly used in Clash configurations:

```yaml
rule-providers:
  custom-rules:
    type: file
    behavior: domain
    path: ./clash_rules.yaml
```

## Project Structure

```
rule_converter/
├── config.py          # Configuration parser
├── downloader.py      # Rule downloader
├── parser.py          # Adblock rule parser
├── converter.py       # Clash format converter
├── main.py            # Main application
├── config.yaml        # Configuration file
├── pyproject.toml     # Project dependencies
├── output/            # Generated rulesets
│   └── clash_rules.yaml
└── worker/            # Cloudflare Worker
    ├── worker.js      # Worker implementation
    ├── wrangler.toml  # Worker configuration
    └── README.md      # Worker documentation
```

## How It Works

1. **Configuration Loading**: Reads `config.yaml` and validates settings
2. **Rule Downloading**: Fetches rules from URLs/domains using HTTP requests
3. **Parsing**: Extracts domains from Adblock format (`||domain.com^`)
4. **Deduplication**: Uses sets to automatically remove duplicate domains
5. **Conversion**: Formats domains as Clash DOMAIN-SUFFIX rules
6. **Output**: Saves as YAML file compatible with Clash

## Supported Adblock Formats

The parser supports domain-based Adblock rules:

- `||example.com^` → `example.com`
- `||subdomain.example.com^` → `subdomain.example.com`
- Comments (starting with `!` or `[`) are ignored
- Exception rules (starting with `@@`) are skipped

## Example Output

```
============================================================
Adblock to Clash Rule Converter
============================================================

[1/5] Loading configuration from config.yaml...
✓ Loaded 2 rule sources
✓ Target format: clash

[2/5] Downloading rules from 2 sources...
  [1/2] Fetching: easylist-downloads.adblockplus.org/easylist.txt
      → Found 25000 domains
  [2/2] Fetching: https://easylist-downloads.adblockplus.org/easylist.txt
      → Found 25000 domains

[3/5] Deduplicating rules...
✓ Total unique domains: 25000

[4/5] Converting to Clash ruleset format...
✓ Converted 25000 domains

[5/5] Generating output...
✓ Output saved to: output/clash_rules.yaml

============================================================
Conversion Summary
============================================================
Total domains processed: 25000
Output file: output/clash_rules.yaml
Format: Clash ruleset (DOMAIN-SUFFIX)

✓ Conversion completed successfully!
```

## Error Handling

The converter includes comprehensive error handling:

- Configuration file validation
- Network error retry logic
- Invalid domain filtering
- Graceful failure for individual sources

## Development

### Dependencies

- `pyyaml` - YAML parsing
- `requests` - HTTP requests

### Adding New Features

The modular architecture makes it easy to extend:

- Add new parsers in `parser.py`
- Add new output formats in `converter.py`
- Customize download behavior in `downloader.py`

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
