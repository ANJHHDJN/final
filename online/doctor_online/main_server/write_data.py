import os
import fileinput
from neo4j import GraphDatabase
from config import NEO4J_CONFIG

driver = GraphDatabase.driver(**NEO4J_CONFIG)

def _load_data(load_path):
    # 获得疾病csv列表，把path目录下的所有文件名列出来，除去后缀.csv，获取电脑问题列表
    disease_csv_list = os.listdir(load_path)
    disease_list = list(map(lambda x: x.split(".")[0], disease_csv_list))

    symptom_list = []
    # 遍历疾病csv列表
    for disease_csv in disease_csv_list:
        # 将疾病csv中的每个症状取出存入symptom列表中
        symptom = list(map(lambda x: x.strip(), fileinput.FileInput(os.path.join(load_path, disease_csv))))
        # 过滤掉所有长度异常的症状名
        symptom = list(filter(lambda x: 0 < len(x) < 100, symptom))

        symptom_list.append(symptom)

    # 返回一个字典，电脑问题的名称和症状
    return dict(zip(disease_list, symptom_list))

def write(file_path):
    disease_symptom_dict = _load_data(file_path)

    with driver.session() as session:
        for key, value in disease_symptom_dict.items():
            # 创建电脑问题名称节点
            cypher = "MERGE (a:Disease{name:%r}) RETURN a" % key
            session.run(cypher)
            for v in value:
                # 创建症状节点
                cypher = "MERGE (b:Symptom{name:%r}) RETURN b" %v
                session.run(cypher)
                # 将症状与问题名称连接起来
                cypher = "MATCH (a:Disease{name:%r}) MATCH (b:Symptom{name:%r}) WITH a,b MERGE(a)-[r:dis_to_sym]-(b)"\
                         % (key, v)
                session.run(cypher)
        # 创建索引
        cypher = "CREATE INDEX ON:Disease(name)"
        session.run(cypher)
        cypher = "CREATE INDEX ON:Symptom(name)"
        session.run(cypher)

if __name__ == '__main__':
    path = "/Users/chao/PycharmProjects/tf2/tf_study/AI_Doctor/computer_structured"
    write(path)