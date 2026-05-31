"""
噪声报告生成器
基于《噪声》理论：输出不确定性，让框架自知其局限
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class NoiseReport:
    """噪声报告"""
    code: str
    name: str
    # ROE噪声
    roe_score: float
    roe_ci: str  # 置信区间说明
    roe_data_quality: str
    # 政策噪声
    policy_score: float
    model_agreement: float
    policy_confidence: str
    # 整体噪声
    overall_noise_level: str  # 低/中/高
    overall_confidence: str  # 高/中/低
    # 决策建议
    recommendation: str
    risk_warnings: List[str]


class NoiseReportGenerator:
    """
    噪声报告生成器
    
    基于《噪声》理论：
    - 输出不确定性
    - 让框架自知其局限
    - 决策卫生清单
    """
    
    def __init__(self):
        pass
    
    def generate(self, roe_result: Dict, policy_result: Dict) -> NoiseReport:
        """
        生成噪声报告
        """
        code = roe_result.get("code", "")
        name = roe_result.get("name", "")
        
        # ROE噪声评估
        roe_score = roe_result.get("roe", 0)
        roe_ci = roe_result.get("quality_ci", "未知")
        roe_data_quality = roe_result.get("data_quality", "未知")
        
        # 政策噪声评估
        policy_score = policy_result.overall_score
        model_agreement = policy_result.model_agreement
        policy_confidence = policy_result.confidence
        
        # 整体噪声评估
        overall_noise, overall_confidence = self._assess_overall_noise(
            roe_data_quality, model_agreement, policy_confidence
        )
        
        # 风险警告
        risk_warnings = self._generate_risk_warnings(
            roe_result, policy_result, overall_noise
        )
        
        # 决策建议
        recommendation = self._generate_recommendation(
            overall_confidence, roe_score, policy_score
        )
        
        return NoiseReport(
            code=code,
            name=name,
            roe_score=roe_score,
            roe_ci=roe_ci,
            roe_data_quality=roe_data_quality,
            policy_score=policy_score,
            model_agreement=model_agreement,
            policy_confidence=policy_confidence,
            overall_noise_level=overall_noise,
            overall_confidence=overall_confidence,
            recommendation=recommendation,
            risk_warnings=risk_warnings,
        )
    
    def _assess_overall_noise(
        self, 
        data_quality: str, 
        model_agreement: float, 
        policy_confidence: str
    ) -> Tuple[str, str]:
        """评估整体噪声水平"""
        noise_score = 0
        
        # 数据质量
        if data_quality == "低置信":
            noise_score += 3
        elif data_quality == "中置信":
            noise_score += 1
        
        # 模型一致性
        if model_agreement < 60:
            noise_score += 3
        elif model_agreement < 80:
            noise_score += 1
        
        # 政策置信度
        if policy_confidence == "低":
            noise_score += 2
        elif policy_confidence == "中":
            noise_score += 1
        
        # 综合评估
        if noise_score >= 5:
            return "高", "低"
        elif noise_score >= 3:
            return "中", "中"
        else:
            return "低", "高"
    
    def _generate_risk_warnings(
        self, 
        roe_result: Dict, 
        policy_result: Dict,
        overall_noise: str
    ) -> List[str]:
        """生成风险警告"""
        warnings = []
        
        # 数据质量警告
        if roe_result.get("data_quality") == "低置信":
            warnings.append("⚠️ 数据质量较低，分析结果仅供参考")
        
        # 噪声警告
        if overall_noise == "高":
            warnings.append("⚠️ 分析噪声较高，建议结合其他信息源")
        
        # 负面信号警告
        if policy_result.negative_signals:
            warnings.append(f"⚠️ 存在负面信号: {', '.join(policy_result.negative_signals[:2])}")
        
        # 模型不一致警告
        if policy_result.model_agreement < 60:
            warnings.append("⚠️ 双模型评分不一致，建议人工复核")
        
        return warnings
    
    def _generate_recommendation(self, confidence: str, roe: float, policy: float) -> str:
        """生成决策建议"""
        if confidence == "高" and roe > 10 and policy > 5:
            return "综合评估良好，可考虑配置"
        elif confidence == "中":
            return "综合评估中等，建议结合其他信息决策"
        else:
            return "综合评估置信度低，建议谨慎决策或寻求专业意见"
    
    def format_report(self, report: NoiseReport) -> str:
        """格式化报告输出"""
        lines = [
            f"{'='*60}",
            f"  噪声分析报告 - {report.name} ({report.code})",
            f"{'='*60}",
            "",
            f"【ROE分析】",
            f"  评分: {report.roe_score:.2f}%",
            f"  质量分级: {report.roe_ci}",
            f"  数据质量: {report.roe_data_quality}",
            "",
            f"【政策匹配】",
            f"  评分: {report.policy_score:.1f}/100",
            f"  模型一致性: {report.model_agreement:.1f}%",
            f"  置信度: {report.policy_confidence}",
            "",
            f"【噪声评估】",
            f"  整体噪声水平: {report.overall_noise_level}",
            f"  综合置信度: {report.overall_confidence}",
            "",
            f"【风险警告】",
        ]
        
        for warning in report.risk_warnings:
            lines.append(f"  {warning}")
        
        if not report.risk_warnings:
            lines.append("  暂无显著风险")
        
        lines.extend([
            "",
            f"【决策建议】",
            f"  {report.recommendation}",
            "",
            f"{'='*60}",
        ])
        
        return "\n".join(lines)


# 类型提示
from typing import Tuple
