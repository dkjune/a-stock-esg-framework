# A股ESG分析框架 Skill

针对A股ESG披露的监管要求和企业痛点的智能分析系统。

## 触发条件

当用户提到以下关键词时激活本 Skill：
- ESG、环境、社会、治理、碳排放、碳中和、碳达峰
- A股、上市公司、合规、披露、年报、可持续发展
- 行业对标、ESG评级、中证ESG、华证ESG
- 绿色金融、乡村振兴、双碳

## 核心能力

### 1. 合规性智能检查

**输入**: 企业ESG披露文本（年报、ESG报告、社会责任报告）
**输出**: 合规检查报告 + 整改清单

**执行步骤**:
1. 调用 `ComplianceEngine.check_compliance(document_text, company_name, market_type, industry)` 获取合规报告
2. 报告包含：合规评分、合规项、部分合规项、缺失项
3. 生成整改清单，按优先级排序

**关键参数**:
- `market_type`: 主板/科创板/创业板/北交所
- `industry`: 行业分类（申万一级）
- `document_text`: 完整的ESG披露文本

**示例调用**:
```python
from a_stock_esg import ComplianceEngine, AStockESGConfig

config = AStockESGConfig(market_type="主板", industry="电子")
engine = ComplianceEngine(config)

report = engine.check_compliance(
    document_text="公司温室气体排放总量为100,000吨CO2当量...",
    company_name="示例公司",
    market_type="主板",
    industry="电子"
)

print(f"合规评分: {report.compliance_score}")
print(f"缺失项: {report.missing_items}")
```

**失败模式处理**:
- 若 `document_text` 为空，返回空报告并提示"请提供ESG披露文本"
- 若 `market_type` 不在支持列表，使用"主板"作为默认值
- 若正则匹配失败，跳过该项检查而非报错

### 2. 中文NLP信息提取

**输入**: ESG披露文本
**输出**: 结构化的ESG信息 + 术语识别 + 情感分析

**执行步骤**:
1. 调用 `NLPProcessor.extract_esg_info(text)` 提取ESG信息
2. 调用 `NLPProcessor.identify_terms(text)` 识别ESG术语
3. 调用 `NLPProcessor.analyze_sentiment(text)` 情感分析

**返回结构**:
```python
{
    "extracted_info": [
        {"category": "E", "subcategory": "碳排放", "content": "碳排放量100,000吨", "confidence": 0.9}
    ],
    "identified_terms": [
        {"term": "碳中和", "category": "E"}
    ],
    "sentiment": {
        "sentiment": "positive",
        "score": 0.75,
        "keywords": ["提升", "改善"]
    }
}
```

**失败模式处理**:
- 若文本包含非中文内容，仍尝试提取但降低置信度
- 若术语库未匹配，返回空列表而非报错

### 3. 行业对标分析

**输入**: 公司代码 + 评分
**输出**: 行业排名 + 差异化建议

**执行步骤**:
1. 调用 `BenchmarkAnalyzer.compare_with_industry(company_code, score, year)`
2. 获取行业平均分、排名、百分位
3. 生成优势/劣势分析和差异化建议

**差异化建议规则**:
| 行业 | 建议重点 |
|------|----------|
| 银行 | 绿色金融产品、普惠金融 |
| 电子 | 电子废弃物回收、数据安全 |
| 化工 | 污染排放控制、安全生产 |
| 钢铁 | 碳减排目标、节能技改 |
| 汽车 | 新能源汽车、电池回收 |

**失败模式处理**:
- 若无行业对标数据，使用默认行业平均分65分
- 若公司代码不存在，返回"请检查股票代码"

### 4. A股数据集成

**输入**: 股票代码
**输出**: 实时行情 + 财务数据 + 研报 + 公告

**数据源优先级**:
1. 腾讯财经（不封IP，首选）
2. mootdx（TCP协议，不封IP）
3. 东财（需限流，仅用于独有数据）

**调用方式**:
```python
from a_stock_esg import AStockDataIntegrator, ESGDataPipeline

integrator = AStockDataIntegrator()

# 获取股票信息
stock_info = integrator.get_stock_info("600519")
print(f"公司名称: {stock_info.stock_name}")

# 获取财务数据
financial = integrator.get_financial_data("600519")
print(f"PE(TTM): {financial.pe_ttm}")

# 使用数据管道
pipeline = ESGDataPipeline()
esg_data = pipeline.prepare_esg_analysis("600519")
```

**失败模式处理**:
- 若网络请求超时，重试3次后返回空数据
- 若股票代码无效，返回"未找到该股票信息"

### 5. 可视化看板生成

**输入**: 合规报告
**输出**: HTML看板文件

**执行步骤**:
1. 调用 `Visualizer.create_compliance_dashboard(report, output_path)`
2. 生成包含以下图表的HTML：
   - 维度得分柱状图（E/S/G）
   - 合规状态饼图
   - 合规检查项详情表
   - 改进建议列表

**输出格式**: HTML文件，使用Plotly.js渲染图表

## 监管规则库

### 基础披露要求（所有A股）
| 编号 | 类别 | 要求 | 强制 |
|------|------|------|------|
| E001 | 环境(E) | 碳排放数据 | ✅ |
| E002 | 环境(E) | 碳减排目标 | ✅ |
| E003 | 环境(E) | 能源消耗数据 | ✅ |
| S001 | 社会(S) | 员工信息披露 | ✅ |
| S003 | 社会(S) | 安全生产管理 | ✅ |
| G001 | 治理(G) | 董事会ESG职责 | ✅ |
| G002 | 治理(G) | 反腐败政策 | ✅ |
| G003 | 治理(G) | 数据安全管理 | ✅ |

### 科创板特殊要求
| 编号 | 要求 | 强制 |
|------|------|------|
| E006 | 绿色技术研发投入 | ✅ |
| G005 | 知识产权保护 | ✅ |
| G006 | 科技创新成果 | ✅ |

## 禁止操作

以下操作**绝对不能**执行：
1. 删除或覆盖用户的原始ESG报告文件
2. 修改 `config/` 目录下的配置文件（除非用户明确要求）
3. 将用户的ESG数据上传到第三方服务
4. 在未获得用户许可的情况下提交Git更改

## 输出规范

### 合规检查报告格式
```
═══════════════════════════════════════════════════
           ESG合规检查报告
═══════════════════════════════════════════════════
公司名称: {company_name}
市场类型: {market_type}
行业分类: {industry}
───────────────────────────────────────────────────
合规评分: {compliance_score}/100
合规项: {compliant_items}  部分合规: {partial_items}
缺失项: {missing_items}    不合规: {non_compliant_items}
═══════════════════════════════════════════════════

【环境(E)维度】
✅ E001 碳排放数据 - 已披露
⚠️ E004 水资源管理 - 部分披露
❌ E005 废弃物处理 - 未披露

【社会(S)维度】
✅ S001 员工信息披露 - 已披露
❌ S004 供应链管理 - 未披露

【治理(G)维度】
✅ G001 董事会ESG职责 - 已披露

───────────────────────────────────────────────────
改进建议:
1. 建议补充废弃物处理数据（优先级：高）
2. 建议建立供应链ESG管理体系（优先级：中）
3. 建议披露水资源管理信息（优先级：中）
═══════════════════════════════════════════════════
```

## 版本信息

- **当前版本**: 1.0.0
- **遵循标准**: 达尔文.skill 9维度评估体系
- **许可证**: MIT
- **数据源**: 集成 simonlin1212/a-stock-data (Apache License 2.0)
