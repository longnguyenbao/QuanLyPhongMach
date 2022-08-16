import math
from flask import render_template, url_for, request, redirect, flash
from admin import *
from app import utils, utils1, login
from app.decorator import admin_required
from flask_login import login_user, logout_user
import cloudinary.uploader
from datetime import datetime


@app.route("/")
def home():
    err_msg=""
    try:
        so_benh_nhan = utils1.get_quy_dinh().so_benh_nhan
    except Exception as ex:
        err_msg = str(ex)

    return render_template("index.html", so_benh_nhan=so_benh_nhan, err_msg=err_msg)


@login.user_loader
def load_user(user_id):

    return utils1.get_user_by_id(user_id=user_id)


@app.route("/admin/login", methods=["POST"])
def admin_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = utils1.check_user(username=username,password=password)
    if user:
        login_user(user=user)

    return redirect("/admin")


@app.route("/register", methods=["get", "post"])
def register():
    err_msg = ""
    if request.method.__eq__("POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("pass")
        confirm = request.form.get("confirm")

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get("avatar")
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res["secure_url"]

            try:
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar)
                return redirect(url_for("login"))

            except Exception as ex:
                err_msg = "Đã xảy ra lỗi" + str(ex)
        else:
            err_msg = "Mật khẩu không trùng khớp"

    return render_template("register.html", err_msg=err_msg)


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("pass")
        user = utils1.check_user(username=username, password=password)
        if user:
            login_user(user=user)
            if "next" in request.args and request.args["next"].startswith("http"):
                return redirect(request.args["next"])
            return redirect(url_for(request.args.get("next", "home")))
        else:
            err_msg = "Đã xảy ra lỗi"

    return render_template("login.html", err_msg=err_msg)


@app.route("/user-logout")
def logout():
    logout_user()

    return redirect(url_for("login"))


@app.route("/dang-ky-kham", methods=["get", "post"])
def dang_ky_kham():
    err_msg = ""
    success_msg = ""
    ngay_kham = datetime.today().strftime('%Y-%m-%d')
    if request.method.__eq__("POST"):
        ngay_kham = request.form.get("ngay-kham")
        try:
            if utils1.kiem_tra_ngay_hop_le(ngay_kham):
                if utils1.kiem_tra_ngay_ton_tai(ngay_kham) == 0:
                    utils.them_ngay(ngay_kham)

                danh_sach_ten = request.form.getlist("ho-ten")
                danh_sach_gioi_tinh = request.form.getlist("gioi-tinh")
                danh_sach_nam_sinh = request.form.getlist("nam-sinh")
                danh_sach_dia_chi = request.form.getlist("dia-chi")

                if len(danh_sach_ten) > 0 and len(danh_sach_gioi_tinh) > 0 and len(danh_sach_nam_sinh) > 0 and len(danh_sach_dia_chi) > 0:
                    for (t, g, n, d) in zip(danh_sach_ten, danh_sach_gioi_tinh, danh_sach_nam_sinh, danh_sach_dia_chi):
                        benh_nhan = utils1.get_benh_nhan(t, g, n, d)
                        if benh_nhan.count() == 0: # kiểm tra bệnh nhân đã có trong bảng bệnh nhân chưa nếu chưa thì thêm mới bệnh nhân
                            utils.them_benh_nhan(t, g, n, d)

                        benh_nhan_id = utils1.get_benh_nhan(t, g, n, d).first().id
                        ngay_kham_id = utils1.get_ngay_kham(ngay_kham).id

                        if utils1.kiem_tra_benh_nhan(benh_nhan_id, ngay_kham_id) == 0: # kiểm tra bệnh nhân đã có trong bảng bệnh nhân ngày khám chưa
                            if utils1.kiem_tra_so_benh_nhan_quy_dinh(ngay_kham_id):
                                utils.them_benh_nhan_ngay_kham(benh_nhan_id, ngay_kham_id)
                            else:
                                err_msg += "Đăng ký bệnh nhân {ten_benh_nhan} không thành công do đã đủ số bệnh nhân ngày {ngay} ".format(ten_benh_nhan=t, ngay=ngay_kham)

                if err_msg:
                    raise Exception(err_msg)

                success_msg += "Đăng ký thành công"
                flash(success_msg)
            else:
                err_msg = "Ngày {ngay} không hợp lệ vui lòng đăng ký ngày khác".format(ngay=ngay_kham)
                raise Exception(err_msg)
        except Exception as ex:
            err_msg = "Đã xảy ra lỗi: " + str(ex)

    return render_template("dang-ky-kham.html", err_msg=err_msg, ngay_kham=ngay_kham)


@app.route("/danh-sach-kham", methods=["get", "post"])
@admin_required
def danh_sach_kham():
    tinh_trang = []
    ngay = request.args.get("ngay")
    ngay_kham = ngay

    if utils1.kiem_tra_ngay_ton_tai(ngay_kham):
        page = request.args.get("page", 1)
        danh_sach_kham = utils1.load_danh_sach_benh_nhan_ngay_kham(ngay_kham=ngay_kham, page=int(page))
        for ds in danh_sach_kham:
            if utils1.kiem_tra_phieu_kham_ton_tai(ds[4]) == 0:
                tinh_trang.append(0)
            else:
                tinh_trang.append(1)

        ngay_kham_id = utils1.get_ngay_kham(ngay_kham).id
        quantity = utils1.dem_benh_nham(ngay_kham_id)

        return render_template("danh-sach-kham.html", ngay_kham=ngay_kham, danh_sach=zip(danh_sach_kham, tinh_trang),
                               pages=math.ceil(quantity / app.config["PAGE_SIZE"]))

    if request.method.__eq__("POST"):
        tinh_trang = []
        ngay_kham = request.form.get("ngay-kham")

        if utils1.kiem_tra_ngay_ton_tai(ngay_kham):
            page = request.args.get("page", 1)
            danh_sach_kham = utils1.load_danh_sach_benh_nhan_ngay_kham(ngay_kham=ngay_kham, page=int(page))
            for ds in danh_sach_kham:
                if utils1.kiem_tra_phieu_kham_ton_tai(ds[4]) == 0:
                    tinh_trang.append(0)
                else:
                    tinh_trang.append(1)

            ngay_kham_id = utils1.get_ngay_kham(ngay_kham).id
            quantity = utils1.dem_benh_nham(ngay_kham_id)

            return render_template("danh-sach-kham.html", ngay_kham=ngay_kham,
                                   danh_sach=zip(danh_sach_kham, tinh_trang),
                                   pages=math.ceil(quantity / app.config["PAGE_SIZE"]))

    return render_template("danh-sach-kham.html")


@app.route("/lap-phieu-kham/<int:benh_nhan_ngay_kham_id>", methods=["get", "post"])
@admin_required
def lap_phieu_kham(benh_nhan_ngay_kham_id):
    err_msg = ""
    try:
        thong_tin_benh_nhan_ngay_kham = utils1.get_benh_nhan_ngay_kham(benh_nhan_ngay_kham_id)
        if request.method.__eq__("POST"):
            if utils1.kiem_tra_phieu_kham_ton_tai(benh_nhan_ngay_kham_id) == 0:
                utils.them_phieu_kham(benh_nhan_ngay_kham_id)

                danh_sach_trieu_chung = request.form.getlist('trieu-chung')
                danh_sach_loai_benh = request.form.getlist('loai-benh')

                phieu_kham_id = utils1.get_phieu_kham(benh_nhan_ngay_kham_id).id

                if len(danh_sach_trieu_chung) > 0 and len(danh_sach_loai_benh) > 0:
                    for (t, l) in zip(danh_sach_trieu_chung, danh_sach_loai_benh):
                        if utils1.kiem_tra_trieu_chung_ton_tai(t) == 0:
                            utils.them_trieu_chung(t)
                        if utils1.kiem_tra_loai_benh_ton_tai(l) == 0:
                            utils.them_loai_benh(l)
                        trieu_chung_id = utils1.get_trieu_chung(t).id
                        loai_benh_id = utils1.get_loai_benh(l).id
                        if utils1.kiem_tra_trieu_chung_loai_benh_ton_tai(trieu_chung_id, loai_benh_id, phieu_kham_id) == 0:
                            utils.them_trieu_chung_loai_benh(trieu_chung_id, loai_benh_id, phieu_kham_id)

                danh_sach_thuoc = request.form.getlist("thuoc")
                danh_sach_don_vi = request.form.getlist("don-vi")
                danh_sach_so_luong = request.form.getlist("so-luong")
                danh_sach_cach_dung = request.form.getlist("cach-dung")

                if len(danh_sach_thuoc) > 0 and len(danh_sach_don_vi) > 0 and len(danh_sach_so_luong) > 0 and len(danh_sach_cach_dung) > 0:
                    for (t, d, s, c) in zip(danh_sach_thuoc, danh_sach_don_vi, danh_sach_so_luong, danh_sach_cach_dung):
                        if utils1.kiem_tra_thuoc_ton_tai(t) == 0: #nếu thuốc chưa có trong bảng thuốc
                            if utils1.kiem_tra_so_loai_thuoc_quy_dinh(): #nếu số lượng loại thuốc nhỏ hơn số lượng loại thuốc quy định
                                utils.them_thuoc(t)
                            else:
                                err_msg = "Lưu loại thuốc không thành công do đã quá số lượng thuốc quy định"
                                utils.xoa_phieu_kham(phieu_kham_id)
                                raise Exception(err_msg)

                        thuoc_id = utils1.get_thuoc(t).id
                        don_vi_thuoc_id = utils1.get_don_vi_thuoc(d).id

                        if utils1.kiem_tra_thuoc_don_vi_thuoc_ton_tai(thuoc_id, don_vi_thuoc_id) == 0:
                            utils.them_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id)

                        thuoc_don_vi_thuoc_id = utils1.get_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id).id
                        if utils1.kiem_tra_thuoc_don_vi_thuoc_phieu_kham_ton_tai(phieu_kham_id, thuoc_don_vi_thuoc_id) == 0:
                            utils.them_thuoc_don_vi_thuoc_phieu_kham(phieu_kham_id, thuoc_don_vi_thuoc_id, s, c)

                        utils.cap_nhat_thuoc_don_vi_thuoc(thuoc_id, don_vi_thuoc_id, s)

                success_msg = "Lưu phiếu khám thành công"
                flash(success_msg)

                return redirect(url_for('chi_tiet_phieu_kham', benh_nhan_ngay_kham_id=benh_nhan_ngay_kham_id))

            else:
                err_msg = "Phiếu khám đã tồn tại"
                raise Exception(err_msg)

    except Exception as ex:
        err_msg = "Đả xảy ra lỗi: " + str(ex)

    return render_template("lap-phieu-kham.html", thong_tin_benh_nhan_ngay_kham=thong_tin_benh_nhan_ngay_kham, err_msg=err_msg)


@app.route("/chi-tiet-phieu-kham/<int:benh_nhan_ngay_kham_id>", methods=["get", "post"])
@admin_required
def chi_tiet_phieu_kham(benh_nhan_ngay_kham_id):
    err_msg = ""
    trieu_chung = []
    loai_benh = []
    thuoc = []

    try:
        thong_tin_benh_nhan_ngay_kham = utils1.get_benh_nhan_ngay_kham(benh_nhan_ngay_kham_id)
        phieu_kham = utils1.get_phieu_kham(benh_nhan_ngay_kham_id)
        trieu_chung = utils1.load_danh_sach_trieu_chung_by_phieu_kham_id(phieu_kham.id) # trả về table
        loai_benh = utils1.load_danh_sach_loai_benh_by_phieu_kham_id(phieu_kham.id)
        thuoc = utils1.load_danh_sach_thuoc_by_phieu_kham_id(phieu_kham.id)

        if request.method.__eq__("POST"):
            utils.xoa_phieu_kham(phieu_kham.id)
            return redirect(url_for('danh_sach_kham'))

    except Exception as ex:
        err_msg = "Đả xảy ra lỗi " + str(ex)

    return render_template("chi-tiet-phieu-kham.html", err_msg=err_msg,
                           thong_tin_benh_nhan_ngay_kham=thong_tin_benh_nhan_ngay_kham, trieu_chung=trieu_chung,
                           loai_benh=loai_benh, thuoc=thuoc)


@app.route("/lap-hoa-don/<int:benh_nhan_ngay_kham_id>", methods=["get", "post"])
@admin_required
def lap_hoa_don(benh_nhan_ngay_kham_id):
    err_msg = ""

    try:
        thong_tin_benh_nhan_ngay_kham = utils1.get_benh_nhan_ngay_kham(benh_nhan_ngay_kham_id)
        tien_kham = utils1.get_quy_dinh().so_tien_kham
        if request.method.__eq__("POST"):
            phieu_kham_id = utils1.get_phieu_kham(benh_nhan_ngay_kham_id).id
            if utils1.kiem_tra_hoa_don_ton_tai(phieu_kham_id) == 0:
                tien_kham = request.form.get('tien-kham')
                tien_thuoc = request.form.get('tien-thuoc')
                utils.them_hoa_don(phieu_kham_id, tien_kham, tien_thuoc)
                success_msg = "Lập hóa đơn thành công"
                flash(success_msg)
            else:
                err_msg = "Hóa đơn đã tồn tại"
                raise Exception(err_msg)

    except Exception as ex:
        err_msg = "Đả xảy ra lỗi: " + str(ex)

    return  render_template("lap-hoa-don.html", err_msg=err_msg, thong_tin_benh_nhan_ngay_kham=thong_tin_benh_nhan_ngay_kham, tien_kham=tien_kham)


if __name__ == "__main__":
    app.run(debug=True)