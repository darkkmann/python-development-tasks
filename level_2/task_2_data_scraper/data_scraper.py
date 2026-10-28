"""Fetch selected HTML elements and save their text to a CSV file."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def scrape(url: str, selector: str, timeout: float = 15) -> list[str]:
    """Retrieve URL with requests and extract text matching a CSS selector."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as error:
        raise RuntimeError("Install requirements.txt before using this scraper.") from error
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "TaskScraper/1.0"})
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Request failed: {error}") from error
    soup = BeautifulSoup(response.text, "html.parser")
    return [element.get_text(" ", strip=True) for element in soup.select(selector)]


def save_csv(items: list[str], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["item"])
        writer.writerows([[item] for item in items])


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape a CSS selector into CSV.")
    parser.add_argument("url")
    parser.add_argument("--selector", default="h1", help="CSS selector, such as 'article h2'")
    parser.add_argument("--output", type=Path, default=Path("scraped_data.csv"))
    args = parser.parse_args()
    try:
        items = scrape(args.url, args.selector)
        save_csv(items, args.output)
    except (RuntimeError, OSError) as error:
        print(f"Error: {error}")
        return 1
    print(f"Saved {len(items)} item(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
