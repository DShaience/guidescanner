import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re


from async_lru import alru_cache
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from graphrag.query.cli import run_local_search, run_global_search


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

graphrag_root = Path("/workspaces/guidescanner/src/app/graphrag_data/bg3_shadowheart_tuning")

graphrag_data = graphrag_root / "output"
config_path = graphrag_root / "settings.yaml"
community_level = 2
response_type = "multiple paragraphs"
streaming = False
executor = ThreadPoolExecutor()


async def run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)


async def post_query(config_filepath, data_dir, root_dir, community_level, response_type, streaming, query):
    result = await run_in_thread(run_global_search, config_filepath, data_dir, root_dir, community_level, response_type, streaming, query)
    return result


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search")
@alru_cache(maxsize=128)
async def search(query: str):
    results = await post_query(config_path, graphrag_data, graphrag_root, community_level, response_type, streaming, query)
    formatted_results = format_results(results)
    return {"results": formatted_results}


def format_results(results):
    formatted = []
    text = results[0]
    lines = re.split(r'[\r\n]+', text)
    clean_lines = [line for line in lines if line.strip()]

    for line in clean_lines:
        if line.startswith("## "):
            formatted.append({"type": "main-header", "content": line[3:].strip()})
        elif line.startswith("### "):
            formatted.append({"type": "sub-header1", "content": line[4:].strip()})
        elif line.strip() == "":
            continue
        else:
            formatted.append({"type": "paragraph", "content": line.strip()})
    return formatted


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
