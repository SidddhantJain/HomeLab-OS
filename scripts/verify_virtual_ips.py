import urllib.request

endpoints = [
    ("HomeLab OS (Direct Port)", "http://192.168.0.182:5173"),
    ("MadeNMore Store (Direct Port)", "http://192.168.0.182:5174"),
    ("HomeLab OS (Virtual IP 182)", "http://192.168.0.182/"),
    ("MadeNMore Store (Virtual IP 183)", "http://192.168.0.183/"),
    ("Fisicalflow (Virtual IP 184)", "http://192.168.0.184/"),
    ("MadeNMore 3D Studio (Virtual IP 185)", "http://192.168.0.185/"),
]

for name, url in endpoints:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'HomeLabOS-Tester'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', 'ignore')
            title = "No Title"
            if "<title>" in html:
                title = html.split("<title>")[1].split("</title>")[0]
            print(f"[OK] [{resp.status}] {name} ({url}) -> Title: {title.strip()}")
    except Exception as e:
        print(f"[ERROR] {name} ({url}) -> Error: {e}")
