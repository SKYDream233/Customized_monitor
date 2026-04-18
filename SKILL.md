---
name: hot_monitor
description: 学术科技+数码游戏专属热点监控，覆盖19个平台，支持分领域分析与结构化报告
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      python: ["requests", "beautifulsoup4", "pyyaml", "pygithub", "arxiv", "feedparser"]
    emoji: "🔥"
    category: "information_retrieval"
    author: "Your Name"
    version: "3.0.0"
---

# Hot Monitor 热点监控技能（学术+游戏专属版）

## 触发条件
当用户询问以下内容时触发：
- **学术科技**：最近[领域]有什么论文/预印本/顶会动态、GitHub开源项目、技术突破
- **数码游戏**：最近有什么新游戏发售/版本更新/折扣信息、显卡硬件评测、赛事资讯
- **通用**：生成今日热点报告、跟踪[关键词]动态

## 执行流程
1. **领域识别**：自动判断"学术科技"/"数码游戏"/"通用"
2. **子意图分类**：
   - 学术：论文搜索、顶会追踪、开源项目、技术突破
   - 游戏：游戏新闻、硬件评测、折扣信息、赛事资讯、版本更新
3. **参数提取**：关键词、时间范围、内容类型
4. **数据采集**：加载对应预设，调用专属数据源
5. **分领域分析**：使用学术/游戏专属评估模型
6. **报告生成**：输出对应领域的结构化报告

## 工具调用示例
```bash
# 学术测试
python3 scripts/search_academic.py --keywords "AI" --sources arxiv --limit 5
python3 scripts/search_github.py --keywords "machine-learning" --domain academic --limit 5

# 游戏测试
python3 scripts/search_gaming.py --sources steam --type news --limit 5
python3 scripts/search_china.py --keywords "游戏评测" --sources bilibili --limit 5

# 生成报告
python3 generate_report.py --input results.json --domain academic --output report.md