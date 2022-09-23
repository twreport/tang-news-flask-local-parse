from flask import Blueprint, request, jsonify
from api.controller.parse import ParseController
from api.utils.responses import response_with
from api.utils import responses as resp

parse_routes = Blueprint("parse_routes", __name__)

# 计算每一篇文章的log增长率和阅读数，并存入mongoDB
# ========================= 在用！！！=============================
@parse_routes.route('/', methods=['GET'])
def parse_article():
    parse = ParseController()
    result = parse.parse_article()
    return response_with(resp.SUCCESS_200, value={"result": result})

# 计算每一个公众号的平均阅读量和平均增长率
# ========================= 在用！！！=============================
@parse_routes.route('/avg', methods=['GET'])
def count_avg_of_bizs():
    parse = ParseController()
    result = parse.count_avg_of_bizs()
    return response_with(resp.SUCCESS_200, value={"result": result})

# 扫描比对每一篇文章的得分，决定是否推送到push_weixin_article之中
# ========================= 在用！！！=============================
@parse_routes.route('/scan', methods=['GET'])
def scan_articles():
    parse = ParseController()
    result = parse.scan_articles()
    return response_with(resp.SUCCESS_200, value={"result": result})