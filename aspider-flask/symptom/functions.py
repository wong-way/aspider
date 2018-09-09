import json
from pandas import Series
from tools.neo4j import get_db
from tools.utils import indirect_search


# 用户输入相关症状的关键词，返回与该症状有关信息
def get_disease_list(params, name):
    # keywords 为输入的查找关键词
    keywords = params['keywords']

    # 设置搜索参数
    depth = 2
    gdb = get_db()
    search_type = 'Disease'

    # 搜索疾病相关信息
    diseases = indirect_search(name, keywords, search_type, depth)
    items = []
    response_data = {}

    for disease in diseases:
        item = {}
        count = 0
        item['mimnumber'] = disease['mimnumber']
        item['preferredTitle'] = disease['preferredTitle']
        item['shorteningTitle'] = disease['shorteningTitle']
        query = 'MATCH(node:Disease)--(s:Symptom)--(t:Type)' \
                'MATCH(node:Disease)--(i:Inheritance)' \
                'WHERE node.mimnumber =\'' + disease['mimnumber'] \
                + '\' RETURN count(s) as cnt ,t,i' \
                  '   ORDER BY cnt DESC'
        result = gdb.query(q=query, data_contents=True)
        inheri = result.rows[0][2]['name']
        position = [row[1]['name'] for row in result.rows][0:5]
        item['inheritance'] = inheri
        item['position'] = position
        for row in result.rows:
            count += row[0]
        item['symptomCount'] = count
        items.append(item)

    positions = set()
    inheris = set()

    # 统计所有发病部位和遗传方式
    for disease in diseases:
        query = 'MATCH(node:Disease)--(s:Symptom)--(t:Type)' \
                'MATCH(node:Disease)--(i:Inheritance)' \
                'WHERE node.mimnumber =\'' + disease['mimnumber'] \
                + '\' RETURN t,i'
        result = gdb.query(q=query, data_contents=True)
        for row in result.rows:
            positions.add(row[0]['name'])
            inheris.add(row[1]['name'])
    response_data['list'] = items
    response_data['positions'] = list(positions)
    response_data['inheris'] = list(inheris)

    return json.dumps(response_data)


# 用户输入相关症状关键词，返回与关键词有关统计信息
def get_statistics(params, name):
    # keywords 为输入的查找关键词
    search_type = 'Disease'
    keywords = params['keywords']
    depth = 2

    # 搜索疾病相关信息
    diseases = indirect_search(name, keywords, search_type, depth)
    inheris = []
    response_data = {}
    gdb = get_db()
    for disease in diseases:
        query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
            'mimnumber'] + '\'})-->(inheri:Inheritance) RETURN inheri'
        result = gdb.query(q=query, data_contents=True)
        inheris.append(result.rows[0][0]['name'])

    ss = Series(inheris).value_counts()
    inheris = {}
    try:
        inheris['ar'] = int(ss['Autosomal recessive'])
    except:
        inheris['ar'] = 0
    try:
        inheris['ad'] = int(ss['Autosomal dominant'])
    except:
        inheris['ad'] = 0

    response_data['inheris'] = inheris
    # 对每个疾病提取相关有用信息，构造返回信息

    return json.dumps(response_data)
