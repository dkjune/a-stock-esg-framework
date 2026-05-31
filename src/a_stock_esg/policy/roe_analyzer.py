"""
ROE核心指标分析模块
分析企业ROE变动驱动因素，验证中特估政策效果
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ROEDriver(Enum):
    """ROE驱动因素"""
    PROFIT_MARGIN = "利润率"
    ASSET_TURNOVER = "资产周转率"
    LEVERAGE = "财务杠杆"
    TAX_EFFICIENCY = "税收效率"
    INTEREST_COST = "利息成本"


@dataclass
class ROEComponent:
    """ROE组成部分"""
    driver: ROEDriver
    name: str
    current_value: float
    previous_value: float
    change: float
    contribution_to_roe: float


@dataclass
class ROEAnalysisResult:
    """ROE分析结果"""
    company_code: str
    company_name: str
    current_roe: float
    previous_roe: float
    roe_change: float
    components: List[ROEComponent]
    main_drivers: List[str]
    sustainability_score: float
    recommendations: List[str]


class ROEAnalyzer:
    """
    ROE核心指标分析器
    
    基于杜邦分析法，分解ROE变动驱动因素
    """
    
    def __init__(self):
        """初始化分析器"""
        pass
    
    def analyze_roe(
        self,
        company_code: str,
        company_name: str,
        financial_data: Dict,
        disclosure_text: str = "",
    ) -> ROEAnalysisResult:
        """
        分析ROE
        
        Args:
            company_code: 公司代码
            company_name: 公司名称
            financial_data: 财务数据字典
            disclosure_text: 披露文本（用于分析定性信息）
            
        Returns:
            ROEAnalysisResult: ROE分析结果
        """
        # 提取财务指标
        current_data = financial_data.get("current", {})
        previous_data = financial_data.get("previous", {})
        
        # 计算当前ROE
        current_roe = self._calculate_roe(current_data)
        previous_roe = self._calculate_roe(previous_data)
        
        # 分解ROE驱动因素
        components = self._decompose_roe(current_data, previous_data)
        
        # 识别主要驱动因素
        main_drivers = self._identify_main_drivers(components)
        
        # 评估可持续性
        sustainability_score = self._assess_sustainability(
            current_data, previous_data, disclosure_text
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            current_roe, previous_roe, components, sustainability_score
        )
        
        return ROEAnalysisResult(
            company_code=company_code,
            company_name=company_name,
            current_roe=current_roe,
            previous_roe=previous_roe,
            roe_change=round(current_roe - previous_roe, 2),
            components=components,
            main_drivers=main_drivers,
            sustainability_score=sustainability_score,
            recommendations=recommendations,
        )
    
    def _calculate_roe(self, data: Dict) -> float:
        """计算ROE"""
        net_profit = data.get("net_profit", 0)
        equity = data.get("equity", 0)
        
        if equity == 0:
            return 0.0
        
        return round(net_profit / equity * 100, 2)
    
    def _decompose_roe(
        self,
        current_data: Dict,
        previous_data: Dict,
    ) -> List[ROEComponent]:
        """分解ROE（杜邦分析）"""
        components = []
        
        # 利润率
        current_margin = self._calculate_profit_margin(current_data)
        previous_margin = self._calculate_profit_margin(previous_data)
        
        components.append(ROEComponent(
            driver=ROEDriver.PROFIT_MARGIN,
            name="利润率",
            current_value=current_margin,
            previous_value=previous_margin,
            change=round(current_margin - previous_margin, 2),
            contribution_to_roe=round(current_margin * 0.4, 2),  # 简化贡献度
        ))
        
        # 资产周转率
        current_turnover = self._calculate_asset_turnover(current_data)
        previous_turnover = self._calculate_asset_turnover(previous_data)
        
        components.append(ROEComponent(
            driver=ROEDriver.ASSET_TURNOVER,
            name="资产周转率",
            current_value=current_turnover,
            previous_value=previous_turnover,
            change=round(current_turnover - previous_turnover, 2),
            contribution_to_roe=round(current_turnover * 0.3, 2),
        ))
        
        # 财务杠杆
        current_leverage = self._calculate_leverage(current_data)
        previous_leverage = self._calculate_leverage(previous_data)
        
        components.append(ROEComponent(
            driver=ROEDriver.LEVERAGE,
            name="财务杠杆",
            current_value=current_leverage,
            previous_value=previous_leverage,
            change=round(current_leverage - previous_leverage, 2),
            contribution_to_roe=round(current_leverage * 0.3, 2),
        ))
        
        return components
    
    def _calculate_profit_margin(self, data: Dict) -> float:
        """计算利润率"""
        net_profit = data.get("net_profit", 0)
        revenue = data.get("revenue", 0)
        
        if revenue == 0:
            return 0.0
        
        return round(net_profit / revenue * 100, 2)
    
    def _calculate_asset_turnover(self, data: Dict) -> float:
        """计算资产周转率"""
        revenue = data.get("revenue", 0)
        total_assets = data.get("total_assets", 0)
        
        if total_assets == 0:
            return 0.0
        
        return round(revenue / total_assets, 2)
    
    def _calculate_leverage(self, data: Dict) -> float:
        """计算财务杠杆（权益乘数）"""
        total_assets = data.get("total_assets", 0)
        equity = data.get("equity", 0)
        
        if equity == 0:
            return 1.0
        
        return round(total_assets / equity, 2)
    
    def _identify_main_drivers(self, components: List[ROEComponent]) -> List[str]:
        """识别主要驱动因素"""
        drivers = []
        
        for comp in components:
            if abs(comp.change) > 1.0:  # 变化超过1个百分点
                direction = "提升" if comp.change > 0 else "下降"
                drivers.append(f"{comp.name}{direction}是ROE变动的主要因素")
        
        return drivers if drivers else ["ROE变动较为平稳"]
    
    def _assess_sustainability(
        self,
        current_data: Dict,
        previous_data: Dict,
        disclosure_text: str,
    ) -> float:
        """评估ROE可持续性"""
        score = 50.0  # 基础分
        
        # 检查利润增长是否可持续
        current_profit = current_data.get("net_profit", 0)
        previous_profit = previous_data.get("net_profit", 0)
        
        if previous_profit > 0:
            profit_growth = (current_profit - previous_profit) / previous_profit
            if 0 < profit_growth < 0.3:  # 适度增长
                score += 15
            elif profit_growth >= 0.3:  # 高增长需谨慎
                score -= 5
        
        # 检查杠杆是否过高
        leverage = self._calculate_leverage(current_data)
        if leverage > 3.0:
            score -= 10  # 杠杆过高
        elif leverage < 2.0:
            score += 10  # 杠杆适中
        
        # 检查披露文本中的承诺
        sustainability_keywords = [
            "可持续", "长期", "稳定", "持续", "规划", "战略",
        ]
        
        for keyword in sustainability_keywords:
            if keyword in disclosure_text:
                score += 5
                break
        
        return min(100, max(0, score))
    
    def _generate_recommendations(
        self,
        current_roe: float,
        previous_roe: float,
        components: List[ROEComponent],
        sustainability_score: float,
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # ROE水平建议
        if current_roe > 15:
            recommendations.append("ROE水平较高，盈利能力优秀")
        elif current_roe > 10:
            recommendations.append("ROE水平良好，仍有提升空间")
        elif current_roe > 5:
            recommendations.append("ROE水平一般，建议关注盈利能力改善")
        else:
            recommendations.append("ROE水平较低，需重点关注")
        
        # ROE变动建议
        if current_roe > previous_roe:
            recommendations.append("ROE同比提升，经营改善趋势向好")
        elif current_roe < previous_roe:
            recommendations.append("ROE同比下降，需分析具体原因")
        
        # 驱动因素建议
        for comp in components:
            if comp.driver == ROEDriver.PROFIT_MARGIN and comp.change < -2:
                recommendations.append("利润率下降明显，建议关注成本控制")
            elif comp.driver == ROEDriver.ASSET_TURNOVER and comp.change < -0.1:
                recommendations.append("资产周转效率下降，建议关注资产运营")
            elif comp.driver == ROEDriver.LEVERAGE and comp.change > 0.5:
                recommendations.append("财务杠杆上升，需关注偿债风险")
        
        # 可持续性建议
        if sustainability_score > 70:
            recommendations.append("ROE可持续性较好，投资价值较高")
        elif sustainability_score > 50:
            recommendations.append("ROE可持续性一般，建议进一步分析")
        else:
            recommendations.append("ROE可持续性存疑，需谨慎评估")
        
        return recommendations


@dataclass
class OneFiveRatioResult:
    """一利五率分析结果"""
    company_code: str
    company_name: str
    # 一利：利润总额
    profit_total: float
    profit_total_rank: str
    # 五率
    roe: float  # 净资产收益率
    roa: float  # 总资产收益率
    debt_ratio: float  # 资产负债率
    cash_flow_ratio: float  # 现金流比率
    rd_intensity: float  # 研发投入强度
    overall_score: float
    recommendations: List[str]


class OneFiveRatioAnalyzer:
    """
    一利五率分析器
    
    分析国资委考核指标体系
    """
    
    def __init__(self):
        """初始化分析器"""
        pass
    
    def analyze(
        self,
        company_code: str,
        company_name: str,
        financial_data: Dict,
    ) -> OneFiveRatioResult:
        """
        分析一利五率
        
        Args:
            company_code: 公司代码
            company_name: 公司名称
            financial_data: 财务数据
            
        Returns:
            OneFiveRatioResult: 分析结果
        """
        # 提取指标
        profit_total = financial_data.get("profit_total", 0)
        equity = financial_data.get("equity", 0)
        total_assets = financial_data.get("total_assets", 0)
        total_debt = financial_data.get("total_debt", 0)
        operating_cash_flow = financial_data.get("operating_cash_flow", 0)
        rd_expense = financial_data.get("rd_expense", 0)
        revenue = financial_data.get("revenue", 0)
        
        # 计算指标
        roe = round(profit_total / equity * 100, 2) if equity > 0 else 0
        roa = round(profit_total / total_assets * 100, 2) if total_assets > 0 else 0
        debt_ratio = round(total_debt / total_assets * 100, 2) if total_assets > 0 else 0
        cash_flow_ratio = round(operating_cash_flow / total_debt * 100, 2) if total_debt > 0 else 0
        rd_intensity = round(rd_expense / revenue * 100, 2) if revenue > 0 else 0
        
        # 计算排名（简化）
        profit_total_rank = self._calculate_rank(profit_total, "profit")
        
        # 计算综合得分
        overall_score = self._calculate_score(roe, roa, debt_ratio, cash_flow_ratio, rd_intensity)
        
        # 生成建议
        recommendations = self._generate_recommendations(
            roe, roa, debt_ratio, cash_flow_ratio, rd_intensity
        )
        
        return OneFiveRatioResult(
            company_code=company_code,
            company_name=company_name,
            profit_total=profit_total,
            profit_total_rank=profit_total_rank,
            roe=roe,
            roa=roa,
            debt_ratio=debt_ratio,
            cash_flow_ratio=cash_flow_ratio,
            rd_intensity=rd_intensity,
            overall_score=overall_score,
            recommendations=recommendations,
        )
    
    def _calculate_rank(self, value: float, metric_type: str) -> str:
        """计算排名等级"""
        # 简化的排名逻辑
        if value > 100:
            return "优秀"
        elif value > 50:
            return "良好"
        elif value > 20:
            return "一般"
        else:
            return "待改善"
    
    def _calculate_score(
        self,
        roe: float,
        roa: float,
        debt_ratio: float,
        cash_flow_ratio: float,
        rd_intensity: float,
    ) -> float:
        """计算综合得分"""
        score = 0
        
        # ROE评分（30%）
        if roe > 15:
            score += 30
        elif roe > 10:
            score += 25
        elif roe > 5:
            score += 15
        else:
            score += 5
        
        # ROA评分（20%）
        if roa > 8:
            score += 20
        elif roa > 5:
            score += 15
        elif roa > 3:
            score += 10
        else:
            score += 5
        
        # 资产负债率评分（20%）- 越低越好
        if debt_ratio < 50:
            score += 20
        elif debt_ratio < 65:
            score += 15
        elif debt_ratio < 75:
            score += 10
        else:
            score += 5
        
        # 现金流比率评分（15%）
        if cash_flow_ratio > 30:
            score += 15
        elif cash_flow_ratio > 20:
            score += 12
        elif cash_flow_ratio > 10:
            score += 8
        else:
            score += 3
        
        # 研发投入强度评分（15%）
        if rd_intensity > 5:
            score += 15
        elif rd_intensity > 3:
            score += 12
        elif rd_intensity > 1:
            score += 8
        else:
            score += 3
        
        return round(score, 2)
    
    def _generate_recommendations(
        self,
        roe: float,
        roa: float,
        debt_ratio: float,
        cash_flow_ratio: float,
        rd_intensity: float,
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if roe < 10:
            recommendations.append("ROE偏低，建议提升盈利能力")
        
        if debt_ratio > 70:
            recommendations.append("资产负债率偏高，建议优化资本结构")
        
        if cash_flow_ratio < 15:
            recommendations.append("现金流比率偏低，建议加强现金流管理")
        
        if rd_intensity < 3:
            recommendations.append("研发投入强度偏低，建议加大创新投入")
        
        return recommendations if recommendations else ["各项指标表现良好"]
