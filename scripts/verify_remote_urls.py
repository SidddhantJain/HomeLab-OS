import urllib.request

urls = [
    'http://192.168.0.182:5173',
    'http://192.168.0.182:8000/docs',
    'http://192.168.0.182:8081',
    'http://192.168.0.182:5174',
    'http://192.168.0.182:5175'
]

for url in urls:
    try:
        req = urllib.request.urlopen(url, timeout=3)
        print(f"[ONLINE]  {url} -> {req.status}")
    except Exception as e:
        print(f"[OFFLINE] {url} -> {e}")
