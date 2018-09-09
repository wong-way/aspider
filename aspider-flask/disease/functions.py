import json
from tools.node import Node
from tools.link import Link
from tools.neo4j import get_db
from tools.encoder import MyEncoder


def get_graph(req_param):

    # mimnumber:614172 为输入的查找的疾病的id
    mimnumber = req_param['params']

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

    return json.dumps(res_data, cls=MyEncoder)


def get_detail(req_param):

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


    return json.dumps(res_data)
