import requests
from bs4 import BeautifulSoup
import json
import re
import os

URL = "https://www.city.imabari.ehime.jp/whatsnew.html"

def fetch_and_parse_news():
    print(f"Fetching data from {URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    
    # 文字化け対策
    response.encoding = response.apparent_encoding
    
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []
    
    # 全てのリンク(aタグ)を取得
    links = soup.find_all("a")
    for a in links:
        parent = a.parent
        text_context = parent.get_text() if parent else ""
        
        # テキストから日付（YYYY年M月D日）を抽出
        date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', text_context)
        if date_match:
            title = a.get_text(strip=True)
            # 無効な短いテキストを除外
            if len(title) > 5:
                news_list.append({
                    "date": date_match.group(1),
                    "original": title
                })
    
    # 重複を排除しつつ順序を保持
    seen = set()
    unique_news = []
    for item in news_list:
        if item["original"] not in seen:
            seen.add(item["original"])
            unique_news.append(item)
            
    if not unique_news:
        print("Warning: No news data extracted.")
        return

    # JSONファイルとして出力
    output_file = "news_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_news, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(unique_news)} items to {output_file}.")

if __name__ == "__main__":
    fetch_and_parse_news()
