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
        scraperapi_key = "568f532b77acf94aa5e40033d880fd15"
        target_url = "https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?PRICE_TO=15000&YEAR_MODEL_FROM=1990&YEAR_MODEL_TO=2025"
        scraper_url = f"http://api.scraperapi.com?api_key={scraperapi_key}&url={target_url}&render=true"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with httpx.AsyncClient() as client:
            res = await client.get(scraper_url, headers=headers)

        soup = BeautifulSoup(res.text, "lxml")

        oglasi = []

        # Ovde selektor može da se menja u zavisnosti od strukture
        for ad in soup.select("article[data-testid='search-result-entry']"):
            naslov = ad.select_one("h2")
            cijena = ad.select_one("span")
            link = ad.select_one("a")
            opis = ad.select_one("p")

            if naslov and cijena:
                oglasi.append({
                    "naslov": naslov.text.strip(),
                    "cijena": cijena.text.strip(),
                    "link": f"https://www.willhaben.at{link['href']}" if link else "",
                    "opis": opis.text.strip() if opis else ""
                })

        return oglasi
    except Exception as e:
        return {"error": str(e)}
