from flask import Blueprint, request, jsonify
from api.controller.classify import ClassifyController
from api.utils.responses import response_with
from api.utils import responses as resp

classify_routes = Blueprint("classify_routes", __name__)

# 通过关键词分析每一篇公众号文章的分类
# 数据源：mysql数据库中push_weixin_articles_pool中的所有文章（sort=0）
# 数据分析结果：写回原表
# ========================= 在用！！！=============================
@classify_routes.route('/', methods=['GET'])
def classify_article_by_keywords():
    classify = ClassifyController()
    result = classify.classify_article_by_keywords()
    return response_with(resp.SUCCESS_200, value={"result": result})

# 通过人工智能语义分析，分析每一篇公众号文章的分类
# 正在积累数据，待完成状态
@classify_routes.route('/sci', methods=['GET'])
def make_sci_db():
    classify = ClassifyController()
    result = classify.make_sci_db()
    return response_with(resp.SUCCESS_200, value={"result": result})

# 通过结巴分词，将文章标题分词，将文章正文提取关键词，存入数据库中，方便后续AI分析调用
# 数据源：mysql数据库中push_weixin_articles_pool中的发表两天之内的文章
# 数据分析结果：写入mysql数据库中push_weixin_topics_pool
@classify_routes.route('/text', methods=['GET'])
def make_sci_text():
    classify = ClassifyController()
    result = classify.make_sci_text()
    return response_with(resp.SUCCESS_200, value={"result": result})