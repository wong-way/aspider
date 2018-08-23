# 封装 neo4j 相关工具
from neo4jrestclient.client import GraphDatabase


class Label:

    # key 为此Label 在数据库中的唯一标识符的property, 如 disease 是 mimnumber
    key = ''

    # 此Label 在数据库中的名称（首字母大写）
    label = ''

    # props 记录所有的 property
    props = []

    # key_prop 是一个 property，关键词搜索时，在这个property中进行搜索
    key_prop = ''

    def __init__(self, key, label, props, key_prop):
        self.key = key
        self.label = label
        self.props = props
        self.key_prop = key_prop


# labels 为数据库图的结构
# 此 dict，键为label 的小写名称
labels = {
    'symptom': Label(
        key='id',
        label='Symptom',
        props=['id', 'tid', 'symptom'],
        key_prop='symptom'
    ),

    'disease': Label(
        key='mimnumber',
        label='Disease',
        props=['iid', 'mimnumber', 'preferredTitle', 'shorteningTitle'],
        key_prop='preferredTitle'
    ),

    'gene': Label(
        key='id',
        label='Gene',
        props=['id', 'name', 'number'],
        key_prop='name'
    )
}


def get_db():
    url = "http://118.25.228.26:7474/db/data/"
    username = "neo4j"
    password = "scuse678"
    gdb = GraphDatabase(url, username=username, password=password)
    return gdb
