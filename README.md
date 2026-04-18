Customrized Monitor 学术科技 + 数码游戏专属热点监控系统
基于OpenClaw框架的轻量级多源热点监控技能，专门解决学术科技和数码游戏领域信息分散、获取效率低、通用工具缺乏深度的痛点。无需服务器/数据库，一键部署，自动采集10 个已实现平台数据，通过分领域AI分析生成结构化报告。
✨ 核心特性
10 个已实现平台全覆盖：学术 (arXiv)、游戏 (Steam)、通用 (Bing/DuckDuckGo/HackerNews)、中文 (搜狗 / B 站 / 微博)、开源 (GitHub)
分领域智能分析：学术看期刊 / 引用 / 机构，游戏看官方 / 评分 / 热度，告别标题党
双模板报告输出：学术 / 游戏专属报告格式，展示核心指标
一键领域切换：预设学术 / 游戏配置，自动加载对应数据源和分析模型
B 站 UP 主追踪：自动检测 UP 主名称，直接抓取最新视频
轻量无依赖：仅需 Python 环境，无需复杂部署，支持本地运行
完善错误处理：单个平台失败不影响整体运行，详细日志输出

📦 快速开始
环境要求
Python 3.8+
OpenClaw 0.5.0+
安装步骤
创建技能目录并下载文件
bash
运行
mkdir -p ~/.openclaw/workspace/skills/hot_monitor
cd ~/.openclaw/workspace/skills/hot_monitor
# 将所有代码文件复制到该目录
安装 Python 依赖
bash
运行
pip install -r requirements.txt
配置 API 密钥（可选但强烈推荐）
编辑config.yaml文件，填写你的 GitHub Token（大幅提升 API 速率限制）：
yaml
github:
  access_token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GitHub Token 获取：GitHub Settings → Developer settings → Personal access tokens → Generate new token（无需勾选任何权限）
重载技能使其生效
在 OpenClaw 聊天界面输入：
plaintext
/reload skills
或在命令行执行：
bash
运行
openclaw skills reload

🚀 使用方法
在 OpenClaw 中使用（推荐）
直接输入自然语言指令即可触发：
plaintext
🔥 最近一周AI领域有什么重要论文？
🔥 今天Steam上有什么新游戏发售？
🔥 跟踪GPT-5的最新动态，重点看GitHub和arXiv
🔥 切换到学术科技监控模式
🔥 生成今日数码游戏热点报告
命令行直接使用
bash
运行
# 学术热点采集（arXiv）
python3 scripts/search_academic.py --keywords "大语言模型" --days 7 --limit 10

# 游戏热点采集（Steam）
python3 scripts/search_gaming.py --sources steam --type news --limit 10

# GitHub Trending
python3 scripts/search_github.py --trending --language python --domain academic --limit 5

# 中文平台采集
python3 scripts/search_china.py --keywords "黑神话：悟空" --sources bilibili,weibo --limit 3

# 生成报告
python3 generate_report.py --input results.json --domain academic --output report.md

📁 文件结构
plaintext
hot_monitor/
├── SKILL.md              # OpenClaw技能核心定义（必须在根目录）
├── README.md             # 项目说明文档
├── requirements.txt      # Python依赖清单
├── config.yaml           # 全局配置文件
├── analysis_engine.py    # 分领域热点分析引擎
├── generate_report.py    # 双模板报告生成器
├── scripts/              # 数据采集脚本（全部可运行）
│   ├── search_general.py # 通用国际平台(Bing/DuckDuckGo/HackerNews)
│   ├── search_china.py   # 中文平台(搜狗/B站/微博)
│   ├── search_github.py  # GitHub平台(Trending/关键词搜索)
│   ├── search_academic.py# 学术平台(已实现arXiv)
│   └── search_gaming.py  # 游戏平台(已实现Steam)
└── presets/              # 领域预设配置
    ├── academic.yaml     # 学术科技预设
    └── gaming.yaml       # 数码游戏预设