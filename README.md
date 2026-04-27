# UCS Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

UCS Optimizer 是一个用于水泥强度预测和环境影响评估的工具，基于 Gradient Boosting 算法和生命周期评估 (LCA) 方法。

## 功能特点

- **水泥强度预测**：使用 Gradient Boosting 算法预测水泥的抗压强度 (UCS)
- **环境影响评估**：计算碳排放量、能耗和成本等环境指标
- **模型微调**：支持使用新数据对现有模型进行微调
- **可视化分析**：生成模型评估图、LCA指标分布图和相关性热图
- **命令行接口**：提供简单易用的命令行工具
- **Python API**：支持在 Python 代码中集成使用

## 安装

### 从源码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/ucs-optimizer.git
   cd ucs-optimizer
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 安装软件：
   ```bash
   pip install -e .
   ```

## 快速开始

### 命令行使用

#### 1. 运行完整分析

```bash
ucs-optimizer analyze --data data/sample_cement_data.xlsx --lci data/sample_lci_data.xlsx --output results
```

#### 2. 训练模型

```bash
ucs-optimizer train --data data/sample_cement_data.xlsx --output results
```

#### 3. 微调模型

```bash
ucs-optimizer fine-tune --model results/ucs_model.pkl --data data/sample_cement_data.xlsx --output results
```

### Python API 使用

```python
from ucs_optimizer.core.optimizer import UCSOptimizer

# 初始化优化器
optimizer = UCSOptimizer()
optimizer.set_result_directory('results')

# 运行完整分析
lca_results, lca_metrics = optimizer.run_full_analysis(
    'data/sample_cement_data.xlsx',
    lci_file='data/sample_lci_data.xlsx'
)

# 保存模型
optimizer.save_model('models/ucs_model.pkl')
```

## 目录结构

```
ucs_optimizer/
├── core/              # 核心功能模块
│   ├── __init__.py
│   ├── ucs_model.py   # UCS预测模型
│   ├── lca_calculator.py  # LCA计算模块
│   └── optimizer.py   # 集成优化器
├── cli/               # 命令行接口
│   ├── __init__.py
│   └── main.py        # 命令行主程序
├── visualization/     # 可视化模块
│   ├── __init__.py
│   └── visualizer.py  # 可视化功能
├── data/              # 示例数据
│   ├── sample_cement_data.xlsx  # 示例水泥实验数据
│   └── sample_lci_data.xlsx     # 示例生命周期清单数据
├── config/            # 配置文件
│   └── config.json    # 配置信息
├── docs/              # 文档
│   └── usage_guide.md # 使用指南
├── setup.py           # 安装配置
├── requirements.txt   # 依赖项
└── README.md          # 项目说明
```

## 输入数据格式

### 水泥实验数据

| 列名 | 描述 | 单位 |
|------|------|------|
| MC | 含水率 | % |
| CTR | 水泥-尾矿比 | - |
| UCS | 抗压强度 | MPa |

### 生命周期清单数据

| 列名 | 描述 | 单位 |
|------|------|------|
| Materials/curving condition | 材料名称 | - |
| Cost（＄ /kg） | 成本 | $/kg |
| Carbon footprint（kg/kg） | 碳足迹 | kg CO2/kg |
| Energy consumption（kWh/t） | 能耗 | kWh/ton |

## 输出结果

### 分析结果文件

- `full_analysis_results.xlsx`：包含UCS预测值和LCA指标
- `ucs_model.pkl`：训练好的模型

### 可视化结果

- `model_evaluation.png`：模型评估图
- `lca_metrics_distribution.png`：LCA指标分布图
- `ucs_vs_lca_metrics.png`：UCS与LCA指标关系图
- `lca_correlation_matrix.png`：LCA指标相关性热图

## 环境指标说明

- **总碳足迹_kgCO2**：总碳排放量
- **总能耗_kWh**：总能耗
- **总成本_USD**：总成本
- **碳足迹_per_MPa**：单位强度碳排放量
- **能耗_per_MPa**：单位强度能耗
- **成本_per_MPa**：单位强度成本

## 技术原理

### UCS预测模型

- **算法**：Gradient Boosting Regressor
- **特征**：MC（含水率）、CTR（水泥-尾矿比）
- **评估指标**：R²、RMSE、MAE

### LCA计算

- **碳足迹**：基于水泥用量和碳排放系数计算
- **能耗**：基于水泥用量和能耗系数计算
- **成本**：基于水泥和水的用量及成本计算

## 示例

### 命令行示例

```bash
# 运行完整分析
ucs-optimizer analyze --data data/sample_cement_data.xlsx --lci data/sample_lci_data.xlsx --output results

# 输出结果
开始运行完整分析...
生命周期清单数据读取成功
水泥碳排放系数: 0.82 kg CO2/kg
水泥能耗系数: 115.0 kWh/ton
水泥成本: 0.084 $/kg
水成本: 0.001 $/kg
成功加载数据，特征数量: 2, 样本数量: 15
数据集划分完成: 训练集 12 样本, 测试集 3 样本
开始训练Gradient Boosting模型...
模型训练完成!
模型评估结果:
R²分数: 0.9876
均方误差(MSE): 0.0123 MPa²
均方根误差(RMSE): 0.1109 MPa
平均绝对误差(MAE): 0.0987 MPa
开始LCA计算...
LCA计算完成！
完整分析结果已保存至: results/full_analysis_results.xlsx

LCA指标统计:
平均水泥质量: 35.71 kg
平均总碳足迹: 29.28 kg CO2
平均总能耗: 4.11 kWh
平均总成本: 3.00 USD
平均碳足迹_per_MPa: 7.02 kg CO2/MPa
平均能耗_per_MPa: 0.99 kWh/MPa
平均成本_per_MPa: 0.72 USD/MPa
可视化结果已保存至: results/visualizations
```

## 贡献

欢迎提交 issue 和 pull request 来改进这个项目。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 联系方式

- **作者**：Your Name
- **邮箱**：your.email@example.com
- **GitHub**：[https://github.com/yourusername/ucs-optimizer](https://github.com/yourusername/ucs-optimizer)
