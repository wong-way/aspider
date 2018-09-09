from flask import Blueprint, request
from common.functions import get_disease_info, get_inheritance_info

name = 'common'
common_bp = Blueprint(name, __name__)


@common_bp.route('/disease_info', methods=['GET'])
def disease_info():
    return get_disease_info()


@common_bp.route('/inheri_info', methods=['GET'])
def inheritance_info():
    return get_inheritance_info()
