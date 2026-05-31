"""
中特估政策匹配度分析模块（前景理论优化版）
融入：
- 权重差异化（已落地政策权重更高）
- 负面语义识别（损失厌恶：负面信息权重2.5倍）
- 确定性机会/主题性机会分类
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
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


# 前景理论优化：权重差异化（已落地政策权重更高）
POLICY_WEIGHTS = {
    "国企改革": 0.20,  # 已落地考核政策，权重提升
    "ROE提升": 0.20,   # 已纳入央企考核，权重提升
    "数字化转型": 0.10,
    "绿色发展": 0.12,
    "创新驱动": 0.12,
    "区域发展": 0.08,
    "消费升级": 0.08,
    "供应链安全": 0.10,
}

# 前景理论优化：负面语义关键词（损失厌恶：负面信息权重2.5倍）
NEGATIVE_KEYWORDS = {
    "国企改革": ["暂不改革", "维持现状", "无改革计划", "暂缓推进"],
    "ROE提升": ["ROE下降", "利润下滑", "盈利能力减弱", "暂无改善"],
    "数字化转型": ["暂不转型", "维持传统模式", "无数字化计划"],
    "绿色发展": ["暂无减排目标", "碳排放增加", "环保投入下降"],
    "创新驱动": ["研发投入下降", "专利减少", "创新停滞"],
    "区域发展": ["无区域布局", "业务收缩"],
    "消费升级": ["品牌价值下降", "市场份额萎缩"],
    "供应链安全": ["供应链中断", "供应商风险"],
}

# 正面语义加分项（实际行动加分）
POSITIVE_ACTION_KEYWORDS = {
    "市值管理": ["回购", "增持", "提升分红", "股权激励", "员工持股"],
    "ROE考核": ["ROE纳入考核", "净利润考核", "经营效率考核"],
}


@dataclass
class PolicyMatchResult:
    """政策匹配结果（前景理论优化版）"""
    code: str
    name: str
    overall_score: float
    dimension_scores: Dict[str, float]
    matched: List[str]
    unmatched: List[str]
    negative_signals: List[str]  # 负面信号（损失厌恶）
    positive_actions: List[str]  # 正面实际行动
    recommendations: List[str]
    # 前景理论优化
    opportunity_type: str  # 确定性价值机会/主题性交易机会/低匹配机会
    opportunity_detail: str  # 机会详情


class PolicyAnalyzer:
    """
    中特估政策匹配度分析器（前景理论优化版）
    
    核心优化：
    1. 权重差异化 - 已落地政策权重更高
    2. 负面语义识别 - 损失厌恶，负面信息权重2.5倍
    3. 机会分类 - 确定性/主题性/低匹配
    """
    
    def __init__(self):
        pass
    
    def analyze(self, code: str, name: str, disclosure_text: str, industry: str = "") -> PolicyMatchResult:
        """
        分析政策匹配度（前景理论优化）
        
        Args:
            code: 股票代码
            name: 公司名称
            disclosure_text: 披露文本
            industry: 行业
            
        Returns:
            PolicyMatchResult: 匹配结果
        """
        text_lower = disclosure_text.lower()
        
        # 按维度计算得分（权重差异化）
        dimension_scores = {}
        negative_signals = []
        
        for dim_name, weight in POLICY_WEIGHTS.items():
            # 正面匹配
            positive_score = self._check_positive_match(dim_name, text_lower)
            
            # 负面信号检测（前景理论：损失厌恶，负面权重2.5倍）
            negative_score, negative_signal = self._check_negative_match(dim_name, text_lower)
            
            # 加权得分
            dim_score = (positive_score - negative_score * 2.5) * weight * 100
            dimension_scores[dim_name] = max(0, round(dim_score, 1))
            
            if negative_signal:
                negative_signals.append(negative_signal)
        
        # 正面实际行动检测
        positive_actions = self._check_positive_actions(text_lower)
        
        # 计算总分
        overall_score = sum(dimension_scores.values())
        
        # 识别匹配/未匹配维度
        matched = [dim for dim, score in dimension_scores.items() if score > 10]
        unmatched = [dim for dim, score in dimension_scores.items() if score <= 10]
        
        # 机会分类（前景理论）
        opportunity_type, opportunity_detail = self._classify_opportunity(
            overall_score, negative_signals, positive_actions
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            overall_score, matched, unmatched, negative_signals, positive_actions, industry
        )
        
        return PolicyMatchResult(
            code=code,
            name=name,
            overall_score=round(overall_score, 1),
            dimension_scores=dimension_scores,
            matched=matched,
            unmatched=unmatched,
            negative_signals=negative_signals,
            positive_actions=positive_actions,
            recommendations=recommendations,
            opportunity_type=opportunity_type,
            opportunity_detail=opportunity_detail,
        )
    
    def _check_positive_match(self, dimension: str, text: str) -> float:
        """检查正面匹配"""
        keywords = {
            "国企改革": ["改革", "治理", "股权激励", "混改", "董事会"],
            "ROE提升": ["ROE", "利润", "盈利", "分红", "回报"],
            "数字化转型": ["数字化", "智能制造", "信息化", "工业互联网"],
            "绿色发展": ["碳中和", "碳达峰", "清洁能源", "环保"],
            "创新驱动": ["研发", "专利", "创新", "技术"],
            "区域发展": ["一带一路", "长三角", "粤港澳", "区域"],
            "消费升级": ["品牌", "国货", "消费升级"],
            "供应链安全": ["自主可控", "国产替代", "供应链"],
        }
        
        kw_list = keywords.get(dimension, [])
        if not kw_list:
            return 0
        
        match_count = sum(1 for kw in kw_list if kw in text)
        return match_count / len(kw_list)
    
    def _check_negative_match(self, dimension: str, text: str) -> Tuple[float, str]:
        """检查负面信号（前景理论：损失厌恶）"""
        negative_kws = NEGATIVE_KEYWORDS.get(dimension, [])
        
        for kw in negative_kws:
            if kw in text:
                return 1.0, f"{dimension}: {kw}"
        
        return 0.0, ""
    
    def _check_positive_actions(self, text: str) -> List[str]:
        """检查正面实际行动"""
        actions = []
        
        for category, keywords in POSITIVE_ACTION_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    actions.append(f"{category}: {kw}")
        
        return actions
    
    def _classify_opportunity(
        self, 
        score: float, 
        negative_signals: List[str], 
        positive_actions: List[str]
    ) -> Tuple[str, str]:
        """
        分类机会类型（前景理论）
        
        核心逻辑：
        - ≥80分 + 无负面信号 + 有正面行动 → 确定性价值机会
        - 60-80分 → 主题性交易机会
        - <60分 → 低匹配机会
        """
        has_negative = len(negative_signals) > 0
        has_actions = len(positive_actions) > 0
        
        if score >= 80 and not has_negative and has_actions:
            return "确定性价值机会", "高匹配度，政策催化明确，具备业绩+估值双升基础"
        elif score >= 60:
            if has_negative:
                return "主题性交易机会", "政策方向符合，但存在负面信号，波动风险较高"
            else:
                return "主题性交易机会", "政策方向符合，存在主题催化机会，但基本面改善尚未落地"
        else:
            return "低匹配机会", "政策匹配度较低，建议关注其他标的"
    
    def _generate_recommendations(
        self, 
        score: float, 
        matched: List[str], 
        unmatched: List[str],
        negative_signals: List[str],
        positive_actions: List[str],
        industry: str
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 优势
        if matched:
            recommendations.append(f"优势维度: {', '.join(matched[:3])}")
        
        # 劣势
        if unmatched:
            recommendations.append(f"建议加强: {', '.join(unmatched[:3])}")
        
        # 负面信号（损失厌恶：提前披露）
        if negative_signals:
            recommendations.append(f"⚠️ 负面信号: {', '.join(negative_signals[:2])}")
        
        # 正面行动
        if positive_actions:
            recommendations.append(f"✅ 正面行动: {', '.join(positive_actions[:2])}")
        
        # 行业建议
        industry_tips = {
            "电力": "建议关注清洁能源转型和碳减排进展",
            "银行": "建议关注绿色金融和数字化转型",
            "白酒": "建议关注品牌价值和渠道建设",
        }
        if industry in industry_tips:
            recommendations.append(industry_tips[industry])
        
        return recommendations if recommendations else ["继续保持现有披露策略"]
