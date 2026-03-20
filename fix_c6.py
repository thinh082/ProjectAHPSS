import pathlib

path = pathlib.Path("app/services/ahp_service.py")
content = path.read_text(encoding="utf-8")

old = '{"id": "C5", "name": "Camera", "col": "chat_luong_camera", "lower_is_better": False},'
new = old + '\n        {"id": "C6", "name": "Thiết kế", "col": "thiet_ke", "lower_is_better": False},'

if old not in content:
    print("ERROR: C5 line not found in file!")
else:
    content = content.replace(old, new)
    path.write_text(content, encoding="utf-8")
    print("Successfully added C6 criterion!")
