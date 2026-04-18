import argparse
import json
import sys
from github import Github, GithubException
from datetime import datetime, timedelta
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def search_github_trending(language=None, since="daily", limit=10, domain=None):
    config = load_config()
    g = Github(config["github"].get("access_token")) if config["github"].get("access_token") else Github()
    
    try:
        since_date = datetime.utcnow() - timedelta(days=1 if since=="daily" else 7 if since=="weekly" else 30)
        query = f"created:>{since_date.strftime('%Y-%m-%d')}"
        if language: query += f" language:{language}"
        if domain == "academic": query += " topic:machine-learning topic:deep-learning"
        if domain == "gaming": query += " topic:game-development topic:unity topic:unreal-engine"
        
        repos = g.search_repositories(query=query, sort="stars", order="desc")[:limit]
        results = []
        for repo in repos:
            results.append({
                "title": f"{repo.full_name} - {repo.description}",
                "content": f"星标: {repo.stargazers_count} | Forks: {repo.forks_count} | 语言: {repo.language}",
                "url": repo.html_url,
                "source": "GitHub Trending",
                "publishedAt": repo.created_at.isoformat() + "Z",
                "engagement": {"stars": repo.stargazers_count, "forks": repo.forks_count},
                "domain": domain
            })
        return results
    except GithubException as e:
        print(f"GitHub API错误: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="GitHub热点采集")
    parser.add_argument("--keywords", help="搜索关键词")
    parser.add_argument("--trending", action="store_true", help="搜索Trending repos")
    parser.add_argument("--language", help="语言过滤")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily")
    parser.add_argument("--domain", choices=["academic", "gaming", "general"], default="general")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.trending:
        results = search_github_trending(args.language, args.since, args.limit, args.domain)
    else:
        results = []  # 关键词搜索实现略
    print(json.dumps(results, ensure_ascii=False))

if __name__ == "__main__":
    main()