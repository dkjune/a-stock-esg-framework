"""
A股适配版富士通AI分析逻辑框架
针对A股ESG披露的监管要求和企业痛点的智能分析系统
支持中国特色估值体系（中特估）投资分析
"""

__version__ = "2.0.0"
__author__ = "A-Stock ESG Team"

# 核心配置
from .core.config import AStockESGConfig

# 合规检查（包含政策分析、风险分析）
from .compliance import (
    ComplianceEngine,
    ComplianceReport,
    ComplianceItem,
    ComplianceStatus,
    ChinaValuationPolicyAnalyzer,
    PolicyMatchResult,
    ROEAnalyzer,
    OneFiveRatioAnalyzer,
    DisclosureQualityAnalyzer,
    DisclosureQualityResult,
    InformationSource,
)

# 数据源
from .data.collector import DataCollector
from .data.parser import DocumentParser
from .data.astock_integration import AStockDataIntegrator, ESGDataPipeline

# NLP处理
from .nlp.processor import NLPProcessor

# 可视化与投资分析
from .visualization import (
    BenchmarkAnalyzer,
    BenchmarkComparison,
    DifferentiationSuggestion,
    Visualizer,
    DashboardConfig,
    PersonalInvestorScorer,
    StockFactorGenerator,
    StockScore,
    ScoringResult,
)

# 知识图谱
from .knowledge_graph.graph import KnowledgeGraph

__all__ = [
    # 核心配置
    "AStockESGConfig",
    # 合规检查
    "ComplianceEngine",
    "ComplianceReport",
    "ComplianceItem",
    "ComplianceStatus",
    # 政策分析
    "ChinaValuationPolicyAnalyzer",
    "PolicyMatchResult",
    "ROEAnalyzer",
    "OneFiveRatioAnalyzer",
    # 风险分析
    "DisclosureQualityAnalyzer",
    "DisclosureQualityResult",
    "InformationSource",
    # 数据源
    "DataCollector",
    "DocumentParser",
    "AStockDataIntegrator",
    "ESGDataPipeline",
    # NLP处理
    "NLPProcessor",
    # 可视化
    "BenchmarkAnalyzer",
    "BenchmarkComparison",
    "DifferentiationSuggestion",
    "Visualizer",
    "DashboardConfig",
    # 投资分析
    "PersonalInvestorScorer",
    "StockFactorGenerator",
    "StockScore",
    "ScoringResult",
    # 知识图谱
    "KnowledgeGraph",
]
