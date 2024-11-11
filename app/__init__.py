import site_models as models
import asyncio, threading, importlib, inspect
from functions import *
from classes import LogManager

async def main(model):
    try:
        modulo = importlib.import_module('site_models')
        logger = LogManager(model)
        classModel = getattr(modulo, model)(logger)
    except Exception as e:
        print(e)
    
    page = 1
    try:
        while True:
            print(f"| {page} | {model} |")
            tree = await classModel.getPage(page)
            page_data = data_page(classModel.pxpath, tree, classModel.key_model)
            
            if len(page_data) != 0:
                await classModel.getPosts(page_data, classModel.sxpath, model)
                page += 1
            else: break
    except Exception as e:
        pass
    
def run_in_thread(model):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main(model))
    finally:
        loop.close()

if __name__ == "__main__":
    # nmodels = [model[0] for model in inspect.getmembers(models, inspect.isclass)]

    nmodels = ["BurburinhoNews", "BahiaNoAr"]
    # nmodels = ["BahiaNoAr"]
    # nmodels = ["JornalGrandeBahia"]
    # nmodels = ["LfNews"]
    # nmodels = ["RelataBahia"]
    # nmodels = ["VilasMagazine"]
    
    threads = list()
    for model in nmodels:
        thread = threading.Thread(target=run_in_thread, args=(model,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()