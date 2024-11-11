from scraper import Scraper
import threading

class BurburinhoNews(Scraper):
    def __init__(self, logger):
        logger.msg("into", "Objeto inicializado")
        self.key_model = 0
        self.url = "https://burburinhonews.com.br/categorias/noticias/page/"
        self.pxpath = dict(
            title = '//article/div/h2/a[@class="post-url post-title"]',
            link = '//article/div/h2/a[@class="post-url post-title"]',
            date = '//article/div/div/span/time',
        )
        self.sxpath = dict(
            text = '//div[@class="entry-content clearfix single-post-content"]',
            tag = '//a[@rel="tag"]',
            category = '//div[@class="post-header-title"]/div[@class="term-badges floated"]/span/a'
        )
        self.per_page = 10
        self.logger = logger

    def run(self):
        self.logger.msg("into", "Objeto inicializado")
  
    def __del__(self):
        pass

    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)

class BahiaNoAr(Scraper):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.key_model = 1
        self.url = "https://bahianoar.com/categoria/noticias/page/"
        self.pxpath = dict(
            title = '//div[@class="row mb-4"]/div/a/p',
            link = '//div[@class="row mb-4"]/div/a',
            date = '//div[@class="row mb-4"]/div/a/div[@class="info-date d-flex align-items-center font-weight-normal mb-1"]/p',
        )
        self.sxpath = dict(
            text = '//div[@class="post-content"]',
            tag = '//div[@class="post_tags d-inline-block"]/a',
            category = '//a[@rel="category tag"]'
        )
        self.per_page = 10
        self.logger = logger

    def run(self):
        pass
    
    def __del__(self):
        pass

    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)
        
class JornalGrandeBahia(Scraper):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key_model = 2
        self.url = "https://jornalgrandebahia.com.br/ultimas-noticias/page/"
        self.pxpath = dict(
            title = '//header[@class="mh-posts-list-header"]/h3[@class="entry-title mh-posts-list-title"]/a',
            link = '//header[@class="mh-posts-list-header"]/h3[@class="entry-title mh-posts-list-title"]/a',
            date = '//span[@class="entry-meta-date updated"]/a',
        )
        self.sxpath = dict(
            text = '//div[@class="entry-content clearfix"]',
            tag = '//a[@rel="tag"]',
            category = '//header/div/span/a[@rel="category tag"]',
        )
        self.per_page = 25

    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)

class LfNews(Scraper):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key_model = 3
        self.url = "https://lfnews.com.br/categorias/noticias/page/"
        self.pxpath = dict(
            title = '//div[@class="entry-blog-header"]/h2',
            link = '//div[@class="entry-blog-header"]/h2/a',
            date = '//span[@class="post-meta-date"]'
        )
        self.sxpath = dict(
            text = "//div[@class='post-body clearfix']",
            tag = '//a[@rel="tag"]',
            category = '//a[@class="post-cat"]'
        )
        self.per_page = 10
    
    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)
        
class RelataBahia(Scraper):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key_model = 4
        self.url = "https://relatabahia.com.br/noticias/pagina/"
        self.pxpath = dict(
            title = '//div[@class="box_titulo"]',
            link = '//div[@class="box_titulo"]/h4/a',
            date = '//div[@class="data_horizontal"]',
        )
        self.sxpath = dict(
            text = '//div[@class="conteudo_post"]',
            tag = '//div[@class="lista_tags_noticias"]/ul/li/a',
            category = '//h2[@class="nome_categoria"]'
        )
        self.per_page = 30

    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)
                
class VilasMagazine(Scraper):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key_model = 5
        self.url = "https://vilasmagazine.com.br/categoria/noticias/page/"
        self.pxpath = dict(
            title = '//div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-info"]/h3[@class="entry-title td-module-title"]/a',
            link = '//div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-info"]/h3[@class="entry-title td-module-title"]/a',
            date = '//*[@class="td_block_inner tdb-block-inner td-fix-index"]/div[@class="tdb_module_loop td_module_wrap td-animation-stack td-cpt-post"]/div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-info"]/div[@class="td-editor-date"]/span[@class="td-author-date"]/span[@class="td-post-date"]/time[@class="entry-date updated td-module-date"]',
        )
        self.sxpath = dict(
            text = '//div[@class="td-post-content tagdiv-type"]',
            tag = '//ul[@class="td-tags td-post-small-box clearfix"]/li/a',
            category = '//ul[@class="td-category"]/li/a'
        )
        self.per_page = 12
    
    async def getPage(self, page_number):
        return await super().getPage(f"{self.url}{page_number}")

    async def getPosts(self, posts, xpath, model):
        await super().getPosts(posts, xpath, model)