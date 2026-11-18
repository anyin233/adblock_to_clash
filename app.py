"""Web UI for Adblock to Clash rule converter."""
from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import tempfile
import os

from downloader import RuleDownloader
from parser import AdblockParser
from converter import ClashConverter

app = Flask(__name__)

# Supported formats
SUPPORTED_INPUT_FORMATS = ['adblock']
SUPPORTED_OUTPUT_FORMATS = [
    'clash-domain-suffix',
    'clash-domain',
    'clash-domain-keyword'
]


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html',
                         input_formats=SUPPORTED_INPUT_FORMATS,
                         output_formats=SUPPORTED_OUTPUT_FORMATS)


@app.route('/convert', methods=['POST'])
def convert():
    """Convert rules from URL."""
    try:
        data = request.get_json()
        
        # Validate input
        url = data.get('url', '').strip()
        input_format = data.get('input_format', 'adblock')
        output_format = data.get('output_format', 'clash')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if input_format not in SUPPORTED_INPUT_FORMATS:
            return jsonify({'error': f'Unsupported input format: {input_format}'}), 400
        
        if output_format not in SUPPORTED_OUTPUT_FORMATS:
            return jsonify({'error': f'Unsupported output format: {output_format}'}), 400
        
        # Download rules
        downloader = RuleDownloader()
        content = downloader.download(url)
        downloader.close()
        
        # Parse rules based on input format
        if input_format == 'adblock':
            parser = AdblockParser()
            domains = parser.parse(content)
        else:
            return jsonify({'error': f'Parser not implemented for: {input_format}'}), 500
        
        if not domains:
            return jsonify({'error': 'No valid domains found in the rule source'}), 400
        
        # Convert to output format
        if output_format.startswith('clash-'):
            # Extract rule type from format (e.g., 'clash-domain-suffix' -> 'domain-suffix')
            rule_type = output_format.replace('clash-', '')
            converter = ClashConverter()
            
            # Create temporary file for output
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f'converted_rules_{os.getpid()}.yaml')
            
            converter.convert(domains, output_path, rule_type=rule_type)
            
            # Read the converted content
            with open(output_path, 'r', encoding='utf-8') as f:
                converted_content = f.read()
            
            # Clean up temp file
            os.remove(output_path)
            
            stats = converter.get_stats(domains)
        else:
            return jsonify({'error': f'Converter not implemented for: {output_format}'}), 500
        
        return jsonify({
            'success': True,
            'stats': {
                'total_domains': stats['total_domains'],
                'input_format': input_format,
                'output_format': output_format,
                'source_url': url
            },
            'content': converted_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    """Download the converted rules as a file."""
    try:
        data = request.get_json()
        content = data.get('content', '')
        output_format = data.get('output_format', 'clash')
        
        if not content:
            return jsonify({'error': 'No content to download'}), 400
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filename = f'converted_rules.yaml' if output_format == 'clash' else f'converted_rules.txt'
        output_path = os.path.join(temp_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return send_file(output_path,
                        as_attachment=True,
                        download_name=filename,
                        mimetype='text/yaml' if output_format == 'clash' else 'text/plain')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
