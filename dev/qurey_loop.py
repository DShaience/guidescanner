import datetime as dt
import json
from pathlib import Path
from graphrag.query.cli import run_local_search


ROOT_DIR = Path("/workspaces/guidescanner/graphrag_tests/full_bg3")

if __name__ == "__main__":
    config_filepath = ROOT_DIR / "settings.yaml"
    data_dir = ROOT_DIR / "output"
    community_level = 2
    response_type = "multiple paragraphs"
    streaming = False
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    results_file = f"/workspaces/guidescanner/data/query_results/{ROOT_DIR.name}_{timestamp}.json"               

    while True:
        query = input("Enter a query: ")
        if query == "exit":
            break
        result = run_local_search(
            config_filepath,
            data_dir,
            ROOT_DIR,
            community_level,
            response_type,
            streaming,
            query,
        )

        # import pprint
        # pprint.pprint(result)
        # pprint.pprint(result[0])
        # pprint.pprint(type(result))
        # pprint.pprint(result.keys())
        # break
        print("\n")
        with open(results_file, 'a', encoding='utf-8-sig') as f:
            json_line = json.dumps({"query": query, "result": result[0]}, indent=4)
            f.write(json_line + "\n")        


