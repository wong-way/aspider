from tools.neo4j import get_db
import json


def get_disease_info():
    gdb = get_db()
    query = "MATCH(node:Disease)-[r]-()  where node.shorteningTitle <> \'null\' return node, count(r) order by count(r)  desc limit 20"
    result = gdb.query(q=query, data_contents=True)
    disease = []
    count = []

    for row in result.rows:
        disease.append(row[0]['shorteningTitle'])
        count.append(row[1])
    data = {'disease': disease, 'count': count}

    return json.dumps(data)


def get_inheritance_info():
    gdb = get_db()
    query = "MATCH(disease)--(result:Inheritance) return result,count(*) order by(count(*)) asc"
    result = gdb.query(q=query, data_contents=True)
    inheri = []
    count = []
    items = []
    for row in result.rows:

        if 'name' in row[0].keys():
            inheri.append(row[0]['name'])
            count.append(row[1])
            item = {"value": row[1], "name": row[0]['name']}
            items.append(item)
    data = {'inheritance': inheri, 'items': items}

    return json.dumps(data)
