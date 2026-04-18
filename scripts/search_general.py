import argparse
import json
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

# 统一请求头，模拟浏览器避免反爬
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate"
}

def search_bing(keywords, limit=10):
    """Bing网页搜索（无API密钥）"""
    results = []
    try:
        url = "https://cn.bing.com/search"
        params = {
            "q": keywords,
            "count": limit,
            "first": 1,
            "FORM": "PORE"
        }
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for item in soup.select("li.b_algo")[:limit]:
            title_elem = item.select_one("h2 a")
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link = title_elem["href"]
            content_elem = item.select_one("p")
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # 提取发布时间
            time_elem = item.select_one("span.sb_time")
            published_at = datetime.utcnow().isoformat() + "Z"
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                # 处理"X天前"格式
                if "天前" in time_text:
                    days = int(re.findall(r"\d+", time_text)[0])
                    published_at = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
            
            results.append({
                "title": title,
                "content": content[:300],  # 限制摘要长度
                "url": link,
                "source": "Bing",
                "publishedAt": published_at,
                "engagement": {},
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"Bing搜索错误: {str(e)}", file=sys.stderr)
        return []

def search_duckduckgo(keywords, limit=10):
    """DuckDuckGo网页搜索（无API密钥，隐私友好）"""
    results = []
    try:
        url = "https://html.duckduckgo.com/html/"
        params = {
            "q": keywords,
            "kl": "cn-zh",
            "df": "d"  # 最近一天
        }
        response = requests.post(url, data=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for item in soup.select("div.result")[:limit]:
            title_elem = item.select_one("h2 a")
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link = title_elem["href"]
            content_elem = item.select_one("a.result__snippet")
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            results.append({
                "title": title,
                "content": content[:300],
                "url": link,
                "source": "DuckDuckGo",
                "publishedAt": datetime.utcnow().isoformat() + "Z",
                "engagement": {},
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"DuckDuckGo搜索错误: {str(e)}", file=sys.stderr)
        return []

def search_hackernews(keywords, limit=10):
    """HackerNews官方API搜索（无密钥，技术热点首选）"""
    results = []
    try:
        # 先搜索相关故事ID
        search_url = f"https://hn.algolia.com/api/v1/search?query={keywords}&tags=story&hitsPerPage={limit}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for hit in data["hits"][:limit]:
            published_at = datetime.fromtimestamp(hit["created_at_i"]).isoformat() + "Z"
            results.append({
                "title": hit["title"],
                "content": f"点数: {hit['points']} | 评论数: {hit['num_comments']}",
                "url": hit["url"] if hit["url"] else f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "source": "HackerNews",
                "publishedAt": published_at,
                "engagement": {
                    "points": hit["points"],
                    "comments": hit["num_comments"]
                },
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"HackerNews搜索错误: {str(e)}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="通用国际平台热点采集")
    parser.add_argument("--keywords", required=True, help="搜索关键词")
    parser.add_argument("--sources", default="bing,duckduckgo,hackernews", help="数据源（逗号分隔）")
    parser.add_argument("--limit", type=int, default=10, help="每个平台返回结果数量")
    args = parser.parse_args()

    all_results = []
    sources = args.sources.split(",")
    
    if "bing" in sources:
        all_results.extend(search_bing(args.keywords, args.limit))
    if "duckduckgo" in sources:
        all_results.extend(search_duckduckgo(args.keywords, args.limit))
    if "hackernews" in sources:
        all_results.extend(search_hackernews(args.keywords, args.limit))
    
    # 输出统一JSON格式
    print(json.dumps(all_results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()