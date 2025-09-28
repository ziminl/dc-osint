#4test, make it to txt

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

BASE = "https://gall.dcinside.com"
GALLERY_PATTERN = re.compile(r"board/lists/\?id=([^&/#?]+)", re.IGNORECASE)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GCrawler/1.0)"
}

def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    if resp.encoding is None:
        resp.encoding = 'utf-8'
    text = resp.text
    if "�" in text:
        resp.encoding = 'euc-kr'
        text = resp.content.decode('euc-kr', errors='ignore')
    return text

def extract_gallery_links(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    galleries = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base_url, href)
        m = GALLERY_PATTERN.search(full)
        if m:
            galleries.add(full.split('#')[0])
    return galleries

def crawl_main(main_url, delay=1.0):
    all_galleries = set()
    try:
        html = fetch(main_url)
    except Exception as e:
        print(f"[ERR] fetch 실패: {main_url} -> {e}")
    else:
        glinks = extract_gallery_links(html, main_url)
        print(f"[INFO] {main_url} 에서 {len(glinks)}개 갤러리 링크 발견")
        all_galleries.update(glinks)
        time.sleep(delay)
    return sorted(all_galleries)

if __name__ == "__main__":
    main_url = "https://gall.dcinside.com"
    galleries = crawl_main(main_url, delay=1.0)
    for g in galleries:
        print(g)
    print("총 갤러리 개수:", len(galleries))

