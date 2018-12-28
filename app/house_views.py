import os

from flask import Blueprint, render_template, jsonify, request, session
from app.models import Area, Facility, House, HouseImage, User, Order
from utils.settings import MEDIA_PATH

house_blue = Blueprint('house',__name__)


@house_blue.route('/index/')
def house():
    return render_template('index.html')


@house_blue.route('/detail/',methods=['GET'])
def detail():
    return render_template('detail.html')

@house_blue.route('/detail/<int:id>/',methods=['GET'])
def house_detail(id):
    house = House.query.get(id)
    facility_list = house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    booking = 1
    if 'user_id' in session:
        if house.user_id == session['user_id']:
            booking = 0
    return jsonify({'code':200,'msg':'请求成功','house':house.to_full_dict(),'facility_list':facility_dict_list,'booking':booking})



@house_blue.route('/newhouse/',methods=['GET'])
def newhouse():
    return render_template('newhouse.html')

@house_blue.route('/newhouse/',methods=['POST'])
def post_newhouse():
    params = request.form.to_dict()
    facility_ids = request.form.getlist('facility')
    house = House()
    house.user_id = session['user_id']
    house.area_id = params.get('area_id')
    house.title = params.get('title')
    house.price = params.get('price')
    house.address = params.get('address')
    house.room_count = params.get('room_count')
    house.acreage = params.get('acreage')
    house.beds = params.get('beds')
    house.unit = params.get('unit')
    house.capacity = params.get('capacity')
    house.deposit = params.get('deposit')
    house.min_days = params.get('min_days')
    house.max_days = params.get('max_days')
    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
    house.add_update()
    return jsonify({'code':200,'msg':'请求成功','house_id':house.id})

@house_blue.route('/image/',methods=['POST'])
def newhouse_image():
    house_id = request.form.get('house_id')
    house_image = request.files.get('house_image')
    image_name = 'house-%s-%s' % (house_id,house_image.filename)
    url = os.path.join(MEDIA_PATH,image_name)
    house_image.save(url)
    image = HouseImage()
    image.house_id = house_id
    image.url = '/static/images/%s' % (image_name)
    image.add_update()
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image.url
        house.add_update()
        # 返回图片信息
    return jsonify({'code':200,'msg':'请求成功','url':image.url})


@house_blue.route('/area_facility/',methods=['GET'])
def area_facility():
    #查询地址
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    #查询设施
    facility_list = Facility.query.all()
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    return jsonify(area=area_dict_list,facility=facility_dict_list)


@house_blue.route('/booking/',methods=['GET'])
def booking():
    return render_template('booking.html')


@house_blue.route('/getbookingbyid/<int:id>/')
def get_booking_by_id(id):
    house = House.query.get(id)
    return jsonify(house=house.to_dict())


@house_blue.route('/hindex/', methods=['GET'])
def hindex():
    user_name = ''
    code = ''
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = 200
    hlist = House.query.order_by(House.id.desc()).all()[:5]
    hlist2 = [house.to_dict() for house in hlist]
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    return jsonify(code=code, name=user_name, hlist=hlist2, alist=area_dict_list)

@house_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')

@house_blue.route('/searchall/', methods=['GET'])
def searchall():
    dict = request.args
    sort_key = dict.get('sk')
    a_id = dict.get('aid')
    begin_date = dict.get('sd')
    end_date = dict.get('ed')

    houses = House.query.filter_by(area_id=a_id)
    if 'user_id' in session:
        hlist = houses.filter(House.user_id != (session['user_id']))
    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    order_list = Order.query.filter(Order.status != 'REJECTED')
    # 情况一：
    order_list1 = Order.query.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
    # 情况二：
    order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
    # 情况三：
    order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
    # 情况四：
    order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids = [order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
        # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = hlist.filter(House.id.notin_(house_ids))
    # 排序规则,默认根据最新排列
    sort = House.id.desc()
    if sort_key == 'booking':
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        sort = House.price.asc()
    elif sort_key == 'price-des':
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    # hlist = [house.to_dict() for house in hlist]
    houselist = []
    for house in hlist:
        housedict = house.to_dict()
        user = User.query.get(house.user_id)
        housedict['landlord'] = user.avatar
        houselist.append(housedict)
    # 获取区域信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    return jsonify(code=200, houses=houselist, areas=area_dict_list)
