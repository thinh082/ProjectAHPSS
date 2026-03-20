"""Script thêm C2 matrix vào hardcoded_matrices.py"""
import pathlib

path = pathlib.Path("app/services/hardcoded_matrices.py")
content = path.read_text(encoding="utf-8")

c2_block = '''# ─────────────────────────────────────────────
# C2: Hiệu năng (lower_is_better = False)
# ─────────────────────────────────────────────
C2_MATRIX_STR = [
    # S24U   S24+    S24    ZF5    ZFl5   A54    A34    S23U   A73    M34
    ["1",   "1",   "2",   "2",   "3",   "6",   "7",   "5/2", "4",   "6"  ],  # S24 Ultra
    ["1",   "1",   "2",   "2",   "3",   "6",   "7",   "5/2", "4",   "6"  ],  # S24+
    ["1/2", "1/2", "1",   "1",   "2",   "5",   "6",   "2",   "3",   "5"  ],  # S24
    ["1/2", "1/2", "1",   "1",   "2",   "5",   "6",   "2",   "3",   "5"  ],  # Z Fold5
    ["1/3", "1/3", "1/2", "1/2", "1",   "4",   "5",   "3/2", "5/2", "4"  ],  # Z Flip5
    ["1/6", "1/6", "1/5", "1/5", "1/4", "1",   "2",   "1/3", "1",   "2"  ],  # A54
    ["1/7", "1/7", "1/6", "1/6", "1/5", "1/2", "1",   "1/4", "1/2", "1"  ],  # A34
    ["2/5", "2/5", "1/2", "1/2", "2/3", "3",   "4",   "1",   "2",   "3"  ],  # S23 Ultra
    ["1/4", "1/4", "1/3", "1/3", "2/5", "1",   "2",   "1/2", "1",   "2"  ],  # A73 5G
    ["1/6", "1/6", "1/5", "1/5", "1/4", "1/2", "1",   "1/3", "1/2", "1"  ],  # M34 5G
]

'''

old_marker = "# ─────────────────────────────────────────────\n# C2-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n"
if old_marker in content:
    content = content.replace(old_marker, c2_block + "# ─────────────────────────────────────────────\n# C3-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n", 1)
    print("✓ Added C2 block")
else:
    print("ERROR: marker not found!")
    exit(1)

# Cập nhật HARDCODED_MATRICES dict: "C2": None -> "C2": C2_MATRIX_STR
content = content.replace('"C2": None,', '"C2": C2_MATRIX_STR,', 1)
print("✓ Updated HARDCODED_MATRICES dict for C2")

path.write_text(content, encoding="utf-8")
print("Done!")
