import pandas as pd
import os
from ucs_optimizer.core.ucs_model import GradientBoostingUCSModel
from ucs_optimizer.core.lca_calculator import LCACalculator
from ucs_optimizer.visualization.visualizer import Visualizer

class UCSOptimizer:
    def __init__(self):
        self.ucs_model = GradientBoostingUCSModel()
        self.lca_calculator = LCACalculator()
        self.visualizer = Visualizer()
        self.result_dir = None
    
    def set_result_directory(self, directory):
        """设置结果保存目录"""
        self.result_dir = directory
        os.makedirs(self.result_dir, exist_ok=True)
        self.ucs_model.create_result_directory(self.result_dir)
    
    def load_lci_data(self, lci_file):
        """加载生命周期清单数据"""
        self.lca_calculator.load_lci_data(lci_file)
    
    def train_ucs_model(self, data_file, params=None):
        """训练UCS预测模型"""
        # 加载数据
        X, y, feature_names = self.ucs_model.load_data(data_file)
        print(f"成功加载数据，特征数量: {X.shape[1]}, 样本数量: {X.shape[0]}")
        
        # 8/2划分训练集和测试集
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"数据集划分完成: 训练集 {X_train.shape[0]} 样本, 测试集 {X_test.shape[0]} 样本")
        
        # 训练模型
        self.ucs_model.train_model(X_train, y_train, params)
        
        # 评估模型
        evaluation_results = self.ucs_model.evaluate(X_test, y_test)
        
        return evaluation_results
    
    def load_ucs_model(self, model_path):
        """加载UCS预测模型"""
        self.ucs_model.load_model(model_path)
    
    def fine_tune_ucs_model(self, data_file, params=None):
        """使用新数据微调UCS预测模型"""
        # 加载数据
        X, y, feature_names = self.ucs_model.load_data(data_file)
        
        # 8/2划分训练集和测试集
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 微调模型
        self.ucs_model.fine_tune(X_train, y_train, params)
        
        # 评估模型
        evaluation_results = self.ucs_model.evaluate(X_test, y_test)
        
        return evaluation_results
    
    def predict_ucs(self, X):
        """预测UCS值"""
        return self.ucs_model.predict(X)
    
    def calculate_lca(self, df, total_mass=1000):
        """计算LCA指标"""
        return self.lca_calculator.calculate_lca(df, total_mass)
    
    def train(self, data_path, test_size=0.2, random_state=42, target_column=None):
        """训练UCS预测模型（支持Streamlit文件对象）
        
        Args:
            data_path: 数据文件路径或Streamlit文件对象
            test_size: 测试集比例
            random_state: 随机种子
            target_column: 手动指定的目标列名
        """
        # 加载数据
        X, y, feature_names = self.ucs_model.load_data(data_path, target_column=target_column)
        print(f"成功加载数据，特征数量: {X.shape[1]}, 样本数量: {X.shape[0]}")
        
        # 划分训练集和测试集
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        print(f"数据集划分完成: 训练集 {X_train.shape[0]} 样本, 测试集 {X_test.shape[0]} 样本")
        
        # 训练模型
        model = self.ucs_model.train_model(X_train, y_train)
        
        # 评估模型
        metrics = self.ucs_model.evaluate(X_test, y_test)
        
        return model, metrics
    
    def predict(self, input_data, model_path=None):
        """预测UCS值（支持Streamlit文件对象）"""
        # 加载数据
        if hasattr(input_data, 'read'):
            df = pd.read_excel(input_data, engine='openpyxl')
        else:
            df = pd.read_excel(input_data, engine='openpyxl')
        
        # 提取特征 - 使用所有12个特征变量
        target_column = 'UCS (Mpa)'
        if target_column not in df.columns:
            possible_columns = ['UCS', 'UCS (MPa)', '抗压强度']
            for col in possible_columns:
                if col in df.columns:
                    target_column = col
                    break
        
        # 使用所有12个特征变量
        X = df.drop(target_column, axis=1) if target_column in df.columns else df
        
        # 预测
        predictions = self.ucs_model.predict(X)
        
        # 创建结果DataFrame
        result_df = df.copy()
        result_df['Predicted UCS'] = predictions
        
        return result_df
    
    def run_full_analysis(self, data_file, lci_file=None, model_path=None, params=None):
        """运行完整的分析流程"""
        # 加载LCI数据（如果提供）
        if lci_file:
            self.load_lci_data(lci_file)
        
        # 加载或训练模型
        if model_path:
            self.load_ucs_model(model_path)
        else:
            self.train_ucs_model(data_file, params)
        
        # 加载原始数据
        if hasattr(data_file, 'read'):
            df = pd.read_excel(data_file, engine='openpyxl')
        else:
            df = pd.read_excel(data_file, engine='openpyxl')
        
        # 预测UCS值（如果模型已训练）
        if hasattr(self.ucs_model, 'full_pipeline') and self.ucs_model.full_pipeline:
            # 提取特征
            target_column = 'UCS (Mpa)'
            if target_column not in df.columns:
                possible_columns = ['UCS', 'UCS (MPa)', '抗压强度']
                for col in possible_columns:
                    if col in df.columns:
                        target_column = col
                        break
            
            X = df.drop(target_column, axis=1) if target_column in df.columns else df
            df['Predicted UCS'] = self.ucs_model.predict(X)
        
        # 计算LCA指标
        lca_results = self.calculate_lca(df)
        
        # 保存结果
        if self.result_dir:
            output_file = os.path.join(self.result_dir, 'full_analysis_results.xlsx')
            lca_results.to_excel(output_file, index=False)
            print(f'完整分析结果已保存至: {output_file}')
        
        # 获取LCA指标统计信息
        lca_metrics = self.lca_calculator.get_lca_metrics(lca_results)
        print('\nLCA指标统计:')
        for key, value in lca_metrics.items():
            print(f'{key}: {value:.2f}')
        
        # 生成可视化结果
        self.visualize_results(lca_results)
        
        return lca_results, lca_metrics
    
    def save_model(self, model_path):
        """保存模型"""
        self.ucs_model.save_model(model_path)
    
    def visualize_results(self, lca_results):
        """可视化分析结果"""
        if not self.result_dir:
            raise ValueError("请先设置结果保存目录")
        
        # 创建可视化结果目录
        viz_dir = os.path.join(self.result_dir, 'visualizations')
        os.makedirs(viz_dir, exist_ok=True)
        
        # 绘制LCA指标分布图
        self.visualizer.plot_lca_metrics(lca_results, viz_dir)
        
        # 绘制UCS与LCA指标关系图
        self.visualizer.plot_ucs_vs_lca(lca_results, viz_dir)
        
        # 绘制LCA指标相关性热图
        self.visualizer.plot_correlation_matrix(lca_results, viz_dir)
        
        print(f'可视化结果已保存至: {viz_dir}')
    
    def visualize_model_evaluation(self, y_true, y_pred, model_name="Gradient Boosting"):
        """可视化模型评估结果"""
        if not self.result_dir:
            raise ValueError("请先设置结果保存目录")
        
        # 创建可视化结果目录
        viz_dir = os.path.join(self.result_dir, 'visualizations')
        os.makedirs(viz_dir, exist_ok=True)
        
        # 绘制模型评估图
        save_path = os.path.join(viz_dir, 'model_evaluation.png')
        self.visualizer.plot_model_evaluation(y_true, y_pred, save_path, model_name)

