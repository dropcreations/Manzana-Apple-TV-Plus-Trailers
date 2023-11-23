import unicodedata

def sanitize(f):
    b = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\0']
    f = ''.join(c for c in f if c not in b)
    f = ''.join(c for c in f if 31 < ord(c))
    f = unicodedata.normalize("NFKD", f)
    f = f.rstrip(". ")
    return f.strip()