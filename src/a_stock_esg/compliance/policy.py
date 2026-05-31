"""
中特估政策匹配度分析模块
针对A股中国特色估值体系建设，分析企业非财务信息披露与政策导向的匹配度
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class PolicyCategory(Enum):
    """政策类别"""
    SOE_REFORM = "国企改革"
    ROE_OPTIMIZATION = "ROE提升"
    DIGITAL_TRANSFORMATION = "数字化转型"
    GREEN_DEVELOPMENT = "绿色发展"
    INNOVATION_DRIVEN = "创新驱动"
    REGIONAL_DEVELOPMENT = "区域发展"
    CONSUMPTION_UPGRADE = "消费升级"
    SUPPLY_CHAIN_SECURITY = "供应链安全"


@dataclass
class PolicyIndicator:
    """政策指标"""
    indicator_id: str
    category: PolicyCategory
    name: str
    description: str
    keywords: List[str]
    weight: float = 1.0


@dataclass
class PolicyMatchResult:
    """政策匹配结果"""
    company_code: str
    company_name: str
    overall_score: float
    category_scores: Dict[str, float]
    matched_policies: List[str]
    recommendations: List[str]
    risk_flags: List[str]


class ChinaValuationPolicyAnalyzer:
    """
    中特估政策匹配度分析器
    
    分析企业非财务信息披露与"中特估"政策导向的匹配度
    """
    
    def __init__(self):
        """初始化分析器"""
        self.policy_indicators = self._load_policy_indicators()
    
    def _load_policy_indicators(self) -> List[PolicyIndicator]:
        """加载政策指标"""
        indicators = [
            # 国企改革指标
            PolicyIndicator(
                indicator_id="SOE001",
                category=PolicyCategory.SOE_REFORM,
                name="治理结构优化",
                description="董事会结构、管理层激励、股权多元化等改革措施",
                keywords=["董事会", "管理层", "股权激励", "混合所有制", "公司治理"],
                weight=1.2,
            ),
            PolicyIndicator(
                indicator_id="SOE002",
                category=PolicyCategory.SOE_REFORM,
                name="经营效率提升",
                description="一利五率指标改善、运营效率提升等",
                keywords=["ROE", "净资产收益率", "利润", "营收", "运营效率"],
                weight=1.5,
            ),
            PolicyIndicator(
                indicator_id="SOE003",
                category=PolicyCategory.SOE_REFORM,
                name="股东回报增强",
                description="分红政策、回购计划、市值管理等",
                keywords=["分红", "回购", "派息", "股东回报", "市值管理"],
                weight=1.3,
            ),
            
            # ROE提升指标
            PolicyIndicator(
                indicator_id="ROE001",
                category=PolicyCategory.ROE_OPTIMIZATION,
                name="盈利能力改善",
                description="毛利率、净利率等盈利能力指标提升",
                keywords=["毛利率", "净利率", "盈利能力", "利润增长"],
                weight=1.5,
            ),
            PolicyIndicator(
                indicator_id="ROE002",
                category=PolicyCategory.ROE_OPTIMIZATION,
                name="资产周转效率",
                description="总资产周转率、存货周转率等效率指标",
                keywords=["周转率", "资产效率", "运营效率"],
                weight=1.2,
            ),
            PolicyIndicator(
                indicator_id="ROE003",
                category=PolicyCategory.ROE_OPTIMIZATION,
                name="杠杆优化",
                description="资产负债率、财务杠杆等结构优化",
                keywords=["资产负债率", "财务杠杆", "资本结构"],
                weight=1.0,
            ),
            
            # 数字化转型指标
            PolicyIndicator(
                indicator_id="DIG001",
                category=PolicyCategory.DIGITAL_TRANSFORMATION,
                name="数字化投入",
                description="数字化转型投入、智能制造等",
                keywords=["数字化", "智能制造", "信息化", "数字化转型"],
                weight=1.0,
            ),
            PolicyIndicator(
                indicator_id="DIG002",
                category=PolicyCategory.DIGITAL_TRANSFORMATION,
                name="数据资产",
                description="数据资产管理、数据要素价值挖掘",
                keywords=["数据资产", "数据要素", "数据管理"],
                weight=0.8,
            ),
            
            # 绿色发展指标
            PolicyIndicator(
                indicator_id="GRN001",
                category=PolicyCategory.GREEN_DEVELOPMENT,
                name="碳减排",
                description="碳排放管理、碳中和目标",
                keywords=["碳排放", "碳中和", "碳达峰", "温室气体"],
                weight=1.2,
            ),
            PolicyIndicator(
                indicator_id="GRN002",
                category=PolicyCategory.GREEN_DEVELOPMENT,
                name="清洁能源",
                description="清洁能源使用、可再生能源占比",
                keywords=["清洁能源", "可再生能源", "风电", "光伏"],
                weight=1.0,
            ),
            
            # 创新驱动指标
            PolicyIndicator(
                indicator_id="INN001",
                category=PolicyCategory.INNOVATION_DRIVEN,
                name="研发投入",
                description="研发支出、研发人员占比",
                keywords=["研发投入", "研发支出", "研发人员", "技术创新"],
                weight=1.3,
            ),
            PolicyIndicator(
                indicator_id="INN002",
                category=PolicyCategory.INNOVATION_DRIVEN,
                name="知识产权",
                description="专利数量、技术成果",
                keywords=["专利", "知识产权", "技术成果", "发明专利"],
                weight=1.0,
            ),
            
            # 区域发展指标
            PolicyIndicator(
                indicator_id="REG001",
                category=PolicyCategory.REGIONAL_DEVELOPMENT,
                name="区域布局",
                description="区域发展战略响应、产业转移参与",
                keywords=["一带一路", "京津冀", "长三角", "粤港澳", "区域发展"],
                weight=0.8,
            ),
            
            # 消费升级指标
            PolicyIndicator(
                indicator_id="CON001",
                category=PolicyCategory.CONSUMPTION_UPGRADE,
                name="品牌建设",
                description="品牌价值、国货品牌、消费升级",
                keywords=["品牌", "国货", "消费升级", "品牌价值"],
                weight=0.9,
            ),
            
            # 供应链安全指标
            PolicyIndicator(
                indicator_id="SUP001",
                category=PolicyCategory.SUPPLY_CHAIN_SECURITY,
                name="自主可控",
                description="核心技术自主可控、供应链安全",
                keywords=["自主可控", "国产替代", "供应链安全", "核心自主"],
                weight=1.2,
            ),
        ]
        
        return indicators
    
    def analyze_policy_match(
        self, 
        document_text: str,
        company_code: str = "",
        company_name: str = "",
        industry: str = "",
        is_soe: bool = False,
    ) -> PolicyMatchResult:
        """
        分析政策匹配度
        
        Args:
            document_text: 企业披露文本
            company_code: 公司代码
            company_name: 公司名称
            industry: 行业
            is_soe: 是否为国有企业
            
        Returns:
            PolicyMatchResult: 政策匹配结果
        """
        # 计算各维度得分
        category_scores = {}
        matched_policies = []
        
        for indicator in self.policy_indicators:
            # 计算匹配度
            match_score = self._calculate_match_score(indicator, document_text)
            
            if match_score > 0:
                category_name = indicator.category.value
                if category_name not in category_scores:
                    category_scores[category_name] = []
                category_scores[category_name].append(match_score * indicator.weight)
                matched_policies.append(f"{indicator.name}: {match_score:.2f}")
        
        # 计算平均分
        avg_scores = {}
        for cat, scores in category_scores.items():
            avg_scores[cat] = round(sum(scores) / len(scores) * 100, 2)
        
        # 计算总分
        if avg_scores:
            overall_score = sum(avg_scores.values()) / len(avg_scores)
        else:
            overall_score = 0
        
        # 国企加分
        if is_soe:
            overall_score = min(100, overall_score * 1.1)
        
        # 生成建议
        recommendations = self._generate_recommendations(avg_scores, industry)
        
        # 生成风险提示
        risk_flags = self._identify_risks(document_text, avg_scores)
        
        return PolicyMatchResult(
            company_code=company_code,
            company_name=company_name,
            overall_score=round(overall_score, 2),
            category_scores=avg_scores,
            matched_policies=matched_policies[:10],  # 取前10个
            recommendations=recommendations,
            risk_flags=risk_flags,
        )
    
    def _calculate_match_score(
        self, 
        indicator: PolicyIndicator, 
        text: str
    ) -> float:
        """计算单个指标匹配度"""
        match_count = 0
        
        for keyword in indicator.keywords:
            if keyword in text:
                match_count += 1
        
        if match_count == 0:
            return 0.0
        
        # 匹配度 = 匹配关键词数 / 总关键词数
        return match_count / len(indicator.keywords)
    
    def _generate_recommendations(
        self, 
        scores: Dict[str, float],
        industry: str
    ) -> List[str]:
        """生成投资建议"""
        recommendations = []
        
        # 找出得分最高的维度
        if scores:
            best_category = max(scores, key=scores.get)
            recommendations.append(f"公司在{best_category}方面披露较为充分，符合政策导向")
        
        # 找出得分最低的维度
        if scores:
            worst_category = min(scores, key=scores.get)
            if scores[worst_category] < 30:
                recommendations.append(f"公司在{worst_category}方面披露不足，建议关注")
        
        # 行业特定建议
        industry_suggestions = {
            "公用事业": "建议关注清洁能源转型和碳减排进展",
            "银行": "建议关注绿色金融和普惠金融业务发展",
            "电子": "建议关注核心技术自主可控和研发投入",
            "化工": "建议关注安全生产和环保投入",
            "钢铁": "建议关注碳减排目标和节能技改项目",
            "汽车": "建议关注新能源汽车转型和智能驾驶布局",
        }
        
        if industry in industry_suggestions:
            recommendations.append(industry_suggestions[industry])
        
        return recommendations
    
    def _identify_risks(
        self, 
        text: str,
        scores: Dict[str, float]
    ) -> List[str]:
        """识别风险点"""
        risks = []
        
        # 检查是否有模糊表述
        vague_phrases = [
            "大概", "可能", "也许", "或许", "一定程度上",
            "总体而言", "一般来说", "通常情况下",
        ]
        
        for phrase in vague_phrases:
            if phrase in text:
                risks.append(f"发现模糊表述: '{phrase}'，披露不够具体")
        
        # 检查是否有夸大表述
        exaggerated_phrases = [
            "领先全球", "世界一流", "绝对领先", "遥遥领先",
            "全国第一", "行业第一", "市场第一",
        ]
        
        for phrase in exaggerated_phrases:
            if phrase in text:
                risks.append(f"发现夸大表述: '{phrase}'，需谨慎验证")
        
        # 检查政策匹配度是否过低
        if scores and sum(scores.values()) / len(scores) < 20:
            risks.append("整体政策匹配度较低，可能与中特估方向契合度不足")
        
        return risks
    
    def get_policy_summary(self) -> Dict:
        """获取政策摘要"""
        summary = {}
        
        for indicator in self.policy_indicators:
            cat_name = indicator.category.value
            if cat_name not in summary:
                summary[cat_name] = []
            summary[cat_name].append({
                "id": indicator.indicator_id,
                "name": indicator.name,
                "weight": indicator.weight,
            })
        
        return summary
