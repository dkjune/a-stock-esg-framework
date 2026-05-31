"""
A股适配版富士通AI分析逻辑框架
针对A股ESG披露的监管要求和企业痛点的智能分析系统
支持中国特色估值体系（中特估）投资分析
"""

__version__ = "2.0.0"
__author__ = "A-Stock ESG Team"

from .core.config import AStockESGConfig
from .compliance.engine import ComplianceEngine
from .data.collector import DataCollector
from .data.parser import DocumentParser
from .data.astock_integration import AStockDataIntegrator, ESGDataPipeline
from .nlp.processor import NLPProcessor
from .visualization.benchmark import BenchmarkAnalyzer
from .visualization.visualizer import Visualizer
from .knowledge_graph.graph import KnowledgeGraph

# 中特估政策分析模块
from .policy.china_valuation import ChinaValuationPolicyAnalyzer, PolicyMatchResult
from .policy.roe_analyzer import ROEAnalyzer, OneFiveRatioAnalyzer

# 风险分析模块
from .risk.disclosure_quality import DisclosureQualityAnalyzer, DisclosureQualityResult

# 投资分析模块
from .investment.personal_scorer import PersonalInvestorScorer, StockFactorGenerator

__all__ = [
    # 核心模块
    "AStockESGConfig",
    "ComplianceEngine",
    "DataCollector",
    "DocumentParser",
    "AStockDataIntegrator",
    "ESGDataPipeline",
    "NLPProcessor",
    "BenchmarkAnalyzer",
    "Visualizer",
    "KnowledgeGraph",
    # 中特估分析模块
    "ChinaValuationPolicyAnalyzer",
    "PolicyMatchResult",
    "ROEAnalyzer",
    "OneFiveRatioAnalyzer",
    # 风险分析模块
    "DisclosureQualityAnalyzer",
    "DisclosureQualityResult",
    # 投资分析模块
    "PersonalInvestorScorer",
    "StockFactorGenerator",
]
