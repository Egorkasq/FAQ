from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from app.schemas.faq_schemas import FaqInfo, FoundInfo, ESInfo, AnswersText
from starlette import status
from app.depences.depences import prepare_test_req, union_find_info

info_router = APIRouter()
es_client = Elasticsearch("http://62.109.17.147:9200")
test = es_client.ping()


@info_router.post(
    "/get_info",
    summary="get info for text",
    response_model=FoundInfo,
    responses={
        404: {"description": "Information wasn't found"},
        408: {"description": "Elastic search server is unvailable"}
    })
async def search_info(req_info: FaqInfo):

    multi_match_body = {
        "query": {
            "multi_match":{
                "query": prepare_test_req(req_info.text_for_search), 
                "fields":["name", "keyword ^ 2", "description"], 
                "fuzziness": "AUTO"}
                }, 
            "size": 4
            }

    more_like_this_body = {
            "query": 
                {
                    "more_like_this": 
                    {
                        "fields": ["name", "description", "keyword"], 
                        "like": prepare_test_req(req_info.text_for_search),
                        "min_term_freq": 1,
                        "min_doc_freq": 1,
                        "max_query_terms": 15,
                        
                        
                    },
                },
            }
    try:
        multi_find_results = es_client.search(index="faq", body=multi_match_body)
        like_find_results = es_client.search(index="faq", body=more_like_this_body)

    except Exception as e:
        raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "Elastic search server is unvailable") from e

    result = union_find_info([multi_find_results, like_find_results])
    print(result)
    if len(result) == 0:
        return HTTPException(status.HTTP_404_NOT_FOUND, "Information wasn't found")
    return FoundInfo(possible_answers=result)



@info_router.post(
    "/save_info",
    summary="save info to es",
    responses={
        408: {"description": "Elastic search server is unvailable"},
    })
def save_info_es(info: ESInfo):
    try:
        es_client.index(index="faq", body=info)
    except Exception as e:
        raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "ES anvailable") from e


@info_router.post(
    "/get_answer_on_question",
    summary="Get answer on question",
    response_model=AnswersText,
    responses={
        404: {"description": "Information wasn't found"}
    }
)
async def get_answers(question: FaqInfo):
    try:
        print(question.text_for_search)
        result = es_client.search(index="faq", body={"query": {"match": {'name': question.text_for_search}}})
    except Exception as e:
        raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "ES anvailable") from e
    result = result["hits"]["hits"][0]
    text_description = result["_source"]["description"]
    return AnswersText(answer_text=text_description)
