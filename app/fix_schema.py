import os

filepath = r'd:\\Project\\ProjectAHPSS\\app\\schemas\\ahp_schema.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_validator = """
    @field_validator("weights")
    @classmethod
    def validate_weights(cls, v):
        if len(v) != 5:
            raise ValueError("Phải cung cấp chính xác 5 trọng số.")
        # Do sai số số thực, kiểm tra tổng xấp xỉ 1.0
        if abs(sum(v) - 1.0) > 1e-4:
            raise ValueError("Tổng các trọng số phải bằng 1.0.")
        return v
"""

new_validator = """
    @field_validator("weights")
    @classmethod
    def validate_weights(cls, v):
        if len(v) != 6:
            raise ValueError("Phải cung cấp chính xác 6 trọng số.")
        # Do sai số số thực, kiểm tra tổng xấp xỉ 1.0
        if abs(sum(v) - 1.0) > 1e-4:
            raise ValueError("Tổng các trọng số phải bằng 1.0.")
        return v
"""

if old_validator.strip() in content:
    content = content.replace(old_validator.strip(), new_validator.strip())
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Schema updated logic.")
else:
    print("Old validator not found. Here is what we have:")
    print("========")
    print(content[-500:])
