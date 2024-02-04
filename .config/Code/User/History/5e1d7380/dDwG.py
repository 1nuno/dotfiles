from bs4 import BeautifulSoup as bs
from lxml import etree
import requests as r
import time
import csv

if __name__ == "__main__":
    full_url_hrefs = []
    full_url_texts = []
    response = r.get("https://www.pgdlisboa.pt/leis/lei_main.php")
    soup = bs(response.text, "html.parser")
    dom = etree.HTML(str(soup))
    is_next = "avança 1 página"
    page_num = 0
    while True:
        url_hrefs = [
            "https://www.pgdlisboa.pt/leis/" + i
            for i in dom.xpath("//td/table/tr[2]//div//a/@href")
            if i != ""
        ]

        full_url_hrefs.extend(url_hrefs)

        untreated_url_texts = [
            i
            for i in dom.xpath("//td/table/tr[2]//div//a//text()")
            if not i.startswith("\xa0\xa0")
        ]

        for i in range(0, len(untreated_url_texts), 2):
            if i < len(untreated_url_texts) - 1:
                url_text = (
                    untreated_url_texts[i].strip("\xa0")
                    + " "
                    + untreated_url_texts[i + 1].strip("\xa0")
                )
                full_url_texts.append(url_text)

        with open("links_to_scrape_22_01_24.csv", "a", newline="") as f:
            for href, text in zip(full_url_hrefs, full_url_texts):
                writer = csv.writer(f)
                writer.writerow([href, text])

        full_url_hrefs = []
        full_url_texts = []
        page_num += 1
        print(f"page: {page_num}")

        if not is_next:
            print(is_next)
            print("BREAK")
            break

        next_url = (
            "https://www.pgdlisboa.pt/leis/"
            + dom.xpath(
                '//td/table/following-sibling::div/a[img[contains(@alt,"Avança 1 página")]]//@href'
            )[0]
        )

        response = r.get(next_url)
        soup = bs(response.text, "html.parser")
        dom = etree.HTML(str(soup))
        is_next = dom.xpath(
            '//td/table/following-sibling::div/a[img[contains(@alt,"Avança 1 página")]]//@href'
        )
        time.sleep(2)
