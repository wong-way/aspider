# author : Wei
# date :2018-04-17
# func : handle about json data
import json
from tools.neo4j import get_db
from django.http import HttpResponse


def get_json_res(querys):
    gdb = get_db()
    results = []
    try:
        for query in querys:
            result = gdb.query(query, data_contents=True)
            results.append(result.graph)
        info = {'msg': '查询成功', 'code': 1}
        res = {'info': info, 'data': results}
    except :
        info = {'msg': '查询失败', 'code': 0}
        res = {'info': info, 'data': ''}

    return HttpResponse(json.dumps(obj=res, ensure_ascii=False), content_type='application/json')


def get_data(querys):
    gdb = get_db()
    results = []

    for query in querys:
        result = gdb.query(query, data_contents=True)
        results.append(result.graph)

    return results
