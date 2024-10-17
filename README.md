# Guidescanner
Scraping, indexing (RAG) and querying guides

## Scanner Recipe

1. Use `src/scanner/scanner_main.py` to scan and dump to json the content of a selected website.<br>
Dump the raw-output into a directory, `raw-output`.<br>
``` 
python scanner_main.py --parent_subdomain "http://www.mysite.com/biology/cell-biology" --parent_url "http://www.mysite.com/biology/cell-biology/course-lectures" --output_dir "/workspace/data/raw-scraped-data" --debug 
```

2. Use `src/scanner/parse_scanned_files_for_graphrag.py` to parse the output json files into text files. <br>
If this doesn't work completely out of the box, review the json schema of the output files in the first step and make adjustments.<br>
The objective of this step is to create a series of *clean* text files (remove a lot of irrelevancies from the scraping process) to make the job easier for the downstream GraphRAG Indexer. <br>
```
python parse_scanned_files_for_graphrag.py --input_dir "/workspace/data/raw-scraped-data" --output_dir "/path/to/output/text/files"
```


Following that, you may set-up and run GraphRAG.


## GraphRAG Recipe for Creating and Updating Index
1. Create an empty dir for GraphRAG: <br>
```
python -m graphrag.index --init --root /workspaces/guidescanner/graphrag
```

2. Edit the ```settings.yaml``` to include the appropriate LLM / API settings <br>
Common pitfalls: when the API version is a shortdate (YYYY-MM-DD) such as 2023-05-15, GraphRAG may have an error when parsing this value from the YAML (it will parse it to date). Instead, use a string qualifier "2023-05-15".

3. Run <br>
```
python -m graphrag.index --root /workspaces/guidescanner/graphrag
```
to index the data.

4. [Optional] Query locally or globally (commandline):<br>
```
python -m graphrag.query --root /workspaces/guidescanner/graphrag --method local "Who is Scrooge, and what are his main relationships?"
```

```
python -m graphrag.query --root /workspaces/guidescanner/graphrag --method global "What are the top themes in this story?"
```
This is good for sanity checks.

5. [Optional] Query example from script. Loop and try questioning GraphRAG. <br>
The results are saved locally. It is good for debugging and comparing changes / improvements to the indexing process (i.e., use the same questions / queries). See `dev/qurey_loop.py`
``` 
python qurey_loop.py --root_dir "/workspaces/guidescanner/graphrag" 
```


References: 
* https://microsoft.github.io/graphrag/get_started/




