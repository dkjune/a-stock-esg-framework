"""
政策匹配度分析模块（噪声优化版）
基于《噪声》理论：
- 通用化二进制计分（规则替代直觉）
- 双模型校验（独立验证）
- 决策卫生清单
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# 通用化政策维度（适用于所有A股）
# ═══════════════════════════════════════════════════════════════════════════

POLICY_DIMENSIONS = {
    "治理激励": {
        "description": "股权激励、高管增持、员工持股等",
        "rules": [
            {"id": "G1", "keyword": "股权激励", "weight": 1},
            {"id": "G2", "keyword": "高管增持", "weight": 1},
            {"id": "G3", "keyword": "员工持股", "weight": 1},
            {"id": "G4", "keyword": "回购", "weight": 1},
        ]
    },
    "盈利质量": {
        "description": "自由现金流、净利润质量等",
        "rules": [
            {"id": "P1", "keyword": "自由现金流", "weight": 1},
            {"id": "P2", "keyword": "净利润增长", "weight": 1},
            {"id": "P3", "keyword": "ROE提升", "weight": 1},
            {"id": "P4", "keyword": "分红", "weight": 1},
        ]
    },
    "技术投入": {
        "description": "研发强度、专利、数字化等",
        "rules": [
            {"id": "T1", "keyword": "研发投入", "weight": 1},
            {"id": "T2", "keyword": "专利", "weight": 1},
            {"id": "T3", "keyword": "数字化", "weight": 1},
            {"id": "T4", "keyword": "智能制造", "weight": 1},
        ]
    },
    "绿色发展": {
        "description": "碳排放、环保投入等",
        "rules": [
            {"id": "E1", "keyword": "碳排放", "weight": 1},
            {"id": "E2", "keyword": "碳中和", "weight": 1},
            {"id": "E3", "keyword": "清洁能源", "weight": 1},
            {"id": "E4", "keyword": "环保投入", "weight": 1},
        ]
    },
    "创新驱动": {
        "description": "研发强度、专利增速等",
        "rules": [
            {"id": "I1", "keyword": "研发强度", "weight": 1},
            {"id": "I2", "keyword": "专利增速", "weight": 1},
            {"id": "I3", "keyword": "创新", "weight": 1},
        ]
    },
    "区域布局": {
        "description": "营收区域集中度、区域风险",
        "rules": [
            {"id": "R1", "keyword": "区域", "weight": 1},
            {"id": "R2", "keyword": "全国布局", "weight": 1},
            {"id": "R3", "keyword": "国际化", "weight": 1},
        ]
    },
    "消费升级": {
        "description": "产品单价、高端线占比",
        "rules": [
            {"id": "C1", "keyword": "品牌", "weight": 1},
            {"id": "C2", "keyword": "高端", "weight": 1},
            {"id": "C3", "keyword": "消费升级", "weight": 1},
        ]
    },
    "供应链安全": {
        "description": "客户/供应商集中度",
        "rules": [
            {"id": "S1", "keyword": "供应链", "weight": 1},
            {"id": "S2", "keyword": "自主可控", "weight": 1},
            {"id": "S3", "keyword": "国产替代", "weight": 1},
        ]
    },
}

# 负面信号关键词（噪声优化：损失厌恶）
NEGATIVE_SIGNALS = [
    "暂不", "暂缓", "无计划", "维持现状", "下降", "减少", "下滑",
    "风险", "亏损", "违规", "处罚", "诉讼",
]


@dataclass
class PolicyMatchResult:
    """政策匹配结果（噪声优化版）"""
    code: str
    name: str
    overall_score: float
    dimension_scores: Dict[str, float]
    matched_dimensions: List[str]
    unmatched_dimensions: List[str]
    negative_signals: List[str]
    positive_actions: List[str]
    # 双模型校验
    model_a_score: float
    model_b_score: float
    model_agreement: float  # 一致性（Cohen's Kappa简化版）
    # 置信度
    confidence: str  # 高/中/低
    confidence_note: str
    # 机会分类
    opportunity_type: str
    opportunity_detail: str
    recommendations: List[str]


class PolicyAnalyzer:
    """
    政策匹配度分析器（噪声优化版）
    
    基于《噪声》理论：
    1. 通用化二进制计分（规则替代直觉）
    2. 双模型校验（独立验证）
    3. 决策卫生清单
    """
    
    def __init__(self):
        pass
    
    def analyze(self, code: str, name: str, disclosure_text: str, industry: str = "") -> PolicyMatchResult:
        """
        分析政策匹配度（噪声优化版）
        """
        text_lower = disclosure_text.lower()
        
        # 模型A：关键词计分
        score_a, matched_a, negative_a, positive_a = self._score_by_keywords(text_lower)
        
        # 模型B：规则计分（二进制）
        score_b, matched_b = self._score_by_rules(text_lower)
        
        # 双模型一致性
        agreement = 1 - abs(score_a - score_b) / max(score_a, score_b, 1)
        
        # 综合得分（取均值）
        overall_score = (score_a + score_b) / 2
        
        # 匹配/未匹配维度
        matched = list(set(matched_a + matched_b))
        unmatched = [dim for dim in POLICY_DIMENSIONS.keys() if dim not in matched]
        
        # 负面信号检测
        negative_signals = self._detect_negative_signals(text_lower)
        
        # 正面实际行动
        positive_actions = self._detect_positive_actions(text_lower)
        
        # 置信度评估
        confidence, confidence_note = self._assess_confidence(
            agreement, len(negative_signals), len(positive_actions)
        )
        
        # 机会分类
        opportunity_type, opportunity_detail = self._classify_opportunity(
            overall_score, negative_signals, positive_actions, confidence
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            overall_score, matched, unmatched, negative_signals, positive_actions, confidence
        )
        
        return PolicyMatchResult(
            code=code,
            name=name,
            overall_score=round(overall_score, 1),
            dimension_scores={},  # 简化：不输出维度详情
            matched_dimensions=matched,
            unmatched_dimensions=unmatched,
            negative_signals=negative_signals,
            positive_actions=positive_actions,
            model_a_score=round(score_a, 1),
            model_b_score=round(score_b, 1),
            model_agreement=round(agreement * 100, 1),
            confidence=confidence,
            confidence_note=confidence_note,
            opportunity_type=opportunity_type,
            opportunity_detail=opportunity_detail,
            recommendations=recommendations,
        )
    
    def _score_by_keywords(self, text: str) -> Tuple[float, List[str], List[str], List[str]]:
        """模型A：关键词计分"""
        score = 0
        matched = []
        negative = []
        positive = []
        
        for dim_name, dim_config in POLICY_DIMENSIONS.items():
            for rule in dim_config["rules"]:
                if rule["keyword"] in text:
                    score += rule["weight"]
                    matched.append(dim_name)
                    
                    # 检查是否有负面信号
                    if any(neg in text for neg in NEGATIVE_SIGNALS):
                        # 如果关键词附近有负面信号，扣分
                        negative.append(f"{dim_name}: {rule['keyword']}")
                    else:
                        positive.append(f"{dim_name}: {rule['keyword']}")
        
        return score, list(set(matched)), negative, positive
    
    def _score_by_rules(self, text: str) -> Tuple[float, List[str]]:
        """模型B：规则计分（二进制）"""
        score = 0
        matched = []
        
        # 简化的二进制规则
        rules = [
            ("治理激励", ["股权激励", "高管增持", "员工持股"]),
            ("盈利质量", ["净利润增长", "ROE提升", "分红"]),
            ("技术投入", ["研发投入", "专利", "数字化"]),
            ("绿色发展", ["碳中和", "清洁能源", "环保投入"]),
            ("创新驱动", ["创新", "研发强度"]),
            ("区域布局", ["全国布局", "国际化"]),
            ("消费升级", ["品牌", "高端"]),
            ("供应链安全", ["自主可控", "国产替代"]),
        ]
        
        for dim_name, keywords in rules:
            if any(kw in text for kw in keywords):
                score += 1
                matched.append(dim_name)
        
        return score, matched
    
    def _detect_negative_signals(self, text: str) -> List[str]:
        """检测负面信号（损失厌恶）"""
        signals = []
        
        for neg in NEGATIVE_SIGNALS:
            if neg in text:
                signals.append(neg)
        
        return signals
    
    def _detect_positive_actions(self, text: str) -> List[str]:
        """检测正面实际行动"""
        actions = []
        
        action_keywords = ["回购", "增持", "提升分红", "股权激励", "员工持股"]
        for kw in action_keywords:
            if kw in text:
                actions.append(kw)
        
        return actions
    
    def _assess_confidence(self, agreement: float, negative_count: int, positive_count: int) -> Tuple[str, str]:
        """评估置信度"""
        if agreement > 0.8 and negative_count == 0 and positive_count > 0:
            return "高", "双模型一致，无负面信号，有正面行动"
        elif agreement > 0.6:
            return "中", "双模型基本一致"
        else:
            return "低", "双模型不一致，建议人工复核"
    
    def _classify_opportunity(
        self, 
        score: float, 
        negative_signals: List[str], 
        positive_actions: List[str],
        confidence: str
    ) -> Tuple[str, str]:
        """分类机会类型"""
        has_negative = len(negative_signals) > 0
        has_actions = len(positive_actions) > 0
        
        if score >= 5 and not has_negative and has_actions and confidence == "高":
            return "确定性价值机会", "高匹配度，政策催化明确，具备业绩+估值双升基础"
        elif score >= 3:
            if has_negative:
                return "主题性交易机会", "政策方向符合，但存在负面信号，波动风险较高"
            else:
                return "主题性交易机会", "政策方向符合，存在主题催化机会"
        else:
            return "低匹配机会", "政策匹配度较低，建议关注其他标的"
    
    def _generate_recommendations(self, score, matched, unmatched, negative_signals, positive_actions, confidence) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if matched:
            recommendations.append(f"匹配维度: {', '.join(matched[:3])}")
        
        if negative_signals:
            recommendations.append(f"⚠️ 负面信号: {', '.join(negative_signals[:2])}")
        
        if positive_actions:
            recommendations.append(f"✅ 正面行动: {', '.join(positive_actions[:2])}")
        
        if confidence == "低":
            recommendations.append("⚠️ 评分置信度较低，建议人工复核")
        
        return recommendations if recommendations else ["建议关注基本面变化"]
