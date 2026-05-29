"""
行业对标分析模块
对比同行业A股公司的披露深度和得分，生成差异化建议
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from ..data.collector import DataCollector, CompanyInfo, IndustryBenchmark


@dataclass
class BenchmarkComparison:
    """对标比较结果"""
    company_code: str
    company_name: str
    industry: str
    market_type: str
    company_score: float
    industry_average: float
    industry_rank: int
    total_companies: int
    percentile: float
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DifferentiationSuggestion:
    """差异化建议"""
    category: str
    suggestion: str
    expected_impact: str
    priority: str  # high, medium, low


class BenchmarkAnalyzer:
    """
    行业对标分析器
    
    对比同行业A股公司的披露深度和得分，生成差异化建议
    """
    
    def __init__(self, data_collector: DataCollector):
        """
        初始化对标分析器
        
        Args:
            data_collector: 数据收集器实例
        """
        self.data_collector = data_collector
    
    def compare_with_industry(
        self, 
        company_code: str, 
        company_score: float,
        year: int = 2024
    ) -> BenchmarkComparison:
        """
        与行业对标
        
        Args:
            company_code: 公司代码
            company_score: 公司ESG评分
            year: 年份
            
        Returns:
            BenchmarkComparison: 对标比较结果
        """
        company = self.data_collector.get_company_info(company_code)
        if not company:
            raise ValueError(f"未找到公司信息: {company_code}")
        
        benchmark = self.data_collector.get_industry_benchmark(
            company.industry, company.market_type, year
        )
        
        # 如果没有行业对标数据，使用默认值
        if not benchmark:
            industry_average = 65.0
            total_companies = 100
        else:
            industry_average = benchmark.average_score
            total_companies = 100  # 简化处理
        
        # 计算排名和百分位
        if company_score >= industry_average:
            rank = int(total_companies * 0.3)
        else:
            rank = int(total_companies * 0.7)
        
        percentile = (1 - rank / total_companies) * 100
        
        # 生成优势和劣势分析
        strengths, weaknesses = self._analyze_strengths_weaknesses(
            company_score, industry_average
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            company_score, industry_average, weaknesses
        )
        
        return BenchmarkComparison(
            company_code=company_code,
            company_name=company.company_name,
            industry=company.industry,
            market_type=company.market_type,
            company_score=company_score,
            industry_average=industry_average,
            industry_rank=rank,
            total_companies=total_companies,
            percentile=round(percentile, 2),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )
    
    def _analyze_strengths_weaknesses(
        self, 
        company_score: float, 
        industry_average: float
    ) -> Tuple[List[str], List[str]]:
        """分析优势和劣势"""
        strengths = []
        weaknesses = []
        
        score_diff = company_score - industry_average
        
        if score_diff > 10:
            strengths.append("ESG评分显著高于行业平均水平")
            strengths.append("在ESG披露方面具有领先优势")
        elif score_diff > 0:
            strengths.append("ESG评分略高于行业平均水平")
        
        if score_diff < -10:
            weaknesses.append("ESG评分显著低于行业平均水平")
            weaknesses.append("需要大幅提升ESG披露质量")
        elif score_diff < 0:
            weaknesses.append("ESG评分略低于行业平均水平")
        
        return strengths, weaknesses
    
    def _generate_recommendations(
        self, 
        company_score: float, 
        industry_average: float,
        weaknesses: List[str]
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if company_score < industry_average:
            recommendations.append("建议加强ESG信息披露，提升披露质量")
            recommendations.append("参考行业领先企业的披露实践")
        
        if company_score < 60:
            recommendations.append("建议建立完善的ESG治理体系")
            recommendations.append("建议聘请专业ESG咨询机构提供指导")
        
        if company_score >= 80:
            recommendations.append("继续保持ESG披露优势，争取行业标杆地位")
            recommendations.append("考虑发布独立的ESG报告，展示ESG成果")
        
        return recommendations
    
    def get_industry_ranking(
        self, 
        industry: str, 
        market_type: str,
        year: int = 2024
    ) -> List[Dict]:
        """
        获取行业排名
        
        Args:
            industry: 行业
            market_type: 市场类型
            year: 年份
            
        Returns:
            List[Dict]: 排名列表
        """
        # 这里需要从数据库获取行业所有公司的评分
        # 简化处理，返回示例数据
        ranking = [
            {"rank": 1, "company_code": "000001", "company_name": "示例公司A", "score": 92.5},
            {"rank": 2, "company_code": "000002", "company_name": "示例公司B", "score": 88.3},
            {"rank": 3, "company_code": "000003", "company_name": "示例公司C", "score": 85.1},
            {"rank": 4, "company_code": "000004", "company_name": "示例公司D", "score": 78.6},
            {"rank": 5, "company_code": "000005", "company_name": "示例公司E", "score": 72.4},
        ]
        
        return ranking
    
    def generate_differentiation_suggestions(
        self, 
        company_code: str,
        industry: str,
        market_type: str
    ) -> List[DifferentiationSuggestion]:
        """
        生成差异化建议
        
        Args:
            company_code: 公司代码
            industry: 行业
            market_type: 市场类型
            
        Returns:
            List[DifferentiationSuggestion]: 差异化建议列表
        """
        suggestions = []
        
        # 根据行业生成差异化建议
        industry_suggestions = {
            "银行": [
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="突出绿色金融产品创新，如绿色信贷、绿色债券",
                    expected_impact="提升ESG投资者认可度",
                    priority="high",
                ),
                DifferentiationSuggestion(
                    category="社会(S)",
                    suggestion="强调普惠金融服务，支持小微企业和乡村振兴",
                    expected_impact="展示社会责任担当",
                    priority="medium",
                ),
            ],
            "电子": [
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="披露电子废弃物回收和有害物质管理措施",
                    expected_impact="展示环保责任",
                    priority="high",
                ),
                DifferentiationSuggestion(
                    category="社会(S)",
                    suggestion="强调数据安全和隐私保护措施",
                    expected_impact="提升投资者信任",
                    priority="high",
                ),
            ],
            "化工": [
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="重点披露污染排放控制和清洁生产措施",
                    expected_impact="降低环境风险感知",
                    priority="high",
                ),
                DifferentiationSuggestion(
                    category="社会(S)",
                    suggestion="强调安全生产管理和职业健康保护",
                    expected_impact="展示安全责任",
                    priority="high",
                ),
            ],
            "钢铁": [
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="突出碳减排目标和节能技改项目",
                    expected_impact="展示低碳转型决心",
                    priority="high",
                ),
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="披露能源消耗强度下降措施",
                    expected_impact="展示能效提升成果",
                    priority="medium",
                ),
            ],
            "汽车": [
                DifferentiationSuggestion(
                    category="环境(E)",
                    suggestion="强调新能源汽车发展和电池回收措施",
                    expected_impact="展示绿色转型成果",
                    priority="high",
                ),
                DifferentiationSuggestion(
                    category="社会(S)",
                    suggestion="披露智能驾驶安全测试和数据安全措施",
                    expected_impact="展示技术创新责任",
                    priority="medium",
                ),
            ],
        }
        
        # 获取行业特定建议
        if industry in industry_suggestions:
            suggestions.extend(industry_suggestions[industry])
        
        # 通用建议
        suggestions.append(
            DifferentiationSuggestion(
                category="治理(G)",
                suggestion="完善ESG治理架构，明确董事会ESG职责",
                expected_impact="提升公司治理水平",
                priority="medium",
            )
        )
        
        return suggestions
    
    def get_disclosure_depth_analysis(
        self, 
        company_code: str,
        industry: str
    ) -> Dict:
        """
        分析披露深度
        
        Args:
            company_code: 公司代码
            industry: 行业
            
        Returns:
            Dict: 披露深度分析结果
        """
        # 示例分析结果
        analysis = {
            "overall_depth": "中等",
            "dimensions": {
                "环境(E)": {
                    "score": 65,
                    "items_disclosed": ["碳排放", "能源消耗"],
                    "items_missing": ["水资源", "废弃物", "生物多样性"],
                },
                "社会(S)": {
                    "score": 70,
                    "items_disclosed": ["员工信息", "安全生产"],
                    "items_missing": ["供应链管理", "社区关系"],
                },
                "治理(G)": {
                    "score": 75,
                    "items_disclosed": ["董事会结构", "商业道德"],
                    "items_missing": ["数据安全"],
                },
            },
            "comparison_with_peers": {
                "scope_3_disclosed": False,
                "scope_3_peer_average": 45,
                "benchmark_status": "低于同行",
            },
        }
        
        return analysis
