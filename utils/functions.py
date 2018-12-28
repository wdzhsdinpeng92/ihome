from functools import wraps

from flask import session,redirect,url_for


def login_required(func):
    @wraps(func)
    def check_status(*args,**kwargs):
        try:
            session['user_id']
        except:
            return redirect(url_for('user.login'))
        return func(*args,**kwargs)
    return check_status

def get_sqlalchemy_uri(DATABASE):
    # mysql+pymysql://root:123456@127.0.0.1:3306/flask7
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']
    return '%s+%s://%s:%s@%s:%s/%s' % (engine, driver,
                                       user, password,
                                       host, port, name
                                       )