import os
import requests
from bs4 import BeautifulSoup


SOURCES = {
    "hdfc_large_cap": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
    "hdfc_equity": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
    "hdfc_elss": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    "hdfc_small_cap": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
    "hdfc_balanced_advantage": "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth",
}


OUTPUT_DIR = "data/raw"


def collect_page(name, url):
    print(f"Downloading: {name}")

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    clean_text = "\n".join(lines)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{name}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"Source URL: {url}\n\n")
        file.write(clean_text)

    print(f"Saved: {output_file}")


def main():
    for name, url in SOURCES.items():
        try:
            collect_page(name, url)
        except Exception as error:
            print(f"ERROR for {name}: {error}")


if __name__ == "__main__":
    main()