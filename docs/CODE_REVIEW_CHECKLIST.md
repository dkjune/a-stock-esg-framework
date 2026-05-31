# 代码审查检查清单

防止硬编码bug的长效机制

## 1. 数据获取检查

### 检查点
- [ ] API返回数据是否经过验证
- [ ] 数据类型转换是否有异常处理
- [ ] 空值/None是否正确处理
- [ ] 数值范围是否合理

### 常见陷阱
```python
# ❌ 错误：硬编码默认值
asset_turnover = 0.6
debt_ratio = 45.0

# ✓ 正确：基于行业经验值或API获取
asset_turnover = get_industry_average("电力", "asset_turnover")
debt_ratio = get_financial_data(code, "debt_ratio")
```

## 2. 财务指标计算检查

### 杜邦恒等式验证
```
ROE = 净利率 × 资产周转率 × 权益乘数
```

### 检查点
- [ ] 净利率、资产周转率、权益乘数是否在合理范围
- [ ] 三者乘积是否等于ROE
- [ ] 权益乘数 = 1 / (1 - 负债率)

### 行业合理范围
| 行业 | ROE | 净利率 | 资产周转率 | 负债率 |
|------|-----|--------|------------|--------|
| 电力 | 5-30% | 5-70% | 0.1-1.0 | 20-80% |
| 银行 | 8-20% | 20-50% | 0.02-0.1 | 85-95% |
| 白酒 | 15-40% | 20-50% | 0.3-1.0 | 20-50% |

## 3. 数据验证流程

### 每次数据获取后
```python
from a_stock_esg import validator

# 验证财务数据
results = validator.validate_financial_snapshot(
    code="600900",
    roe=roe,
    net_margin=net_margin,
    asset_turnover=asset_turnover,
    debt_ratio=debt_ratio,
    pe=pe,
    pb=pb,
    industry="电力"
)

summary = validator.get_validation_summary(results)
if not summary["all_passed"]:
    print(f"数据验证失败: {summary['invalid_fields']}")
    # 处理异常
```

## 4. 代码审查要点

### 必须检查
1. **硬编码数值** - 是否有魔法数字
2. **默认值** - 是否合理，是否有注释说明来源
3. **异常处理** - API失败时的fallback是否合理
4. **数据验证** - 是否调用验证器

### 审查问题
1. "这个0.6是怎么来的？"
2. "如果API返回空值会怎样？"
3. "这个计算公式有验证过吗？"
4. "行业基准数据来源是什么？"

## 5. 提交前检查

```bash
# 运行数据验证测试
python tests/test_data.py

# 检查是否有硬编码
grep -n "= 0\.\|= [0-9]\+\." src/a_stock_esg/*.py
```
