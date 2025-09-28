import requests
from bs4 import BeautifulSoup
import sys

def crawl_gall(id_param, s_keyword, output_file, page=1):
    base_url = "https://gall.dcinside.com/board/lists/"
    params = {
        'id': id_param,
        's_type': 'search_name',
        's_keyword': s_keyword,
        'search_pos': '',
        'page': page,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10, allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 302 or not response:
            return False
    except requests.RequestException as e:
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    em_tags = soup.find_all("em", class_=["icon_img", "icon_txt"])
    if not em_tags:
        return False

    results = [em_tag.next_sibling.get_text() for em_tag in em_tags if not em_tag.next_sibling.name == 'b']
    if not results:
        return False
    
    try:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("==========유저:"+ str(s_keyword)+"=========="+'\n')
            f.write("==========갤러리URL:"+"https://gall.dcinside.com/board/lists/?id="+str(id_param)+"=========="+'\n')
            f.write("=========="+"페이지 수:"+str(page)+"=========="+'\n')
            for line in results:
                f.write(line + '\n')
    except Exception as e:
        sys.exit()

    return True

if __name__ == "__main__":
    s_keyword = input("USERName input:")
    with open("1.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    s_keyword_file = s_keyword + ".txt"
    lines = [line.split("?id=")[-1].strip() for line in lines]
    for id_param in lines:
        page = 1
        while True:
            if not crawl_gall(id_param=id_param, s_keyword=s_keyword, page=page, output_file=s_keyword_file):
                break
            page = page + 1
    print('Done!')
