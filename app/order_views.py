from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session

from app.models import House, Order

order_blue = Blueprint('order',__name__)


@order_blue.route('/', methods=['POST'])
def order():
    dict = request.form
    house_id = int(dict.get('house_id'))
    start_date = datetime.strptime(dict.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')
    if not all([house_id, start_date, end_date]):
        return jsonify({'code':1009,'msg':'请填写入住时间'})
    if start_date > end_date:
        return jsonify({'code':1010,'msg':'请正确填写入住时间'})
    try:
        house = House.query.get(house_id)
    except:
        return jsonify({'code':1011,'msg':'没有相应的房间信息'})
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price
    try:
        order.add_update()
    except:
        return jsonify({'code': 401, 'msg': '数据库错误'})

    return jsonify({'code':200, 'msg': '请求成功'})


@order_blue.route('/orders/')
def orders():
    return render_template('orders.html')

@order_blue.route('/allorders/', methods=['GET'])
def all_orders():
    uid = session['user_id']
    order_list = Order.query.filter(Order.user_id == uid).order_by(Order.id.desc())
    order_list2 = [order.to_dict() for order in order_list]
    return jsonify({'code':200,'msg':'请求成功','olist':order_list2})

@order_blue.route('/lorders/', methods=['GET'])
def lorders_html():
    return render_template('lorders.html')


@order_blue.route('/fd/',methods=['GET'])
def lorders():
    user_id=session['user_id']
    hlist=House.query.filter(House.user_id == user_id)
    hid_list=[house.id for house in hlist]
    order_list=Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
    olist=[order.to_dict() for order in order_list]
    return jsonify({'code':'200','msg':'请求成功','olist':olist})

@order_blue.route('/order/<int:id>/',methods=['PUT'])
def status(id):
    status=request.form.get('status')
    order=Order.query.get(id)
    order.status=status
    if status in ['REJECTED','COMPLETE']:
        order.comment=request.form.get('comment')
    try:
        order.add_update()
    except:
        return jsonify({'code': 401, 'msg': '数据库错误'})

    return jsonify({'code':200, 'msg': '请求成功'})