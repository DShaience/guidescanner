import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.logger_web import logger

from pathlib import Path
import re
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from graphrag.query.cli import run_local_search, run_global_search


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

# Define the paths for each game
game_paths = {
    "JediSurvivor": Path(os.path.join(os.getcwd(), "app/graphrag_data/jedi_survivor")),
    "BO6": Path(os.path.join(os.getcwd(), "app/graphrag_data/blackops6")),
    "BG3": Path(os.path.join(os.getcwd(), "app/graphrag_data/bg3")),
    "Mafia": Path(os.path.join(os.getcwd(), "app/graphrag_data/mafia"))  # todo: reindex Mafia. Seems to have a problem
}

community_level = 2
response_type = "multiple paragraphs"
streaming = False
executor = ThreadPoolExecutor()
cache = {}

async def run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    logger.info(f"Running {func.__name__} in thread with args: {args}")
    return await loop.run_in_executor(executor, func, *args)


async def post_query(config_filepath, data_dir, root_dir, community_level, response_type, streaming, query):
    logger.info(f"Running query: {query}")
    result = await run_in_thread(run_global_search, config_filepath, data_dir, root_dir, community_level, response_type, streaming, query)
    return result


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=JSONResponse)
async def search_post(query: str = Form(...), game: str = Form(...)):
    # Set the graphrag_root based on the selected game
    graphrag_root = game_paths.get(game, game_paths["JediSurvivor"])
    graphrag_data = graphrag_root / "output"
    config_path = graphrag_root / "settings.yaml"

    # Create a cache key based on the query and game
    cache_key = f"{game}:{query}"

    # Check if the result is in the cache
    if cache_key in cache:
        logger.info(f"Cache hit for key: {cache_key}")
        formatted_result = cache[cache_key]
    else:
        logger.info(f"Cache miss for key: {cache_key}")
        # Process the form data
        result = await post_query(config_path, graphrag_data, graphrag_root, community_level, response_type, streaming, query)
        logger.info(f"Completed query.")
        formatted_result = format_results(result)
        # Store the result in the cache
        cache[cache_key] = formatted_result

    return JSONResponse(content={"results": formatted_result})


def remove_bracketed_text(sentence):
    # Regular expression to match text within brackets at the end of a sentence
    pattern = r'\s*\[.*?\]\.?\s*$'
    cleaned_sentence = re.sub(pattern, '.', sentence)
    return cleaned_sentence.strip()


def format_results(results):
    logger.info(f"Formatting result.")
    formatted = []
    text = results[0]
    lines = re.split(r'(?:\r|\n)+', text)
    clean_lines = [remove_bracketed_text(line) for line in lines if line.strip()]

    for line in clean_lines:
        if line.startswith("## "):
            formatted.append({"type": "main-header", "content": line[3:].strip()})
        elif line.startswith("### "):
            formatted.append({"type": "sub-header1", "content": line[4:].strip()})
        elif line.strip() == "":
            continue
        else:
            formatted.append({"type": "paragraph", "content": line.strip()})
    logger.info(f"Formatting completed successfully.")
    return formatted


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

