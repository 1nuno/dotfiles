import aiohttp
import asyncio
from contextlib import contextmanager
import random
from user_agent import generate_user_agent
import csv


headers = [{"User-Agent": generate_user_agent()} for _ in range(60)]

didnt_scrape = []


def strip_list(string, to_strip=" "):
    if len(string.strip(to_strip)) == 0:
        return False
    return True


headers_in_use = []


@contextmanager
def allocate_header():
    header = random.choice(headers)

    try:
        headers_in_use.append(header)
        yield header
    finally:
        headers_in_use.remove(header)


ccc = 0


async def scrape_page(url: str, session: aiohttp.ClientSession):
    """Scrape the JSON from a page"""
    with allocate_header() as header:
        async with session.get(url, headers=header, timeout=300) as resp:
            global ccc
            ccc += 1
            html = await resp.text()

            if resp.status == 200:
                print(f"success mf!! ----{ccc}")
                
                with open("unparsed_data.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([html, url, ccc])
                    

            else:
                print(f"SHIT TRAGIC NEW PATEK:  ----{ccc}: {resp.status}")
                didnt_scrape.append(url)

                file = open("didnt_scrape.txt", "a")
                file.write(url + "\n")
                file.close()


async def bound_scrape(url, session, semaphore: asyncio.Semaphore):
    """Scrape the page with binding by semaphore"""
    async with semaphore:
        return await scrape_page(url, session)


async def main():
    sem = asyncio.Semaphore(1000)
    file = open("links_to_scrape.txt", "r")
    urls = [i.strip() for i in file.readlines()]
    file.close()

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls[:2000]:
            tasks.append(asyncio.create_task(bound_scrape(url, session, sem)))
            await asyncio.sleep(
                0.2
            )  # Added a timeout to avoid completely slamming the server
            print("Request sent.")

        results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


if __name__ == "__main__":
    asyncio.run(main())

    print("END")
