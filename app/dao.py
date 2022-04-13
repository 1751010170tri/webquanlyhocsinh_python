from flask import request, flash, redirect, url_for
import hashlib

from flask_login import login_user
from sqlalchemy import func

from app import db, app
from app.models import HocSinh, Lop, Hoc, MonHoc


def loplist ():
    loplist= HocSinh.query\
    .join(Lop, HocSinh.lop_id == Lop.id) \
    .add_columns(HocSinh.firstname, HocSinh.lastname, Lop.name)\
    .all()
    return loplist


def GetStudentList(keyword=None, classname=None):
    student_list = HocSinh.query
    if keyword:
        student_list = student_list.filter(HocSinh.firstname.contains(keyword))
    if classname:
        student_list = student_list.filter(HocSinh.lop_id == classname)
    return student_list.all()


def add_mark(diem15p_lan1_ky1,diem15p_lan2_ky1,diem15p_lan3_ky1,diem15p_lan1_ky2,diem15p_lan2_ky2,diem15p_lan3_ky2,diem1tietlan1_ky1,diem1tiet_lan2_ky1,diem1tiet_lan1_ky2,diem1tiet_lan2_ky2,diemcuoiky1,diemcuoiky2,diemtb_ky1,diemtb_ky2,diemtb_canam,hocsinh_id,monhoc_id):
    try:
        new_hoc = Hoc(
            diem15p_lan1_ky1= diem15p_lan1_ky1 ,
            diem15p_lan2_ky1= diem15p_lan2_ky1 ,
            diem15p_lan3_ky1= diem15p_lan3_ky1 ,
            diem15p_lan1_ky2= diem15p_lan1_ky2 ,
            diem15p_lan2_ky2= diem15p_lan2_ky2 ,
            diem15p_lan3_ky2= diem15p_lan3_ky2 ,
            diem1tietlan1_ky1= diem1tietlan1_ky1 ,
            diem1tiet_lan2_ky1= diem1tiet_lan2_ky1 ,
            diem1tiet_lan1_ky2= diem1tiet_lan1_ky2,
            diem1tiet_lan2_ky2= diem1tiet_lan2_ky2 ,
            diemcuoiky1= diemcuoiky1,
            diemcuoiky2= diemcuoiky2,
            diemtb_ky1= diemtb_ky1,
            diemtb_ky2= diemtb_ky2,
            diemtb_canam= diemtb_canam,
            hocsinh_id= hocsinh_id,
            monhoc_id=monhoc_id,
        )
        db.session.add(new_hoc)
        db.session.commit()
        return Hoc.query.all()
    except Exception as ex:
        print(ex)
        return False


def tinhdiem(id):
    loplist = HocSinh.query \
        .join(Hoc, HocSinh.bangdiem == Hoc.hocsinh_id)\
        .add_columns(HocSinh.diemky1, HocSinh.diemky2,
                     Hoc.diemtb_ky1, Hoc.diemtb_ky2,Hoc.hocsinh_id,
                     ).filter(Hoc.hocsinh_id == id)  \
        .all()
    total1 = 0
    total2 = 0
    for i in loplist:
        total1 += i.diemtb_ky1
        total2 += i.diemtb_ky2
    HocSinh.diemky1 = total1/9
    HocSinh.diemky2 =  total2/9
    return loplist

def ClassStudent():
    class_name = Lop.query.all()
    return class_name

if __name__ =="__main__":
    print(tinhdiem(1))
