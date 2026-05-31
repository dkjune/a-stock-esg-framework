# A股ESG分析框架 | China ESG Analysis Framework

> A股适配版富士通AI分析逻辑框架 — 针对中国特色估值体系（中特估）的ESG投资分析工具

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](#)

---

## 简介

本框架将富士通AI分析非财务信息披露的思路，完全适配A股市场投资应用场景。针对A股ESG披露的监管要求（沪深交易所指引、科创板/创业板强制披露规则）和企业痛点（合规性不明确、信息分散、对标困难），帮助企业提升非财务信息披露质量，同时为投资者提供价值发现工具。

**核心定位：** 用AI分析企业非财务信息披露，挖掘符合"中特估"政策导向、正在优化治理提升资本回报、尚未被市场充分定价的价值标的。

---

## 核心功能

### 合规与政策分析
- **ESG合规检查** — 基于A股监管规则引擎，自动扫描披露文本，标记缺失项和不符合项
- **中特估政策匹配** — 对标国企改革、ROE提升等本土战略方向，识别真正受益政策红利的标的
- **一利五率分析** — 对标国资委考核指标体系，评估企业经营质量

### 数据与分析
- **多源信息整合** — 中文NLP提取年报、ESG报告中的非财务信息
- **ROE驱动因素分析** — 杜邦分析法分解ROE变动，验证改革是否转化为资本回报提升
- **披露质量评估** — 话术识别、信息矛盾检测，规避信披造假风险

### 投资应用
- **个人投资者评分** — AAA到C的等级评分，快速筛选标的
- **选股因子生成** — 将非财务披露质量转化为量化因子，接入量化模型
- **行业对标分析** — 对比同行业公司披露深度和改革进度

---

## 项目结构

```
a_stock_esg_framework/
├── src/a_stock_esg/
│   ├── core/              # 核心配置
│   ├── compliance/        # 合规检查 + 政策分析 + 风险分析
│   ├── data/              # 数据源（集成a-stock-data）
│   ├── nlp/               # 中文NLP处理
│   ├── visualization/     # 可视化 + 投资评分
│   └── knowledge_graph/   # 知识图谱
├── examples/              # 示例脚本
└── tests/                 # 测试文件
```

---

## 快速开始

```python
from a_stock_esg import (
    ComplianceEngine,
    ChinaValuationPolicyAnalyzer,
    ROEAnalyzer,
    PersonalInvestorScorer,
)

# 合规检查
engine = ComplianceEngine()
report = engine.check_compliance(document_text, "公司名称", "主板", "电子")

# 中特估政策匹配
policy_analyzer = ChinaValuationPolicyAnalyzer()
policy_result = policy_analyzer.analyze_policy_match(document_text)

# ROE分析
roe_analyzer = ROEAnalyzer()
roe_result = roe_analyzer.analyze_roe(company_code, company_name, financial_data)

# 投资评分
scorer = PersonalInvestorScorer()
stock_score = scorer.score_stock(company_code, company_name, analysis_data)
```

---

## 分析维度

| 维度 | 说明 | 投资价值 |
|------|------|----------|
| 政策匹配度 | 对标中特估、国企改革等本土战略 | 识别真正受益政策红利的标的 |
| ESG合规性 | 整合多渠道披露内容 | 快速排雷，规避高风险标的 |
| ROE可持续性 | 验证改革是否转化为资本回报 | 找到真正具备价值重估基础的标的 |
| 披露质量 | 话术识别、信息矛盾检测 | 规避信披造假、蹭热点炒作的标的 |

---

## 适用场景

- **个人投资者** — 轻量化评分工具，快速筛选优质标的
- **机构投资者** — 选股因子生成，优化量化策略
- **企业IR** — ESG披露质量自检，提升信息披露水平
- **研究人员** — A股非财务信息分析研究

---

## 数据来源

- 企业年报、ESG报告、社会责任报告
- 沪深交易所公告
- 国资委考核指标
- 第三方ESG评级（中证ESG、华证ESG等）

---

## 许可证

MIT License

---

*本框架仅供学习研究使用，不构成投资建议。投资有风险，入市需谨慎。*
