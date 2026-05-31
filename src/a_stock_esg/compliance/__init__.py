"""
A股ESG合规性检查模块
基于A股监管规则引擎，自动扫描企业披露文本，标记缺失项和不符合项
包含政策匹配度分析和披露质量分析
"""

from .engine import (
    ComplianceEngine,
    ComplianceReport,
    ComplianceItem,
    ComplianceStatus,
)
from .policy import (
    ChinaValuationPolicyAnalyzer,
    PolicyMatchResult,
)
from .roe import (
    ROEAnalyzer,
    OneFiveRatioAnalyzer,
)
from .disclosure import (
    DisclosureQualityAnalyzer,
    DisclosureQualityResult,
    InformationSource,
)

__all__ = [
    # 合规检查
    "ComplianceEngine",
    "ComplianceReport",
    "ComplianceItem",
    "ComplianceStatus",
    # 政策分析
    "ChinaValuationPolicyAnalyzer",
    "PolicyMatchResult",
    # ROE分析
    "ROEAnalyzer",
    "OneFiveRatioAnalyzer",
    # 披露质量
    "DisclosureQualityAnalyzer",
    "DisclosureQualityResult",
    "InformationSource",
]
