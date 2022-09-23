import os
import logging
from flask import Flask
from flask import jsonify
from api.utils.database import mysql_db
from api.utils.database import ma
from flask_mongoengine import MongoEngine
from api.routes.parse import parse_routes
from api.routes.location import location_routes
from api.routes.classify import classify_routes
from api.routes.topic import topic_routes
from api.routes.fly import fly_routes
from api.routes.test import test_routes
from api.utils.responses import response_with
import api.utils.responses as resp
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

# 根据不同环境读取相应配置
app.config.from_object(app_config)

# 避免中文返回ascii码
app.config['JSON_AS_ASCII'] = False

# 设置mongoDB
app.config['MONGODB_SETTINGS'] = {
    'db': 'weixin',
    'host': '10.168.1.100',
    'port': 27017
}
mongo_db = MongoEngine()
mongo_db.init_app(app)


# 初始化数据库和json模块
mysql_db.init_app(app)
ma.init_app(app)
with app.app_context():
    mysql_db.create_all()

# 注册模块的路由
app.register_blueprint(parse_routes, url_prefix='/api/parse')
app.register_blueprint(location_routes, url_prefix='/api/location')
app.register_blueprint(classify_routes, url_prefix='/api/classify')
app.register_blueprint(fly_routes, url_prefix='/api/fly')
app.register_blueprint(test_routes, url_prefix='/api/test')
app.register_blueprint(topic_routes, url_prefix='/api/topic')

# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
