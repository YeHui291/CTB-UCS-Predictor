import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import gaussian_kde

# 设置中文字体（可选，根据需求调整）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 英文期刊推荐字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['font.family'] = 'serif'  # 使用serif字体系列
plt.rcParams['font.serif'] = ['Times New Roman']  # 英文新罗马字体

# 顶刊配色方案配置
COLOR_SCHEMES = {
    # Nature期刊风格：深蓝主调 + 温暖橙红对比，专业且适合打印
    1: ['viridis', 'Blues', 'Oranges', '#D55E00'],    
    # Science期刊风格：深绿主调 + 紫色对比，色彩平衡感强
    2: ['plasma', 'Greens', 'Purples', '#CC79A7'],    
    # 通用学术期刊风格：深灰主调 + 蓝色对比，经典学术配色
    3: ['cividis', 'Greys', 'Blues', '#0072B2']      
}

# 标记方案配置
MARKER_LIB = {
    1: {
        'scatter': 'o',      # 圆形标记
        'regression': '-',   # 实线
        'confidence': '--',  # 虚线
        'histogram': 'bar',  # 柱状图
        'marker_size': 80,   # 标记大小
        'line_width': 2.5    # 线宽
    }
}

class Visualizer:
    def __init__(self):
        pass
    
    def plot_model_evaluation(self, y_true, y_pred, save_path, model_name="Gradient Boosting"):
        """绘制模型评估图"""
        # 计算评估指标
        from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        n_samples = len(y_true)
        
        # 全局最大值（统一坐标轴范围）
        max_val = max(np.max(y_true), np.max(y_pred)) * 1.05  # 留出5%余量
        
        # 初始化画布
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # 绘制散点图
        scatter = ax.scatter(
            y_pred, y_true,
            c=y_true, cmap='viridis',
            marker='o', edgecolor='black', linewidth=0.5,
            s=80, alpha=1
        )
        
        # 完美拟合参考线
        ax.plot([0, max_val], [0, max_val],
              color='#D55E00', linestyle='--', linewidth=1.5)
        
        # 坐标轴配置
        ax.set_xlim(0, max_val)
        ax.set_ylim(0, max_val)
        ax.set_xlabel('Predicted UCS (MPa)', fontsize=16)
        ax.set_ylabel('Experimental UCS (MPa)', fontsize=16)
        
        # 标注模型信息和评估指标
        ax.text(0.05, 0.93, f'Model: {model_name}', transform=ax.transAxes,
              fontweight='bold', fontsize=14)
        ax.text(0.05, 0.86, f'$R^2$={r2:.4f}', transform=ax.transAxes, fontsize=14)
        ax.text(0.05, 0.79, f'RMSE={rmse:.4f} MPa', transform=ax.transAxes, fontsize=14)
        ax.text(0.05, 0.72, f'MAE={mae:.4f} MPa', transform=ax.transAxes, fontsize=14)
        ax.text(0.05, 0.65, f'N={n_samples}', transform=ax.transAxes, fontsize=14)
        
        # 设置刻度字体
        ax.tick_params(axis='both', which='major', labelsize=14)
        
        # 保存图片
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'模型评估图已保存至: {save_path}')
    
    def plot_lca_metrics(self, df, save_dir):
        """绘制LCA指标分布图"""
        # 创建输出文件夹
        os.makedirs(save_dir, exist_ok=True)
        
        # LCA指标分布直方图（2x3布局）
        fig, axes = plt.subplots(2, 3, figsize=(18, 12), constrained_layout=True)
        metrics = ['总碳足迹_kgCO2', '总能耗_kWh', '总成本_USD', 
                  '碳足迹_per_MPa', '能耗_per_MPa', '成本_per_MPa']
        metric_names = ['Total Carbon Footprint (kgCO2)', 'Total Energy Consumption (kWh)', 'Total Cost (USD)',
                      'Carbon Footprint per MPa', 'Energy Consumption per MPa', 'Cost per MPa']
        titles = ['Total Carbon Footprint Distribution', 'Total Energy Consumption Distribution', 'Total Cost Distribution',
                'Carbon Footprint per MPa Distribution', 'Energy Consumption per MPa Distribution', 'Cost per MPa Distribution']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for i, (metric, metric_name, title, color) in enumerate(zip(metrics, metric_names, titles, colors)):
            if metric in df.columns:
                row = i // 3
                col = i % 3
                
                # 绘制直方图
                axes[row, col].hist(df[metric], bins=30, alpha=0.8, color=color, edgecolor='black', linewidth=0.8)
                
                # 设置标题和标签
                axes[row, col].set_title(title, fontname='Times New Roman', fontsize=18, fontweight='bold')
                axes[row, col].set_xlabel(metric_name, fontname='Times New Roman', fontsize=16)
                axes[row, col].set_ylabel('Frequency', fontname='Times New Roman', fontsize=16)
                
                # 设置刻度字体
                axes[row, col].tick_params(axis='both', which='major', labelsize=14, labelfontfamily='Times New Roman')
                
                # 设置轴脊
                for spine in axes[row, col].spines.values():
                    spine.set_linewidth(1.2)
        
        save_path = os.path.join(save_dir, 'lca_metrics_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'LCA指标分布直方图已保存至: {save_path}')
    
    def plot_ucs_vs_lca(self, df, save_dir):
        """绘制UCS与LCA指标关系图"""
        # 创建输出文件夹
        os.makedirs(save_dir, exist_ok=True)
        
        # UCS与归一化指标关系图（1x3布局）
        fig, axes = plt.subplots(1, 3, figsize=(24, 8), constrained_layout=True)
        norm_metrics = ['碳足迹_per_MPa', '能耗_per_MPa', '成本_per_MPa']
        norm_names = ['Carbon Footprint per MPa', 'Energy Consumption per MPa', 'Cost per MPa']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, (metric, name, color) in enumerate(zip(norm_metrics, norm_names, colors)):
            if metric in df.columns and 'UCS' in df.columns:
                # 绘制散点图
                axes[i].scatter(df['UCS'], df[metric], alpha=0.6, color=color, s=60, edgecolor='black', linewidth=0.5)
                
                # 设置标题和标签
                axes[i].set_title(f'Relationship between UCS and {name}', fontname='Times New Roman', fontsize=18, fontweight='bold')
                axes[i].set_xlabel('UCS (MPa)', fontname='Times New Roman', fontsize=16)
                axes[i].set_ylabel(name, fontname='Times New Roman', fontsize=16)
                
                # 设置刻度字体
                axes[i].tick_params(axis='both', which='major', labelsize=14, labelfontfamily='Times New Roman')
                
                # 设置轴脊
                for spine in axes[i].spines.values():
                    spine.set_linewidth(1.2)
        
        save_path = os.path.join(save_dir, 'ucs_vs_lca_metrics.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'UCS与LCA指标关系图已保存至: {save_path}')
    
    def plot_correlation_matrix(self, df, save_dir):
        """绘制LCA指标相关性热图"""
        # 创建输出文件夹
        os.makedirs(save_dir, exist_ok=True)
        
        # 选择需要计算相关性的列
        corr_columns = ['总碳足迹_kgCO2', '总能耗_kWh', '总成本_USD', '碳足迹_per_MPa', '能耗_per_MPa', '成本_per_MPa', 'UCS', '水泥质量_kg', 'MC', 'CTR']
        available_columns = [col for col in corr_columns if col in df.columns]
        
        if len(available_columns) > 1:
            # 计算相关系数矩阵
            corr_matrix = df[available_columns].corr()
            
            # 绘制热图
            fig, ax = plt.subplots(figsize=(12, 10), constrained_layout=True)
            cax = ax.matshow(corr_matrix, cmap='coolwarm')
            
            # 添加颜色条
            cbar = fig.colorbar(cax, label='Correlation Coefficient')
            cbar.ax.yaxis.label.set_fontname('Times New Roman')
            cbar.ax.yaxis.label.set_fontsize(16)
            cbar.ax.tick_params(labelsize=14, labelfontfamily='Times New Roman')
            
            # 设置标签
            ax.set_xticks(np.arange(len(available_columns)))
            ax.set_yticks(np.arange(len(available_columns)))
            ax.set_xticklabels(available_columns, fontname='Times New Roman', fontsize=12, rotation=45, ha='right')
            ax.set_yticklabels(available_columns, fontname='Times New Roman', fontsize=12)
            
            # 设置标题
            ax.set_title('Correlation Matrix of LCA Metrics', fontname='Times New Roman', fontsize=18, fontweight='bold')
            
            save_path = os.path.join(save_dir, 'lca_correlation_matrix.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            print(f'LCA指标相关性热图已保存至: {save_path}')
