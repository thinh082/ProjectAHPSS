"""Script thêm C4 matrix vào hardcoded_matrices.py"""
import pathlib

path = pathlib.Path("app/services/hardcoded_matrices.py")
content = path.read_text(encoding="utf-8")

c4_block = '''# ─────────────────────────────────────────────
# C4: Lưu trữ (lower_is_better = False)
# ─────────────────────────────────────────────
C4_MATRIX_STR = [
    # S24U    S24+   S24    ZF5    ZFl5   A54    A34    S23U    A73    M34
    ["1",    "4",   "4",   "4",   "16",  "4",   "4",   "1",    "1/2", "4"  ],  # S24 Ultra
    ["1/4",  "1",   "2",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # S24+
    ["1/4",  "1/2", "1",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # S24
    ["1/4",  "1",   "1",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # Z Fold5
    ["1/16", "1/4", "1/4", "1/4", "1",   "1/4", "1/4", "1/16", "1/8", "1/4"],  # Z Flip5
    ["1/4",  "1",   "1",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # A54
    ["1/4",  "1",   "1",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # A34
    ["1",    "4",   "4",   "4",   "16",  "4",   "4",   "1",    "2",   "4"  ],  # S23 Ultra
    ["2",    "2",   "2",   "2",   "8",   "2",   "2",   "1/2",  "1",   "2"  ],  # A73 5G
    ["1/4",  "1",   "1",   "1",   "4",   "1",   "1",   "1/4",  "1/2", "1"  ],  # M34 5G
]

'''

old_marker = "# ─────────────────────────────────────────────\n# C4-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n"
if old_marker in content:
    content = content.replace(old_marker, c4_block + "# ─────────────────────────────────────────────\n# C5-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n", 1)
    print("✓ Added C4 block")
else:
    print("ERROR: marker not found!")
    exit(1)

content = content.replace('"C4": None,', '"C4": C4_MATRIX_STR,', 1)
print("✓ Updated HARDCODED_MATRICES dict for C4")

path.write_text(content, encoding="utf-8")
print("Done!")
