# coding=utf-8
"""
    views for symptom.
    Developed by Jaho. 2018/04/22
"""

import json

from pandas import DataFrame
from django.http import HttpResponse
from tools.neo4j import get_db, labels
from django.views.decorators.csrf import csrf_exempt


# 用户输入相关症状关键词，返回与关键词有关的症状
@csrf_exempt
def search(request, name):

    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param.get('params')

    result = direct_search(name, keywords)

    # ---------------- 我这里没有处理result为空的情况 -----------------

    # 传入 columns 生成 DataFrame
    frame = DataFrame(result, columns=labels[name].props)

    # 添加关键词计数列，初始化为0
    frame['count'] = 0

    # 开始进行关键词命中统计，按从高到低排序
    for keyword in keywords:
        frame['count'] = frame[labels[name].key_prop].apply(
            lambda x: frame['count'] + 1 if keyword in x else frame['count'] + 0)

    frame = frame.sort_values(by='count', axis=0, ascending=False)

    # 返回行数据数组，如果需要修改返回数据的格式，在此进行结果的装配即可
    response = HttpResponse(frame.to_json(orient='records'))
    return response


# 用户输入相关症状关键词，返回与关键词相关的症状所相连的疾病和基因
@csrf_exempt
def links(request, name):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))

    # keywords 为输入的查找关键词
    keywords = req_param.get('keywords')
    # types为用户勾选的想要查找的间接的信息
    types = req_param.get('types')
    # 最大搜索深度
    depth = req_param.get('depth')

    # 比如勾选了 "疾病，基因"
    # 业务处理逻辑为：
    # 1. 根据关键词查找关键词有关的symptom
    # 2. 遍历每个症状，查找与他有关的 疾病，基因 信息

    data = direct_search(name, keywords)
    gdb = get_db()

    for node in data:
        node['neighbors'] = {}
        for type in types:
            node_match = 'MATCH(node:' + labels[name].label + '{' + labels[name].key + ':\'' + node[labels[name].key] + '\'})'
            rela_match = '-[*1..' + str(depth) + ']-'
            resu_match = '(result:' + type + ') RETURN result'
            query = node_match + rela_match + resu_match

            result = gdb.query(q=query, data_contents=True)

            if len(result) > 0:
                neighbors = [row[0] for row in result.rows]
                node['neighbors'][type] = neighbors

    # 返回行数据数组，每个节点的neighbors 字段存储与他相关的节点
    response = HttpResponse(json.dumps(data))
    return response


def direct_search(name, keywords):

    # 根据关键词生成正则表达式
    reg = '.*|.*'.join(keywords)

    reg = '\'.*' + reg + '.*\''

    # 生成Cypher语句，并进行查找
    gdb = get_db()
    query = 'MATCH(node:' + labels[name].label + ') WHERE node.' + labels[name].key_prop + ' =~ ' + reg + ' RETURN node'

    # -------------在下面这条语句可以设置返回的数据类型，包括是否返回关系等----------------
    result = gdb.query(q=query, data_contents=True)

    # 将查找到的数据整理为 Pandas 的 DataFrame
    data = [row[0] for row in result.rows]
    return data
