from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/oglasi")
async def oglasi():
    try:
        url = "http://api.scraperapi.com?api_key=568f532b77acf94aa5e40033d880fd15&url=https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?PRICE_TO=15000&YEAR_MODEL_FROM=1990&YEAR_MODEL_TO=2025"

        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            print(f"Status code: {res.status_code}")
            print(f"Content snippet: {res.text[:500]}")  # samo prvih 500 znakova da se ne zatrpaš

            soup = BeautifulSoup(res.text, "lxml")

            oglasi = []

            for ad in soup.select("article[data-testid='search-result-entry']"):
                naslov = ad.select_one("h2") or ad.select_one("h3")
                cijena = ad.select_one("span.Text-sc-1cyh90m-0")
                link = ad.select_one("a")["href"] if ad.select_one("a") else ""
                opis = ad.select_one("p") or ad.select_one("div")

                if naslov and cijena:
                    oglasi.append({
                        "naslov": naslov.text.strip(),
                        "cijena": cijena.text.strip(),
                        "link": f"https://www.willhaben.at{link}",
                        "opis": opis.text.strip() if opis else "",
                    })

            return oglasi

    except Exception as e:
        print(f"Greška: {e}")
        return {"error": str(e)}
