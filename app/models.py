from sqlalchemy import Column, Integer, String, Text, Numeric
from .database import Base

class SamsungPhone(Base):
    __tablename__ = "samsung_phones"

    id = Column(Integer, primary_key=True, index=True)
    mau_dien_thoai = Column(String(255))
    gia_usd = Column(Numeric(10, 2))
    hieu_nang = Column(Text)
    dung_luong_luu_tru = Column(String(50))
    chat_luong_camera = Column(String(50))
    dung_luong_pin = Column(String(50))
    thiet_ke = Column(Text)
