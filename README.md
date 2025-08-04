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

## Simple GraphRAG Indexing Recipe (without prompt auto-tuning)
This basic indexing might prove the easiest way to get GraphRAG working.<br>
Auto-Turning prompts is sometimes very sensitive to types of inputs and internal GraphRAG bits and pieces that are sometimes difficult to pinpoint.<br>
As a first step and sanity, it is encouraged to first run basic indexing before trying the prompt-tuning options.<br>
For this example you may use the same settings.yaml found in:
`src/app/graphrag_data/nvidia_simple` or the one under
`src/app/graphrag_data/holmes/` 
These are settings.yaml produces by the root init command (see below) and modified to use an Azure OpenAI deployment.<br>
If you have access to this deployment, you can you this settings.yaml instead of doing Step (1) (make sure to `az login` !). <br>
Otherwise, do step (1) and modify manually the settings.yaml to match your own LLM deployment. <br>

1. To initialize the directory <br>
```
cd guidescanner/src/app/graphrag_data
graphrag init --root ./nvidia_simple/
```
<br>
This will create settings.yaml and .env files that you'll have to modify to access your own LLM. 

2. Copy your data (text files) to the input directory <br>
If you're using this guide, the `nvidia_simple/input` will already have input text files, so you may skip this step.
```
cp mydata/*.txt ./nvidia_simple/input
```

3. Run GraphRAG indexing. It will use default options for anything not tuned.
```
graphrag index --root ./nvidia_simple
```

4. You may use the sample dev/qurey_loop.py script to query your indexed data:
```
python dev/qurey_loop.py --root_dir "/workspaces/guidescanner/src/app/graphrag_data/nvidia_simple" 
```

## GraphRAG Recipe for Prompt Tuning
I've temporarily removed this section as several things have changed and broken this guide in updated versions of GraphRAG.<br>
I'll update it when time permits. Alrenatively, you may review prevision version of this file, which may give you a hint about how prompt auto-tune works.

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





