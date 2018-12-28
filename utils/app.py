
from flask import Flask

from app.house_views import house_blue
from app.models import db
from app.order_views import order_blue
from app.views import user_blue
from utils.config import Conf
from utils.settings import STATIC_PATH, TEMPLATE_PATH


def create_app():
    app = Flask(__name__,
                static_folder=STATIC_PATH,
                template_folder=TEMPLATE_PATH
                )
    app.config.from_object(Conf)

    app.register_blueprint(blueprint=user_blue,url_prefix='/user')
    app.register_blueprint(blueprint=house_blue,url_prefix='/house')
    app.register_blueprint(blueprint=order_blue,url_prefix='/order')
    db.init_app(app)

    return app
