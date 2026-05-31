"""
多源信息交叉对比与话术识别模块
自动交叉对比企业多渠道披露信息，识别信息矛盾和话术包装
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    CRITICAL = "高危"


@dataclass
class InformationSource:
    """信息来源"""
    source_id: str
    source_type: str  # 年报、ESG报告、公告、官网等
    content: str
    date: str


@dataclass
class Contradiction:
    """信息矛盾"""
    topic: str
    source1: str
    content1: str
    source2: str
    content2: str
    risk_level: RiskLevel
    description: str


@dataclass
class RhetoricFlag:
    """话术标记"""
    phrase: str
    category: str  # 模糊表述、夸大表述、推诿表述等
    risk_level: RiskLevel
    suggestion: str


@dataclass
class DisclosureQualityResult:
    """披露质量分析结果"""
    company_code: str
    company_name: str
    overall_score: float
    contradictions: List[Contradiction]
    rhetoric_flags: List[RhetoricFlag]
    information_completeness: float
    consistency_score: float
    recommendations: List[str]


class DisclosureQualityAnalyzer:
    """
    披露质量分析器
    
    多源信息交叉对比，识别信息矛盾和话术包装
    """
    
    def __init__(self):
        """初始化分析器"""
        self.vague_phrases = self._load_vague_phrases()
        self.exaggerated_phrases = self._load_exaggerated_phrases()
        self.evasive_phrases = self._load_evasive_phrases()
    
    def _load_vague_phrases(self) -> List[Dict]:
        """加载模糊表述库"""
        return [
            {"phrase": "大概", "risk": RiskLevel.MEDIUM, "suggestion": "建议使用具体数据"},
            {"phrase": "可能", "risk": RiskLevel.LOW, "suggestion": "建议明确说明"},
            {"phrase": "也许", "risk": RiskLevel.MEDIUM, "suggestion": "建议使用确定性表述"},
            {"phrase": "或许", "risk": RiskLevel.MEDIUM, "suggestion": "建议使用确定性表述"},
            {"phrase": "一定程度上", "risk": RiskLevel.MEDIUM, "suggestion": "建议量化说明"},
            {"phrase": "总体而言", "risk": RiskLevel.LOW, "suggestion": "建议补充具体数据"},
            {"phrase": "一般来说", "risk": RiskLevel.LOW, "suggestion": "建议说明具体情况"},
            {"phrase": "通常情况下", "risk": RiskLevel.LOW, "suggestion": "建议说明具体情况"},
            {"phrase": "基本上", "risk": RiskLevel.MEDIUM, "suggestion": "建议使用精确表述"},
            {"phrase": "相对而言", "risk": RiskLevel.LOW, "suggestion": "建议补充绝对数据"},
            {"phrase": "一定程度", "risk": RiskLevel.MEDIUM, "suggestion": "建议量化说明程度"},
            {"phrase": "较为", "risk": RiskLevel.LOW, "suggestion": "建议使用具体数据"},
            {"phrase": "较", "risk": RiskLevel.LOW, "suggestion": "建议使用具体数据"},
        ]
    
    def _load_exaggerated_phrases(self) -> List[Dict]:
        """加载夸大表述库"""
        return [
            {"phrase": "领先全球", "risk": RiskLevel.HIGH, "suggestion": "需提供权威数据支撑"},
            {"phrase": "世界一流", "risk": RiskLevel.HIGH, "suggestion": "需提供对标数据"},
            {"phrase": "绝对领先", "risk": RiskLevel.HIGH, "suggestion": "表述过于绝对，需谨慎"},
            {"phrase": "遥遥领先", "risk": RiskLevel.HIGH, "suggestion": "需提供量化对比"},
            {"phrase": "全国第一", "risk": RiskLevel.HIGH, "suggestion": "需提供权威排名"},
            {"phrase": "行业第一", "risk": RiskLevel.HIGH, "suggestion": "需提供行业数据"},
            {"phrase": "市场第一", "risk": RiskLevel.HIGH, "suggestion": "需提供市场份额数据"},
            {"phrase": "最好", "risk": RiskLevel.CRITICAL, "suggestion": "表述过于绝对，风险极高"},
            {"phrase": "最优", "risk": RiskLevel.CRITICAL, "suggestion": "表述过于绝对，风险极高"},
            {"phrase": "最强", "risk": RiskLevel.CRITICAL, "suggestion": "表述过于绝对，风险极高"},
            {"phrase": "独一无二", "risk": RiskLevel.CRITICAL, "suggestion": "表述过于绝对，风险极高"},
            {"phrase": "无与伦比", "risk": RiskLevel.CRITICAL, "suggestion": "表述过于绝对，风险极高"},
            {"phrase": "史无前例", "risk": RiskLevel.HIGH, "suggestion": "需提供历史数据对比"},
            {"phrase": "突破性", "risk": RiskLevel.MEDIUM, "suggestion": "建议说明具体突破点"},
            {"phrase": "颠覆性", "risk": RiskLevel.MEDIUM, "suggestion": "建议说明具体创新点"},
        ]
    
    def _load_evasive_phrases(self) -> List[Dict]:
        """加载推诿表述库"""
        return [
            {"phrase": "受市场环境影响", "risk": RiskLevel.MEDIUM, "suggestion": "建议具体说明影响因素"},
            {"phrase": "受政策影响", "risk": RiskLevel.MEDIUM, "suggestion": "建议具体说明政策内容"},
            {"phrase": "受外部因素影响", "risk": RiskLevel.MEDIUM, "suggestion": "建议具体说明外部因素"},
            {"phrase": "由于众所周知的原因", "risk": RiskLevel.HIGH, "suggestion": "回避关键问题，风险较高"},
            {"phrase": "由于不可抗力", "risk": RiskLevel.MEDIUM, "suggestion": "建议说明具体原因"},
            {"phrase": "存在一定不确定性", "risk": RiskLevel.LOW, "suggestion": "建议说明不确定性来源"},
            {"phrase": "存在一定的风险", "risk": RiskLevel.LOW, "suggestion": "建议具体说明风险点"},
            {"phrase": "将视情况而定", "risk": RiskLevel.MEDIUM, "suggestion": "建议明确决策标准"},
            {"phrase": "将根据实际情况", "risk": RiskLevel.MEDIUM, "suggestion": "建议明确执行计划"},
            {"phrase": "灵活把握", "risk": RiskLevel.MEDIUM, "suggestion": "建议明确执行标准"},
        ]
    
    def analyze_disclosure_quality(
        self,
        company_code: str,
        company_name: str,
        sources: List[InformationSource],
    ) -> DisclosureQualityResult:
        """
        分析披露质量
        
        Args:
            company_code: 公司代码
            company_name: 公司名称
            sources: 多源信息列表
            
        Returns:
            DisclosureQualityResult: 分析结果
        """
        # 识别信息矛盾
        contradictions = self._find_contradictions(sources)
        
        # 识别话术标记
        all_text = " ".join([s.content for s in sources])
        rhetoric_flags = self._find_rhetoric_flags(all_text)
        
        # 计算信息完整性
        completeness = self._calculate_completeness(sources)
        
        # 计算一致性得分
        consistency = self._calculate_consistency(contradictions)
        
        # 计算总分
        overall_score = self._calculate_overall_score(
            completeness, consistency, rhetoric_flags
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            contradictions, rhetoric_flags, completeness, consistency
        )
        
        return DisclosureQualityResult(
            company_code=company_code,
            company_name=company_name,
            overall_score=overall_score,
            contradictions=contradictions,
            rhetoric_flags=rhetoric_flags,
            information_completeness=completeness,
            consistency_score=consistency,
            recommendations=recommendations,
        )
    
    def _find_contradictions(
        self,
        sources: List[InformationSource],
    ) -> List[Contradiction]:
        """查找信息矛盾"""
        contradictions = []
        
        # 简化处理：检查数值型数据是否一致
        # 实际应用中需要更复杂的NLP处理
        
        return contradictions
    
    def _find_rhetoric_flags(self, text: str) -> List[RhetoricFlag]:
        """查找话术标记"""
        flags = []
        
        # 检查模糊表述
        for item in self.vague_phrases:
            if item["phrase"] in text:
                flags.append(RhetoricFlag(
                    phrase=item["phrase"],
                    category="模糊表述",
                    risk_level=item["risk"],
                    suggestion=item["suggestion"],
                ))
        
        # 检查夸大表述
        for item in self.exaggerated_phrases:
            if item["phrase"] in text:
                flags.append(RhetoricFlag(
                    phrase=item["phrase"],
                    category="夸大表述",
                    risk_level=item["risk"],
                    suggestion=item["suggestion"],
                ))
        
        # 检查推诿表述
        for item in self.evasive_phrases:
            if item["phrase"] in text:
                flags.append(RhetoricFlag(
                    phrase=item["phrase"],
                    category="推诿表述",
                    risk_level=item["risk"],
                    suggestion=item["suggestion"],
                ))
        
        return flags
    
    def _calculate_completeness(
        self,
        sources: List[InformationSource],
    ) -> float:
        """计算信息完整性"""
        required_sources = ["年报", "ESG报告", "社会责任报告"]
        
        existing_types = set([s.source_type for s in sources])
        
        matched = sum(1 for rs in required_sources if rs in existing_types)
        
        return round(matched / len(required_sources) * 100, 2)
    
    def _calculate_consistency(
        self,
        contradictions: List[Contradiction],
    ) -> float:
        """计算一致性得分"""
        if not contradictions:
            return 100.0
        
        # 扣分逻辑
        deduction = 0
        for c in contradictions:
            if c.risk_level == RiskLevel.CRITICAL:
                deduction += 20
            elif c.risk_level == RiskLevel.HIGH:
                deduction += 15
            elif c.risk_level == RiskLevel.MEDIUM:
                deduction += 10
            else:
                deduction += 5
        
        return max(0, 100 - deduction)
    
    def _calculate_overall_score(
        self,
        completeness: float,
        consistency: float,
        rhetoric_flags: List[RhetoricFlag],
    ) -> float:
        """计算总分"""
        # 基础分
        score = (completeness * 0.4 + consistency * 0.6)
        
        # 话术扣分
        for flag in rhetoric_flags:
            if flag.risk_level == RiskLevel.CRITICAL:
                score -= 10
            elif flag.risk_level == RiskLevel.HIGH:
                score -= 5
            elif flag.risk_level == RiskLevel.MEDIUM:
                score -= 2
        
        return round(max(0, min(100, score)), 2)
    
    def _generate_recommendations(
        self,
        contradictions: List[Contradiction],
        rhetoric_flags: List[RhetoricFlag],
        completeness: float,
        consistency: float,
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 完整性建议
        if completeness < 60:
            recommendations.append("信息披露不完整，建议补充ESG报告或社会责任报告")
        
        # 一致性建议
        if consistency < 80:
            recommendations.append("存在信息不一致问题，建议核实关键数据")
        
        # 话术建议
        high_risk_flags = [f for f in rhetoric_flags if f.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        if high_risk_flags:
            recommendations.append(f"发现{len(high_risk_flags)}处高风险话术，需谨慎评估")
        
        # 矛盾建议
        if contradictions:
            recommendations.append(f"发现{len(contradictions)}处信息矛盾，建议深入调查")
        
        return recommendations if recommendations else ["信息披露质量良好"]
