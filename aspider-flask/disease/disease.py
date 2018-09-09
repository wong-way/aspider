from disease.functions import *
from tools import utils
from flask import Blueprint, request

name = 'disease'
disease_bp = Blueprint(name, __name__)


@disease_bp.route('/search', methods=['POST'])
def search():
    # 获取 json 数据
    params = request.get_json()
    return utils.search(params, name)


@disease_bp.route('/links', methods=['POST'])
def links():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.links(req_params, name)


@disease_bp.route('/list', methods=['POST'])
def disease_list():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.get_disease_list(req_params, name)


@disease_bp.route('/statistics', methods=['POST'])
def statistics():
    # 获取 json 数据
    req_params = request.get_json()
    return utils.get_statistics(req_params, name)


@disease_bp.route('/graph', methods=['POST'])
def graph():
    # 获取 json 数据
    req_params = request.get_json()
    return get_graph(req_params)


@disease_bp.route('/link', methods=['POST'])
def link():
    req_params = request.get_json()
    return get_link(req_params)


@disease_bp.route('/top5item', methods=['POST'])
def top100_item():
    req_params = request.get_json()
    return get_top5item(req_params)


@disease_bp.route('/detail', methods=['POST'])
def detail():
    req_params = request.get_json()
    return get_detail(req_params)
