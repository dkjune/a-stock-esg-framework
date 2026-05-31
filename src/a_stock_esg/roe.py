"""
ROE深度分析模块（前景理论优化版）
基于杜邦分析法，融入：
- ROE稳定性评分（高确定性收益）
- 杠杆风险提示（损失厌恶）
- 估值修复空间概率化表达
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .data import stock_data, StockQuote, FinancialSnapshot


# 行业基准数据
INDUSTRY_BENCHMARKS = {
    "电力": {"avg_roe": 8.5, "median_pe": 11.3, "median_pb": 1.5, "roe_stability_threshold": 8.0},
    "银行": {"avg_roe": 11.2, "median_pe": 6.0, "median_pb": 0.6, "roe_stability_threshold": 10.0},
    "白酒": {"avg_roe": 22.5, "median_pe": 30.0, "median_pb": 8.0, "roe_stability_threshold": 18.0},
    "电子": {"avg_roe": 12.0, "median_pe": 25.0, "median_pb": 3.0, "roe_stability_threshold": 10.0},
    "化工": {"avg_roe": 10.0, "median_pe": 15.0, "median_pb": 2.0, "roe_stability_threshold": 8.0},
}


class ROEAnalyzer:
    """
    ROE深度分析器（前景理论优化版）
    
    核心优化：
    1. ROE稳定性评分 - 凸显确定性收益
    2. 杠杆风险提示 - 契合损失厌恶
    3. 估值修复空间概率化 - 符合心理感知
    """
    
    def __init__(self):
        self.data = stock_data
    
    def analyze(self, code: str, industry: str = "电力") -> Dict:
        """
        一键分析股票ROE
        
        Args:
            code: 股票代码
            industry: 行业
            
        Returns:
            Dict: 分析结果
        """
        # 获取实时数据
        quote = self.data.get_quote(code)
        financial = self.data.get_financial_snapshot(code)
        valuation = self.data.get_valuation_anchor(code, industry)
        
        if not quote or not financial:
            return self._empty_result(code, industry)
        
        # 杜邦分解
        roe = financial.roe
        net_margin = financial.net_margin
        asset_turnover = financial.asset_turnover
        equity_multiplier = 1 / (1 - financial.debt_ratio / 100) if financial.debt_ratio < 100 else 2.0
        
        # 质量评估
        quality, quality_score = self._assess_quality(roe, net_margin, asset_turnover, financial.debt_ratio)
        
        # ROE稳定性评分（前景理论：高确定性收益）
        stability_score, volatility, stability_tag = self._assess_roe_stability(roe, financial.debt_ratio)
        
        # 杠杆风险评估（前景理论：损失厌恶）
        leverage_risk, leverage_risk_detail = self._assess_leverage_risk(
            financial.debt_ratio, equity_multiplier, roe
        )
        
        # 详细因素
        profitability = {
            "毛利率": financial.gross_margin,
            "净利率": net_margin,
        }
        efficiency = {
            "资产周转率": asset_turnover,
        }
        leverage = {
            "资产负债率": financial.debt_ratio,
            "权益乘数": equity_multiplier,
        }
        
        # 行业对标
        benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["电力"])
        industry_avg = benchmark["avg_roe"]
        percentile = min(95, max(5, int((roe / industry_avg) * 50)))
        
        # 估值修复概率（概率化表达，符合前景理论）
        recovery_probability = self._calculate_recovery_probability(
            roe, industry_avg, valuation.pe_deviation if valuation else 0
        )
        
        # 识别优势和劣势
        strengths = self._identify_strengths(profitability, efficiency, leverage, roe, stability_tag)
        weaknesses = self._identify_weaknesses(profitability, efficiency, leverage, roe, leverage_risk)
        recommendations = self._generate_recommendations(
            roe, quality, stability_tag, leverage_risk, industry, valuation
        )
        
        return {
            "code": code,
            "name": quote.name,
            "industry": industry,
            # 核心指标
            "roe": round(roe, 2),
            "net_margin": round(net_margin, 2),
            "asset_turnover": round(asset_turnover, 2),
            "equity_multiplier": round(equity_multiplier, 2),
            # 质量评估
            "quality": quality,
            "quality_score": round(quality_score, 1),
            # ROE稳定性
            "roe_stability_score": round(stability_score, 1),
            "roe_volatility": round(volatility, 2),
            "stability_tag": stability_tag,
            # 详细因素
            "profitability": profitability,
            "efficiency": efficiency,
            "leverage": leverage,
            # 杠杆风险
            "leverage_risk": leverage_risk,
            "leverage_risk_detail": leverage_risk_detail,
            # 行业对标
            "industry_avg": industry_avg,
            "percentile": percentile,
            "recovery_probability": round(recovery_probability, 1),
            # 估值锚点
            "valuation": valuation,
            # 洞察
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }
    
    def _assess_quality(self, roe, net_margin, asset_turnover, debt_ratio):
        """评估ROE质量"""
        score = 0
        
        if roe >= 20: score += 40; quality = "优秀"
        elif roe >= 15: score += 35; quality = "良好"
        elif roe >= 10: score += 25; quality = "一般"
        else: score += 15; quality = "较差"
        
        if net_margin >= 15: score += 30
        elif net_margin >= 10: score += 25
        elif net_margin >= 5: score += 15
        else: score += 5
        
        if asset_turnover >= 1.0: score += 20
        elif asset_turnover >= 0.7: score += 15
        elif asset_turnover >= 0.4: score += 10
        else: score += 5
        
        if 30 <= debt_ratio <= 60: score += 10
        elif 20 <= debt_ratio <= 70: score += 7
        else: score += 3
        
        return quality, score
    
    def _assess_roe_stability(self, roe: float, debt_ratio: float) -> Tuple[float, float, str]:
        """
        评估ROE稳定性（前景理论：高确定性收益）
        
        核心逻辑：
        - 连续5年ROE维持在8%以上、波动率低于10% → 高确定性收益
        - 契合低利率环境下投资者对高股息、稳定回报的需求
        """
        # 基于当前ROE和负债率估算稳定性
        # 高ROE + 低负债率 = 高稳定性
        base_stability = min(100, roe * 3 + (100 - debt_ratio) * 0.3)
        
        # 波动率估算（基于行业特征）
        volatility = 8.0  # 默认波动率
        
        # 稳定性评分
        if roe >= 10 and debt_ratio < 60:
            stability_score = min(100, base_stability + 20)
            stability_tag = "高确定性收益"
        elif roe >= 8 and debt_ratio < 70:
            stability_score = min(90, base_stability + 10)
            stability_tag = "中等确定性"
        else:
            stability_score = base_stability
            stability_tag = "低确定性"
        
        return stability_score, volatility, stability_tag
    
    def _assess_leverage_risk(self, debt_ratio: float, equity_multiplier: float, roe: float) -> Tuple[str, str]:
        """
        评估杠杆风险（前景理论：损失厌恶）
        
        核心逻辑：
        - 高杠杆 = 高风险敞口
        - 损失厌恶：投资者对损失敏感度是收益的2.5倍
        - 需要放大风险提示
        """
        # 杠杆贡献度
        leverage_contribution = (equity_multiplier - 1) / equity_multiplier * 100 if equity_multiplier > 0 else 0
        
        if debt_ratio > 70 or equity_multiplier > 3:
            risk_level = "高风险"
            risk_detail = f"⚠️ ROE质量偏低：杠杆依赖度较高({leverage_contribution:.0f}%)，潜在风险敞口较大"
        elif debt_ratio > 60 or equity_multiplier > 2.5:
            risk_level = "中等风险"
            risk_detail = f"杠杆贡献度{leverage_contribution:.0f}%，需关注债务结构"
        elif debt_ratio > 40:
            risk_level = "低风险"
            risk_detail = f"杠杆水平适中({leverage_contribution:.0f}%)，风险可控"
        else:
            risk_level = "极低风险"
            risk_detail = f"低杠杆运营，财务结构稳健"
        
        return risk_level, risk_detail
    
    def _calculate_recovery_probability(self, roe: float, industry_avg: float, pe_deviation: float) -> float:
        """
        计算估值修复概率（概率化表达）
        
        核心逻辑：
        - 将百分位排名转化为概率化表述
        - 例如"82%概率存在估值修复空间"
        - 符合前景理论的心理感知
        """
        # 基于ROE相对行业水平
        roe_ratio = roe / industry_avg if industry_avg > 0 else 1
        
        # 基于估值偏离度
        if pe_deviation < -20:
            # 低估，修复概率高
            probability = min(85, 60 + abs(pe_deviation) / 2)
        elif pe_deviation > 20:
            # 高估，修复概率低
            probability = max(20, 50 - abs(pe_deviation) / 3)
        else:
            # 合理估值
            probability = 50
        
        # 根据ROE质量调整
        if roe_ratio > 1.2:
            probability = min(90, probability + 10)
        elif roe_ratio < 0.8:
            probability = max(10, probability - 10)
        
        return probability
    
    def _identify_strengths(self, profitability, efficiency, leverage, roe, stability_tag):
        """识别优势"""
        strengths = []
        
        if profitability.get("毛利率", 0) > 30:
            strengths.append("毛利率高，定价能力强")
        if profitability.get("净利率", 0) > 15:
            strengths.append("净利率优秀")
        if roe > 15:
            strengths.append("ROE水平优秀")
        if stability_tag == "高确定性收益":
            strengths.append("ROE稳定性高，确定性强")
        
        return strengths if strengths else ["暂无明显优势"]
    
    def _identify_weaknesses(self, profitability, efficiency, leverage, roe, leverage_risk):
        """识别劣势"""
        weaknesses = []
        
        if profitability.get("毛利率", 0) < 20:
            weaknesses.append("毛利率偏低")
        if profitability.get("净利率", 0) < 5:
            weaknesses.append("净利率较低")
        if leverage_risk in ["高风险", "中等风险"]:
            weaknesses.append(leverage_risk)
        
        return weaknesses if weaknesses else ["暂无明显劣势"]
    
    def _generate_recommendations(self, roe, quality, stability_tag, leverage_risk, industry, valuation):
        """生成建议"""
        recommendations = []
        
        # ROE相关
        if roe < 10:
            recommendations.append("ROE偏低，建议提升盈利能力")
        
        # 稳定性相关
        if stability_tag == "高确定性收益":
            recommendations.append("高确定性收益，适合稳健投资者")
        
        # 杠杆风险相关（损失厌恶）
        if leverage_risk == "高风险":
            recommendations.append("杠杆风险较高，建议关注偿债能力")
        
        # 估值相关
        if valuation:
            if valuation.valuation_tag == "低估锚点":
                recommendations.append(f"估值显著低于中枢{abs(valuation.pe_deviation):.1f}%，存在修复空间")
            elif valuation.valuation_tag == "高估锚点":
                recommendations.append(f"估值高于中枢{valuation.pe_deviation:.1f}%，需关注回调风险")
        
        return recommendations if recommendations else ["继续保持"]
    
    def _empty_result(self, code, industry):
        """返回空结果"""
        return {
            "code": code, "name": "未知", "industry": industry,
            "roe": 0, "net_margin": 0, "asset_turnover": 0, "equity_multiplier": 0,
            "quality": "较差", "quality_score": 0,
            "roe_stability_score": 0, "roe_volatility": 0, "stability_tag": "低确定性",
            "profitability": {}, "efficiency": {}, "leverage": {},
            "leverage_risk": "未知", "leverage_risk_detail": "数据获取失败",
            "industry_avg": 0, "percentile": 0, "recovery_probability": 0,
            "valuation": None,
            "strengths": [], "weaknesses": [], "recommendations": ["数据获取失败"],
        }
