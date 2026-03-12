# Cấu trúc dự án FastAPI (Đơn giản)

Đây là cấu trúc thư mục tối giản, phù hợp cho các dự án nhỏ hoặc người mới bắt đầu.

## Sơ đồ cấu trúc

```text
.
├── app/                  # Thư mục chính
│   ├── main.py           # File chạy chính, chứa các routes
│   ├── database.py       # Kết nối Database
│   ├── models.py         # Khai báo bảng Database
│   ├── schemas.py        # Pydantic models (Dữ liệu đầu vào/ra)
│   └── crud.py           # Các hàm xử lý dữ liệu (DB logic)
├── .env                  # Biến môi trường
├── .gitignore            # Bỏ qua file rác
├── requirements.txt      # Thư viện cần dùng
└── README.md             # Hướng dẫn
```

## Chi tiết các file

1.  **app/main.py**: Chứa code khởi tạo FastAPI và các API endpoints (ví dụ: `@app.get("/")`).
2.  **app/database.py**: Cấu hình kết nối SQLAlchemy hoặc các thư viện DB khác.
3.  **app/models.py**: Chứa các class định nghĩa bảng trong Database.
4.  **app/schemas.py**: Chứa các class Pydantic để kiểm tra dữ liệu gửi lên và nhận về.
5.  **app/crud.py**: Tập hợp các hàm thực hiện Create, Read, Update, Delete để giữ cho `main.py` gọn gàng.

## Cách chạy nhanh

- Cài đặt: `pip install fastapi uvicorn`
- Chạy server: `uvicorn app.main:app --reload`
