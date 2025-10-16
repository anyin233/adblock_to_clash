"""Rule downloader module."""
import requests
from typing import Optional
from urllib.parse import urlparse


class RuleDownloader:
    """Downloads rules from URLs."""
    
    def __init__(self, timeout: int = 30):
        """Initialize downloader.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download(self, url_or_domain: str) -> str:
        """Download rules from URL or domain.
        
        Args:
            url_or_domain: URL or domain to download from
            
        Returns:
            Rule content as string
            
        Raises:
            requests.RequestException: If download fails
        """
        url = self._normalize_url(url_or_domain)
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to download from {url}: {e}")
    
    def _normalize_url(self, url_or_domain: str) -> str:
        """Normalize URL or domain to a valid URL.
        
        Args:
            url_or_domain: URL or domain string
            
        Returns:
            Normalized URL with scheme
        """
        url = url_or_domain.strip()
        
        # Check if it's already a URL with scheme
        parsed = urlparse(url)
        if parsed.scheme in ('http', 'https'):
            return url
        
        # Assume it's a domain and add https://
        if not url.startswith('http'):
            url = f'https://{url}'
        
        return url
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
