"""
    Global search reference: https://microsoft.github.io/graphrag/examples_notebooks/global_search/
    Local search reference: https://microsoft.github.io/graphrag/examples_notebooks/local_search/
"""
 
import argparse
import datetime as dt
import json
from pathlib import Path
from graphrag.query.cli import run_local_search, run_global_search

# ROOT_DIR = Path("/workspaces/guidescanner/graphrag_tests/full_bg3")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run query loop with specified ROOT_DIR")
    parser.add_argument('--root_dir', type=str, default="/workspaces/guidescanner/graphrag_tests/full_bg3_v2", help='Root directory for the query loop')
    parser.add_argument('--global_mode', action='store_true', default=True, help='Run the query loop in global mode. Otherwise, run in local mode.')

    args = parser.parse_args()
    ROOT_DIR = Path(args.root_dir)

    global_mode = args.global_mode

    config_filepath = ROOT_DIR / "settings.yaml"
    data_dir = ROOT_DIR / "output"
    community_level = 2

    response_type = "multiple paragraphs"
    streaming = False
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    results_file = f"/workspaces/guidescanner/data/query_results/{ROOT_DIR.name}_{timestamp}.json"               


    print(f"Running {'global' if global_mode else 'local'} search")
    while True:
        query = input("Enter a query: ")
        # if the query is any of the following, exit the loop: exit, quit, q, quit(), exit()
        if query in ["exit", "quit", "q", "quit()", "exit()"]:
            break

        if global_mode:
            result = run_global_search(config_filepath, data_dir, ROOT_DIR, community_level, response_type, streaming, query)
        else:        
            result = run_local_search(config_filepath, data_dir, ROOT_DIR, community_level, response_type, streaming, query)

        print("\n")
        with open(results_file, 'a', encoding='utf-8-sig') as f:
            json_line = json.dumps({"query": query, "result": result[0]}, indent=4)
            f.write(json_line + "\n")        


