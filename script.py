import re, hashlib, os, base64

SRC = "index.html"
OUT = "assets"
os.makedirs(OUT, exist_ok=True)

ext = {"jpeg":"jpg","jpg":"jpg","png":"png","gif":"gif","webp":"webp",
       "svg+xml":"svg","mp4":"mp4","webm":"webm","quicktime":"mov",
       "ogg":"ogg","mpeg":"mp3","mp3":"mp3","wav":"wav"}

html = open(SRC, encoding="utf-8").read()
# para antes da aspa/parêntese que fecha o atributo ou o url() do CSS
pat = re.compile(r'data:(image|video|audio)/([A-Za-z0-9.+-]+);base64,([A-Za-z0-9+/=\s]+?)(?=["\')])')

seen = {}
def repl(m):
    kind, sub, b64 = m.group(1), m.group(2).lower(), m.group(3)
    data = base64.b64decode(re.sub(r"\s+", "", b64))
    h = hashlib.sha1(data).hexdigest()[:10]
    name = f"{kind}_{h}.{ext.get(sub, sub.split('+')[0])}"
    if h not in seen:
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(data)
        seen[h] = round(len(data)/1024)
    return f"{OUT}/{name}"

new = pat.sub(repl, html)
open("index.clean.html", "w", encoding="utf-8").write(new)

print(f"{len(seen)} arquivos extraídos pra {OUT}/")
print(f"index.html: {os.path.getsize('index.html')//1024} KB -> "
      f"index.clean.html: {len(new.encode())//1024} KB")