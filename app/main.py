from flask import render_template, redirect, request, flash, url_for,session, app
from flask_login import login_user
from app import app, login, dao
from app.models import *
import hashlib
import time


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        if user:
            if user.type == 0:
                login_user(user=user)
            if user.type == 1:
                return render_template("user/menu.html")
    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/themhs", methods=['GET', 'POST'])
def insert():

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gioitinh = request.form['gioitinh']
        diachi = request.form['diachi']
        email = request.form['email']
        birth = request.form['birth']
        l = request.form['lop_id']
        lop = Lop.query.get(l)
        s = QuyDinh.query.get(1)

        if lop.siso < s.siso:
            my_data = HocSinh(firstname, lastname, gioitinh, diachi, email, birth, lop.id)
            db.session.add(my_data)
            db.session.commit()
            lop.siso = lop.siso + 1
            db.session.commit()
            flash("Thêm Học Sinh Thành Công")
            return redirect(url_for('insert'))
        else:
            flash("Đã Đủ Số Lượng Học Sinh")
            return redirect(url_for('insert'))
    lop = db.session.query(Lop).all()
    return render_template("user/themhs.html",Lop = lop)


@app.route("/diemmon", methods=['GET', 'POST'])
def hocsinh():
    lop = db.session.query(Lop).all()
    return render_template("user/tongketky.html", lop=lop)


@app.route("/dslop", methods=['GET', 'POST'])
def dslop():
    lop = db.session.query(Lop).all()
    return render_template("user/danhsachlop.html", lop=lop)


@app.route("/diemky",methods=['GET', 'POST'])
def show1():

    id_lop = int(request.args.get("id"))
    l = Lop.query.get(id_lop)

    hs = db.session.query(HocSinh).all()

    return render_template("user/diemky.html", id_lop=l.id,lp = l, hocsinh=hs)


@app.route("/xemct",methods=['GET', 'POST'])
def show():

    id_lop = int(request.args.get("id"))
    l = Lop.query.get(id_lop)

    hs = db.session.query(HocSinh).all()

    return render_template("user/chitiet.html", id_lop=l.id,lp = l, hocsinh=hs)


@app.route('/student-list', methods=["GET", 'POST'])
def GetStudentList():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    classname = request.args["classname"] if request.args.get("classname") else None
    return render_template("user/search.html", student_list=dao.GetStudentList(keyword=keyword, classname=classname)
                    , classes=dao.ClassStudent())


@app.route('/nhapdiem', methods=["GET", 'POST'])
def add_mark():
    if request.method == 'POST':
        t1 = request.form.get("t1")
        t2 = request.form.get("t2")
        t3 = request.form.get("t3")
        t4 = request.form.get("t4")
        t5 = request.form.get("t5")
        t6 = request.form.get("t6")
        x1 = request.form.get("x1")
        x2 = request.form.get("x2")
        x3 = request.form.get("x3")
        x4 = request.form.get("x4")
        k1 = request.form.get("k1")
        k2 = request.form.get("k2")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")
        e = request.form.get("e")
        h = request.form['namehs']
        m = request.form['namemon']

        if dao.add_mark(diem15p_lan1_ky1=t1, diem15p_lan2_ky1=t2, diem15p_lan3_ky1=t3,
                        diem15p_lan1_ky2=t4, diem15p_lan2_ky2=t5, diem15p_lan3_ky2=t6,
                        diem1tietlan1_ky1=x1, diem1tiet_lan2_ky1=x2, diem1tiet_lan1_ky2=x3, diem1tiet_lan2_ky2=x4,
                        diemcuoiky1=k1, diemcuoiky2=k2,
                        diemtb_ky1=p1, diemtb_ky2=p2,
                        diemtb_canam=e,
                        hocsinh_id=h,
                        monhoc_id=m):
            flash("thêm điểm thành công")
            return redirect(url_for('show2'))
        else:
            flash("Lỗi!!!")

    return redirect(url_for('show2'))


@app.route('/chonlop')
def show3():
    l=Lop.query.all()
    return render_template("user/chonlop.html", Lop=l)


@app.route('/chonlopsua')
def show4():
    l=Lop.query.all()
    return render_template("user/chonlopsua.html", Lop=l)


@app.route('/chonhs',methods=["GET", 'POST'])
def show5():
    if request.method == 'POST':
        id = request.form.get("namelop")
        hs = HocSinh.query.filter(HocSinh.lop_id == id)
        mh = MonHoc.query.all()
        return render_template("user/editmark.html", HocSinh=hs, MonHoc=mh)
    return redirect(url_for('show4'))


@app.route('/nhapdiem1',methods=["GET", 'POST'])
def show2():
    if request.method == 'POST':
        id=request.form.get("namelop")
        hs= HocSinh.query.filter(HocSinh.lop_id==id)
        mh= MonHoc.query.all()
        return render_template("user/nhapdiem.html", HocSinh=hs, MonHoc=mh)
    return redirect(url_for('show3'))


@app.route('/editmark',methods=["GET", 'POST'])
def edit_mark():
    if request.method == "POST":
        t1 = request.form.get("t1")
        t2 = request.form.get("t2")
        t3 = request.form.get("t3")
        t4 = request.form.get("t4")
        t5 = request.form.get("t5")
        t6 = request.form.get("t6")
        x1 = request.form.get("x1")
        x2 = request.form.get("x2")
        x3 = request.form.get("x3")
        x4 = request.form.get("x4")
        k1 = request.form.get("k1")
        k2 = request.form.get("k2")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")
        e = request.form.get("e")
        h = request.form['namehs']
        m = request.form['namemon']

        if Hoc.query.filter(Hoc.hocsinh_id == h, Hoc.monhoc_id == m):
            Hoc.diem15p_lan1_ky1 = t1
            Hoc.diem15p_lan2_ky1_ky1 = t2
            Hoc.diem15p_lan3_ky1_ky1 = t3
            Hoc.diem15p_lan1_ky2 = t4
            Hoc.diem15p_lan2_ky2 = t5
            Hoc.diem15p_lan3_ky2 = t6
            Hoc.diem1tietlan1_ky1 = x1
            Hoc.diem1tiet_lan2_ky1 = x2
            Hoc.diem1tiet_lan1_ky2 = x3
            Hoc.diem1tiet_lan2_ky2 = x4
            Hoc.diemcuoiky1 = k1
            Hoc.diemcuoiky2 = k2
            Hoc.diemtb_ky1 = p1
            Hoc.diemtb_ky2 = p2
            Hoc.diemtb_canam = e
            db.session.commit()
            flash("Sửa điểm thành công")
            return redirect(url_for('show5'))
        else:
            flash("Đã xảy ra lỗi!!!")

    return redirect(url_for('show4'))


if __name__ == '__main__':
    app.run(debug=True)
