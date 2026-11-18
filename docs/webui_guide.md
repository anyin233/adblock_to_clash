# Web UI Usage Guide

## Overview

The Rule Converter Web UI provides a user-friendly interface for converting Adblock format rules to Clash ruleset format.

## Features

- 🌐 **Web-based Interface**: Easy-to-use browser interface
- 📥 **URL Input**: Enter rule source URLs directly
- 🔄 **Format Selection**: Choose input and output formats
- 📊 **Real-time Statistics**: View conversion stats
- 📋 **Copy to Clipboard**: One-click copy of converted rules
- ⬇️ **Download**: Download converted rules as a file

## Starting the Web UI

```bash
# Using uv (recommended)
uv run python app.py

# Using standard Python
python app.py
```

The web UI will be available at: http://127.0.0.1:8080

## Using the Web UI

### 1. Enter Rule Source URL

In the "Rule Source URL" field, enter the URL of the Adblock rules you want to convert:

- Full URLs: `https://easylist-downloads.adblockplus.org/easylist.txt`
- Domain paths: `easylist-downloads.adblockplus.org/easylist.txt`

### 2. Select Input Format

Choose the format of your source rules:
- **Adblock** (default): Standard Adblock format rules

### 3. Select Output Format

Choose the desired output format:
- **Clash** (default): Clash ruleset format with DOMAIN-SUFFIX rules

### 4. Convert

Click the "Convert Rules" button to start the conversion process. The UI will:
- Show a loading spinner
- Download rules from the specified URL
- Parse and convert the rules
- Display statistics and results

### 5. View Results

After conversion, you'll see:

**Statistics:**
- Total domains converted
- Input format used
- Output format generated
- Source URL

**Output Box:**
- Preview of converted rules in YAML format
- Scrollable view for large rulesets

### 6. Copy or Download

**Copy to Clipboard:**
- Click the "📋 Copy to Clipboard" button
- Rules are copied and button shows "✅ Copied!" confirmation

**Download File:**
- Click the "⬇️ Download File" button
- Rules are downloaded as `converted_rules.yaml`

## Supported Formats

### Input Formats
- **Adblock**: Standard Adblock Plus format
  - Domain rules: `||example.com^`
  - Supports automatic domain extraction

### Output Formats
- **Clash**: Clash ruleset format
  - Uses `DOMAIN-SUFFIX` rules
  - YAML format compatible with Clash

## Error Handling

The UI provides clear error messages for:
- Invalid URLs
- Network errors
- Empty rule sources
- Invalid formats
- Server errors

## Tips

1. **Large Rulesets**: The UI can handle large rulesets (20,000+ domains)
2. **URL Formats**: Both full URLs and domain paths are supported
3. **Multiple Sources**: Convert one source at a time
4. **Mobile Friendly**: Responsive design works on mobile devices

## API Endpoints

The web UI exposes the following API endpoints:

### POST /convert
Convert rules from a URL.

**Request:**
```json
{
  "url": "https://example.com/rules.txt",
  "input_format": "adblock",
  "output_format": "clash"
}
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_domains": 25000,
    "input_format": "adblock",
    "output_format": "clash",
    "source_url": "https://example.com/rules.txt"
  },
  "content": "payload:\n  - DOMAIN-SUFFIX,example.com\n  ..."
}
```

## Troubleshooting

**Port Already in Use:**
If port 8080 is already in use, modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8081)
```

**Connection Errors:**
- Check your internet connection
- Verify the URL is accessible
- Some sources may block automated requests

**No Domains Found:**
- Verify the source contains Adblock format rules
- Check if the URL is correct
- Ensure the source is not empty or inaccessible
