# A股中特估分析框架 v2.1

> 聚焦核心价值：ROE深度分析 + 中特估政策匹配度分析

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/Version-2.1-orange.svg)](#)

---

## 精简后的核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| **数据获取** | `data.py` | 融合a-stock-data API，实时获取PE/PB/市值 |
| **ROE分析** | `roe.py` | 杜邦分解 + 行业对标 + 质量评估 |
| **政策匹配** | `policy.py` | 8维度语义分析 + 匹配度评分 |

## 快速开始

```python
from a_stock_esg import ROEAnalyzer, PolicyAnalyzer

# ROE分析
roe_analyzer = ROEAnalyzer()
result = roe_analyzer.analyze("600886", industry="电力")
print(f"ROE: {result.roe}% | 质量: {result.quality.value}")

# 政策匹配
policy_analyzer = PolicyAnalyzer()
result = policy_analyzer.analyze(
    code="600886",
    name="国投电力",
    disclosure_text="公司积极推进国企改革...",
    industry="电力"
)
print(f"政策匹配分: {result.overall_score}")
```

## 数据来源

融合 [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) V3.2.1：

| 数据层 | API | 用途 |
|--------|-----|------|
| 行情层 | 腾讯财经 | PE/PB/市值/换手率（不封IP） |
| 资金层 | 东财push2 | 资金流向（限流） |
| 信号层 | 东财datacenter | 龙虎榜/融资融券（限流） |

## 分析维度

### ROE深度分析
- 杜邦分解：ROE = 净利率 × 资产周转率 × 权益乘数
- 质量评估：优秀/良好/一般/较差
- 行业对标：百分位排名
- 优劣势识别

### 中特估政策匹配
- 国企改革
- ROE提升
- 数字化转型
- 绿色发展
- 创新驱动
- 区域发展
- 消费升级
- 供应链安全

## 项目结构

```
a_stock_esg_framework/
├── src/a_stock_esg/
│   ├── __init__.py      # 入口
│   ├── data.py          # 数据获取（融合a-stock-data）
│   ├── roe.py           # ROE深度分析
│   └── policy.py        # 政策匹配分析
├── examples/
│   ├── quick_analysis.py    # 快速分析示例
│   └── deep_analysis.py     # 深度分析示例
└── tests/
```

## 许可证

MIT License
