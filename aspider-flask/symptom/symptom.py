from tools import utils
from flask import Blueprint, request

name = 'symptom'
symptom_bp = Blueprint(name, __name__)


@symptom_bp.route('/search', methods=['POST'])
def search():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.search(req_params, name)


@symptom_bp.route('/links', methods=['POST'])
def links():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.links(req_params, name)


@symptom_bp.route('/list', methods=['POST'])
def disease_list():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.get_disease_list(req_params, name)


@symptom_bp.route('/statistics', methods=['POST'])
def statistics():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.get_statistics(req_params, name)

