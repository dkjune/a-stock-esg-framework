"""
数据验证测试
确保财务数据推算的准确性
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import stock_data
from a_stock_esg.validator import validator


def test_financial_data():
    """测试财务数据推算"""
    print("=" * 70)
    print("财务数据验证测试")
    print("=" * 70)
    
    test_cases = [
        ("600900", "长江电力", "电力"),
        ("600011", "华能国际", "电力"),
        ("600886", "国投电力", "电力"),
        ("600863", "华能蒙电", "电力"),
    ]
    
    all_passed = True
    
    for code, name, industry in test_cases:
        print(f"\n{name} ({code}):")
        
        quote = stock_data.get_quote(code)
        financial = stock_data.get_financial_snapshot(code)
        
        if not quote or not financial:
            print("  ✗ 数据获取失败")
            all_passed = False
            continue
        
        # 验证数据
        results = validator.validate_financial_snapshot(
            code=code,
            roe=financial.roe,
            net_margin=financial.net_margin,
            asset_turnover=financial.asset_turnover,
            debt_ratio=financial.debt_ratio,
            pe=quote.pe_ttm,
            pb=quote.pb,
            industry=industry,
        )
        
        summary = validator.get_validation_summary(results)
        
        for r in results:
            print(f"  {r.message}")
        
        if summary["all_passed"]:
            print(f"  ✓ 验证通过 ({summary['valid']}/{summary['total']})")
        else:
            print(f"  ✗ 验证失败: {summary['invalid_fields']}")
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ 所有测试通过")
    else:
        print("✗ 存在测试失败")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    test_financial_data()
