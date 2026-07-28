#!/usr/bin/env python3
import os
import csv

ROOT = '.'
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}
OUT_PATH = 'docs/REPO_INDEX.csv'
rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # skip ignored dirs
    parts = dirpath.strip(os.sep).split(os.sep)
    if any(p in IGNORE_DIRS for p in parts):
        continue
    for fname in filenames:
        rel = os.path.join(dirpath, fname).lstrip('./')
        # skip the output file if re-run
        if rel == OUT_PATH:
            continue
        try:
            size = os.path.getsize(os.path.join(dirpath, fname))
        except Exception:
            size = ''
        lines = ''
        full = os.path.join(dirpath, fname)
        try:
            with open(full, 'r', encoding='utf-8') as fh:
                # count lines for text files
                lines = sum(1 for _ in fh)
        except Exception:
            lines = ''
        top = rel.split('/')[0] if '/' in rel else rel
        rows.append((rel, top, size, lines))

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', newline='', encoding='utf-8') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['path', 'top_level', 'size_bytes', 'lines'])
    writer.writerows(rows)

print(f'Wrote {OUT_PATH} with {len(rows)} entries')
