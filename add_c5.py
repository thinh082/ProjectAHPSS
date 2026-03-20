"""Script thêm C5 matrix vào hardcoded_matrices.py"""
import pathlib

path = pathlib.Path("app/services/hardcoded_matrices.py")
content = path.read_text(encoding="utf-8")

c5_block = '''# ─────────────────────────────────────────────
# C5: Camera (lower_is_better = False)
# ─────────────────────────────────────────────
C5_MATRIX_STR = [
    # S24U   S24+   S24    ZF5    ZFl5   A54    A34    S23U   A73    M34
    ["1",   "2",   "4",   "2",   "3",   "1",   "1",   "1",   "1/2", "2"  ],  # S24 Ultra
    ["1/2", "1",   "3",   "2",   "2",   "1/2", "1/2", "1",   "1",   "1/3"],  # S24+
    ["1/4", "1/3", "1",   "1/2", "1/2", "1/4", "1/4", "1/2", "1/2", "1/5"],  # S24
    ["1/2", "1/2", "2",   "1",   "1",   "1/2", "1/2", "1",   "1",   "1/3"],  # Z Fold5
    ["1/3", "1/2", "2",   "1",   "1",   "1/2", "1/2", "1",   "1",   "1/3"],  # Z Flip5
    ["1",   "2",   "4",   "2",   "2",   "1",   "1",   "1",   "1",   "1/2"],  # A54
    ["1",   "2",   "4",   "2",   "2",   "1",   "1",   "1",   "1",   "1/2"],  # A34
    ["1",   "1",   "2",   "1",   "1",   "1",   "1",   "1",   "1",   "1/2"],  # S23 Ultra
    ["2",   "1",   "2",   "1",   "1",   "1",   "1",   "1",   "1",   "1/2"],  # A73 5G
    ["1/2", "3",   "5",   "3",   "3",   "2",   "2",   "2",   "2",   "1"  ],  # M34 5G
]

'''

old_marker = "# ─────────────────────────────────────────────\n# C5-C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n"
if old_marker in content:
    content = content.replace(old_marker, c5_block + "# ─────────────────────────────────────────────\n# C6: sẽ được bổ sung sau\n# ─────────────────────────────────────────────\n", 1)
    print("✓ Added C5 block")
else:
    print("ERROR: marker not found!")
    exit(1)

content = content.replace('"C5": None,', '"C5": C5_MATRIX_STR,', 1)
print("✓ Updated HARDCODED_MATRICES dict for C5")

path.write_text(content, encoding="utf-8")
print("Done!")
