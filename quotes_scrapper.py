import requests
from bs4 import BeautifulSoup
import json

base_url = "https://quotes.toscrape.com"
url = "/page/1/"

all_data = []

while True:
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        break

    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]

        all_data.append({
            "quote": text,
            "author": author,
            "tags": tags
        })

    next_btn = soup.find("li", class_="next")
    if next_btn:
        url = next_btn.find("a")["href"]
    else:
        break

with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)

print(f"Scraped {len(all_data)} quotes.")