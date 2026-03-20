"""Script thêm C6 (Thiết kế) matrix vào hardcoded_matrices.py"""
import pathlib

path = pathlib.Path("app/services/hardcoded_matrices.py")
content = path.read_text(encoding="utf-8")

c6_block = '''# ─────────────────────────────────────────────
# C6: Thiết kế (lower_is_better = False)
# ─────────────────────────────────────────────
C6_MATRIX_STR = [
    # S24U   S24+   S24    ZF5    ZFl5   A54    A34    S23U   A73    M34
    ["1",   "2",   "2",   "3",   "3",   "6",   "6",   "3",   "5",   "7"  ],  # S24 Ultra
    ["1/2", "1",   "1",   "2",   "2",   "5",   "5",   "2",   "4",   "6"  ],  # S24+
    ["1/2", "1",   "1",   "2",   "2",   "5",   "5",   "2",   "4",   "6"  ],  # S24
    ["1/3", "1/2", "1/2", "1",   "1",   "4",   "4",   "1",   "3",   "5"  ],  # Z Fold5
    ["1/3", "1/2", "1/2", "1",   "1",   "4",   "4",   "1",   "3",   "5"  ],  # Z Flip5
    ["1/6", "1/5", "1/5", "1/4", "1/4", "1",   "1",   "1/4", "2",   "4"  ],  # A54
    ["1/6", "1/5", "1/5", "1/4", "1/4", "1",   "1",   "1/4", "2",   "4"  ],  # A34
    ["1/3", "1/2", "1/2", "1",   "1",   "4",   "4",   "1",   "3",   "5"  ],  # S23 Ultra
    ["1/5", "1/4", "1/4", "1/3", "1/3", "1/2", "1/2", "1/3", "1",   "3"  ],  # A73 5G
    ["1/7", "1/6", "1/6", "1/5", "1/5", "1/4", "1/4", "1/5", "1/3", "1"  ],  # M34 5G
]

'''

old_marker = "# ─────────────────────────────────────────────\n# C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n"
if old_marker in content:
    content = content.replace(old_marker, c6_block, 1)
    print("✓ Added C6 block")
else:
    print("ERROR: marker not found!")
    exit(1)

content = content.replace('"C6": None,', '"C6": C6_MATRIX_STR,', 1)
print("✓ Updated HARDCODED_MATRICES dict for C6")

path.write_text(content, encoding="utf-8")
print("Done!")
