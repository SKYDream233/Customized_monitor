import json
import sys
from datetime import datetime

def analyze_academic(item):
    score = 0
    importance = "medium"
    if item.get("journal") in ["Nature", "Science"]:
        importance = "urgent"
    elif item.get("journal") in ["NeurIPS", "ICML", "CVPR"]:
        score += 40
    if item.get("citations", 0) > 100:
        score += 30
    if score > 60:
        importance = "high"
    return {
        "isReal": True,
        "relevance": 85,
        "importance": importance,
        "summary": f"{item['title']} — {item.get('authors', ['未知作者'])[0]}等发表于{item.get('journal', '未知期刊')}"
    }

def analyze_gaming(item):
    score = 0
    importance = "medium"
    if item.get("is_official"):
        score += 50
    if item.get("metacritic_score", 0) >= 90:
        score += 40
    if score > 70:
        importance = "high"
    if item.get("is_official") and score > 90:
        importance = "urgent"
    return {
        "isReal": True,
        "relevance": 90,
        "importance": importance,
        "summary": f"{item['title']} — 来自{item['source']}"
    }

def main():
    parser = argparse.ArgumentParser(description="热点分析引擎")
    parser.add_argument("--input", required=True)
    parser.add_argument("--domain", required=True, choices=["academic", "gaming", "general"])
    args = parser.parse_args()

    with open(args.input, "r") as f:
        items = json.load(f)
    
    analyzed = []
    for item in items:
        if args.domain == "academic":
            analysis = analyze_academic(item)
        elif args.domain == "gaming":
            analysis = analyze_gaming(item)
        else:
            analysis = {"isReal": True, "relevance": 70, "importance": "medium", "summary": item["title"]}
        item.update(analysis)
        analyzed.append(item)
    
    analyzed.sort(key=lambda x: ["low", "medium", "high", "urgent"].index(x["importance"]), reverse=True)
    print(json.dumps(analyzed, ensure_ascii=False))

if __name__ == "__main__":
    main()