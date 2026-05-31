"""
达尔文进化脚本 - ESG框架Skill优化

受 darwin-skill 启发的自主进化系统
评估 → 改进 → 测试 → 保留或回滚

使用方法:
    python scripts/evolve.py --skill SKILL.md --test test-prompts.json
"""

import json
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class EvaluationResult:
    """评估结果"""
    dimension: str
    score: float
    max_score: float
    feedback: str
    suggestions: List[str]


@dataclass
class EvolutionRound:
    """进化轮次"""
    round_id: int
    timestamp: str
    dimension_improved: str
    score_before: float
    score_after: float
    diff: float
    committed: bool


class DarwinEvolver:
    """
    达尔文进化器
    
    基于darwin-skill的9维度评估体系，自动评估和改进ESG框架Skill
    """
    
    # 9维度评估标准（满分100）
    DIMENSIONS = {
        "completeness": {"weight": 15, "description": "完整性 - 覆盖所有必要的功能和场景"},
        "clarity": {"weight": 12, "description": "清晰性 - 指令明确，无歧义"},
        "specificity": {"weight": 12, "description": "可执行具体性 - 禁用模糊词"},
        "error_handling": {"weight": 10, "description": "失败模式编码 - 显式编码已知失败路径"},
        "safety": {"weight": 10, "description": "安全性 - 高风险行动黑名单"},
        "examples": {"weight": 10, "description": "示例质量 - 提供可执行的代码示例"},
        "edge_cases": {"weight": 8, "description": "边界处理 - 处理空值、无效输入等"},
        "consistency": {"weight": 8, "description": "一致性 - 格式、术语、风格统一"},
        "practicality": {"weight": 15, "description": "实用性 - 实际效果验证"},
    }
    
    # 反例黑名单
    ANTI_PATTERNS = [
        "同一个 AI 又改又评",
        "用 git reset --hard 当回滚手段",
        "为凑分而堆冗余",
        "跳过测试提示词直接评分",
        "一轮内改多个维度",
        "干跑比例 > 30%",
        "静默跳过异常",
        "忽视维度相关簇",
    ]
    
    def __init__(self, skill_path: str, test_path: str):
        """
        初始化进化器
        
        Args:
            skill_path: SKILL.md 文件路径
            test_path: test-prompts.json 文件路径
        """
        self.skill_path = Path(skill_path)
        self.test_path = Path(test_path)
        self.history: List[EvolutionRound] = []
        self.current_score = 0.0
        
    def load_skill(self) -> str:
        """加载Skill内容"""
        return self.skill_path.read_text(encoding="utf-8")
    
    def load_tests(self) -> List[Dict]:
        """加载测试集"""
        return json.loads(self.test_path.read_text(encoding="utf-8"))
    
    def evaluate_skill(self, skill_content: str) -> List[EvaluationResult]:
        """
        评估Skill（静态分析）
        
        基于9维度进行结构评分
        """
        results = []
        
        # 1. 完整性评估
        completeness_score = self._evaluate_completeness(skill_content)
        results.append(EvaluationResult(
            dimension="completeness",
            score=completeness_score,
            max_score=15,
            feedback=self._get_completeness_feedback(completeness_score),
            suggestions=self._get_completeness_suggestions(skill_content),
        ))
        
        # 2. 清晰性评估
        clarity_score = self._evaluate_clarity(skill_content)
        results.append(EvaluationResult(
            dimension="clarity",
            score=clarity_score,
            max_score=12,
            feedback=self._get_clarity_feedback(clarity_score),
            suggestions=self._get_clarity_suggestions(skill_content),
        ))
        
        # 3. 可执行具体性评估
        specificity_score = self._evaluate_specificity(skill_content)
        results.append(EvaluationResult(
            dimension="specificity",
            score=specificity_score,
            max_score=12,
            feedback=self._get_specificity_feedback(specificity_score),
            suggestions=self._get_specificity_suggestions(skill_content),
        ))
        
        # 4. 失败模式编码评估
        error_score = self._evaluate_error_handling(skill_content)
        results.append(EvaluationResult(
            dimension="error_handling",
            score=error_score,
            max_score=10,
            feedback=self._get_error_feedback(error_score),
            suggestions=self._get_error_suggestions(skill_content),
        ))
        
        # 5. 安全性评估
        safety_score = self._evaluate_safety(skill_content)
        results.append(EvaluationResult(
            dimension="safety",
            score=safety_score,
            max_score=10,
            feedback=self._get_safety_feedback(safety_score),
            suggestions=self._get_safety_suggestions(skill_content),
        ))
        
        # 6. 示例质量评估
        examples_score = self._evaluate_examples(skill_content)
        results.append(EvaluationResult(
            dimension="examples",
            score=examples_score,
            max_score=10,
            feedback=self._get_examples_feedback(examples_score),
            suggestions=self._get_examples_suggestions(skill_content),
        ))
        
        # 7. 边界处理评估
        edge_score = self._evaluate_edge_cases(skill_content)
        results.append(EvaluationResult(
            dimension="edge_cases",
            score=edge_score,
            max_score=8,
            feedback=self._get_edge_feedback(edge_score),
            suggestions=self._get_edge_suggestions(skill_content),
        ))
        
        # 8. 一致性评估
        consistency_score = self._evaluate_consistency(skill_content)
        results.append(EvaluationResult(
            dimension="consistency",
            score=consistency_score,
            max_score=8,
            feedback=self._get_consistency_feedback(consistency_score),
            suggestions=self._get_consistency_suggestions(skill_content),
        ))
        
        # 9. 实用性评估
        practicality_score = self._evaluate_practicality(skill_content)
        results.append(EvaluationResult(
            dimension="practicality",
            score=practicality_score,
            max_score=15,
            feedback=self._get_practicality_feedback(practicality_score),
            suggestions=self._get_practicality_suggestions(skill_content),
        ))
        
        return results
    
    def _evaluate_completeness(self, content: str) -> float:
        """评估完整性"""
        score = 0.0
        
        # 检查必要章节
        required_sections = [
            "触发条件", "核心能力", "执行步骤", "失败模式处理",
            "禁止操作", "输出规范", "版本信息"
        ]
        for section in required_sections:
            if section in content:
                score += 2
        
        # 检查功能模块
        required_modules = ["合规检查", "NLP提取", "行业对标", "数据集成", "可视化"]
        for module in required_modules:
            if module in content:
                score += 0.6
        
        return min(score, 15)
    
    def _evaluate_clarity(self, content: str) -> float:
        """评估清晰性"""
        score = 0.0
        
        # 检查是否有明确的步骤
        if "执行步骤" in content:
            score += 4
        
        # 检查是否有输入输出说明
        if "输入:" in content and "输出:" in content:
            score += 4
        
        # 检查是否有参数说明
        if "关键参数" in content or "参数说明" in content:
            score += 2
        
        # 检查格式是否清晰
        if "###" in content or "##" in content:
            score += 2
        
        return min(score, 12)
    
    def _evaluate_specificity(self, content: str) -> float:
        """评估可执行具体性"""
        score = 0.0
        
        # 禁用模糊词检查
        vague_words = ["建议", "可以考虑", "根据情况", "灵活把握", "视情况而定"]
        for word in vague_words:
            if word not in content:
                score += 2
        
        # 检查是否有具体示例
        if "示例调用" in content or "示例" in content:
            score += 2
        
        return min(score, 12)
    
    def _evaluate_error_handling(self, content: str) -> float:
        """评估失败模式编码"""
        score = 0.0
        
        # 检查是否有失败模式处理
        if "失败模式处理" in content:
            score += 5
        
        # 检查是否有错误处理说明
        error_keywords = ["若", "如果", "异常", "错误", "失败"]
        for keyword in error_keywords:
            if keyword in content:
                score += 1
        
        return min(score, 10)
    
    def _evaluate_safety(self, content: str) -> float:
        """评估安全性"""
        score = 0.0
        
        # 检查是否有禁止操作
        if "禁止操作" in content:
            score += 5
        
        # 检查是否提到安全相关关键词
        safety_keywords = ["删除", "覆盖", "上传", "提交"]
        for keyword in safety_keywords:
            if f"不能{keyword}" in content or f"禁止{keyword}" in content:
                score += 1.25
        
        return min(score, 10)
    
    def _evaluate_examples(self, content: str) -> float:
        """评估示例质量"""
        score = 0.0
        
        # 检查是否有代码示例
        if "```python" in content:
            score += 5
        
        # 检查是否有输出格式示例
        if "输出格式" in content or "示例输出" in content:
            score += 3
        
        # 检查示例是否可执行
        if "from a_stock_esg import" in content:
            score += 2
        
        return min(score, 10)
    
    def _evaluate_edge_cases(self, content: str) -> float:
        """评估边界处理"""
        score = 0.0
        
        # 检查是否处理空值
        if "空" in content or "空值" in content:
            score += 2
        
        # 检查是否处理无效输入
        if "无效" in content or "不存在" in content:
            score += 2
        
        # 检查是否处理网络异常
        if "超时" in content or "网络" in content:
            score += 2
        
        # 检查是否有默认值
        if "默认" in content:
            score += 2
        
        return min(score, 8)
    
    def _evaluate_consistency(self, content: str) -> float:
        """评估一致性"""
        score = 0.0
        
        # 检查术语一致性
        if "ESG" in content and "环境、社会、治理" in content:
            score += 2
        
        # 检查格式一致性
        if content.count("###") >= 3:
            score += 2
        
        # 检查代码风格一致性
        if content.count("```python") >= 2:
            score += 2
        
        # 检查章节结构一致性
        if "##" in content and "###" in content:
            score += 2
        
        return min(score, 8)
    
    def _evaluate_practicality(self, content: str) -> float:
        """评估实用性"""
        score = 0.0
        
        # 检查是否集成实际数据源
        if "a-stock-data" in content or "腾讯财经" in content:
            score += 5
        
        # 检查是否有实际的API调用
        if "requests.get" in content or "API" in content:
            score += 3
        
        # 检查是否有实际的输出格式
        if "═══" in content or "输出规范" in content:
            score += 3
        
        # 检查是否有版本信息
        if "版本" in content:
            score += 2
        
        # 检查是否有许可证信息
        if "许可证" in content or "License" in content:
            score += 2
        
        return min(score, 15)
    
    def _get_completeness_feedback(self, score: float) -> str:
        if score >= 12:
            return "完整性优秀，覆盖了所有必要功能"
        elif score >= 9:
            return "完整性良好，可补充部分功能"
        else:
            return "完整性不足，需要补充核心功能"
    
    def _get_completeness_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "触发条件" not in content:
            suggestions.append("添加触发条件章节")
        if "失败模式处理" not in content:
            suggestions.append("添加失败模式处理章节")
        if "禁止操作" not in content:
            suggestions.append("添加禁止操作章节")
        return suggestions
    
    def _get_clarity_feedback(self, score: float) -> str:
        if score >= 10:
            return "清晰性优秀，指令明确"
        elif score >= 7:
            return "清晰性良好，可进一步明确"
        else:
            return "清晰性不足，需要重新组织"
    
    def _get_clarity_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "执行步骤" not in content:
            suggestions.append("为每个功能添加明确的执行步骤")
        if "输入:" not in content:
            suggestions.append("添加输入输出说明")
        return suggestions
    
    def _get_specificity_feedback(self, score: float) -> str:
        if score >= 10:
            return "可执行具体性优秀，无模糊表述"
        elif score >= 7:
            return "可执行具体性良好，可减少模糊词"
        else:
            return "可执行具体性不足，存在模糊表述"
    
    def _get_specificity_suggestions(self, content: str) -> List[str]:
        suggestions = []
        vague_words = ["建议", "可以考虑", "根据情况", "灵活把握"]
        for word in vague_words:
            if word in content:
                suggestions.append(f"将'{word}'替换为具体指令")
        return suggestions
    
    def _get_error_feedback(self, score: float) -> str:
        if score >= 8:
            return "失败模式编码优秀"
        elif score >= 5:
            return "失败模式编码良好，可补充更多场景"
        else:
            return "失败模式编码不足"
    
    def _get_error_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "失败模式处理" not in content:
            suggestions.append("添加失败模式处理章节")
        if "若" not in content:
            suggestions.append("使用'若...则...'格式描述错误处理")
        return suggestions
    
    def _get_safety_feedback(self, score: float) -> str:
        if score >= 8:
            return "安全性优秀"
        elif score >= 5:
            return "安全性良好，可补充更多禁止操作"
        else:
            return "安全性不足"
    
    def _get_safety_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "禁止操作" not in content:
            suggestions.append("添加禁止操作章节")
        return suggestions
    
    def _get_examples_feedback(self, score: float) -> str:
        if score >= 8:
            return "示例质量优秀"
        elif score >= 5:
            return "示例质量良好，可补充更多示例"
        else:
            return "示例质量不足"
    
    def _get_examples_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "```python" not in content:
            suggestions.append("添加Python代码示例")
        if "输出格式" not in content:
            suggestions.append("添加输出格式示例")
        return suggestions
    
    def _get_edge_feedback(self, score: float) -> str:
        if score >= 6:
            return "边界处理优秀"
        elif score >= 4:
            return "边界处理良好"
        else:
            return "边界处理不足"
    
    def _get_edge_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "空" not in content:
            suggestions.append("添加空值处理说明")
        if "无效" not in content:
            suggestions.append("添加无效输入处理说明")
        return suggestions
    
    def _get_consistency_feedback(self, score: float) -> str:
        if score >= 6:
            return "一致性优秀"
        elif score >= 4:
            return "一致性良好"
        else:
            return "一致性不足"
    
    def _get_consistency_suggestions(self, content: str) -> List[str]:
        return ["保持术语和格式统一"]
    
    def _get_practicality_feedback(self, score: float) -> str:
        if score >= 12:
            return "实用性优秀，集成实际数据源"
        elif score >= 9:
            return "实用性良好"
        else:
            return "实用性不足"
    
    def _get_practicality_suggestions(self, content: str) -> List[str]:
        suggestions = []
        if "a-stock-data" not in content:
            suggestions.append("集成A股数据源")
        if "═══" not in content:
            suggestions.append("添加格式化的输出示例")
        return suggestions
    
    def calculate_total_score(self, results: List[EvaluationResult]) -> float:
        """计算总分"""
        return sum(r.score for r in results)
    
    def generate_report(self, results: List[EvaluationResult]) -> str:
        """生成评估报告"""
        total = self.calculate_total_score(results)
        
        report = f"""
═══════════════════════════════════════════════════════════════
           ESG框架Skill评估报告
═══════════════════════════════════════════════════════════════
评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总分: {total:.1f}/100
═══════════════════════════════════════════════════════════════

【9维度评分详情】
"""
        
        for result in results:
            bar_length = int(result.score / result.max_score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            report += f"""
{result.dimension:20s} [{bar}] {result.score:.1f}/{result.max_score}
  反馈: {result.feedback}
"""
            if result.suggestions:
                report += "  建议:\n"
                for s in result.suggestions:
                    report += f"    • {s}\n"
        
        report += """
═══════════════════════════════════════════════════════════════
"""
        
        return report
    
    def find_weakest_dimension(self, results: List[EvaluationResult]) -> Optional[EvaluationResult]:
        """找到最弱的维度"""
        if not results:
            return None
        
        # 按得分比例排序
        sorted_results = sorted(results, key=lambda r: r.score / r.max_score)
        return sorted_results[0]
    
    def apply_improvement(self, dimension: str, suggestions: List[str]) -> bool:
        """
        应用改进
        
        Args:
            dimension: 需要改进的维度
            suggestions: 改进建议
            
        Returns:
            bool: 是否成功应用
        """
        print(f"\n🔴 CHECKPOINT: 准备改进维度 '{dimension}'")
        print(f"改进建议:")
        for s in suggestions:
            print(f"  • {s}")
        
        # 这里可以添加自动改进逻辑
        # 或者等待用户确认后手动改进
        
        return True
    
    def git_commit(self, message: str) -> bool:
        """Git提交"""
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", message], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def git_revert(self) -> bool:
        """Git回滚"""
        try:
            subprocess.run(["git", "revert", "HEAD", "--no-edit"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def run_evolution(self, max_rounds: int = 10):
        """
        运行进化循环
        
        Args:
            max_rounds: 最大轮次
        """
        print("🧬 达尔文进化系统启动")
        print("=" * 60)
        
        # 加载Skill
        skill_content = self.load_skill()
        
        # 初始评估
        print("\n📊 Phase 1: 基线评估")
        results = self.evaluate_skill(skill_content)
        self.current_score = self.calculate_total_score(results)
        print(self.generate_report(results))
        
        # 进化循环
        for round_id in range(1, max_rounds + 1):
            print(f"\n🔄 Phase 2: 第 {round_id} 轮进化")
            
            # 找到最弱维度
            weakest = self.find_weakest_dimension(results)
            if not weakest:
                print("没有找到可改进的维度")
                break
            
            print(f"目标维度: {weakest.dimension} (当前: {weakest.score}/{weakest.max_score})")
            
            # 应用改进
            if not self.apply_improvement(weakest.dimension, weakest.suggestions):
                print("改进应用失败")
                continue
            
            # 重新评估
            skill_content = self.load_skill()
            new_results = self.evaluate_skill(skill_content)
            new_score = self.calculate_total_score(new_results)
            
            # 棘轮机制：只保留改进
            if new_score > self.current_score:
                print(f"✅ 改进成功: {self.current_score:.1f} → {new_score:.1f} (+{new_score - self.current_score:.1f})")
                self.current_score = new_score
                results = new_results
                
                # 提交
                self.git_commit(f"feat: improve {weakest.dimension} (score: {new_score:.1f})")
            else:
                print(f"❌ 改进无效: {self.current_score:.1f} → {new_score:.1f}")
                # 回滚
                self.git_revert()
            
            # 早停机制
            if new_score - self.current_score < 1:
                print("\n🛑 早停: 单轮涨幅 < 1 分")
                break
            
            print(self.generate_report(new_results))
        
        print("\n" + "=" * 60)
        print(f"🧬 进化完成! 最终得分: {self.current_score:.1f}/100")
        print("=" * 60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="达尔文进化系统 - ESG框架Skill优化")
    parser.add_argument("--skill", default="SKILL.md", help="SKILL.md文件路径")
    parser.add_argument("--test", default="test-prompts.json", help="测试集文件路径")
    parser.add_argument("--rounds", type=int, default=10, help="最大进化轮次")
    
    args = parser.parse_args()
    
    evolver = DarwinEvolver(args.skill, args.test)
    evolver.run_evolution(args.rounds)


if __name__ == "__main__":
    main()
