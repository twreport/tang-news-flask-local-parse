from flask import Blueprint, request, jsonify
from api.controller.location import LocationController
from api.utils.responses import response_with
from api.utils import responses as resp

location_routes = Blueprint("location_routes", __name__)

# ========================= 在用！！！=============================
@location_routes.route('/', methods=['GET'])
def parse_article_location():
    location = LocationController()
    result = location.parse_article_location()
    return response_with(resp.SUCCESS_200, value={"result": result})