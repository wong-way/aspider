import json

from neo4jrestclient.client import GraphDatabase

# Create your tests here.
from pandas import DataFrame

from symptom.views import direct_search
from tools.neo4j import get_db, labels


# 假设目前搜索的参数为：在 symptom 中根据 keywords 进行搜索
name = 'symptom'
# keywords 为输入的查找关键词
keywords = ['adult male', '151']
types = ['Disease', 'Gene']
data = direct_search(name, keywords)

# 最大搜索深度
depth = 2
gdb = get_db()
for node in data:
    node['neighbors'] = []
    for type in types:
        node_match = 'MATCH(node:' + labels[name].label + '{id:\'' + node['id'] + '\'})'
        rela_match = '-[*1..' + str(depth) + ']-'
        resu_match = '(result:' + type + ') RETURN result'
        query = node_match + rela_match + resu_match
        print(query)
        result = gdb.query(q=query, data_contents=True)

        if len(result) > 0:
            neighbors = [row[0] for row in result.rows]
            node['neighbors'].extend(neighbors)

print(json.dumps(data))
