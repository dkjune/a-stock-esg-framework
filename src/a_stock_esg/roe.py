"""
ROE深度分析模块
基于杜邦分析法，分解ROE变动驱动因素
集成数据获取，支持一键分析
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from .data import stock_data, StockQuote, FinancialSnapshot


class ROEQuality(Enum):
    """ROE质量等级"""
    EXCELLENT = "优秀"  # ROE > 20%
    GOOD = "良好"       # ROE 15-20%
    FAIR = "一般"       # ROE 10-15%
    POOR = "较差"       # ROE < 10%


@dataclass
class ROEResult:
    """ROE分析结果"""
    # 基本信息
    code: str
    name: str
    industry: str
    
    # 核心指标
    roe: float
    net_margin: float
    asset_turnover: float
    equity_multiplier: float
    
    # 质量评估
    quality: ROEQuality
    quality_score: float
    
    # 详细因素
    profitability: Dict[str, float]
    efficiency: Dict[str, float]
    leverage: Dict[str, float]
    
    # 行业对标
    industry_avg: float
    percentile: float
    
    # 洞察
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


# 行业基准数据
INDUSTRY_BENCHMARKS = {
    "电力": {"avg_roe": 8.5, "avg_margin": 15.0, "avg_turnover": 0.4, "avg_leverage": 55.0},
    "银行": {"avg_roe": 11.2, "avg_margin": 30.0, "avg_turnover": 0.05, "avg_leverage": 92.0},
    "白酒": {"avg_roe": 22.5, "avg_margin": 35.0, "avg_turnover": 0.6, "avg_leverage": 35.0},
    "电子": {"avg_roe": 12.0, "avg_margin": 12.0, "avg_turnover": 0.8, "avg_leverage": 40.0},
    "化工": {"avg_roe": 10.0, "avg_margin": 10.0, "avg_turnover": 0.7, "avg_leverage": 50.0},
}


class ROEAnalyzer:
    """
    ROE深度分析器
    
    一键获取数据并进行杜邦分析
    """
    
    def __init__(self):
        self.data = stock_data
    
    def analyze(self, code: str, industry: str = "电力") -> ROEResult:
        """
        一键分析股票ROE
        
        Args:
            code: 股票代码
            industry: 行业
            
        Returns:
            ROEResult: 分析结果
        """
        # 1. 获取实时数据
        quote = self.data.get_quote(code)
        financial = self.data.get_financial_snapshot(code)
        
        if not quote or not financial:
            return self._empty_result(code, industry)
        
        # 2. 杜邦分解
        roe = financial.roe
        net_margin = financial.net_margin
        asset_turnover = financial.asset_turnover
        equity_multiplier = 1 / (1 - financial.debt_ratio / 100) if financial.debt_ratio < 100 else 2.0
        
        # 3. 详细因素
        profitability = {
            "毛利率": financial.gross_margin,
            "净利率": net_margin,
            "成本费用率": 100 - net_margin,
        }
        
        efficiency = {
            "资产周转率": asset_turnover,
            "存货周转率": asset_turnover * 5,
            "应收账款周转率": asset_turnover * 10,
        }
        
        leverage = {
            "资产负债率": financial.debt_ratio,
            "权益乘数": equity_multiplier,
            "债务权益比": financial.debt_ratio / (100 - financial.debt_ratio) if financial.debt_ratio < 100 else 10,
        }
        
        # 4. 质量评估
        quality, quality_score = self._assess_quality(roe, net_margin, asset_turnover, financial.debt_ratio)
        
        # 5. 行业对标
        benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["电力"])
        industry_avg = benchmark["avg_roe"]
        percentile = min(95, max(5, int((roe / industry_avg) * 50)))
        
        # 6. 识别优劣势
        strengths = self._identify_strengths(profitability, efficiency, leverage)
        weaknesses = self._identify_weaknesses(profitability, efficiency, leverage)
        recommendations = self._generate_recommendations(roe, quality, weaknesses, industry)
        
        return ROEResult(
            code=code,
            name=quote.name,
            industry=industry,
            roe=round(roe, 2),
            net_margin=round(net_margin, 2),
            asset_turnover=round(asset_turnover, 2),
            equity_multiplier=round(equity_multiplier, 2),
            quality=quality,
            quality_score=round(quality_score, 1),
            profitability=profitability,
            efficiency=efficiency,
            leverage=leverage,
            industry_avg=industry_avg,
            percentile=percentile,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )
    
    def analyze_batch(self, codes: List[str], industry: str = "电力") -> List[ROEResult]:
        """批量分析"""
        return [self.analyze(code, industry) for code in codes]
    
    def _assess_quality(self, roe, net_margin, asset_turnover, debt_ratio):
        """评估ROE质量"""
        score = 0
        
        # ROE水平（40%）
        if roe >= 20: score += 40; quality = ROEQuality.EXCELLENT
        elif roe >= 15: score += 35; quality = ROEQuality.GOOD
        elif roe >= 10: score += 25; quality = ROEQuality.FAIR
        else: score += 15; quality = ROEQuality.POOR
        
        # 盈利能力（30%）
        if net_margin >= 15: score += 30
        elif net_margin >= 10: score += 25
        elif net_margin >= 5: score += 15
        else: score += 5
        
        # 运营效率（20%）
        if asset_turnover >= 1.0: score += 20
        elif asset_turnover >= 0.7: score += 15
        elif asset_turnover >= 0.4: score += 10
        else: score += 5
        
        # 杠杆风险（10%）
        if 30 <= debt_ratio <= 60: score += 10
        elif 20 <= debt_ratio <= 70: score += 7
        else: score += 3
        
        return quality, score
    
    def _identify_strengths(self, profitability, efficiency, leverage):
        """识别优势"""
        strengths = []
        
        if profitability.get("毛利率", 0) > 30:
            strengths.append("毛利率高，定价能力强")
        if profitability.get("净利率", 0) > 15:
            strengths.append("净利率优秀")
        if efficiency.get("资产周转率", 0) > 1.0:
            strengths.append("资产周转效率高")
        if leverage.get("资产负债率", 50) < 40:
            strengths.append("财务结构稳健")
        if leverage.get("权益乘数", 2) < 1.5:
            strengths.append("低杠杆运营")
        
        return strengths if strengths else ["暂无明显优势"]
    
    def _identify_weaknesses(self, profitability, efficiency, leverage):
        """识别劣势"""
        weaknesses = []
        
        if profitability.get("毛利率", 0) < 20:
            weaknesses.append("毛利率偏低")
        if profitability.get("净利率", 0) < 5:
            weaknesses.append("净利率较低")
        if efficiency.get("资产周转率", 0) < 0.5:
            weaknesses.append("资产周转效率低")
        if leverage.get("资产负债率", 50) > 70:
            weaknesses.append("杠杆率偏高")
        
        return weaknesses if weaknesses else ["暂无明显劣势"]
    
    def _generate_recommendations(self, roe, quality, weaknesses, industry):
        """生成建议"""
        recommendations = []
        
        if roe < 10:
            recommendations.append("ROE偏低，建议提升盈利能力或优化资产结构")
        
        if quality == ROEQuality.POOR:
            recommendations.append("ROE质量较差，需多维度改进")
        
        for w in weaknesses:
            if "毛利率" in w:
                recommendations.append("建议通过产品升级提升毛利率")
            elif "周转" in w:
                recommendations.append("建议优化资产配置提升周转效率")
            elif "杠杆" in w:
                recommendations.append("建议控制债务规模优化资本结构")
        
        industry_tips = {
            "电力": "关注电价政策和清洁能源转型",
            "银行": "关注净息差和资产质量",
            "白酒": "关注品牌力和渠道效率",
        }
        if industry in industry_tips:
            recommendations.append(industry_tips[industry])
        
        return recommendations if recommendations else ["继续保持"]
    
    def _empty_result(self, code, industry):
        """返回空结果"""
        return ROEResult(
            code=code, name="未知", industry=industry,
            roe=0, net_margin=0, asset_turnover=0, equity_multiplier=0,
            quality=ROEQuality.POOR, quality_score=0,
            profitability={}, efficiency={}, leverage={},
            industry_avg=0, percentile=0,
            strengths=[], weaknesses=[], recommendations=["数据获取失败"],
        )
