#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otimiza as capas de assets/covers/ para a web.

Para cada <nome>-<pt|en>.jpg:
  · redimensiona para no máximo 640px de largura (as capas nunca são exibidas maiores)
  · regrava o JPG com qualidade 84, progressivo
  · gera o .webp equivalente
  · gera a miniatura de 320px em assets/covers/thumbs/ (usada no hero da home)
  · registra as dimensões finais em dims.json (usado por build.py)

Uso:  python optimize-covers.py
Requer: pillow  (pip install pillow)
"""
import glob, json, os, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
COVERS = ROOT / "assets" / "covers"
THUMBS = COVERS / "thumbs"
MAX_W = 640
THUMB_W = 320

THUMBS.mkdir(parents=True, exist_ok=True)
dims = {}
before = after = 0

for src in sorted(COVERS.glob("*.jpg")):
    if not re.match(r"^[a-z0-9]+-(pt|en)$", src.stem):
        continue
    before += src.stat().st_size
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > MAX_W:
        im = im.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
    im.save(src, "JPEG", quality=84, optimize=True, progressive=True)
    im.save(src.with_suffix(".webp"), "WEBP", quality=82, method=6)
    th = round(im.size[1] * THUMB_W / im.size[0])
    im.resize((THUMB_W, th), Image.LANCZOS).save(
        THUMBS / src.name, "JPEG", quality=82, optimize=True, progressive=True)
    dims[src.stem] = list(im.size)
    after += src.stat().st_size + src.with_suffix(".webp").stat().st_size
    print(f"  · {src.name}  {w}×{h} → {im.size[0]}×{im.size[1]}")

(ROOT / "dims.json").write_text(json.dumps(dims, indent=0), encoding="utf-8")
print(f"\nJPG originais: {before/1e6:.1f} MB → jpg+webp finais: {after/1e6:.1f} MB")
print("dims.json atualizado. Rode `python build.py` em seguida.")
