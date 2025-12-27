import re
from urllib.parse import urlparse

def is_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()

    if url.lower().startswith(('javascript:', 'data:', 'vbscript', 'file:')):
        return False
    
    try:
        parsed = urlparse(url if url.startswith('http') else f'https://{url}')
    except:
        return False

    if parsed.scheme not in ('http', 'https'):
        return False
    
    if not parsed.netloc or '.' not in parsed.netloc:
        return False
    
    bloqueados = ['localhost', '127.0.0.1', '0.0.0.0', '192.168', '10.', '172.']
    if any(blocked in parsed.netloc.lower() for blocked in bloqueados):
        return False
    
    return True

def get_url_error(url):
    if not url:
        return "URL é obrigatória"
    
    url = url.strip()

    if url.lower().startswith(('javascript:', 'data:', 'vbscript:', 'file:')):
        return "URL contém protocolo não permitido"
    
    if any(blocked in url.lower() for blocked in ['localhost', '127.0.0.1', '192.168.']):
        return "URLs locais não são permitidas"
    
    return "URL inválida. Use: http://example.com"
