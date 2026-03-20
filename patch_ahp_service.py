"""
Script để patch ahp_service.py:
- Thêm import từ hardcoded_matrices
- Thêm ORDER BY id vào query
- Sửa evaluate_criteria để dùng hardcoded matrix nếu có
"""
import pathlib

path = pathlib.Path("app/services/ahp_service.py")
content = path.read_text(encoding="utf-8")

# 1. Thêm import hardcoded_matrices sau dòng import SamsungPhone
old_import = "from app.models import SamsungPhone"
new_import = (
    "from app.models import SamsungPhone\n"
    "from app.services.hardcoded_matrices import HARDCODED_MATRICES, matrix_str_to_float"
)
if new_import not in content:
    content = content.replace(old_import, new_import, 1)
    print("✓ Added import")
else:
    print("- Import already exists, skipping")

# 2. Thêm ORDER BY id vào query
old_query = "query = select(SamsungPhone)"
new_query = "query = select(SamsungPhone).order_by(SamsungPhone.id)"
if old_query in content:
    content = content.replace(old_query, new_query, 1)
    print("✓ Added ORDER BY id")
else:
    print("- ORDER BY already added or query not found")

# 3. Thay phần tính matrix động bằng logic check hardcoded trước
old_matrix_block = (
    "        matrix = [[1.0] * n for _ in range(n)]\n"
    "        matrix_str = [[\"1\"] * n for _ in range(n)]\n"
    "        \n"
    "        vals = [parse_numeric(getattr(p, col_name, 0)) for p in phones]\n"
    "        \n"
    "        for i in range(n):\n"
    "            for j in range(n):\n"
    "                if i == j:\n"
    "                    matrix[i][j] = 1.0\n"
    "                    matrix_str[i][j] = \"1\"\n"
    "                elif i < j:\n"
    "                    vi = vals[i]\n"
    "                    vj = vals[j]\n"
    "                    \n"
    "                    if vi == 0: vi = 0.1\n"
    "                    if vj == 0: vj = 0.1\n"
    "                    \n"
    "                    if lower_is_better:\n"
    "                        ratio = vj / vi\n"
    "                    else:\n"
    "                        ratio = vi / vj\n"
    "                        \n"
    "                    scale = get_ahp_scale(ratio)\n"
    "                    \n"
    "                    if ratio >= 1:\n"
    "                        matrix[i][j] = float(scale)\n"
    "                        matrix[j][i] = 1.0 / scale\n"
    "                        matrix_str[i][j] = str(scale)\n"
    "                        matrix_str[j][i] = f\"1/{scale}\"\n"
    "                    else:\n"
    "                        scale = get_ahp_scale(1/ratio)\n"
    "                        matrix[i][j] = 1.0 / scale\n"
    "                        matrix[j][i] = float(scale)\n"
    "                        matrix_str[i][j] = f\"1/{scale}\"\n"
    "                        matrix_str[j][i] = str(scale)\n"
)

new_matrix_block = (
    "        # Ưu tiên dùng hardcoded matrix nếu có, nếu không dùng tính động\n"
    "        hardcoded = HARDCODED_MATRICES.get(crit[\"id\"])\n"
    "        if hardcoded is not None:\n"
    "            matrix_str = [row[:] for row in hardcoded]\n"
    "            matrix = matrix_str_to_float(matrix_str)\n"
    "        else:\n"
    "            matrix = [[1.0] * n for _ in range(n)]\n"
    "            matrix_str = [[\"1\"] * n for _ in range(n)]\n"
    "            \n"
    "            vals = [parse_numeric(getattr(p, col_name, 0)) for p in phones]\n"
    "            \n"
    "            for i in range(n):\n"
    "                for j in range(n):\n"
    "                    if i == j:\n"
    "                        matrix[i][j] = 1.0\n"
    "                        matrix_str[i][j] = \"1\"\n"
    "                    elif i < j:\n"
    "                        vi = vals[i]\n"
    "                        vj = vals[j]\n"
    "                        \n"
    "                        if vi == 0: vi = 0.1\n"
    "                        if vj == 0: vj = 0.1\n"
    "                        \n"
    "                        if lower_is_better:\n"
    "                            ratio = vj / vi\n"
    "                        else:\n"
    "                            ratio = vi / vj\n"
    "                            \n"
    "                        scale = get_ahp_scale(ratio)\n"
    "                        \n"
    "                        if ratio >= 1:\n"
    "                            matrix[i][j] = float(scale)\n"
    "                            matrix[j][i] = 1.0 / scale\n"
    "                            matrix_str[i][j] = str(scale)\n"
    "                            matrix_str[j][i] = f\"1/{scale}\"\n"
    "                        else:\n"
    "                            scale = get_ahp_scale(1/ratio)\n"
    "                            matrix[i][j] = 1.0 / scale\n"
    "                            matrix[j][i] = float(scale)\n"
    "                            matrix_str[i][j] = f\"1/{scale}\"\n"
    "                            matrix_str[j][i] = str(scale)\n"
)

if old_matrix_block in content:
    content = content.replace(old_matrix_block, new_matrix_block, 1)
    print("✓ Replaced dynamic matrix block with hardcoded check")
else:
    print("ERROR: matrix block not found! Check indentation in ahp_service.py")

path.write_text(content, encoding="utf-8")
print("Done! ahp_service.py updated.")
