"""
个人投资者评分工具
为普通投资者提供轻量化的A股非财务信息披露评分
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class InvestmentStyle(Enum):
    """投资风格"""
    VALUE = "价值投资"
    GROWTH = "成长投资"
    BALANCED = "均衡投资"
    INCOME = "收益型投资"


@dataclass
class InvestorProfile:
    """投资者画像"""
    risk_tolerance: str  # 保守、稳健、激进
    investment_horizon: str  # 短期、中期、长期
    focus_areas: List[str]  # 关注领域
    investment_style: InvestmentStyle


@dataclass
class StockScore:
    """股票评分"""
    stock_code: str
    stock_name: str
    overall_score: float
    dimension_scores: Dict[str, float]
    rank: str  # AAA, AA, A, BBB, BB, B, CCC, CC, C
    risk_level: str
    highlights: List[str]
    warnings: List[str]
    recommendation: str


@dataclass
class ScoringResult:
    """评分结果"""
    stocks: List[StockScore]
    market_overview: Dict
    top_picks: List[str]
    risk_stocks: List[str]


class PersonalInvestorScorer:
    """
    个人投资者评分工具
    
    批量处理全A股非财务信息，输出直观综合评分
    """
    
    def __init__(self):
        """初始化评分器"""
        self.dimension_weights = {
            "policy_match": 0.25,  # 政策匹配度
            "disclosure_quality": 0.20,  # 披露质量
            "roe_performance": 0.25,  # ROE表现
            "governance_score": 0.15,  # 治理评分
            "risk_level": 0.15,  # 风险水平
        }
    
    def score_stock(
        self,
        stock_code: str,
        stock_name: str,
        analysis_data: Dict,
    ) -> StockScore:
        """
        为单只股票评分
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            analysis_data: 分析数据
            
        Returns:
            StockScore: 评分结果
        """
        # 计算各维度得分
        dimension_scores = {}
        
        # 政策匹配度得分
        dimension_scores["policy_match"] = analysis_data.get("policy_match_score", 50)
        
        # 披露质量得分
        dimension_scores["disclosure_quality"] = analysis_data.get("disclosure_quality_score", 50)
        
        # ROE表现得分
        dimension_scores["roe_performance"] = analysis_data.get("roe_score", 50)
        
        # 治理评分
        dimension_scores["governance_score"] = analysis_data.get("governance_score", 50)
        
        # 风险水平得分（风险越低得分越高）
        risk_score = 100 - analysis_data.get("risk_score", 50)
        dimension_scores["risk_level"] = risk_score
        
        # 计算总分
        overall_score = sum(
            dimension_scores[dim] * weight
            for dim, weight in self.dimension_weights.items()
        )
        
        # 确定等级
        rank = self._determine_rank(overall_score)
        
        # 确定风险水平
        risk_level = self._determine_risk_level(dimension_scores["risk_level"])
        
        # 生成亮点和警告
        highlights = self._identify_highlights(dimension_scores, analysis_data)
        warnings = self._identify_warnings(dimension_scores, analysis_data)
        
        # 生成建议
        recommendation = self._generate_recommendation(
            overall_score, rank, risk_level, highlights, warnings
        )
        
        return StockScore(
            stock_code=stock_code,
            stock_name=stock_name,
            overall_score=round(overall_score, 2),
            dimension_scores=dimension_scores,
            rank=rank,
            risk_level=risk_level,
            highlights=highlights,
            warnings=warnings,
            recommendation=recommendation,
        )
    
    def _determine_rank(self, score: float) -> str:
        """确定等级"""
        if score >= 90:
            return "AAA"
        elif score >= 80:
            return "AA"
        elif score >= 70:
            return "A"
        elif score >= 60:
            return "BBB"
        elif score >= 50:
            return "BB"
        elif score >= 40:
            return "B"
        elif score >= 30:
            return "CCC"
        elif score >= 20:
            return "CC"
        else:
            return "C"
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """确定风险水平"""
        if risk_score >= 80:
            return "低风险"
        elif risk_score >= 60:
            return "中低风险"
        elif risk_score >= 40:
            return "中风险"
        elif risk_score >= 20:
            return "中高风险"
        else:
            return "高风险"
    
    def _identify_highlights(
        self,
        dimension_scores: Dict[str, float],
        analysis_data: Dict,
    ) -> List[str]:
        """识别亮点"""
        highlights = []
        
        if dimension_scores.get("policy_match", 0) >= 80:
            highlights.append("政策匹配度高，符合中特估方向")
        
        if dimension_scores.get("roe_performance", 0) >= 80:
            highlights.append("ROE表现优秀，盈利能力强")
        
        if dimension_scores.get("disclosure_quality", 0) >= 80:
            highlights.append("信息披露质量高，透明度好")
        
        if dimension_scores.get("governance_score", 0) >= 80:
            highlights.append("公司治理规范，管理水平高")
        
        return highlights
    
    def _identify_warnings(
        self,
        dimension_scores: Dict[str, float],
        analysis_data: Dict,
    ) -> List[str]:
        """识别警告"""
        warnings = []
        
        if dimension_scores.get("policy_match", 0) < 40:
            warnings.append("政策匹配度低，可能不符合中特估方向")
        
        if dimension_scores.get("roe_performance", 0) < 40:
            warnings.append("ROE表现不佳，盈利能力待改善")
        
        if dimension_scores.get("disclosure_quality", 0) < 40:
            warnings.append("信息披露质量差，透明度不足")
        
        if dimension_scores.get("risk_level", 0) < 30:
            warnings.append("风险水平较高，需谨慎投资")
        
        return warnings
    
    def _generate_recommendation(
        self,
        overall_score: float,
        rank: str,
        risk_level: str,
        highlights: List[str],
        warnings: List[str],
    ) -> str:
        """生成建议"""
        if overall_score >= 80:
            return "强烈推荐：综合表现优秀，值得重点关注"
        elif overall_score >= 70:
            return "推荐：综合表现良好，可适当配置"
        elif overall_score >= 60:
            return "中性：综合表现一般，需结合其他因素判断"
        elif overall_score >= 50:
            return "谨慎：存在一定风险，建议谨慎考虑"
        else:
            return "回避：综合表现较差，建议回避"
    
    def batch_score(
        self,
        stocks_data: List[Dict],
    ) -> ScoringResult:
        """
        批量评分
        
        Args:
            stocks_data: 股票数据列表
            
        Returns:
            ScoringResult: 评分结果
        """
        scored_stocks = []
        
        for stock_data in stocks_data:
            score = self.score_stock(
                stock_code=stock_data.get("code", ""),
                stock_name=stock_data.get("name", ""),
                analysis_data=stock_data.get("analysis", {}),
            )
            scored_stocks.append(score)
        
        # 按得分排序
        scored_stocks.sort(key=lambda x: x.overall_score, reverse=True)
        
        # 计算市场概览
        market_overview = self._calculate_market_overview(scored_stocks)
        
        # 选出Top推荐
        top_picks = [s.stock_code for s in scored_stocks[:5]]
        
        # 选出风险股
        risk_stocks = [s.stock_code for s in scored_stocks if s.risk_level == "高风险"]
        
        return ScoringResult(
            stocks=scored_stocks,
            market_overview=market_overview,
            top_picks=top_picks,
            risk_stocks=risk_stocks,
        )
    
    def _calculate_market_overview(
        self,
        stocks: List[StockScore],
    ) -> Dict:
        """计算市场概览"""
        if not stocks:
            return {}
        
        scores = [s.overall_score for s in stocks]
        
        return {
            "total_stocks": len(stocks),
            "average_score": round(sum(scores) / len(scores), 2),
            "high_score_count": sum(1 for s in scores if s >= 80),
            "low_score_count": sum(1 for s in scores if s < 50),
            "distribution": {
                "AAA": sum(1 for s in stocks if s.rank == "AAA"),
                "AA": sum(1 for s in stocks if s.rank == "AA"),
                "A": sum(1 for s in stocks if s.rank == "A"),
                "BBB": sum(1 for s in stocks if s.rank == "BBB"),
                "BB及以下": sum(1 for s in stocks if s.rank in ["BB", "B", "CCC", "CC", "C"]),
            }
        }


class StockFactorGenerator:
    """
    选股因子生成器
    
    将非财务披露质量转化为量化选股因子
    """
    
    def __init__(self):
        """初始化因子生成器"""
        self.factor_names = [
            "policy_match_factor",
            "disclosure_quality_factor",
            "roe_sustainability_factor",
            "governance_factor",
            "risk_factor",
        ]
    
    def generate_factors(
        self,
        stock_scores: List[StockScore],
    ) -> List[Dict]:
        """
        生成选股因子
        
        Args:
            stock_scores: 股票评分列表
            
        Returns:
            List[Dict]: 因子数据列表
        """
        factors = []
        
        for score in stock_scores:
            factor = {
                "stock_code": score.stock_code,
                "stock_name": score.stock_name,
                "policy_match_factor": score.dimension_scores.get("policy_match", 50) / 100,
                "disclosure_quality_factor": score.dimension_scores.get("disclosure_quality", 50) / 100,
                "roe_sustainability_factor": score.dimension_scores.get("roe_performance", 50) / 100,
                "governance_factor": score.dimension_scores.get("governance_score", 50) / 100,
                "risk_factor": score.dimension_scores.get("risk_level", 50) / 100,
                "composite_factor": score.overall_score / 100,
            }
            factors.append(factor)
        
        return factors
    
    def calculate_factor_returns(
        self,
        factors: List[Dict],
        returns: Dict[str, float],
    ) -> Dict:
        """
        计算因子收益
        
        Args:
            factors: 因子数据
            returns: 股票收益率
            
        Returns:
            Dict: 因子收益分析
        """
        factor_returns = {}
        
        for factor_name in self.factor_names:
            # 按因子值排序
            sorted_factors = sorted(
                factors,
                key=lambda x: x.get(factor_name, 0),
                reverse=True,
            )
            
            # 计算多空组合收益
            top_half = sorted_factors[:len(sorted_factors)//2]
            bottom_half = sorted_factors[len(sorted_factors)//2:]
            
            top_return = sum(
                returns.get(f["stock_code"], 0) for f in top_half
            ) / len(top_half) if top_half else 0
            
            bottom_return = sum(
                returns.get(f["stock_code"], 0) for f in bottom_half
            ) / len(bottom_half) if bottom_half else 0
            
            factor_returns[factor_name] = {
                "long_return": round(top_return * 100, 2),
                "short_return": round(bottom_return * 100, 2),
                "spread": round((top_return - bottom_return) * 100, 2),
            }
        
        return factor_returns
