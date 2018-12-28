import os
import random
import re
from flask import Blueprint, render_template, jsonify, request, session


from app.form import UserRegisterForm, UserLoginForm
from app.models import User, House
from utils.functions import login_required
from utils.settings import MEDIA_PATH

user_blue = Blueprint('user',__name__)

@user_blue.route('img_code/',methods=['GET'])
def img_code():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['code'] = code
    return jsonify({'code':200,'msg':'请求成功','data':code})

@user_blue.route('/register/',methods=['GET','POST'])
def register():
    form = UserRegisterForm()
    if request.method == 'GET':
        return render_template('register.html',form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            mobile = form.mobile.data
            password = form.password.data
            imagecode = request.form.get('imagecode')
            code = session.get('code')
            if imagecode != code:
                return jsonify({'code':1007,'msg':'验证码错误'})
            user = User.query.filter(User.phone == mobile).first()
            if user:
                return jsonify({'code': 1001, 'msg': '该用户已注册'})
            user = User()
            user.phone = mobile
            user.password = password
            user.name = '爱家'+mobile
            user.add_update()
            return jsonify({'code':200,'msg':'请求成功'})
        else:
            return jsonify({'code': 1002, 'msg': '请求失败'})


@user_blue.route('/login/',methods=['GET','POST'])
def login():
    form = UserLoginForm()
    if request.method == 'GET':
        return render_template('login.html',form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            mobile = form.mobile.data
            password = form.password.data
            user = User.query.filter(User.phone == mobile).first()
            if not user:
                return jsonify({'code': 1003, 'msg': '用户没有注册，请前往注册'})
            if not user.check_pwd(password):
                return jsonify({'code': 1004, 'msg': '密码不正确'})
            session['user_id'] = user.id
            return jsonify({'code': 200, 'msg': '请求成功'})




@user_blue.route('/user_index/',methods=['GET'])
def user_index():
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    user_info = user.to_basic_dict()
    return jsonify({'code': 200, 'msg': '请求成功', 'user_info': user_info})


@user_blue.route('/get_user/',methods=['GET'])
def get_user():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        user_info = user.to_basic_dict() if user else {}
        user_auth = user.to_auth_dict() if user else {}
        return jsonify({'code':200,'msg':'请求成功','user_info':user_info,'user_auth':user_auth})


@user_blue.route('/my/',methods=['GET'])
@login_required
def my():
    if request.method == 'GET':
        return render_template('my.html')


@user_blue.route('/profile/',methods=['GET','POST','PATCH'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'POST':
        avatar = request.files.get('avatar')
        name = request.form.get('name')
        user_id = session['user_id']
        user = User.query.get(user_id)
        if avatar:
            avatar_name = 'user-%s-%s' % (user_id,avatar.filename)
            path = os.path.join(MEDIA_PATH, avatar_name)
            avatar.save(path)
            user.avatar = avatar_name
        if name:
            user.name = name if name else ''
        user.add_update()
        user_info = user.to_basic_dict()
        return jsonify({'code':200,'msg':'请求成功','user_info':user_info})

@user_blue.route('/myprofile/',methods=['GET'])
def myprofile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_info = user.to_basic_dict()
    return jsonify({'code': 200, 'msg': '请求成功', 'user_info': user_info})

@user_blue.route('/auth/',methods=['GET'])
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')

@user_blue.route('/user_auth/',methods=['GET','POST'])
def user_auth():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user_auth = user.to_auth_dict()
        if user_auth['id_name']:
            return jsonify({'code':200,'msg':'请求成功','user_auth':user_auth})
        else:
            return jsonify({'code': 1005, 'msg': '该用户未实名认证'})
    if request.method == 'POST':
        id_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        name = r'^(([a-zA-Z+\.?\·?a-zA-Z+]{2,30}$)|([\u4e00-\u9fa5+\·?\u4e00-\u9fa5+]{2,30}$))'
        card = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)'
        user = User.query.filter(User.id_card == id_card).first()
        if user:
            return jsonify({'code':1006,'msg':'该身份证已注册'})
        if all([id_name,id_card]):
            if re.fullmatch(card,id_card) and re.fullmatch(name,id_name):
                user_id = session.get('user_id')
                user = User.query.get(user_id)
                user.id_card = id_card
                user.id_name = id_name
                user.add_update()
                user_auth = user.to_auth_dict()
                return jsonify({'code':200,'msg':'请求成功','user_auth':user_auth})
            else:
                return jsonify({'code':1008,'msg':'请输入正确实名信息'})

@user_blue.route('/myhouse/',methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')

@user_blue.route('/user_myhouse/',methods=['GET','POST'])
def user_myhouse():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user.id_name:
            house_list = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
            house_list2 = []
            for house in house_list:
                house_list2.append(house.to_dict())
            return jsonify({'code':200,'msg':'请求成功','hlist':house_list2})
        else:
            return jsonify({'code':1005,'msg':'该用户未实名认证'})


@user_blue.route('/logout/', methods=['DELETE'])
@login_required
def user_logout():
    session.clear()
    return jsonify({'code':200,'msg':'请求成功'})