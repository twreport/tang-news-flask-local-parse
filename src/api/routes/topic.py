from flask import Blueprint, request, jsonify
from api.controller.topic import TopicController
from api.utils.responses import response_with
from api.utils import responses as resp

topic_routes = Blueprint("topic_routes", __name__)

@topic_routes.route('/cluster', methods=['GET'])
def get_test_list():
    topic = TopicController()
    result = topic.make_cluster()
    return response_with(resp.SUCCESS_200, value={"result": result})
