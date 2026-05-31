"""
中特估政策匹配度分析模块
基于多维度语义理解，评估企业与中特估政策的契合度
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class PolicyDimension(Enum):
    """政策维度"""
    SOE_REFORM = "国企改革"
    ROE_IMPROVEMENT = "ROE提升"
    DIGITAL_TRANS = "数字化转型"
    GREEN_DEVELOP = "绿色发展"
    INNOVATION = "创新驱动"
    REGIONAL_DEV = "区域发展"
    CONSUMPTION = "消费升级"
    SUPPLY_CHAIN = "供应链安全"


@dataclass
class PolicyMatchResult:
    """政策匹配结果"""
    code: str
    name: str
    overall_score: float
    dimension_scores: Dict[str, float]
    matched: List[str]
    unmatched: List[str]
    evidence: Dict[str, List[str]]
    recommendations: List[str]


# 政策指标配置
POLICY_INDICATORS = {
    PolicyDimension.SOE_REFORM: {
        "weight": 1.5,
        "indicators": [
            {"name": "治理结构", "keywords": ["董事会", "管理层", "股权激励", "公司治理", "独立董事"]},
            {"name": "经营效率", "keywords": ["ROE", "利润增长", "营收增长", "运营效率", "降本增效"]},
            {"name": "股东回报", "keywords": ["分红", "回购", "派息", "股东回报", "市值管理"]},
        ],
    },
    PolicyDimension.ROE_IMPROVEMENT: {
        "weight": 1.5,
        "indicators": [
            {"name": "盈利能力", "keywords": ["毛利率", "净利率", "盈利", "利润"]},
            {"name": "资产效率", "keywords": ["周转率", "资产效率", "运营效率"]},
            {"name": "资本结构", "keywords": ["资产负债率", "财务杠杆", "资本结构"]},
        ],
    },
    PolicyDimension.DIGITAL_TRANS: {
        "weight": 1.0,
        "indicators": [
            {"name": "数字化投入", "keywords": ["数字化", "智能制造", "信息化", "工业互联网"]},
            {"name": "数据资产", "keywords": ["数据资产", "数据要素", "数据管理"]},
        ],
    },
    PolicyDimension.GREEN_DEVELOP: {
        "weight": 1.2,
        "indicators": [
            {"name": "碳减排", "keywords": ["碳排放", "碳中和", "碳达峰", "温室气体", "低碳"]},
            {"name": "清洁能源", "keywords": ["清洁能源", "可再生能源", "风电", "光伏", "新能源"]},
            {"name": "环保投入", "keywords": ["环保投入", "污染治理", "废弃物"]},
        ],
    },
    PolicyDimension.INNOVATION: {
        "weight": 1.3,
        "indicators": [
            {"name": "研发投入", "keywords": ["研发投入", "研发支出", "研发人员", "技术创新"]},
            {"name": "知识产权", "keywords": ["专利", "知识产权", "技术成果", "发明专利"]},
            {"name": "技术突破", "keywords": ["突破", "自主可控", "国产替代", "核心技术"]},
        ],
    },
    PolicyDimension.REGIONAL_DEV: {
        "weight": 0.8,
        "indicators": [
            {"name": "区域布局", "keywords": ["一带一路", "京津冀", "长三角", "粤港澳"]},
            {"name": "乡村振兴", "keywords": ["乡村振兴", "扶贫", "共同富裕"]},
        ],
    },
    PolicyDimension.CONSUMPTION: {
        "weight": 0.9,
        "indicators": [
            {"name": "品牌建设", "keywords": ["品牌", "国货", "消费升级", "民族品牌"]},
            {"name": "产品质量", "keywords": ["质量", "品质", "标准", "认证"]},
        ],
    },
    PolicyDimension.SUPPLY_CHAIN: {
        "weight": 1.1,
        "indicators": [
            {"name": "自主可控", "keywords": ["自主可控", "国产替代", "供应链安全", "核心自主"]},
            {"name": "产业链整合", "keywords": ["产业链", "供应链", "上下游", "产业协同"]},
        ],
    },
}


class PolicyAnalyzer:
    """
    中特估政策匹配度分析器
    
    基于多维度语义理解，评估企业与中特估政策的契合度
    """
    
    def __init__(self):
        pass
    
    def analyze(self, code: str, name: str, disclosure_text: str, industry: str = "") -> PolicyMatchResult:
        """
        分析政策匹配度
        
        Args:
            code: 股票代码
            name: 公司名称
            disclosure_text: 披露文本
            industry: 行业
            
        Returns:
            PolicyMatchResult: 匹配结果
        """
        text_lower = disclosure_text.lower()
        
        # 按维度计算得分
        dimension_scores = {}
        evidence = {}
        
        for dim, config in POLICY_INDICATORS.items():
            dim_name = dim.value
            dim_score = 0
            dim_evidence = []
            
            for indicator in config["indicators"]:
                # 计算匹配度
                matched_kws = [kw for kw in indicator["keywords"] if kw in text_lower]
                if indicator["keywords"]:
                    match_ratio = len(matched_kws) / len(indicator["keywords"])
                else:
                    match_ratio = 0
                
                # 加权得分
                indicator_score = match_ratio * 100
                dim_score += indicator_score
                
                if matched_kws:
                    dim_evidence.append(f"{indicator['name']}: {', '.join(matched_kws[:3])}")
            
            # 维度平均分
            indicator_count = len(config["indicators"])
            dimension_scores[dim_name] = round(dim_score / indicator_count * config["weight"], 1) if indicator_count > 0 else 0
            evidence[dim_name] = dim_evidence
        
        # 计算总分
        total_weight = sum(c["weight"] for c in POLICY_INDICATORS.values())
        overall_score = sum(
            score / c["weight"] * c["weight"] 
            for (dim, score), c in zip(dimension_scores.items(), POLICY_INDICATORS.values())
        ) / total_weight if total_weight > 0 else 0
        
        # 识别匹配/未匹配维度
        matched = [dim for dim, score in dimension_scores.items() if score > 30]
        unmatched = [dim for dim, score in dimension_scores.items() if score <= 30]
        
        # 生成建议
        recommendations = self._generate_recommendations(dimension_scores, matched, unmatched, industry)
        
        return PolicyMatchResult(
            code=code,
            name=name,
            overall_score=round(overall_score, 1),
            dimension_scores=dimension_scores,
            matched=matched,
            unmatched=unmatched,
            evidence=evidence,
            recommendations=recommendations,
        )
    
    def _generate_recommendations(self, dimension_scores, matched, unmatched, industry):
        """生成建议"""
        recommendations = []
        
        if matched:
            recommendations.append(f"优势维度: {', '.join(matched)}")
        
        if unmatched:
            recommendations.append(f"建议加强: {', '.join(unmatched)}")
        
        industry_tips = {
            "电力": "建议重点披露清洁能源转型、碳减排进展",
            "银行": "建议重点披露绿色金融、普惠金融",
            "白酒": "建议重点披露品牌价值、产品质量",
            "电子": "建议重点披露核心技术自主可控、研发投入",
        }
        if industry in industry_tips:
            recommendations.append(industry_tips[industry])
        
        return recommendations if recommendations else ["继续保持现有披露策略"]
