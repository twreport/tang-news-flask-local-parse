# 本模块负责上传推荐文章到tangwei.cc云端
from flask import Blueprint, request, jsonify
from api.controller.fly import FlyController
from api.utils.responses import response_with
from api.utils import responses as resp

fly_routes = Blueprint("fly_routes", __name__)

@fly_routes.route('/test', methods=['GET'])
def fly_test():
    fly = FlyController()
    result = fly.fly_test()
    return response_with(resp.SUCCESS_200, value={"result": result})