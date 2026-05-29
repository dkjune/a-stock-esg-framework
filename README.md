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
git clone https://github.com/your-username/a-stock-esg-framework.git
cd a-stock-esg-framework

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 快速开始

### 基础使用

```python
from a_stock_esg import AStockESGAnalyzer, AStockESGConfig
from a_stock_esg.core.config import MarketType, IndustryClassification

# 创建配置
config = AStockESGConfig(
    market_type=MarketType.MAIN_BOARD,
    industry=IndustryClassification.ELECTRONICS,
)

# 创建分析器
analyzer = AStockESGAnalyzer(config)

# 分析ESG文档
result = analyzer.analyze_document(
    document_text="你的ESG报告文本...",
    company_name="示例公司",
    market_type="主板",
    industry="电子",
)

# 查看合规报告
print(f"合规评分: {result['compliance_report'].compliance_score}")
print(f"合规项: {result['compliance_report'].compliant_items}")
print(f"缺失项: {result['compliance_report'].missing_items}")
```

### 生成可视化看板

```python
# 生成看板
dashboard_path = analyzer.generate_dashboard(
    result['compliance_report'],
    output_path="my_esg_dashboard.html"
)
print(f"看板已生成: {dashboard_path}")
```

### 行业对标分析

```python
# 获取行业对标
comparison = analyzer.get_benchmark_comparison(
    company_code="000001",
    company_score=75.5,
    year=2024,
)

print(f"行业排名: {comparison.industry_rank}/{comparison.total_companies}")
print(f"百分位: {comparison.percentile}%")
```

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
```

## 贡献

欢迎贡献代码和提出建议！

## 许可证

MIT License
