#!/usr/bin/env python3
"""Normalize the Conductor frames and pack per-animation spritesheets.

Each source frame is cropped differently, so we:
  1. strip stray disconnected fragments (keep components near the biggest one)
  2. crop to content bbox
  3. anchor every frame bottom-center on a shared canvas per animation
  4. pack frames horizontally into one spritesheet per animation
Outputs spritesheets + a meta report of frame sizes for the JS manifest.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/mnt/user-data/uploads/Chapter 6 -Final Boss/Assets"
OUT = ("/home/claude/repo/public/assets/images/conductor")
os.makedirs(OUT, exist_ok=True)

ANIMS = {
    "idle":   ["conductor_idle_%d.png" % i for i in range(1, 6)],
    "move":   ["conductor_movement_%d.png" % i for i in range(1, 6)],
    "baton":  ["conductor_baton_attack_%d.png" % i for i in range(1, 6)],
    "locom":  ["conductor_locomotive_attack_v2_%d.png" % i for i in range(1, 6)],
    "magic":  ["conductor_magic_attack_%d.png" % i for i in range(1, 6)],
    "damage": ["conductor_damage_%d.png" % i for i in range(1, 4)],
    "defeat": ["conductor_defeat _1.png", "conductor_defeat_2.png"],
}

def clean_and_crop(im):
    a = np.array(im)
    alpha = a[..., 3]
    mask = alpha > 12
    if not mask.any():
        return im
    labels, n = ndimage.label(mask)
    if n > 1:
        sizes = ndimage.sum(mask, labels, range(1, n + 1))
        main = int(np.argmax(sizes)) + 1
        ys, xs = np.where(labels == main)
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        keep = np.zeros_like(mask)
        for comp in range(1, n + 1):
            if comp == main:
                keep |= labels == comp
                continue
            cys, cxs = np.where(labels == comp)
            # keep fragments that are large or close to the main body
            # only keep fragments that actually overlap the main body's bbox
            overlaps = not (cxs.max() < x0 or cxs.min() > x1 or
                            cys.max() < y0 or cys.min() > y1)
            if overlaps and sizes[comp - 1] > 0.01 * sizes[main - 1]:
                keep |= labels == comp
        a = a.copy()
        a[..., 3] = np.where(keep, alpha, 0)
        mask = a[..., 3] > 12
    ys, xs = np.where(mask)
    return Image.fromarray(a).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

meta = {}
for anim, files in ANIMS.items():
    frames = [clean_and_crop(Image.open(os.path.join(SRC, f)).convert("RGBA")) for f in files]
    fw = max(f.width for f in frames)
    fh = max(f.height for f in frames)
    sheet = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        # bottom-center anchor
        x = i * fw + (fw - f.width) // 2
        y = fh - f.height
        sheet.paste(f, (x, y))
    path = os.path.join(OUT, f"{anim}.png")
    sheet.save(path, optimize=True)
    meta[anim] = {"frameWidth": fw, "frameHeight": fh, "frames": len(frames),
                  "medianH": int(np.median([f.height for f in frames]))}
    print(anim, meta[anim], f"sheet={sheet.size}", f"{os.path.getsize(path)//1024}KB")

with open(os.path.join(OUT, "meta.json"), "w") as fp:
    json.dump(meta, fp, indent=2)
print("OK")
