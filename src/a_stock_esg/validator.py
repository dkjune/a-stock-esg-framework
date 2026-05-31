"""
数据验证模块
确保财务数据推算的准确性和合理性
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    field: str
    value: float
    expected_range: Tuple[float, float]
    message: str


class DataValidator:
    """
    数据验证器
    
    用于检查财务数据推算是否合理
    """
    
    # 电力行业财务指标合理范围（基于实际财报数据）
    INDUSTRY_RANGES = {
        "电力": {
            "roe": (5.0, 30.0),           # ROE: 5%-30%
            "net_margin": (5.0, 70.0),     # 净利率: 5%-70%（水电高，火电低）
            "asset_turnover": (0.1, 1.0),  # 资产周转率: 0.1-1.0
            "debt_ratio": (20.0, 80.0),    # 负债率: 20%-80%
            "pe": (5.0, 50.0),             # PE: 5-50
            "pb": (0.5, 10.0),             # PB: 0.5-10
        },
        "银行": {
            "roe": (8.0, 20.0),
            "net_margin": (20.0, 50.0),
            "asset_turnover": (0.02, 0.1),
            "debt_ratio": (85.0, 95.0),
            "pe": (3.0, 15.0),
            "pb": (0.3, 2.0),
        },
        "白酒": {
            "roe": (15.0, 40.0),
            "net_margin": (20.0, 50.0),
            "asset_turnover": (0.3, 1.0),
            "debt_ratio": (20.0, 50.0),
            "pe": (20.0, 60.0),
            "pb": (5.0, 20.0),
        },
    }
    
    # 杜邦恒等式验证容差
    DUPONT_TOLERANCE = 1.0  # 允许1%的误差
    
    def __init__(self):
        pass
    
    def validate_financial_snapshot(
        self,
        code: str,
        roe: float,
        net_margin: float,
        asset_turnover: float,
        debt_ratio: float,
        pe: float,
        pb: float,
        industry: str = "电力",
    ) -> List[ValidationResult]:
        """
        验证财务快照数据
        
        Args:
            code: 股票代码
            roe: ROE
            net_margin: 净利率
            asset_turnover: 资产周转率
            debt_ratio: 负债率
            pe: PE
            pb: PB
            industry: 行业
            
        Returns:
            List[ValidationResult]: 验证结果列表
        """
        results = []
        ranges = self.INDUSTRY_RANGES.get(industry, self.INDUSTRY_RANGES["电力"])
        
        # 验证各指标范围
        validations = [
            ("roe", roe, ranges["roe"]),
            ("net_margin", net_margin, ranges["net_margin"]),
            ("asset_turnover", asset_turnover, ranges["asset_turnover"]),
            ("debt_ratio", debt_ratio, ranges["debt_ratio"]),
            ("pe", pe, ranges["pe"]),
            ("pb", pb, ranges["pb"]),
        ]
        
        for field_name, value, (min_val, max_val) in validations:
            is_valid = min_val <= value <= max_val
            results.append(ValidationResult(
                is_valid=is_valid,
                field=field_name,
                value=value,
                expected_range=(min_val, max_val),
                message=f"{field_name}: {value:.2f} {'✓' if is_valid else '✗'} (范围: {min_val}-{max_val})",
            ))
        
        # 验证杜邦恒等式: ROE = 净利率 × 资产周转率 × 权益乘数
        equity_multiplier = 1 / (1 - debt_ratio / 100) if debt_ratio < 100 else 2.0
        calculated_roe = net_margin * asset_turnover * equity_multiplier
        roe_diff = abs(calculated_roe - roe)
        
        results.append(ValidationResult(
            is_valid=roe_diff <= self.DUPONT_TOLERANCE,
            field="dupont_check",
            value=roe_diff,
            expected_range=(0, self.DUPONT_TOLERANCE),
            message=f"杜邦恒等式验证: 计算ROE={calculated_roe:.2f}%, 实际ROE={roe:.2f}%, 差异={roe_diff:.2f}% {'✓' if roe_diff <= self.DUPONT_TOLERANCE else '✗'}",
        ))
        
        # 验证ROE与PE/PB关系: ROE = PB/PE * 100
        if pe > 0 and pb > 0:
            implied_roe = (pb / pe) * 100
            pe_pb_diff = abs(implied_roe - roe)
            results.append(ValidationResult(
                is_valid=pe_pb_diff <= 2.0,
                field="pe_pb_check",
                value=pe_pb_diff,
                expected_range=(0, 2.0),
                message=f"PE/PB验证: 隐含ROE={implied_roe:.2f}%, 实际ROE={roe:.2f}%, 差异={pe_pb_diff:.2f}% {'✓' if pe_pb_diff <= 2.0 else '✗'}",
            ))
        
        return results
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict:
        """获取验证摘要"""
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        invalid = [r for r in results if not r.is_valid]
        
        return {
            "total": total,
            "valid": valid,
            "invalid": len(invalid),
            "pass_rate": round(valid / total * 100, 1) if total > 0 else 0,
            "invalid_fields": [r.field for r in invalid],
            "all_passed": len(invalid) == 0,
        }


# 全局验证器实例
validator = DataValidator()
