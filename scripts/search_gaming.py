import argparse
import json
import sys
import requests
from datetime import datetime

def search_steam_news(limit=10):
    try:
        url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
        params = {"appid": 0, "count": limit, "maxlength": 300}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        results = []
        for item in data["appnews"]["newsitems"]:
            results.append({
                "title": item["title"],
                "content": item["contents"],
                "url": item["url"],
                "source": "Steam",
                "publishedAt": datetime.fromtimestamp(item["date"]).isoformat() + "Z",
                "engagement": {"views": item["views"]},
                "is_official": True,
                "domain": "gaming"
            })
        return results
    except Exception as e:
        print(f"Steam错误: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="游戏热点采集")
    parser.add_argument("--sources", default="steam")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--type", choices=["news", "reviews", "sales"], default="news")
    args = parser.parse_args()

    all_results = []
    if "steam" in args.sources:
        all_results.extend(search_steam_news(args.limit))
    print(json.dumps(all_results, ensure_ascii=False))

if __name__ == "__main__":
    main()