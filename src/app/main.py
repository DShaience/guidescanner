import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from graphrag.query.cli import run_local_search, run_global_search


app = FastAPI()
# templates = Jinja2Templates(directory="app/templates")
templates = Jinja2Templates(directory="templates")
# graphrag_root = Path("app/data/mafia_autotune")
graphrag_root = Path("/workspaces/guidescanner/graphrag_tests/bg3_shadowheart_tuning")
graphrag_data = graphrag_root / "output"
config_path = graphrag_root / "settings.yaml"
community_level = 2
response_type = "multiple paragraphs"
streaming = False
executor = ThreadPoolExecutor()


async def run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)


# def post_query(config_filepath, data_dir, root_dir, community_level, response_type, streaming, query):
#     result = run_global_search(config_filepath, data_dir, root_dir, community_level, response_type, streaming, query)
#     return result

async def post_query(config_filepath, data_dir, root_dir, community_level, response_type, streaming, query):
    result = await run_in_thread(run_global_search, config_filepath, data_dir, root_dir, community_level, response_type, streaming, query)
    return result


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str):
    results = await post_query(config_path, graphrag_data, graphrag_root, community_level, response_type, streaming, query)  # Perform search based on query
    return templates.TemplateResponse("results.html", {"request": request, "results": results})

