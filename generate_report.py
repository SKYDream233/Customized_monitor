import argparse
import json
from datetime import datetime

def generate_academic_report(items, keyword):
    report = f"## 🔬 学术科技热点监控报告 — {keyword}\n"
    report += f"> 扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据源: arXiv, GitHub等\n\n"
    
    urgent = [i for i in items if i["importance"] == "urgent"]
    high = [i for i in items if i["importance"] == "high"]
    
    if urgent:
        report += "### 🚨 重大突破 (Urgent)\n"
        for item in urgent:
            report += f"- **{item['title']}** — {item['summary']}\n"
            report += f"  📝 期刊: {item.get('journal', '未知')} | 👥 作者: {', '.join(item.get('authors', ['未知']))[:20]}\n"
            report += f"  🔗 链接: {item['url']}\n\n"
    
    if high:
        report += "### 🔴 重要进展 (High)\n"
        for item in high[:5]:
            report += f"- **{item['title']}** — {item['summary']}\n"
            report += f"  🔗 链接: {item['url']}\n\n"
    
    report += f"---\n共发现 {len(items)} 条学术热点，其中重大突破 {len(urgent)} 条，重要进展 {len(high)} 条\n"
    return report

def generate_gaming_report(items, keyword):
    report = f"## 🎮 数码游戏热点监控报告 — {keyword}\n"
    report += f"> 扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据源: Steam, IGN等\n\n"
    
    urgent = [i for i in items if i["importance"] == "urgent"]
    high = [i for i in items if i["importance"] == "high"]
    
    if urgent:
        report += "### 🚨 重磅公告 (Urgent)\n"
        for item in urgent:
            report += f"- **{item['title']}** — {item['summary']}\n"
            report += f"  🔗 链接: {item['url']}\n\n"
    
    if high:
        report += "### 🔴 热门资讯 (High)\n"
        for item in high[:5]:
            report += f"- **{item['title']}** — {item['summary']}\n"
            report += f"  🔗 链接: {item['url']}\n\n"
    
    report += f"---\n共发现 {len(items)} 条游戏热点，其中重磅公告 {len(urgent)} 条，热门资讯 {len(high)} 条\n"
    return report

def main():
    parser = argparse.ArgumentParser(description="报告生成")
    parser.add_argument("--input", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--keyword", default="热点")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        items = json.load(f)
    
    if args.domain == "academic":
        report = generate_academic_report(items, args.keyword)
    else:
        report = generate_gaming_report(items, args.keyword)
    
    with open(args.output, "w") as f:
        f.write(report)
    print(report)

if __name__ == "__main__":
    main()