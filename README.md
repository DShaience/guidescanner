# GuideScanner
Scraping, indexing (RAG) and querying guides

## Try it out!
How many times while searching a clue for a game online, have you stumbled on a spoiler? <br>
Or had a verryyy long manual, that you just wanted to query from time to time, not just CTRL+F.<br>
Tried to get an answer for one single question but ended up reading 10 pages?<br>
No more! 

I have indexed guides of several games and software manuals, giving *you* the ability to query them using natural language! <br>
Available [here](https://guidescanner-app.politebay-d54f15ab.eastus2.azurecontainerapps.io/).
* https://guidescanner-app.politebay-d54f15ab.eastus2.azurecontainerapps.io/

For example, try selecting DeepStream, and ask: <br>
`"Please tell me how DeepStream nvDCF tracker works, and what are its key parameters"`

## GraphRAG Recipe for Creating and Updating Index
1. Create an empty dir for GraphRAG: <br>
If you are using Azure OpenAI, remember to first use `az login`.<br>
```
python -m graphrag init --root /workspaces/guidescanner/src/app/graphrag_data/nvidia_new/
```

2. Edit the ```settings.yaml``` to include the appropriate LLM / API settings <br>
Specifically note the following fields that should be populated according to your deployment on both chat model and embedding model (otherwise graphrag may throw some really hairy error messages):<br>
model, type, deployment_name, api_base, api_version, auth_type, and api_key / audience fields under both chat model and embedding model.<br>
As a reference, you may use this project's settings.yaml which is included with a sample dataset at
`src/app/graphrag_data`
You should leave encoding_model as cl100k_base.<br>
Common pitfalls: when the API version is a shortdate (YYYY-MM-DD) such as 2023-05-15, GraphRAG may have an error when parsing this value from the YAML (it will parse it to date). Instead, use a string qualifier "2023-05-15".<br>
Note that if you are using Azure, all of these values can be found in Azure AI Foundry / Azure OpenAI inside each deployment. You'll need to set-up a chat model and a text embedding model.<br>

3. Auto-tune prompts according to your data:
```
cd /workspaces/guidescanner/src/app/graphrag_data/nvidia_new/
python -m graphrag prompt-tune --root /workspaces/guidescanner/src/app/graphrag_data/nvidia_new  --config /workspaces/guidescanner/src/app/graphrag_data/nvidia_new/settings.yaml --domain "software development" --discover-entity-types --min-examples-required 10 --selection-method auto
```

4. Run <br>
```
python -m graphrag index --root /workspaces/guidescanner/src/app/graphrag_data/nvidia_new --config /workspaces/guidescanner/src/app/graphrag_data/nvidia_new/settings.yaml

```
to index the data.

5. [Optional] Query locally or globally (commandline):<br>
```
python -m graphrag query --root /workspaces/guidescanner/src/app/graphrag_data/nvidia_new --method local -q "Tell me how Deepstream nvDCF tracker is working and what are its key parameters."
```

```
python -m graphrag query --root /workspaces/guidescanner/src/app/graphrag_data/nvidia_new --method global -q "Tell me about Deepstream trackers"
```
This is good for sanity checks.

5. [Optional] Query example from script. Loop and try questioning GraphRAG. <br>
The results are saved locally. It is good for debugging and comparing changes / improvements to the indexing process (i.e., use the same questions / queries). See `dev/qurey_loop.py`
``` 
python qurey_loop.py --root_dir "/workspaces/guidescanner/graphrag" 
```

6. When running the app via docker container, use this to run with the host's azure login

```
docker run -v ~/.azure:/root/.azure -p 8000:8000 -it [your-image-id]
```

# Appendix
## Scanner Recipe
This is a smaller scanner and crawler to sift and download text from various webpages, for being used in graphrag/inputs directory.<br>
It is optional to use that, and any other method to prepare text or json files for consumption is acceptable (although, for non-text files you may need to change settings.yaml) <br>

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


References: 
* https://microsoft.github.io/graphrag/get_started/
* Auto-tuning GraphRag prompts: https://www.microsoft.com/en-us/research/blog/graphrag-auto-tuning-provides-rapid-adaptation-to-new-domains/





