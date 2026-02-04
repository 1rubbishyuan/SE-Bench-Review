import json


def ground_truth_search(doc_path: str, selected_functions: list):
    search_result = []
    with open(doc_path, "r") as f:
        for line in f:
            data = json.loads(line)
            if data["original_name"] in selected_functions:
                search_result.append({data["curr_name"]: data["rewritten_doc"]})
    return search_result


class SearchTool:
    def __init__(self, search_alg: str, doc_path):
        self.search_alg = search_alg
        self.doc_path = doc_path

    def search(self, response: str, extro_info: dict):
        if self.search_alg == "ground_truth":
            return ground_truth_search(
                doc_path=self.doc_path,
                selected_functions=extro_info["selected_functions"],
            )
        else:
            # TODO: complete your own search tool
            pass
