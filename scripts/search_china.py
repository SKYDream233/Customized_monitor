import argparse
import json
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.bilibili.com/"
}

def search_sogou(keywords, limit=10):
    """搜狗网页搜索（无API密钥）"""
    results = []
    try:
        url = "https://www.sogou.com/web"
        params = {
            "query": keywords,
            "num": limit,
            "ie": "utf8"
        }
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for item in soup.select("div.results div.vrwrap")[:limit]:
            title_elem = item.select_one("h3 a")
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            # 处理搜狗跳转链接
            raw_link = title_elem["href"]
            if raw_link.startswith("/link?url="):
                # 直接获取真实链接（简化版，如需完整可添加跳转解析）
                link = f"https://www.sogou.com{raw_link}"
            else:
                link = raw_link
            
            content_elem = item.select_one("div.ft")
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # 提取发布时间
            time_elem = item.select_one("span.gray")
            published_at = datetime.utcnow().isoformat() + "Z"
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                if "天前" in time_text:
                    days = int(re.findall(r"\d+", time_text)[0])
                    published_at = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
                elif "小时前" in time_text:
                    hours = int(re.findall(r"\d+", time_text)[0])
                    published_at = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
            
            results.append({
                "title": title,
                "content": content[:300],
                "url": link,
                "source": "搜狗搜索",
                "publishedAt": published_at,
                "engagement": {},
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"搜狗搜索错误: {str(e)}", file=sys.stderr)
        return []

def search_bilibili(keywords, limit=10, detect_account=False):
    """B站搜索（无API密钥），支持UP主账号检测"""
    results = []
    try:
        # 第一步：检测是否为UP主账号
        if detect_account:
            search_url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword={keywords}&page=1&pagesize=1"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            data = response.json()
            if data["code"] == 0 and data["data"]["numResults"] > 0:
                # 找到UP主，抓取最新视频
                mid = data["data"]["result"][0]["mid"]
                return get_bilibili_user_videos(mid, limit)
        
        # 第二步：普通视频搜索
        search_url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={keywords}&page=1&pagesize={limit}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        data = response.json()
        
        if data["code"] != 0:
            return []
        
        for video in data["data"]["result"][:limit]:
            published_at = datetime.fromtimestamp(video["pubdate"]).isoformat() + "Z"
            results.append({
                "title": video["title"].replace("<em class=\"keyword\">", "").replace("</em>", ""),
                "content": f"UP主: {video['author']} | 简介: {video['description'][:100]}",
                "url": f"https://www.bilibili.com/video/{video['bvid']}",
                "source": "B站",
                "publishedAt": published_at,
                "engagement": {
                    "view": video["play"],
                    "like": video["like"],
                    "comment": video["review"],
                    "danmaku": video["danmaku"]
                },
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"B站搜索错误: {str(e)}", file=sys.stderr)
        return []

def get_bilibili_user_videos(mid, limit=10):
    """获取指定UP主的最新视频"""
    results = []
    try:
        url = f"https://api.bilibili.com/x/space/arc/search?mid={mid}&ps={limit}&tid=0&pn=1&order=pubdate"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        
        if data["code"] != 0:
            return []
        
        for video in data["data"]["list"]["vlist"][:limit]:
            published_at = datetime.fromtimestamp(video["created"]).isoformat() + "Z"
            results.append({
                "title": video["title"],
                "content": f"UP主: {video['author']} | 简介: {video['description'][:100]}",
                "url": f"https://www.bilibili.com/video/{video['bvid']}",
                "source": f"B站UP主@{video['author']}",
                "publishedAt": published_at,
                "engagement": {
                    "view": video["play"],
                    "like": video["like"],
                    "comment": video["comment"],
                    "danmaku": video["video_review"]
                },
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"获取UP主视频错误: {str(e)}", file=sys.stderr)
        return []

def search_weibo(keywords, limit=10):
    """微博移动端搜索（无API密钥）"""
    results = []
    try:
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{keywords}&page_type=searchall"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        
        if data["ok"] != 1:
            return []
        
        for card in data["data"]["cards"][:limit]:
            if card["card_type"] != 9:  # 只处理微博卡片
                continue
            
            mblog = card["mblog"]
            published_at = datetime.strptime(mblog["created_at"], "%a %b %d %H:%M:%S %z %Y").isoformat()
            
            # 处理长文本
            content = mblog["text"]
            if mblog.get("isLongText"):
                content = mblog["longText"]["content"] if "longText" in mblog else content
            
            # 去除HTML标签
            content = re.sub(r"<[^>]+>", "", content)
            
            results.append({
                "title": f"@{mblog['user']['screen_name']}: {content[:50]}...",
                "content": content[:300],
                "url": f"https://weibo.com/{mblog['user']['id']}/{mblog['bid']}",
                "source": "微博",
                "publishedAt": published_at,
                "engagement": {
                    "reposts": mblog["reposts_count"],
                    "comments": mblog["comments_count"],
                    "likes": mblog["attitudes_count"]
                },
                "domain": "general"
            })
        return results
    except Exception as e:
        print(f"微博搜索错误: {str(e)}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="中文平台热点采集")
    parser.add_argument("--keywords", required=True, help="搜索关键词")
    parser.add_argument("--sources", default="sogou,bilibili,weibo", help="数据源（逗号分隔）")
    parser.add_argument("--limit", type=int, default=10, help="每个平台返回结果数量")
    parser.add_argument("--detect-account", action="store_true", help="检测B站UP主账号并抓取最新视频")
    args = parser.parse_args()

    all_results = []
    sources = args.sources.split(",")
    
    if "sogou" in sources:
        all_results.extend(search_sogou(args.keywords, args.limit))
    if "bilibili" in sources:
        all_results.extend(search_bilibili(args.keywords, args.limit, args.detect_account))
    if "weibo" in sources:
        all_results.extend(search_weibo(args.keywords, args.limit))
    
    print(json.dumps(all_results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()