from app import app, db, utils, utils1
from app.models import QuyDinh, Thuoc, DonViThuoc, User, UserRole
from flask import redirect, request
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose("/")
    def index(self):
        thang_thong_ke = request.args.get("thang-thong-ke")

        thong_ke_doanh_thu = utils1.doanh_thu_stat(thang_thong_ke=thang_thong_ke)
        tong_doanh_thu = 0
        for tkdt in thong_ke_doanh_thu:
            if tkdt[2]:
                tong_doanh_thu += tkdt[2]

        thong_ke_su_dung_thuoc = utils1.su_dung_thuoc_stat(thang_thong_ke=thang_thong_ke)

        return self.render("admin/stats.html", thang_thong_ke=thang_thong_ke, thong_ke_doanh_thu=thong_ke_doanh_thu, tong_doanh_thu=tong_doanh_thu, thong_ke_su_dung_thuoc=thong_ke_su_dung_thuoc)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AdminAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ThuocView(AdminAuthenticatedView):
    column_filters = ["ten_thuoc"]


class DonViThuocView(AdminAuthenticatedView):
    column_filters = ["ten_don_vi"]


admin=Admin(app=app, name="Quản lý phòng mạch", template_mode="bootstrap4", index_view=MyAdminIndexView())
admin.add_view(AdminAuthenticatedView(User, db.session))
admin.add_view(AdminAuthenticatedView(QuyDinh, db.session, name="Quy định"))
admin.add_view(ThuocView(Thuoc, db.session, name="Thuốc"))
admin.add_view(DonViThuocView(DonViThuoc, db.session, name="Đơn vị thuốc"))
admin.add_view(StatsView(name="Thống kê"))
admin.add_view(LogoutView(name="Đăng xuất"))