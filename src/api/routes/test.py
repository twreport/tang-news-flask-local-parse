from flask import Blueprint, request, jsonify
from api.controller.test import TestController
from api.utils.responses import response_with
from api.utils import responses as resp

test_routes = Blueprint("test_routes", __name__)

@test_routes.route('/', methods=['GET'])
def get_test_list():
    test = TestController()
    result = test.get_test_list()
    return response_with(resp.SUCCESS_200, value={"result": result})

@test_routes.route('/push', methods=['GET'])
def test_push_article():
    test = TestController()
    result = test.test_push_article()
    return response_with(resp.SUCCESS_200, value={"result": result})


@test_routes.route('/status', methods=['GET'])
def check_status():
    test = TestController()
    result = test.check_status()
    return response_with(resp.SUCCESS_200, value={"result": result})