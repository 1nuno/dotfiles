import requests
from datetime import datetime, timedelta

initial_date = datetime(1982, 5, 1)
final_date = datetime(1982, 5, 31)
i_date = str(initial_date.date()).split('-')
f_date = str(final_date.date()).split('-')
i_day,i_month,i_year = i_date[2],i_date[1],i_date[0]
f_day ,f_month,f_year = f_date[2],f_date[1],f_date[0]

url = "https://busca.tjsc.jus.br/jurisprudencia/buscaajax.do"
payload = f"=q%3D&=only_ementa%3D&=frase%3D&=excluir%3D&=qualquer%3D&=%3D&=prox1%3D&=prox2%3D&=proxc%3D&sort=dtJulgamento%2Bdesc&ps=50&busca=avancada&pg=1&flapto=1&datainicial={i_day}%2F{i_month}%2F{i_year}&datafinal={f_day}%2F{f_month}%2F{f_year}&radio_campo=ementa&categoria%5B%5D=acordaos&categoria%5B%5D=acma&categoria%5B%5D=recurso&faceta=false"
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

response = requests.request("POST", url, data=payload, headers=headers)
while initial_date.date() < datetime(2023, 4, 1).date():
            advance_one_month()
            payloads.append(f"=q%3D&=only_ementa%3D&=frase%3D&=excluir%3D&=qualquer%3D&=%3D&=prox1%3D&=prox2%3D&=proxc%3D&sort=dtJulgamento%2Bdesc&ps=50&busca=avancada&pg=1&flapto=1&datainicial={self.i_day}%2F{self.i_month}%2F{self.i_year}&datafinal={self.f_day}%2F{self.f_month}%2F{self.f_year}&radio_campo=ementa&categoria%5B%5D=acordaos&categoria%5B%5D=acma&categoria%5B%5D=recurso&faceta=false")

print(response.text)