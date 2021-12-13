from elasticsearch import Elasticsearch
from datetime import datetime
from fastapi import FastApi
from schema import ReqInfo


from elasticsearch import Elasticsearch

app = FastApi
es_client = Elasticsearch("http://10.32.1.22:9200")


# test_2 = es_client.search(index="faq", body={"query": {"match": {'name':'общежитие'}}})
# test_3 = es_client.search(index="faq", body={"query": {"more_like_this": {"fields": ["name", "description"], "like": "общежитие", "min_term_freq": 0, "max_query_terms": 12}}})


# print("****************")
# print(test_2)
# print("******************")
# print(test_3)

@app.post("/")
def search_info(req_info: ReqInfo):
    test_2 = es_client.search(index="faq", body={"query": {"match": {'name':req_info.req_text}}})
    test_3 = es_client.search(index="faq", body={"query": {"more_like_this": {"fields": ["name", "description"], "like": req_info.req_text, "min_term_freq": 0, "max_query_terms": 12}}})
    print(test_2)
    print(test_3)


