from tools.json_handler import get_json_res
import json
from pandas import DataFrame, Series
from django.http import HttpResponse
from tools.neo4j import get_db, labels
from tools.node import Node
from tools.link import Link
from tools.encoder import MyEncoder
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse('hello world!')


# 用户输入相关症状关键词，返回与关键词有关的症状
@csrf_exempt
def search(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param.get('params')

    name = 'disease'
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
    print(keywords)
    # 设置搜索参数
    name = 'disease'
    # 搜索疾病相关信息
    diseases = direct_search(name, keywords)

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
        if None != result.rows:
            position = [row[0]['name'] for row in result.rows]
        else:
            position = []
        if len(position) > 0:
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


# 用户输入相关基因关键词，返回与关键词有关疾病列表信息
@csrf_exempt
def get_disease_list2(request):
    # 获取请求参数
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    keywords = req_param['params']
    name = 'disease'
    # 搜索疾病相关信息
    gdb = get_db()
    items = []
    response_data = {}
    diseases = direct_search(name, keywords)
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
    name = 'disease'

    # 搜索疾病相关信息
    diseases = direct_search(name, keywords)
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


# 间接查询，查询相关的
def indirect_search(name, keywords, type, depth=2):
    # 根据关键词生成正则表达式
    reg = '.*|.*'.join(keywords)
    reg = '\'.*' + reg + '.*\''
    data = []
    # 生成Cypher语句，并进行查找
    gdb = get_db()
    query = 'MATCH(node:' + labels[name].label + ')' + '-[*1..' + str(
        depth) + ']-' + '(result:' + type + ')' + ' WHERE node.' + labels[
                name].key_prop + ' =~ ' + reg + ' RETURN result'

    # -------------在下面这条语句可以设置返回的数据类型，包括是否返回关系等----------------
    result = gdb.query(q=query, data_contents=True)
    if len(result) > 0:
        # 将查找到的数据整理为 Pandas 的 DataFrame
        data = [row[0] for row in result.rows]

    return data


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

    name = 'disease'
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


# 用户输入相关症状关键词，返回与关键词相关的症状所相连的疾病和基因
@csrf_exempt
def get_detail(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # mimnumber 为输入的查找的疾病的id
    mimnumber = req_param['params']
    res_data = {}
    # 生成Cypher语句，并进行查找
    gdb = get_db()
    query = 'MATCH(node:Disease) WHERE node.mimnumber = \'' + mimnumber + '\'RETURN node'
    result = gdb.query(q=query, data_contents=True)

    disease = [row[0] for row in result.rows][0]
    res_data['mimnumber'] = disease['mimnumber']
    res_data['preferredTitle'] = disease['preferredTitle']
    res_data['shorteningTitle'] = disease['shorteningTitle']

    # 查询疾病的遗传方式
    query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
        'mimnumber'] + '\'})-->(inheri:Inheritance) RETURN inheri'
    result = gdb.query(q=query, data_contents=True)
    res_data['inheritance'] = result.rows[0][0]['name']

    # 查询疾病症状并按类别分
    query = 'MATCH(d:Disease{mimnumber:' + '\'' + disease[
        'mimnumber'] + '\'})-->(symp:Symptom)-->(type:Type)  RETURN symp,type'
    result = gdb.query(q=query, data_contents=True)
    symptoms = []
    temp = {}
    for r in result.rows:
        type = r[1]['name']
        if type in temp:
            temp[type].append(r[0]['symptom'])
        else:
            temp[type] = []
            temp[type].append(r[0]['symptom'])

    for key in temp:
        item = {'type': key, 'symptom': temp[key]}
        symptoms.append(item)

    res_data['symptoms'] = symptoms

    response = HttpResponse(json.dumps(res_data))
    return response


@csrf_exempt
def get_graph(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # mimnumber:614172 为输入的查找的疾病的id
    mimnumber = req_param['params']
    res_data = {}
    # 生成Cypher语句，并进行查找
    gdb = get_db()

    query = 'MATCH(node:Disease)--(s:Symptom)--(t:Type)' \
            'MATCH(node:Disease)--(g:Gene)' \
            'MATCH(node:Disease)--(i:Inheritance)' \
            'WHERE node.mimnumber =\'' + mimnumber + '\'RETURN node,s,t,g,i'
    result = gdb.query(q=query, data_contents=True)

    # disease = [row for row in result.rows]
    nodes = set()
    links = set()
    for row in result.rows:
        disease = Node("disease",
                       "mimnumber:" + row[0]["mimnumber"] + "</br>" + "prefferred title:" + row[0]["preferredTitle"])
        symptom = Node("symptom", "symptom:" + row[1]["symptom"])
        type = Node("type", "type:" + row[2]["name"])
        gene = Node("gene", "name:" + row[3]["name"] + "</br>" + "id:" + row[3]["number"])
        inheri = Node("inheritance", "inheritance:" + row[4]["name"])
        nodes.add(disease)
        nodes.add(symptom)
        nodes.add(type)
        nodes.add(gene)
        nodes.add(inheri)

        link1 = Link(disease.name, symptom.name, "Behave")
        link2 = Link(symptom.name, type.name, "Belong")
        link3 = Link(gene.name, disease.name, "Cause")
        link4 = Link(disease.name, inheri.name, "Observe")
        links.add(link1)
        links.add(link2)
        links.add(link3)
        links.add(link4)
    res_data = {'nodes': list(nodes), "links": list(links)}

    response = HttpResponse(json.dumps(res_data, cls=MyEncoder))

    return response


@csrf_exempt
def node_test(request):
    print("test node")
    node1 = Node('huangwei', 18)
    node2 = Node('huangwei', 18)
    test = set([node1, node2])
    response = HttpResponse(json.dumps(list(test), cls=MyEncoder))
    return response


@csrf_exempt
def get_top5item(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    mimnumber = req_param['params']
    gdb = get_db()
    query = 'MATCH(d:Disease{mimnumber:\'' + mimnumber + '\'})-->(s:Symptom)--(result:Disease) WITH d,result, count(*) AS path order by path desc RETURN d,result,path limit 100'
    result = gdb.query(q=query, data_contents=True)
    res_data = []
    for row in result.rows:
        item = {"source": row[0], "target": row[1], 'path': row[2]}
        res_data.append(item)
    return HttpResponse(json.dumps(res_data))


@csrf_exempt
def init_link_of_disease(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    params = req_param['params']
    gdb = get_db()
    query = 'MATCH(source:Disease{mimnumber:\'' + params[0] + '\'})--(path:Symptom)--(target:Disease{mimnumber:\'' + \
            params[1] + '\'}) return source,path,target'
    result = gdb.query(q=query, data_contents=True)

    items = []
    nodes = set()
    links = set()
    for row in result.rows:
        source = Node("disease",
                      "mimnumber:" + row[0]["mimnumber"] + "</br>" + "prefferred title:" + row[0]["preferredTitle"])
        symptom = Node("symptom", "symptom:" + row[1]["symptom"])
        target = Node("disease",
                      "mimnumber:" + row[2]["mimnumber"] + "</br>" + "prefferred title:" + row[2]["preferredTitle"])

        link1 = Link(source.name, symptom.name, "Behave")
        link2 = Link(target.name, symptom.name, "Behave")
        nodes.add(source)
        nodes.add(symptom)
        nodes.add(target)
        links.add(link1)
        links.add(link2)
        item = {"source": row[0], "path": row[1], 'target': row[2]}
        items.append(item)
    res_data = {'nodes': list(nodes), "links": list(links)}

    response = HttpResponse(json.dumps(res_data, cls=MyEncoder))
    # response = HttpResponse(json.dumps(items))
    return response


@csrf_exempt
def get_link_of_disease(request):
    req_param = json.loads(str(request.body, encoding='utf-8'))
    # keywords 为输入的查找关键词
    params = req_param['params']
    gdb = get_db()
    items = []
    nodes = set()
    links = set()

    for index in range(len(params)):
        if index == 0:
            continue
        query = 'MATCH(source:Disease{mimnumber:\'' + params[0] + '\'})--(path:Symptom)--(target:Disease{mimnumber:\'' + \
                params[index] + '\'}) return source,path,target'
        result = gdb.query(q=query, data_contents=True)

        for row in result.rows:
            source = Node("disease",
                          "mimnumber:" + row[0]["mimnumber"] + "</br>" + "prefferred title:" + row[0]["preferredTitle"])
            symptom = Node("symptom", "symptom:" + row[1]["symptom"])
            target = Node("disease",
                          "mimnumber:" + row[2]["mimnumber"] + "</br>" + "prefferred title:" + row[2]["preferredTitle"])

            link1 = Link(source.name, symptom.name, "Behave")
            link2 = Link(target.name, symptom.name, "Behave")
            nodes.add(source)
            nodes.add(symptom)
            nodes.add(target)
            links.add(link1)
            links.add(link2)
            item = {"source": row[0], "path": row[1], 'target': row[2]}
            items.append(item)
    res_data = {'nodes': list(nodes), "links": list(links)}

    response = HttpResponse(json.dumps(res_data, cls=MyEncoder))
    # response = HttpResponse(json.dumps(items))
    return response


# author :lai lingxin
@csrf_exempt
def search_disease(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        disease_list = req_json['params']
        for item in disease_list:
            query = "MATCH (d:Disease{{preferredTitle:'{value}'}}) RETURN d".format(value=item)
            queryGene = "MATCH(g:Gene)-[:CAUSE]->(d:Disease{{preferredTitle:'{value}'}}) RETURN g".format(value=item)
            queryInheri = "MATCH(d:Disease{{preferredTitle:'{value}'}})-[:OBSERVE]->(i:Inheritance) RETURN i".format(
                value=item)
            querys.append(query)
            querys.append(queryGene)
            querys.append(queryInheri)
        # name = request.POST['diseaseName']
        # print(name)
        # query="MATCH(d:Disease) where d.preferredTitle='"+name+"' RETURN d"
        # results=gdb.query(query, data_contents=True)
        # print(results.graph)
        res = get_json_res(querys)
    return res


@csrf_exempt
def search_relate_gene(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        disease_list = req_json['params']
        for item in disease_list:
            query = "MATCH(g:Gene)-[:CAUSE]->(d:Disease{{preferredTitle:'{value}'}}) RETURN g".format(value=item)
            querys.append(query)

    res = get_json_res(querys)
    return res


@csrf_exempt
def search_inheri(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        disease_list = req_json['params']
        for item in disease_list:
            query = "MATCH(d:Disease{{preferredTitle:'{value}'}})-[:OBSERVE]->(i:Inheritance) RETURN i".format(
                value=item)
            querys.append(query)
    res = get_json_res(querys)
    return res


@csrf_exempt
def search_symptom(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        disease_list = req_json['params']
        for item in disease_list:
            query = "MATCH(d:Disease{{preferredTitle:'{value}'}})-[:BEHAVE]->(s:Symptom) RETURN s".format(value=item)
            querys.append(query)
        res = get_json_res(querys)
        return res


@csrf_exempt
def search_similar(request):
    if request.method == 'POST':
        querys = []
        req_json = json.loads(request.body)
        disease_list = req_json['params']
        for item in disease_list:
            query = "MATCH(Disease{preferredTitle:'{value}'})-[:BEHAVE]->(s:Symptom)--(result:Disease) WITH result,count(*) As road WHERE road > 5 RETURN result".format(
                value=item)
            querys.append(query)
        res = get_json_res(querys)
        return res
