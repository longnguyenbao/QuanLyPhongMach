from app import db, utils1
from app.models import User, BenhNhan, NgayKham, BenhNhan_NgayKham, QuyDinh, PhieuKham, TrieuChung, LoaiBenh, TrieuChung_LoaiBenh, Thuoc, DonViThuoc, Thuoc_DonViThuoc, ThuocDonViThuoc_PhieuKham, HoaDon
import hashlib
from flask_login import current_user


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    user = User(ten=name.strip(), username=username.strip(), password=password, email=kwargs.get("email"), avatar=kwargs.get("avatar"))

    db.session.add(user)
    db.session.commit()


def them_ngay(ngay_kham):
    ngay = NgayKham(ngay_kham=ngay_kham)

    db.session.add(ngay)
    db.session.commit()


def them_benh_nhan(ten, gioi_tinh, nam_sinh, dia_chi):
    benh_nhan = BenhNhan(ten=ten, gioi_tinh=gioi_tinh, nam_sinh=nam_sinh, dia_chi=dia_chi, User=current_user)

    db.session.add(benh_nhan)
    db.session.commit()


def them_benh_nhan_ngay_kham(benh_nhan_id, ngay_kham_id):
    benh_nhan_ngay_kham = BenhNhan_NgayKham(benh_nhan_id=benh_nhan_id, ngay_kham_id=ngay_kham_id)

    db.session.add(benh_nhan_ngay_kham)
    db.session.commit()


def them_phieu_kham(benh_nhan_ngay_kham_id):
    phieu_kham = PhieuKham(benh_nhan_ngay_kham_id=benh_nhan_ngay_kham_id)

    db.session.add(phieu_kham)
    db.session.commit()


def them_trieu_chung(ten_trieu_chung):
    trieu_chung = TrieuChung(ten_trieu_chung = ten_trieu_chung)

    db.session.add(trieu_chung)
    db.session.commit()


def them_loai_benh(ten_loai_benh):
    loai_benh = LoaiBenh(ten_loai_benh = ten_loai_benh)

    db.session.add(loai_benh)
    db.session.commit()


def them_trieu_chung_loai_benh(trieu_chung_id, loai_benh_id, phieu_kham_id):
    trieu_chung_loai_benh = TrieuChung_LoaiBenh(trieu_chung_id=trieu_chung_id, loai_benh_id=loai_benh_id,phieu_kham_id=phieu_kham_id)

    db.session.add(trieu_chung_loai_benh)
    db.session.commit()


def them_thuoc(ten_thuoc):
    thuoc = Thuoc(ten_thuoc=ten_thuoc)

    db.session.add(thuoc)
    db.session.commit()


def them_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id):
    thuoc_don_vi_thuoc = Thuoc_DonViThuoc(thuoc_id = thuoc_id, don_vi_thuoc_id = don_vi_thuoc_id)

    db.session.add(thuoc_don_vi_thuoc)
    db.session.commit()


def cap_nhat_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id, so_luong):
    thuoc_don_vi_thuoc = utils1.get_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id)

    thuoc_don_vi_thuoc.tong_so_luong -= int(so_luong)
    db.session.commit()


def them_thuoc_don_vi_thuoc_phieu_kham(phieu_kham_id, thuoc_don_vi_thuoc_id, so_luong, cach_dung):
    thuoc_don_vi_thuoc_phieu_kham = ThuocDonViThuoc_PhieuKham(thuoc_don_vi_thuoc_id=thuoc_don_vi_thuoc_id,
                                                     phieu_kham_id=phieu_kham_id,
                                                     so_luong=so_luong,
                                                     cach_dung=cach_dung)

    db.session.add(thuoc_don_vi_thuoc_phieu_kham)
    db.session.commit()


def xoa_phieu_kham(phieu_kham_id):
    try:
        db.session.query(PhieuKham).filter(PhieuKham.id.__eq__(phieu_kham_id)).delete()
        db.session.commit()
    except:
        db.session.rollback()


def them_hoa_don(phieu_kham_id, tien_kham, tien_thuoc):
    hoa_don = HoaDon(phieu_kham_id=phieu_kham_id, tien_kham=tien_kham, tien_thuoc=tien_thuoc)

    db.session.add(hoa_don)
    db.session.commit()