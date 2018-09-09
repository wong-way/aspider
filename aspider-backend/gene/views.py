from tools.json_handler import get_json_res
from tools.json_handler import get_data
import json

from pandas import DataFrame, Series
from django.http import HttpResponse
from tools.neo4j import get_db, labels
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse('Hello world!')


# 用户输入相关症状关键词，返回与关键词有关的症状
@csrf_exempt
def search(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param.get('params')
    name = 'gene'
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


# 用户输入相关基因关键词，返回与关键词有关疾病列表信息
@csrf_exempt
def get_disease_list(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param['params']

    # 设置搜索参数
    name = 'gene'
    search_type = 'Disease'
    depth = 2

    # 搜索疾病相关信息
    diseases = indirect_search(name, keywords, search_type, depth)

    gdb = get_db()
    response_data = {}
    items = []
    positions = []
    inheris = []

    # 对每个疾病提取相关有用信息，构造返回信息
    for disease in diseases:
        item = {}
        item['mimnumber'] = disease['mimnumber']
        item['preferredTitle'] = disease['preferredTitle']
        item['shorteningTitle'] = disease['shorteningTitle']

        # 查询疾病的遗传方式
        query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
            'mimnumber'] + '\'})-->(inheri:Inheritance) RETURN inheri'
        result = gdb.query(q=query, data_contents=True)
        item['inheritance'] = result.rows[0][0]['name']
        inheris.append(result.rows[0][0]['name'])
        # 统计症状
        query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
            'mimnumber'] + '\'})-->(symp:Symptom) RETURN COUNT(symp)'
        result = gdb.query(q=query, data_contents=True)

        # 查询发病部位
        item['symptomCount'] = result.rows[0][0]
        query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
            'mimnumber'] + '\'})--> (symp:Symptom) -->(type:Type) return type'
        result = gdb.query(q=query, data_contents=True)

        # 统计发病部位数量并排序，取top5
        position = [row[0]['name'] for row in result.rows]
        positions.extend(position)

        ss = Series(position).value_counts()[0:5]
        item['position'] = list(ss.index)

        items.append(item)

    data = DataFrame({'p': positions}).drop_duplicates()
    positions = data['p'].values.tolist()

    data = DataFrame({'i': inheris}).drop_duplicates()
    inheris = data['i'].drop_duplicates().values.tolist()

    response_data['list'] = items
    response_data['positions'] = positions
    response_data['inheris'] = inheris

    response = HttpResponse(json.dumps(response_data))
    return response


@csrf_exempt
def get_disease_list2(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param['params']

    # 设置搜索参数
    name = 'gene'
    search_type = 'Disease'
    depth = 2

    # 搜索疾病相关信息
    diseases = indirect_search(name, keywords, search_type, depth)
    items = []
    response_data = {}
    gdb = get_db()
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
    response = HttpResponse(json.dumps(response_data))
    return response


# 用户输入相关基因关键词，返回与关键词有关统计信息
@csrf_exempt
def get_statistics(request):
    print('to get statistics data')
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param['params']
    name = 'gene'
    search_type = 'Disease'
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
    HttpResponse(json.dumps(response_data))
    # 对每个疾病提取相关有用信息，构造返回信息

    return HttpResponse(json.dumps(response_data))


# 用户输入相关症状关键词，返回与关键词有关的症状
@csrf_exempt
def get_disease_list_old(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))

    # keywords 为输入的查找关键词
    keywords = req_param['params']

    name = 'gene'
    data = direct_search(name, keywords)

    depth = 2
    gdb = get_db()
    response_data = []
    type = 'Disease'
    for node in data:

        # 构造query语句查询相关的疾病
        node_match = 'MATCH(node:' + labels[name].label + '{' + labels[name].key + ':\'' + node[
            labels[name].key] + '\'})'
        rela_match = '-[*1..' + str(depth) + ']-'
        resu_match = '(result:' + type + ') RETURN result'
        query = node_match + rela_match + resu_match
        result = gdb.query(q=query, data_contents=True)

        item = {}
        if len(result) > 0:
            diseases = [row[0] for row in result.rows]
        # 每个疾病提取相关有用信息
        for disease in diseases:
            item['mimnumber'] = disease['mimnumber']
            item['preferredTitle'] = disease['preferredTitle']
            item['shorteningTitle'] = disease['shorteningTitle']
            # 查询疾病的遗传方式
            query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
                'mimnumber'] + '\'})-->(inheri:Inheritance) RETURN inheri'
            result = gdb.query(q=query, data_contents=True)
            item['inheritance'] = result.rows[0][0]['name']
            # 统计症状
            query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
                'mimnumber'] + '\'})-->(symp:Symptom) RETURN COUNT(symp)'
            result = gdb.query(q=query, data_contents=True)
            # 查询发病部位
            item['symptomCount'] = result.rows[0][0]
            query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
                'mimnumber'] + '\'})--> (symp:Symptom) -->(type:Type) return type'
            result = gdb.query(q=query, data_contents=True)
            positions = [row[0] for row in result.rows]
            positions_dict = {}
            # 统计发病部位数量并排序，取top4
            for p in positions:
                if p['name'] not in positions_dict:
                    positions_dict[p['name']] = 1
                else:
                    positions_dict[p['name']] += 1
            positions_dict = sorted(positions_dict.items(), key=lambda x: x[1], reverse=True)
            item['position'] = [p[0] for p in positions_dict[0:5]]

            response_data.append(item)

    response = HttpResponse(json.dumps(response_data))
    return response


# 用户输入相关症状关键词，返回与关键词相关的症状所相连的疾病和基因
@csrf_exempt
def links(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))

    # keywords 为输入的查找关键词
    keywords = req_param.get('keywords')
    # types为用户勾选的想要查找的间接的信息
    types = req_param.get('types')
    # 最大搜索深度
    depth = req_param.get('depth')

    name = 'gene'
    # 比如勾选了 "疾病，基因"
    # 业务处理逻辑为：
    # 1. 根据关键词查找关键词有关的symptom
    # 2. 遍历每个症状，查找与他有关的 疾病，基因 信息

    data = direct_search(name, keywords)
    gdb = get_db()

    for node in data:
        node['neighbors'] = {}
        for type in types:
            node_match = 'MATCH(node:' + labels[name].label + '{' + labels[name].key + ':\'' + node[
                labels[name].key] + '\'})'
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

# 间接查询，查询相关的
def indirect_search(name, keywords, type, depth=2):
    data = []
    # 生成Cypher语句，并进行查找
    gdb = get_db()

    # MARK:: TEST


    # 根据关键词生成 CONTAINS 子句
    phase = 'WHERE '
    for i, keyword in enumerate(keywords):
        if i == 0:
            phase += 'node.' + labels[name].key_prop + ' CONTAINS \'' + keyword + '\''
        else:
            phase += ' OR node.' + labels[name].key_prop + ' CONTAINS \'' + keyword + '\''

    # 构造查询语句
    query = 'MATCH(node:' + labels[name].label + ')' + '-[*1..' + str(
        depth) + ']-' + '(result:' + type + ') ' + phase + ' RETURN result'

    print(query)

    # -------------在下面这条语句可以设置返回的数据类型，包括是否返回关系等----------------
    result = gdb.query(q=query, data_contents=True)


    if len(result) > 0:
        # 将查找到的数据整理为 Pandas 的 DataFrame
        data = [row[0] for row in result.rows]

    return data


def direct_search(name, keywords):

    # 生成Cypher语句，并进行查找
    gdb = get_db()
    phase = 'WHERE '
    for i, keyword in enumerate(keywords):
        if i == 0:
            phase += 'node.' + labels[name].key_prop + ' CONTAINS \'' + keyword + '\''
        else:
            phase += ' OR node.' + labels[name].key_prop + ' CONTAINS \'' + keyword + '\''

    query = 'MATCH(node:' + labels[name].label + ') ' + phase + ' RETURN node'



    # -------------在下面这条语句可以设置返回的数据类型，包括是否返回关系等----------------
    result = gdb.query(q=query, data_contents=True)

    # 将查找到的数据整理为 Pandas 的 DataFrame
    data = [row[0] for row in result.rows]
    return data


# 旧的业务逻辑
# author: huangwei
@csrf_exempt
def search_gene(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        gene_list = req_json['params']
        for item in gene_list:
            query = "MATCH(gene:Gene{{name:'{value}'}}) return gene".format(value=item)
            querys.append(query)
        res = get_json_res(querys)
        return res


@csrf_exempt
def search_relation_disease(request):

    if request.method == 'POST':
        querys = []
        nodes = []
        req_json = json.loads(request.body)
        gene_list = req_json['params']
        for item in gene_list:
            query = "MATCH(gene:Gene{{name:'{value}'}})-->(disease:Disease)-->(inheri:Inheritance) " \
                    "return disease,inheri".format(value=item)
            querys.append(query)
        node_graph = get_data(querys)
        # 获取基因相关遗传方式的数量
        positions = {}
        for node in node_graph[0]:
            nodes.append(node['nodes'][0])
            inheritance = node['nodes'][1]['properties']['name']
            if positions.get(inheritance) is None:
                positions[inheritance] = 1
            else:
                positions[inheritance] += 1
        querys.clear()
        for item in gene_list:
            query = "MATCH(gene:Gene{{name:'{value}'}})-->(disease:Disease)-->(symp:Symptom)-->(type:Type) return type".format(
                value=item)
            querys.append(query)
        # 获取相关症状的集中部位
        type_graph = get_data(querys)
        types = {}
        for node in type_graph[0]:
            type = node['nodes'][0]['properties']['name']
            if types.get(type) is None:
                types[type] = 1
            else:
                types[type] += 1
        result = {'nodes': nodes, 'positions': positions, 'types': types}

        info = {'msg': '查询成功', 'code': 1}
        res = {'info': info, 'data': result}
        return HttpResponse(json.dumps(obj=res, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def search_relation_gene(request):
    if request.method == 'POST':
        req_json = json.loads(request.body)
        gene_list = req_json['params']
        querys = []
        for item in gene_list:
            query = "MATCH(gene:Gene{{name:'{value}'}})-->(d1:Disease)-->(s:Symptom)--(d2:Disease)--(gene2:Gene) return gene2".format(
                value=item)
            querys.append(query)
        res = get_json_res(querys)
        return res
