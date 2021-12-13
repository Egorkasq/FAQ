from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from app.schemas.faq_schemas import FaqInfo, FoundInfo
from starlette import status

info_router = APIRouter()
es_client = Elasticsearch("http://10.32.1.22:9200")
test = es_client.ping()


print(test)

@info_router.post(
    "/get_info",
    summary="get info for text",
    response_model=FoundInfo,
    responses={
        404: {"description": "Information wasn't found"},
        408: {"description": "Elastic search server is unvailable"}
    })
async def search_info(req_info: FaqInfo):
    body = {
        "query": {
            "multi_match":{
                "query":req_info.text_for_search, 
                "fields":["name", "keywords ^ 2", "description ^ 3"], 
                "fuzziness": "AUTO"}
                }, 
            "size": 2
            }
    try:
        find_results = es_client.search(index="faq", body=body)
    except Exception as e:
        raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "Elastic search server is unvailable") from e

    result = []
    if len(find_results):
        for i in find_results:
            result.append(i.get("_source").get("name"))

    if len(result) == 0:
        return HTTPException(status.HTTP_404_NOT_FOUND, "Information wasn't found")
    return FoundInfo(possible_answers=result)
