from app import app, db
from app.models import User, BenhNhan, NgayKham, BenhNhan_NgayKham, QuyDinh, PhieuKham, TrieuChung, LoaiBenh, TrieuChung_LoaiBenh, Thuoc, DonViThuoc, Thuoc_DonViThuoc, ThuocDonViThuoc_PhieuKham, HoaDon
import hashlib
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql import extract


def get_user_by_id(user_id=None):

    return User.query.get(user_id)


def check_user(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

    return None


def kiem_tra_ngay_hop_le(ngay_kham):
    if ngay_kham >= datetime.today().strftime('%Y-%m-%d'):
        return 1
    return 0


def kiem_tra_ngay_ton_tai(ngay_kham): #kiểm tra ngày có trong bảng chưa
    ngay = NgayKham.query.filter(NgayKham.ngay_kham.__eq__(ngay_kham)).count()

    if ngay > 0:
        return 1
    return 0


def get_benh_nhan(ten, gioi_tinh, nam_sinh, dia_chi):
    benh_nhan = BenhNhan.query.filter(BenhNhan.active.__eq__(True)).\
        filter(BenhNhan.ten.__eq__(ten)).\
        filter(BenhNhan.gioi_tinh.__eq__(gioi_tinh)).\
        filter(BenhNhan.nam_sinh.__eq__(nam_sinh)).\
        filter(BenhNhan.dia_chi.__eq__(dia_chi))

    return benh_nhan


def get_ngay_kham(ngay_kham):
    ngay = NgayKham.query.filter(NgayKham.ngay_kham.__eq__(ngay_kham)).first()

    return ngay


def dem_benh_nham(ngay_kham_id):
    return BenhNhan_NgayKham.query.filter(BenhNhan_NgayKham.ngay_kham_id.__eq__(ngay_kham_id)). \
        count()


def kiem_tra_benh_nhan(benh_nhan_id, ngay_kham_id):
    kiem_tra = BenhNhan_NgayKham.query.filter(BenhNhan_NgayKham.benh_nhan_id.__eq__(benh_nhan_id)). \
        filter(BenhNhan_NgayKham.ngay_kham_id.__eq__(ngay_kham_id)). \
        count()

    if kiem_tra > 0:
        return 1
    return 0


def get_quy_dinh():
    quy_dinh = QuyDinh.query.filter(QuyDinh.id.__eq__(1)).first()

    return quy_dinh


def kiem_tra_so_benh_nhan_quy_dinh(ngay_kham_id):
    tong_benh_nhan_trong_ngay = BenhNhan_NgayKham.query.filter(BenhNhan_NgayKham.ngay_kham_id.__eq__(ngay_kham_id)).count()
    quy_dinh = get_quy_dinh()

    if tong_benh_nhan_trong_ngay >= quy_dinh.so_benh_nhan:
        return 0
    return 1


def kiem_tra_so_loai_thuoc_quy_dinh():
    tong_so_loai_thuoc = Thuoc.query.count()
    quy_dinh = get_quy_dinh()

    if tong_so_loai_thuoc >= quy_dinh.so_loai_thuoc:
        return 0
    return 1




def load_danh_sach_benh_nhan_ngay_kham(ngay_kham=None, page=1):
    q = db.session.query(BenhNhan.ten, BenhNhan.gioi_tinh, BenhNhan.nam_sinh, BenhNhan.dia_chi, BenhNhan_NgayKham.id,
                         NgayKham.ngay_kham, BenhNhan.id). \
        join(BenhNhan_NgayKham, BenhNhan_NgayKham.benh_nhan_id.__eq__(BenhNhan.id), isouter=True). \
        join(NgayKham, BenhNhan_NgayKham.ngay_kham_id.__eq__(NgayKham.id), isouter=False)

    if ngay_kham:
        q = q.filter(NgayKham.ngay_kham.__eq__(ngay_kham))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size

    return q.slice(start, start+page_size).all()


def get_benh_nhan_ngay_kham(benh_nhan_ngay_kham_id):
    benh_nhan_ngay_kham = db.session.query(BenhNhan.ten, BenhNhan.gioi_tinh, BenhNhan.nam_sinh, BenhNhan.dia_chi, BenhNhan_NgayKham.id,
                         NgayKham.ngay_kham, BenhNhan.id). \
        join(BenhNhan_NgayKham, BenhNhan_NgayKham.benh_nhan_id.__eq__(BenhNhan.id), isouter=True). \
        join(NgayKham, BenhNhan_NgayKham.ngay_kham_id.__eq__(NgayKham.id), isouter=False).\
        filter(BenhNhan_NgayKham.id.__eq__(benh_nhan_ngay_kham_id)).\
        first()

    return benh_nhan_ngay_kham


def kiem_tra_phieu_kham_ton_tai(benh_nhan_ngay_kham_id):
    kiem_tra = PhieuKham.query.filter(PhieuKham.benh_nhan_ngay_kham_id.__eq__(benh_nhan_ngay_kham_id)).count()

    if kiem_tra > 0:
        return 1
    return 0


def get_phieu_kham(benh_nhan_ngay_kham_id):
    phieu_kham = PhieuKham.query.filter(PhieuKham.benh_nhan_ngay_kham_id.__eq__(benh_nhan_ngay_kham_id)).first()

    return phieu_kham


def kiem_tra_trieu_chung_ton_tai(ten_trieu_chung):
    kiem_tra = TrieuChung.query.filter(TrieuChung.ten_trieu_chung.__eq__(ten_trieu_chung)).count()

    if kiem_tra > 0:
        return 1
    return 0


def kiem_tra_loai_benh_ton_tai(ten_loai_benh):
    kiem_tra = LoaiBenh.query.filter(LoaiBenh.ten_loai_benh.__eq__(ten_loai_benh)).count()

    if kiem_tra > 0:
        return 1
    return 0


def get_trieu_chung(ten_trieu_chung):
    trieu_chung = TrieuChung.query.filter(TrieuChung.ten_trieu_chung.__eq__(ten_trieu_chung)).first()

    return trieu_chung


def get_loai_benh(ten_loai_benh):
    loai_benh = LoaiBenh.query.filter(LoaiBenh.ten_loai_benh.__eq__(ten_loai_benh)).first()

    return loai_benh


def kiem_tra_trieu_chung_loai_benh_ton_tai(trieu_chung_id, loai_benh_id, phieu_kham_id):
    kiem_tra = TrieuChung_LoaiBenh.query.filter(TrieuChung_LoaiBenh.trieu_chung_id.__eq__(trieu_chung_id)).\
        filter(TrieuChung_LoaiBenh.loai_benh_id.__eq__(loai_benh_id)). \
        filter(TrieuChung_LoaiBenh.phieu_kham_id.__eq__(phieu_kham_id)). \
        count()

    if kiem_tra > 0:
        return 1
    return 0


def kiem_tra_thuoc_ton_tai(ten_thuoc):
    kiem_tra = Thuoc.query.filter(Thuoc.ten_thuoc.__eq__(ten_thuoc)).count()

    if kiem_tra > 0:
        return 1
    return 0


def get_thuoc(ten_thuoc):
    thuoc = Thuoc.query.filter(Thuoc.ten_thuoc.__eq__(ten_thuoc)).first()

    return thuoc


def get_don_vi_thuoc(ten_don_vi):
    don_vi = DonViThuoc.query.filter(DonViThuoc.ten_don_vi.__eq__(ten_don_vi)).first()

    return don_vi


def kiem_tra_thuoc_don_vi_thuoc_ton_tai(thuoc_id, don_vi_thuoc_id):
    kiem_tra = Thuoc_DonViThuoc.query.filter(Thuoc_DonViThuoc.thuoc_id.__eq__(thuoc_id)).\
        filter(Thuoc_DonViThuoc.don_vi_thuoc_id.__eq__(don_vi_thuoc_id)).\
        count()

    if kiem_tra > 0:
        return 1
    return 0


def get_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id):
    thuoc_don_vi_thuoc = Thuoc_DonViThuoc.query.filter(Thuoc_DonViThuoc.thuoc_id.__eq__(thuoc_id)).\
        filter(Thuoc_DonViThuoc.don_vi_thuoc_id.__eq__(don_vi_thuoc_id)).\
        first()

    return thuoc_don_vi_thuoc


def kiem_tra_thuoc_don_vi_thuoc_phieu_kham_ton_tai(phieu_kham_id, thuoc_don_vi_thuoc_id):
    kiem_tra = ThuocDonViThuoc_PhieuKham.query.filter(ThuocDonViThuoc_PhieuKham.phieu_kham_id.__eq__(phieu_kham_id)).\
        filter(ThuocDonViThuoc_PhieuKham.thuoc_don_vi_thuoc_id.__eq__(thuoc_don_vi_thuoc_id)).\
        count()

    if kiem_tra > 0:
        return 1
    return 0


def load_danh_sach_trieu_chung_by_phieu_kham_id(phieu_kham_id):
    q = db.session.query(TrieuChung_LoaiBenh.phieu_kham_id, TrieuChung.ten_trieu_chung).\
        filter(TrieuChung_LoaiBenh.phieu_kham_id.__eq__(phieu_kham_id)).\
        join(TrieuChung, TrieuChung.id.__eq__(TrieuChung_LoaiBenh.trieu_chung_id), isouter=False).\
        group_by(TrieuChung.ten_trieu_chung)

    return q


def load_danh_sach_loai_benh_by_phieu_kham_id(phieu_kham_id):
    q = db.session.query(TrieuChung_LoaiBenh.phieu_kham_id, LoaiBenh.ten_loai_benh).\
        filter(TrieuChung_LoaiBenh.phieu_kham_id.__eq__(phieu_kham_id)).\
        join(LoaiBenh, LoaiBenh.id.__eq__(TrieuChung_LoaiBenh.loai_benh_id), isouter=False).\
        group_by(LoaiBenh.ten_loai_benh)

    return q


def load_danh_sach_thuoc_by_phieu_kham_id(phieu_kham_id):
    q = db.session.query(ThuocDonViThuoc_PhieuKham.phieu_kham_id, Thuoc.ten_thuoc, DonViThuoc.ten_don_vi, ThuocDonViThuoc_PhieuKham.so_luong, ThuocDonViThuoc_PhieuKham.cach_dung).\
        filter(ThuocDonViThuoc_PhieuKham.phieu_kham_id.__eq__(phieu_kham_id)). \
        join(Thuoc_DonViThuoc, Thuoc_DonViThuoc.id.__eq__(ThuocDonViThuoc_PhieuKham.thuoc_don_vi_thuoc_id), isouter=False).\
        join(Thuoc, Thuoc.id.__eq__(Thuoc_DonViThuoc.thuoc_id), isouter=False).\
        join(DonViThuoc, DonViThuoc.id.__eq__(Thuoc_DonViThuoc.don_vi_thuoc_id), isouter=False)

    return q


def kiem_tra_hoa_don_ton_tai(phieu_kham_id):
    kiem_tra = HoaDon.query.filter(HoaDon.phieu_kham_id.__eq__(phieu_kham_id)).count()

    if kiem_tra > 0:
        return 1
    return 0


def doanh_thu_stat(thang_thong_ke=None):
    q = db.session.query(NgayKham.ngay_kham, func.count(BenhNhan.id), func.sum(HoaDon.tien_kham)+func.sum(HoaDon.tien_thuoc), extract("day", NgayKham.ngay_kham) ).\
        join(BenhNhan_NgayKham, BenhNhan_NgayKham.ngay_kham_id.__eq__(NgayKham.id), isouter=True).\
        join(BenhNhan, BenhNhan.id.__eq__(BenhNhan_NgayKham.benh_nhan_id), isouter=True).\
        join(PhieuKham, PhieuKham.benh_nhan_ngay_kham_id.__eq__(BenhNhan_NgayKham.id), isouter=True).\
        join(HoaDon, HoaDon.phieu_kham_id.__eq__(PhieuKham.id), isouter=True).\
        group_by(NgayKham.ngay_kham)

    if thang_thong_ke:
        thang_thong_ke = thang_thong_ke.split("-")
        q = q.filter(extract("year", NgayKham.ngay_kham)==thang_thong_ke[0]).\
        filter(extract("month", NgayKham.ngay_kham)==thang_thong_ke[1])

    else:
        thang_thong_ke = datetime.today().strftime('%Y-%m')
        thang_thong_ke = thang_thong_ke.split("-")
        q = q.filter(extract("year", NgayKham.ngay_kham) == thang_thong_ke[0]). \
            filter(extract("month", NgayKham.ngay_kham) == thang_thong_ke[1])

    return q


def su_dung_thuoc_stat(thang_thong_ke=None):
    q = db.session.query(Thuoc.ten_thuoc, DonViThuoc.ten_don_vi, Thuoc_DonViThuoc.tong_so_luong, func.sum(ThuocDonViThuoc_PhieuKham.so_luong) ).\
        join(Thuoc_DonViThuoc, Thuoc_DonViThuoc.don_vi_thuoc_id.__eq__(DonViThuoc.id), isouter=False).\
        join(Thuoc, Thuoc.id.__eq__(Thuoc_DonViThuoc.thuoc_id), isouter=True).\
        join(ThuocDonViThuoc_PhieuKham, ThuocDonViThuoc_PhieuKham.thuoc_don_vi_thuoc_id.__eq__(Thuoc_DonViThuoc.id), isouter=True). \
        join(PhieuKham, PhieuKham.id.__eq__(ThuocDonViThuoc_PhieuKham.phieu_kham_id), isouter=True). \
        group_by(Thuoc.ten_thuoc, DonViThuoc.ten_don_vi)

    if thang_thong_ke:
        thang_thong_ke = thang_thong_ke.split("-")
        q = q.filter(extract("year", PhieuKham.ngay_lap_phieu) == thang_thong_ke[0]). \
            filter(extract("month", PhieuKham.ngay_lap_phieu) == thang_thong_ke[1])

    else:
        thang_thong_ke = datetime.today().strftime('%Y-%m')
        thang_thong_ke = thang_thong_ke.split("-")
        q = q.filter(extract("year", PhieuKham.ngay_lap_phieu) == thang_thong_ke[0]). \
            filter(extract("month", PhieuKham.ngay_lap_phieu) == thang_thong_ke[1])

    return q