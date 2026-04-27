# UCS Optimizer 使用指南

## 1. 安装

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

## 2. 命令行使用

### 2.1 训练模型

```bash
ucs-optimizer train --data data/sample_cement_data.xlsx --lci data/sample_lci_data.xlsx --output results
```

### 2.2 微调模型

```bash
ucs-optimizer fine-tune --model results/ucs_model.pkl --data data/sample_cement_data.xlsx --output results
```

### 2.3 预测UCS值

```bash
ucs-optimizer predict --model results/ucs_model.pkl --data data/sample_cement_data.xlsx --output results
```

### 2.4 计算LCA指标

```bash
ucs-optimizer lca --data data/sample_cement_data.xlsx --lci data/sample_lci_data.xlsx --output results
```

### 2.5 运行完整分析

```bash
ucs-optimizer analyze --data data/sample_cement_data.xlsx --lci data/sample_lci_data.xlsx --output results
```

## 3. Python API 使用

### 3.1 导入模块

```python
from ucs_optimizer.core.optimizer import UCSOptimizer
```

### 3.2 初始化优化器

```python
optimizer = UCSOptimizer()
optimizer.set_result_directory('results')
```

### 3.3 训练模型

```python
optimizer.train_ucs_model('data/sample_cement_data.xlsx')
optimizer.save_model('models/ucs_model.pkl')
```

### 3.4 加载模型并微调

```python
optimizer.load_ucs_model('models/ucs_model.pkl')
optimizer.fine_tune_ucs_model('data/new_cement_data.xlsx')
optimizer.save_model('models/ucs_model_fine_tuned.pkl')
```

### 3.5 运行完整分析

```python
lca_results, lca_metrics = optimizer.run_full_analysis(
    'data/sample_cement_data.xlsx',
    lci_file='data/sample_lci_data.xlsx'
)
```

## 4. 结果解释

### 4.1 UCS预测结果

- `Predicted UCS`: 模型预测的水泥强度值（MPa）

### 4.2 LCA指标

- `总碳足迹_kgCO2`: 总碳排放量（kg CO2）
- `总能耗_kWh`: 总能耗（kWh）
- `总成本_USD`: 总成本（USD）
- `碳足迹_per_MPa`: 单位强度碳排放量（kg CO2/MPa）
- `能耗_per_MPa`: 单位强度能耗（kWh/MPa）
- `成本_per_MPa`: 单位强度成本（USD/MPa）

### 4.3 可视化结果

- `model_evaluation.png`: 模型评估图，展示预测值与真实值的对比
- `lca_metrics_distribution.png`: LCA指标分布图
- `ucs_vs_lca_metrics.png`: UCS与LCA指标关系图
- `lca_correlation_matrix.png`: LCA指标相关性热图

## 5. 常见问题

### 5.1 模型训练失败

- 检查数据文件格式是否正确
- 确保数据中包含UCS列
- 检查数据中是否有缺失值

### 5.2 LCA计算失败

- 检查生命周期清单文件格式是否正确
- 确保文件中包含Cement和Water的数据

### 5.3 可视化结果生成失败

- 确保matplotlib库已正确安装
- 检查输出目录是否有写入权限

## 6. 示例输出

### 6.1 命令行输出示例

```
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
模型评估图已保存至: results/visualizations/model_evaluation.png
LCA指标分布直方图已保存至: results/visualizations/lca_metrics_distribution.png
UCS与LCA指标关系图已保存至: results/visualizations/ucs_vs_lca_metrics.png
LCA指标相关性热图已保存至: results/visualizations/lca_correlation_matrix.png
可视化结果已保存至: results/visualizations
```

### 6.2 输出文件

- `results/full_analysis_results.xlsx`: 完整分析结果
- `results/visualizations/`: 可视化结果目录
- `results/ucs_model.pkl`: 训练好的模型
