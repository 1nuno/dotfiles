import scrapy
from datetime import datetime, timedelta


class TjscSpiderSpider(scrapy.Spider):
    start_time = datetime.now()
    name = "tjsc"
    allowed_domains = ["busca.tjsc.jus.br"]
    url = "https://busca.tjsc.jus.br/jurisprudencia/buscaajax.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://busca.tjsc.jus.br",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=208A8812E6F464B7E0008C6E03F6BB9F",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
   
    def __init__(self):
        self.i = 0
        self.beginning_time = datetime.now()
        self.initial_date = datetime(2018, 1, 1)
        self.final_date = datetime(2018, 1, 30)
        self.i_date = str(self.initial_date.date()).split('-')
        self.f_date = str(self.final_date.date()).split('-')
        self.i_day,self.i_month,self.i_year = self.i_date[2],self.i_date[1],self.i_date[0]
        self.f_day ,self.f_month,self.f_year = self.f_date[2],self.f_date[1],self.f_date[0]
        self.payloads = [f"=q%3D&=only_ementa%3D&=frase%3D&=excluir%3D&=qualquer%3D&=%3D&=prox1%3D&=prox2%3D&=proxc%3D&sort=dtJulgamento%2Bdesc&ps=50&busca=avancada&pg=1&flapto=1&datainicial={self.i_day}%2F{self.i_month}%2F{self.i_year}&datafinal={self.f_day}%2F{self.f_month}%2F{self.f_year}&radio_campo=ementa&categoria%5B%5D=acordaos&categoria%5B%5D=acma&categoria%5B%5D=recurso&faceta=false"]
        while self.initial_date.date() < datetime(2017, 12, 1).date():
            self.advance_one_month()
            self.payloads.append(f"=q%3D&=only_ementa%3D&=frase%3D&=excluir%3D&=qualquer%3D&=%3D&=prox1%3D&=prox2%3D&=proxc%3D&sort=dtJulgamento%2Bdesc&ps=50&busca=avancada&pg=1&flapto=1&datainicial={self.i_day}%2F{self.i_month}%2F{self.i_year}&datafinal={self.f_day}%2F{self.f_month}%2F{self.f_year}&radio_campo=ementa&categoria%5B%5D=acordaos&categoria%5B%5D=acma&categoria%5B%5D=recurso&faceta=false")
        
    def start_requests(self):
        for payload in self.payloads:
            yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse, meta={'page': 1}, method="POST", body=payload)
    
    def advance_one_month(self):
        self.initial_date = self.final_date + timedelta(days=1)
        temp = self.initial_date.replace(day=28) + timedelta(days=4)
        self.final_date = self.initial_date.replace(day=28) + timedelta(days=4) - timedelta(days=temp.day)
        self.i_date = str(self.initial_date.date()).split('-')
        self.f_date = str(self.final_date.date()).split('-')
        self.i_day,self.i_month,self.i_year = self.i_date[2],self.i_date[1],self.i_date[0]
        self.f_day ,self.f_month,self.f_year = self.f_date[2],self.f_date[1],self.f_date[0]

    def parse(self, response):
        links = ["https://busca.tjsc.jus.br/jurisprudencia/" + i for i in response.xpath('//div[@class="resultados"]//div[@class="icones"]//a[starts-with(@href, "html")]/@href').getall()]
        if len(links) > 0:
            for link in links:
                yield scrapy.Request(url=link, headers=self.headers, callback=self.parse_data, meta={'page': response.meta.get('page')}, errback=self.onerror_item)

            total_page_num = int(response.xpath('//div[@id="paginacao"]').xpath('//p[contains(text(),"Página")]//text()').get().split('de')[-1].strip())
            for i in range(2,total_page_num+1):
                self.payload = f"=q%3D&=only_ementa%3D&=frase%3D&=excluir%3D&=qualquer%3D&=%3D&=prox1%3D&=prox2%3D&=proxc%3D&sort=dtJulgamento%2Bdesc&ps=50&busca=avancada&pg={i}&flapto=1&datainicial={self.i_day}%2F{self.i_month}%2F{self.i_year}&datafinal={self.f_day}%2F{self.f_month}%2F{self.f_year}&radio_campo=ementa&categoria%5B%5D=acordaos&categoria%5B%5D=acma&categoria%5B%5D=recurso&faceta=false"
                yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse, meta={'page': i}, method="POST", body=self.payload, errback=self.onerror_full)
    
    def parse_data(self, response):
        ref = ['Processo:',
                'Relator:',
                'Origem:',
                'Orgão Julgador:',
                'Julgado em:',
                'Classe:']
        data = {j.strip().strip(':'):i.strip() for i,j in zip(response.xpath("//div[@class='resultados']//strong/following-sibling::text()[1]").getall(),
                                     response.xpath("//div[@class='resultados']//strong/text()").getall()) if j in ref}
        data['main_text'] = ''.join([i.strip() if len(i.strip()) > 0 else '\n' for i in response.xpath('//div[@class="integra_paragrafo"]//text()').getall()])
        data['link'] = response.url
        data['page'] = response.meta.get('page')
        with open('count.txt', 'a') as f:
            f.write(str(self.i)+'\n')
        print('---------------------------------------------------------------------------------------------------')
        print()
        print(f'SCRAPED {self.i}  TIME  {datetime.now()-self.beginning_time}')
        print()
        print('---------------------------------------------------------------------------------------------------')
        self.i += 1
        yield data

    def onerror_item(self, failure):
        with open('didnt_scrape_item.txt', 'a') as f:
            f.write(str(failure.request.url)+'\n')
        print('---------------------------------------------------------------------------------------------------')
        print()
        print('ADDED TO DIDNT SCRAPE_ITEM')
        print()
        print('---------------------------------------------------------------------------------------------------')

    def onerror_full(self, failure):
        with open('didnt_scrape_full.txt', 'a') as f:
            f.write((failure.request.url)+'\n')
        print('---------------------------------------------------------------------------------------------------')
        print()
        print('ADDED TO DIDNT SCRAPE_FULL')
        print()
        print('---------------------------------------------------------------------------------------------------')
        
    def closed(self, response):
        ending_time = datetime.now()
        duration = ending_time - self.start_time
        with open('duration.txt', 'a') as f:
            f.write(str(duration.seconds)+'\n')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print()
        print(str(duration.seconds))
        print()
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')