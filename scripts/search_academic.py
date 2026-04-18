import argparse
import json
import sys
import arxiv
from datetime import datetime, timedelta

def search_arxiv(keywords, limit=10, days=7):
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=keywords,
            max_results=limit,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        results = []
        for paper in client.results(search):
            if (datetime.utcnow() - paper.published).days > days:
                continue
            results.append({
                "title": paper.title,
                "content": f"摘要: {paper.summary[:200]}...",
                "url": paper.entry_id,
                "source": "arXiv",
                "publishedAt": paper.published.isoformat() + "Z",
                "authors": [a.name for a in paper.authors],
                "journal": "arXiv预印本",
                "citations": 0,
                "domain": "academic"
            })
        return results
    except Exception as e:
        print(f"arXiv错误: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="学术热点采集")
    parser.add_argument("--keywords", required=True)
    parser.add_argument("--sources", default="arxiv")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    all_results = []
    if "arxiv" in args.sources:
        all_results.extend(search_arxiv(args.keywords, args.limit, args.days))
    print(json.dumps(all_results, ensure_ascii=False))

if __name__ == "__main__":
    main()