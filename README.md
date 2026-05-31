# A股适配版富士通AI分析逻辑框架

针对A股ESG披露的监管要求（如沪深交易所指引、科创板/创业板强制披露规则）和企业痛点（合规性不明确、信息分散、对标困难），调整原富士通模型的数据源、规则引擎和功能模块，帮助A股企业提升非财务信息披露质量。

## 核心功能

### 1. 合规性智能检查
- 基于A股监管规则引擎，自动扫描企业披露文本
- 标记缺失项（如碳排放目标、员工权益保护）和不符合项
- 生成合规整改清单，提示科创板企业需补充"绿色技术研发投入"等强制披露内容

### 2. 多源信息整合管理
- 中文NLP技术提取年报、ESG报告中的非财务信息
- 统一存储在中央数据库
- 识别信息冲突（如年报与ESG报告中碳排放数据不一致），并发出预警

### 3. 行业对标与差异化分析
- 对比同行业A股公司的披露深度和得分
- 生成差异化建议，提示传统制造业企业突出"节能技改"项目

### 4. 可视化看板
- 展示企业ESG合规进度、行业排名、风险点分布
- 支持按监管要求（环境、社会、治理三大维度）拆分数据

### 5. A股数据集成
- 集成 [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) 数据源
- 支持实时行情、财务数据、研报、公告等多维度数据获取
- 7层架构、27个端点、13个数据源

## 项目结构

```
a_stock_esg_framework/
├── src/a_stock_esg/           # 核心源代码
│   ├── core/                  # 核心配置
│   │   ├── config.py          # 配置管理
│   │   └── ...
│   ├── compliance/            # 合规性检查
│   │   ├── engine.py          # 合规检查引擎
│   │   └── ...
│   ├── data/                  # 数据源层
│   │   ├── collector.py       # 数据收集器
│   │   ├── parser.py          # 文档解析器
│   │   ├── astock_integration.py  # A股数据集成
│   │   └── ...
│   ├── nlp/                   # 中文NLP处理
│   │   ├── processor.py       # NLP处理器
│   │   └── ...
│   ├── visualization/         # 可视化
│   │   ├── benchmark.py       # 行业对标
│   │   ├── visualizer.py      # 看板生成
│   │   └── ...
│   ├── knowledge_graph/       # 知识图谱
│   │   ├── graph.py           # 图谱构建
│   │   └── ...
│   └── main.py                # 主程序入口
├── examples/                  # 示例脚本
├── tests/                     # 测试文件
├── docs/                      # 文档
├── config/                    # 配置文件
├── setup.py                   # 安装配置
└── requirements.txt           # 依赖列表
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/dkjune/a-stock-esg-framework.git
cd a-stock-esg-framework

# 安装依赖
pip install -r requirements.txt

# 安装a-stock-data依赖（可选）
pip install mootdx stockstats

# 安装包
pip install -e .
```

## 快速开始

### 基础使用

```python
from a_stock_esg import AStockESGConfig, ComplianceEngine, NLPProcessor
from a_stock_esg.core.config import MarketType, IndustryClassification

# 创建配置
config = AStockESGConfig(
    market_type=MarketType.MAIN_BOARD,
    industry=IndustryClassification.ELECTRONICS,
)

# 创建合规检查引擎
engine = ComplianceEngine(config)

# 分析ESG文档
report = engine.check_compliance(
    document_text="你的ESG报告文本...",
    company_name="示例公司",
    market_type="主板",
    industry="电子",
)

# 查看合规报告
print(f"合规评分: {report.compliance_score}")
print(f"合规项: {report.compliant_items}")
print(f"缺失项: {report.missing_items}")
```

### 集成A股数据

```python
from a_stock_esg import AStockDataIntegrator, ESGDataPipeline

# 创建数据集成器
integrator = AStockDataIntegrator()

# 获取股票信息
stock_info = integrator.get_stock_info("600519")
print(f"公司名称: {stock_info.stock_name}")
print(f"所属行业: {stock_info.industry}")

# 获取财务数据
financial = integrator.get_financial_data("600519")
print(f"PE(TTM): {financial.pe_ttm}")
print(f"PB: {financial.pb}")

# 使用数据管道准备ESG分析
pipeline = ESGDataPipeline()
esg_data = pipeline.prepare_esg_analysis("600519")
```

### 行业对标分析

```python
from a_stock_esg import BenchmarkAnalyzer, DataCollector

# 创建数据收集器
data_collector = DataCollector()

# 创建对标分析器
analyzer = BenchmarkAnalyzer(data_collector)

# 获取行业对标
comparison = analyzer.compare_with_industry(
    company_code="000001",
    company_score=75.5,
    year=2024,
)

print(f"行业排名: {comparison.industry_rank}/{comparison.total_companies}")
print(f"百分位: {comparison.percentile}%")
```

## A股数据集成

本框架集成了 [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) 的数据源，提供以下能力：

### 数据源优先级

| 优先级 | 数据源 | 用途 |
|--------|--------|------|
| 1（首选） | mootdx（通达信） | K线/五档/逐笔/财务快照/F10 |
| 2（首选） | 腾讯财经 | 实时价/PE/PB/市值/换手率 |
| 3 | 同花顺 | 强势股/题材归因/北向资金 |
| 4 | 百度股市通 | 概念板块/K线 |
| 5 | 新浪财经 | 财报三表 |
| 6 | 巨潮 cninfo | 公告全文 |
| 7 | iwencai | NL语义搜索 |
| 8 | 东财 | 龙虎榜/解禁/两融/大宗/资金流 |

### 支持的端点

- **行情层**: K线、五档盘口、实时报价、PE/PB/市值
- **研报层**: 研报列表、PDF下载、一致预期
- **信号层**: 强势股、题材归因、北向资金、概念板块
- **资金面**: 融资融券、大宗交易、股东户数、分红送转
- **新闻层**: 个股新闻、全球资讯
- **基础数据**: 季报37字段、F10九大类、财报三表
- **公告层**: 沪深北全量公告

## 技术特点

### 1. A股监管规则引擎
- 支持沪深交易所ESG披露指引
- 覆盖科创板/创业板强制披露规则
- 动态更新国内监管政策

### 2. 中文NLP处理
- 针对A股披露文本优化
- 支持ESG术语识别（如"碳中和""乡村振兴"）
- 情感分析（投资者对ESG信息的反馈）

### 3. 知识图谱
- 关联A股企业的ESG数据与财务指标
- 支持相关性分析（如ROE与碳减排投入的相关性）

### 4. 行业对标
- 对比同板块、同行业A股上市公司的披露水平
- 生成差异化建议

## 支持的监管标准

- 《上市公司自律监管指引第1号》
- 《科创板上市公司自律监管指引第11号》
- 证监会《上市公司ESG信息披露指引》（征求意见稿）
- "双碳"政策要求

## 示例运行

```bash
# 运行基础示例
python examples/basic_usage.py

# 运行A股数据集成示例
python examples/astock_data_integration.py
```

## 贡献

欢迎贡献代码和提出建议！

## 许可证

MIT License
