from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    __table_args__ = {'extend_existing': True}

    ten = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True, nullable=False)
    ngay_gia_nhap = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default="images/default.png", nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    benh_nhan = relationship('BenhNhan', backref='User', cascade="all, delete-orphan", lazy=False)


class BenhNhan(BaseModel):
    __table_args__ = {'extend_existing': True}

    ten = Column(String(50), nullable=False)
    gioi_tinh = Column(String(50), nullable=False)
    nam_sinh = Column(Integer, default=0, nullable=False)
    dia_chi = Column(String(255), nullable=False)
    ngay_dang_ky = Column(DateTime, default=datetime.now(), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    danh_sach_kham = relationship('BenhNhan_NgayKham', backref='BenhNhan', cascade="all, delete-orphan", lazy=False, passive_deletes=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class NgayKham(BaseModel):
    __table_args__ = {'extend_existing': True}

    ngay_kham = Column(DateTime, default=datetime.now())
    danh_sach_kham = relationship('BenhNhan_NgayKham', backref='NgayKham', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class BenhNhan_NgayKham(BaseModel):
    __table_args__ = {'extend_existing': True}

    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id, ondelete="CASCADE"), nullable=False)
    ngay_kham_id = Column(Integer, ForeignKey(NgayKham.id, ondelete="CASCADE"), nullable=False)
    phieu_kham = relationship('PhieuKham', backref='BenhNhan_NgayKham', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class PhieuKham(BaseModel):
    __table_args__ = {'extend_existing': True}

    ngay_lap_phieu = Column(DateTime, default=datetime.now(), nullable=False)
    benh_nhan_ngay_kham_id = Column(Integer, ForeignKey(BenhNhan_NgayKham.id, ondelete="CASCADE"), nullable=False)
    trieu_chung_loai_benh = relationship('TrieuChung_LoaiBenh', backref='PhieuKham', cascade="all, delete-orphan", lazy=False, passive_deletes=True)
    thuoc_don_vi_thuoc_phieu_kham = relationship('ThuocDonViThuoc_PhieuKham', backref='PhieuKham', cascade="all, delete-orphan", lazy=False, passive_deletes=True)
    hoa_don = relationship('HoaDon', backref='PhieuKham', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class TrieuChung(BaseModel):
    __table_args__ = {'extend_existing': True}

    ten_trieu_chung = Column(String(255), nullable=False)
    trieu_chung_loai_benh = relationship('TrieuChung_LoaiBenh', backref='TrieuChung', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class LoaiBenh(BaseModel):
    __table_args__ = {'extend_existing': True}

    ten_loai_benh = Column(String(255), nullable=False)
    trieu_chung_loai_benh = relationship('TrieuChung_LoaiBenh', backref='LoaiBenh', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class TrieuChung_LoaiBenh(BaseModel):
    __table_args__ = {'extend_existing': True}

    trieu_chung_id = Column(Integer, ForeignKey(TrieuChung.id, ondelete="CASCADE"), nullable=False)
    loai_benh_id = Column(Integer, ForeignKey(LoaiBenh.id, ondelete="CASCADE"), nullable=False)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id, ondelete="CASCADE"), nullable=False)


class DonViThuoc(BaseModel):
    __table_args__ = {'extend_existing': True}

    ten_don_vi = Column(String(50), nullable=False)
    thuoc_don_vi_thuoc = relationship('Thuoc_DonViThuoc', backref='DonViThuoc', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class Thuoc(BaseModel):
    __table_args__ = {'extend_existing': True}

    ten_thuoc = Column(String(50), nullable=False)
    thuoc_don_vi_thuoc = relationship('Thuoc_DonViThuoc', backref='Thuoc', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class Thuoc_DonViThuoc(BaseModel):
    __table_args__ = {'extend_existing': True}

    thuoc_id = Column(Integer, ForeignKey(Thuoc.id, ondelete="CASCADE"), nullable=False)
    don_vi_thuoc_id = Column(Integer, ForeignKey(DonViThuoc.id, ondelete="CASCADE"), nullable=False)
    tong_so_luong = Column(Integer, default=100, nullable=False)
    thuoc_don_vi_thuoc_phieu_kham = relationship('ThuocDonViThuoc_PhieuKham', backref='Thuoc_DonViThuoc', cascade="all, delete-orphan", lazy=False, passive_deletes=True)


class ThuocDonViThuoc_PhieuKham(BaseModel):
    __table_args__ = {'extend_existing': True}

    thuoc_don_vi_thuoc_id = Column(Integer, ForeignKey(Thuoc_DonViThuoc.id, ondelete="CASCADE"), nullable=False)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id, ondelete="CASCADE"), nullable=False)
    so_luong = Column(Integer, default=0, nullable=False)
    cach_dung = Column(String(255), nullable=False)


class HoaDon(BaseModel):
    __table_args__ = {'extend_existing': True}

    tien_kham = Column(Float, default=0)
    tien_thuoc = Column(Float, default=0)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id, ondelete="CASCADE"), nullable=False)


class QuyDinh(BaseModel):
    __table_args__ = {'extend_existing': True}

    so_benh_nhan = Column(Integer, default=30, nullable=False)
    so_loai_thuoc = Column(Integer, default=30, nullable=False)
    so_loai_don_vi = Column(Integer, default=2, nullable=False)
    so_tien_kham = Column(Float, default=100000.0, nullable=False)


if __name__ == '__main__':
    db.create_all()

    quy_dinh = QuyDinh(so_benh_nhan=30, so_loai_thuoc=30, so_loai_don_vi=2, so_tien_kham=100000.0)
    db.session.add(quy_dinh)

    don_vi_thuoc_1 = DonViThuoc(ten_don_vi="Viên")
    don_vi_thuoc_2 = DonViThuoc(ten_don_vi="Chai")
    db.session.add(don_vi_thuoc_1)
    db.session.add(don_vi_thuoc_2)

    db.session.commit()