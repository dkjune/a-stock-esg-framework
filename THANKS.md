# 致谢声明

## 数据来源

本项目的数据获取模块参考了以下开源项目的设计思路：

### [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data)

- **项目**: A股全栈数据工具包
- **版本**: V3.2.1
- **作者**: Simon 林
- **许可证**: [Apache License 2.0](https://github.com/simonlin1212/a-stock-data/blob/main/LICENSE)
- **仓库**: https://github.com/simonlin1212/a-stock-data

## 使用说明

本项目**参考**了 a-stock-data 的以下设计理念：

| 设计理念 | 本项目的实现 |
|----------|--------------|
| 数据源优先级 | 优先使用腾讯财经API（不封IP） |
| 东财防封机制 | 实现统一限流入口 `_em_get()` |
| 行情数据获取 | 使用腾讯财经API获取PE/PB/市值 |

## 独立性声明

本项目是**独立开发**的A股中特估分析框架，与 a-stock-data 项目：

- **不是** a-stock-data 的派生作品
- **不是** a-stock-data 的fork或分支
- **不包含** a-stock-data 的源代码

本项目仅参考了其公开文档中描述的数据获取API地址和设计理念，所有代码均为独立编写。

## 许可证合规

根据 Apache License 2.0 的要求：

1. ✅ 保留原始版权声明
2. ✅ 声明参考内容
3. ✅ 包含NOTICE文件
4. ✅ 注明作者和项目链接

## 感谢

感谢 Simon 林 开源的优质数据工具，为A股数据获取提供了有价值的参考！

---

**免责声明**: 本项目与 simonlin1212/a-stock-data 项目无关联关系，仅在许可证允许的范围内参考其设计理念。
