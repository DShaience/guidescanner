# Guidescanner
Scraping, indexing (RAG) and querying guides

## GraphRAG Recipe for Creating and Updating Index
1. Create an empty dir for GraphRAG: <br>
```python -m graphrag.index --init --root /workspaces/guidescanner/graphrag```

2. Edit the ```settings.yaml``` to include the appropriate LLM / API settings <br>
Common pitfalls: when the API version is a shortdate (YYYY-MM-DD) such as 2023-05-15, GraphRAG may have an error when parsing this value from the YAML (it will parse it to date). Instead, use a string qualifier "2023-05-15".

3. Run <br>
```python -m graphrag.index --root /workspaces/guidescanner/graphrag```<br>
to index the data.


References: 
* https://microsoft.github.io/graphrag/get_started/




