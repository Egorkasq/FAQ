import logging
from datetime import datetime
import json

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


es_client = Elasticsearch("http://62.109.17.147:9200")
# es_client = Elasticsearch("http://0.0.0.0:9200")

es_index_client = IndicesClient(es_client)


def return_results(input_data):
    find_results = input_data.get("hits").get("hits")
    result = []

    if len(find_results):

        
        for i in find_results:
            # print()
            result.append(i.get("_source").get("name"))

    return result


test = es_client.ping()
print(es_client.info())



configurations = {
    'settings': {
            'analysis': {
                'analyzer': {
                    'ru': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        "filter": ['lowercase', 'ru_stopwords', 'ru_stemming'],
                    },
                },
                'filter': {
                    'ru_stopwords': {
                        'type': 'stop',
                        'stopwords':
                        u'а,без,более,бы,был,была,были,было,быть,в,вам,вас,весь,во,вот,все,всего,всех,вы,где,да,даже,для,до,его,ее,если,есть,еще,же,за,здесь,и,из,или,им,их,к,как,ко,когда,кто,ли,либо,мне,может,мы,на,надо,наш,не,него,нее,нет,ни,них,но,ну,о,об,однако,он,она,они,оно,от,очень,по,под,при,с,со,так,также,такой,там,те,тем,то,того,тоже,той,только,том,ты,у,уже,хотя,чего,чей,чем,что,чтобы,чье,чья,эта,эти,это,я,при,a,an,and,are,as,at,be,but,by,for,if,in,into,is,it,no,not,of,on,or,such,that,the,their,then,there,these,they,this,to,was,will,with',
                    },
                    'ru_stemming': {
                        'type': 'snowball',
                        'language': 'Russian',
                    },
                },

            }
        },
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "description": {"type": "text"},
            "keywords": {"type": "text"}
        }
    },
}


# create index
status = es_index_client.create(index="faq", body=configurations)
print(status)


with open("data/questions_list.json", "r") as json_file:
    json_file = json.load(json_file)


# additing data
for num, element in enumerate(json_file):
    temp_dict = {
        "name": element,
        "description": json_file.get(element).get("description"),
        "keyword": json_file.get(element).get("keyword"),
    }
    print("temp_dict", temp_dict)
    es_client.index(index="faq", id=num, body=temp_dict)
