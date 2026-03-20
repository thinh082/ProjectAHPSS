"""Script thêm C3 matrix vào hardcoded_matrices.py"""
import pathlib

path = pathlib.Path("app/services/hardcoded_matrices.py")
content = path.read_text(encoding="utf-8")

c3_block = '''# ─────────────────────────────────────────────
# C3: Pin (lower_is_better = False)
# ─────────────────────────────────────────────
C3_MATRIX_STR = [
    # S24U   S24+    S24    ZF5    ZFl5   A54    A34    S23U   A73    M34
    ["1",   "1/2", "2",   "1",   "1",   "3",   "3",   "1",   "3",   "3"  ],  # S24 Ultra
    ["2",   "1",   "3",   "2",   "2",   "4",   "4",   "2",   "4",   "4"  ],  # S24+
    ["1/2", "1/3", "1",   "1/2", "1/2", "2",   "2",   "1/2", "2",   "2"  ],  # S24
    ["1",   "1/2", "2",   "1",   "1",   "3",   "3",   "1",   "3",   "3"  ],  # Z Fold5
    ["1",   "1/2", "2",   "1",   "1",   "3",   "3",   "1",   "3",   "3"  ],  # Z Flip5
    ["1/3", "1/4", "1/2", "1/3", "1/3", "1",   "1",   "1/3", "1",   "1"  ],  # A54
    ["1/3", "1/4", "1/2", "1/3", "1/3", "1",   "1",   "1/3", "1",   "1"  ],  # A34
    ["1",   "1/2", "2",   "1",   "1",   "3",   "3",   "1",   "3",   "3"  ],  # S23 Ultra
    ["1/3", "1/4", "1/2", "1/3", "1/3", "1",   "1",   "1/3", "1",   "1"  ],  # A73 5G
    ["1/3", "1/4", "1/2", "1/3", "1/3", "1",   "1",   "1/3", "1",   "1"  ],  # M34 5G
]

'''

old_marker = "# ─────────────────────────────────────────────\n# C3-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n"
if old_marker in content:
    content = content.replace(old_marker, c3_block + "# ─────────────────────────────────────────────\n# C4-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n", 1)
    print("✓ Added C3 block")
else:
    print("ERROR: marker not found!")
    exit(1)

content = content.replace('"C3": None,', '"C3": C3_MATRIX_STR,', 1)
print("✓ Updated HARDCODED_MATRICES dict for C3")

path.write_text(content, encoding="utf-8")
print("Done!")
