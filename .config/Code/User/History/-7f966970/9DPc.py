from bs4 import BeautifulSoup as bs
import requests as r
from lxml import etree
import pandas as pd
import time
import csv

if __name__ == "__main__":
    with open("pgdl_22_01_24.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "artigos_texto", "sumario", "descricao", "url"])

    links_to_scrape = pd.read_csv("links_to_scrape.csv", header=None)
    full_names, all = (
        links_to_scrape.iloc[:, 1].tolist(),
        links_to_scrape.iloc[:, 0].tolist(),
    )

    for name, url in zip(full_names, all):
        resp = r.get(url)
        s = bs(resp.text, "html.parser")
        d = etree.HTML(str(s))

        artigos = "".join(d.xpath('//font[contains(text(), "Artigo")]//text()')).split(
            "\xa0\xa0"
        )[1:]

        texto = ""
        artigos_texto = []
        c = 0
        for i in d.xpath(
            '//font[contains(text(), "Artigo")]/following::td[contains(@class, "txt_base_n_l")][1]//text()'
        ):
            texto += "\n" + i
            if i.endswith("\t\t"):
                artigos_texto.append(artigos[c] + "\n" + texto)
                texto = ""
                c += 1

        artigos_texto = "**********".join(artigos_texto)

        sumario = d.xpath(
            '//span[b[contains(text(), "SUMÁRIO")]]/following-sibling::div/b/text()'
        )
        if sumario:
            sumario = d.xpath(
                '//span[b[contains(text(), "SUMÁRIO")]]/following-sibling::div/b/text()'
            )[0]

        descricao = d.xpath(
            '//td[contains(@class, "txt_base_n_l") and @colspan="3"]//text()'
        )
        descricao = "\n".join(descricao)

        with open("pgdl_22_01_24.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, artigos_texto, sumario, descricao, url])

        break
        time.sleep(2)
