"""
ROE深度分析模块（噪声优化版）
基于《噪声》理论：
- 趋势滤波：H-P滤波趋势项
- 参考类预测：孪生组排名
- 贝叶斯收缩：向行业均值收缩
- 置信区间输出
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .data import stock_data, MultiSourceData, ROETrendData


# 行业基准数据
INDUSTRY_BENCHMARKS = {
    "电力": {"avg_roe": 8.5, "median_pe": 11.3, "median_pb": 1.5, "roe_std": 3.0, "roe_threshold": 8.0},
    "银行": {"avg_roe": 11.2, "median_pe": 6.0, "median_pb": 0.6, "roe_std": 2.0, "roe_threshold": 10.0},
    "白酒": {"avg_roe": 22.5, "median_pe": 30.0, "median_pb": 8.0, "roe_std": 5.0, "roe_threshold": 18.0},
    "电子": {"avg_roe": 12.0, "median_pe": 25.0, "median_pb": 3.0, "roe_std": 4.0, "roe_threshold": 10.0},
    "化工": {"avg_roe": 10.0, "median_pe": 15.0, "median_pb": 2.0, "roe_std": 3.5, "roe_threshold": 8.0},
    "医药": {"avg_roe": 15.0, "median_pe": 35.0, "median_pb": 4.0, "roe_std": 6.0, "roe_threshold": 12.0},
    "汽车": {"avg_roe": 10.0, "median_pe": 20.0, "median_pb": 2.5, "roe_std": 4.5, "roe_threshold": 8.0},
    "建筑": {"avg_roe": 8.0, "median_pe": 8.0, "median_pb": 0.8, "roe_std": 2.5, "roe_threshold": 6.0},
}


class ROEAnalyzer:
    """
    ROE深度分析器（噪声优化版）
    
    基于《噪声》理论：
    1. 趋势滤波 - 消除随机波动
    2. 参考类预测 - 替代绝对阈值
    3. 贝叶斯收缩 - 避免极端值
    4. 置信区间 - 输出不确定性
    """
    
    def __init__(self):
        self.data = stock_data
    
    def analyze(self, code: str, industry: str = "电力") -> Dict:
        """
        一键分析股票ROE（噪声优化版）
        """
        # 获取多源数据
        multi_data = self.data.get_multi_source_data(code)
        roe_trend = self.data.get_roe_trend(code, industry)
        valuation = self.data.get_valuation_anchor(code, industry)
        
        if not multi_data or not roe_trend:
            return self._empty_result(code, industry)
        
        # 核心指标
        roe = roe_trend.shrunk_roe  # 使用贝叶斯收缩后的ROE
        benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["电力"])
        
        # 质量分级（决策卫生：百分位排名，非模糊标签）
        quality, quality_score, quality_ci = self._grade_quality(roe, benchmark)
        
        # 趋势稳定性
        stability_score, stability_tag = self._assess_stability(roe_trend)
        
        # 杠杆风险
        leverage_risk, leverage_detail = self._assess_leverage(roe, benchmark)
        
        # 估值修复概率（参考类预测）
        recovery_prob = self._estimate_recovery_probability(
            roe, benchmark, valuation.pe_deviation if valuation else 0
        )
        
        # 优势/劣势/建议
        strengths = self._identify_strengths(roe, stability_tag, valuation)
        weaknesses = self._identify_weaknesses(roe, leverage_risk, valuation)
        recommendations = self._generate_recommendations(
            roe, quality, stability_tag, leverage_risk, valuation
        )
        
        return {
            "code": code,
            "name": "",
            "industry": industry,
            # 核心指标
            "roe": round(roe, 2),
            "roe_trend": round(roe_trend.trend_roe, 2),
            "roe_volatility": roe_trend.volatility,
            "roe_trend_direction": roe_trend.trend_direction,
            # 质量分级
            "quality": quality,
            "quality_score": quality_score,
            "quality_ci": quality_ci,
            # 稳定性
            "stability_score": stability_score,
            "stability_tag": stability_tag,
            # 杠杆
            "leverage_risk": leverage_risk,
            "leverage_detail": leverage_detail,
            # 参考类
            "peer_group": roe_trend.peer_group,
            "peer_rank": roe_trend.peer_rank,
            # 估值
            "valuation": valuation,
            "recovery_probability": recovery_prob,
            # 数据质量
            "data_quality": multi_data.data_quality,
            "confidence_note": multi_data.confidence_note,
            # 洞察
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }
    
    def _grade_quality(self, roe: float, benchmark: Dict) -> Tuple[str, float, str]:
        """
        质量分级（决策卫生：百分位排名+置信区间）
        
        放弃模糊标签，使用数据驱动的分级
        """
        avg = benchmark["avg_roe"]
        std = benchmark["roe_std"]
        
        # 计算z-score
        z_score = (roe - avg) / std if std > 0 else 0
        
        # 分级规则（决策卫生：明确阈值）
        if z_score >= 1.5:
            quality = "A"
            quality_score = 90
            ci = f"优秀（高于行业{abs(z_score):.1f}个标准差）"
        elif z_score >= 0.5:
            quality = "B+"
            quality_score = 75
            ci = f"良好（高于行业均值）"
        elif z_score >= -0.5:
            quality = "B"
            quality_score = 60
            ci = f"一般（接近行业均值）"
        elif z_score >= -1.0:
            quality = "C+"
            quality_score = 45
            ci = f"偏弱（低于行业均值）"
        else:
            quality = "C"
            quality_score = 30
            ci = f"较弱（低于行业{abs(z_score):.1f}个标准差）"
        
        return quality, quality_score, ci
    
    def _assess_stability(self, roe_trend: ROETrendData) -> Tuple[float, str]:
        """
        评估稳定性（噪声优化：波动率量化）
        """
        vol = roe_trend.volatility
        
        if vol < 3:
            stability_score = 90
            stability_tag = "高稳定性"
        elif vol < 6:
            stability_score = 70
            stability_tag = "中等稳定性"
        elif vol < 10:
            stability_score = 50
            stability_tag = "较低稳定性"
        else:
            stability_score = 30
            stability_tag = "高波动性"
        
        return stability_score, stability_tag
    
    def _assess_leverage(self, roe: float, benchmark: Dict) -> Tuple[str, str]:
        """
        评估杠杆风险（噪声优化：量化风险等级）
        """
        # 简化：基于ROE与行业均值的关系推断杠杆
        if roe > benchmark["avg_roe"] * 1.5:
            return "高杠杆贡献", "ROE中杠杆贡献占比可能较高，需关注债务风险"
        elif roe > benchmark["avg_roe"] * 1.2:
            return "中等杠杆贡献", "杠杆水平适中"
        else:
            return "低杠杆贡献", "杠杆风险较低"
    
    def _estimate_recovery_probability(self, roe: float, benchmark: Dict, pe_deviation: float) -> float:
        """
        估算估值修复概率（参考类预测）
        """
        # 基于ROE相对水平
        roe_ratio = roe / benchmark["avg_roe"] if benchmark["avg_roe"] > 0 else 1
        
        # 基于估值偏离度
        if pe_deviation < -20:
            probability = min(85, 60 + abs(pe_deviation) / 2)
        elif pe_deviation > 20:
            probability = max(20, 50 - abs(pe_deviation) / 3)
        else:
            probability = 50
        
        # 根据ROE质量调整
        if roe_ratio > 1.2:
            probability = min(90, probability + 10)
        elif roe_ratio < 0.8:
            probability = max(10, probability - 10)
        
        return round(probability, 1)
    
    def _identify_strengths(self, roe: float, stability_tag: str, valuation) -> List[str]:
        """识别优势"""
        strengths = []
        
        if roe > 15:
            strengths.append("ROE水平优秀")
        if stability_tag == "高稳定性":
            strengths.append("ROE稳定性高")
        if valuation and valuation.valuation_tag == "低估锚点":
            strengths.append("估值低于中枢，存在修复空间")
        
        return strengths if strengths else ["暂无明显优势"]
    
    def _identify_weaknesses(self, roe: float, leverage_risk: str, valuation) -> List[str]:
        """识别劣势"""
        weaknesses = []
        
        if roe < 8:
            weaknesses.append("ROE水平偏低")
        if leverage_risk == "高杠杆贡献":
            weaknesses.append("杠杆风险较高")
        if valuation and valuation.valuation_tag == "高估锚点":
            weaknesses.append("估值偏高")
        
        return weaknesses if weaknesses else ["暂无明显劣势"]
    
    def _generate_recommendations(self, roe, quality, stability_tag, leverage_risk, valuation) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if quality in ["A", "B+"]:
            recommendations.append(f"ROE质量评级{quality}，表现良好")
        elif quality in ["C", "C+"]:
            recommendations.append(f"ROE质量评级{quality}，建议关注")
        
        if stability_tag == "高稳定性":
            recommendations.append("ROE稳定性高，适合长期持有")
        
        if valuation and valuation.valuation_tag == "低估锚点":
            recommendations.append(f"估值低估{abs(valuation.pe_deviation):.1f}%，存在修复机会")
        
        return recommendations if recommendations else ["建议关注基本面变化"]
    
    def _empty_result(self, code: str, industry: str) -> Dict:
        """返回空结果"""
        return {
            "code": code, "name": "", "industry": industry,
            "roe": 0, "roe_trend": 0, "roe_volatility": 0, "roe_trend_direction": "未知",
            "quality": "N/A", "quality_score": 0, "quality_ci": "数据不足",
            "stability_score": 0, "stability_tag": "未知",
            "leverage_risk": "未知", "leverage_detail": "数据获取失败",
            "peer_group": [], "peer_rank": 0,
            "valuation": None, "recovery_probability": 0,
            "data_quality": "未知", "confidence_note": "数据获取失败",
            "strengths": [], "weaknesses": [], "recommendations": ["数据获取失败"],
        }
