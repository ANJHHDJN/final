import os
import fileinput
from neo4j import GraphDatabase
from config import NEO4J_CONFIG

driver = GraphDatabase.driver(**NEO4J_CONFIG)

def _load_data(load_path):
    disease_csv_list = os.listdir(load_path)
    disease_list = list(map(lambda x: x.split(".")[0], disease_csv_list))

    symptom_list = []

    for disease_csv in disease_csv_list:
        symptom = list(map(lambda x: x.strip(), fileinput.FileInput(os.path.join(load_path, disease_csv))))

        symptom = list(filter(lambda x: 0 < len(x) < 100, symptom))

        symptom_list.append(symptom)

    return dict(zip(disease_list, symptom_list))

def write(file_path):
    disease_symptom_dict = _load_data(file_path)

    with driver.session() as session:
        for key, value in disease_symptom_dict.items():
            cypher = "MERGE (a:Disease{name:%r}) RETURN a" % key
            session.run(cypher)
            for v in value:
                cypher = "MERGE (b:Symptom{name:%r}) RETURN b" %v
                session.run(cypher)
                cypher = "MATCH (a:Disease{name:%r}) MATCH (b:Symptom{name:%r}) WITH a,b MERGE(a)-[r:dis_to_sym]-(b)"\
                         % (key, v)
                session.run(cypher)
        cypher = "CREATE INDEX ON:Disease(name)"
        session.run(cypher)
        cypher = "CREATE INDEX ON:Symptom(name)"
        session.run(cypher)

if __name__ == '__main__':
    path = "/mydata/code/offline/doctor_data/structured/use/"
    write(path)

