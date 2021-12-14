from pydantic.typing import is_namedtuple


def prepare_test_req(text:str) -> str:
    text = text.replace("?", "")
    text = text.replace(",", "")
    text = text.lower()
    text = text.replace("!", "")
    text = text.replace("?", "")
    return text


def union_find_info(info_list: list) -> list:
    result = []
    for element in info_list:
        if isinstance(element, dict):
            find_info = element.get("hits")["hits"]
            if len(find_info):
                for i in find_info:
                    result.append(i.get("_source").get("name"))
    return list(set(result))
    
