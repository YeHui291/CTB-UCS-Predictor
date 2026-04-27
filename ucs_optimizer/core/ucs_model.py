import pandas as pd
import numpy as np
import os
from datetime import datetime
import joblib
import warnings
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline

warnings.filterwarnings('ignore')

class GradientBoostingUCSModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.imputer = None
        self.result_dir = None
        self.model_name = "Gradient Boosting (GB)"
        self.best_params = None
        self.full_pipeline = None
        
    def create_result_directory(self, base_dir=None):
        """创建结果保存目录"""
        if base_dir:
            result_dir = os.path.join(base_dir, 'results')
        else:
            result_dir = os.path.join(os.getcwd(), 'results')
        os.makedirs(result_dir, exist_ok=True)
        self.result_dir = result_dir
        return result_dir
        
    def load_data(self, file_path):
        """加载数据（支持文件路径和Streamlit文件对象）"""
        if hasattr(file_path, 'read'):
            # 对于文件对象，直接读取
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            # 对于文件路径，检查是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"数据文件不存在: {file_path}")
            df = pd.read_excel(file_path, engine='openpyxl')
        
        # 检查列名是否正确识别（如果列名看起来像数据，尝试重新读取）
        if all(col.startswith('Unnamed:') for col in df.columns):
            # 如果所有列都是Unnamed，尝试将第一行作为列名
            if hasattr(file_path, 'read'):
                # 对于文件对象，需要重置文件指针
                file_path.seek(0)
                df = pd.read_excel(file_path, engine='openpyxl', header=0)
            else:
                # 对于文件路径，直接重新读取
                df = pd.read_excel(file_path, engine='openpyxl', header=0)
        
        # 检查目标列是否存在
        target_column = 'UCS (Mpa)'
        if target_column not in df.columns:
            # 尝试其他可能的命名
            possible_columns = ['UCS', 'UCS (MPa)', '抗压强度', '抗压强度值', 'UCS值', '强度', '水泥强度']
            found = False
            for col in possible_columns:
                if col in df.columns:
                    target_column = col
                    found = True
                    break
            
            if not found:
                raise ValueError(f"数据中未找到UCS相关列，请检查数据文件。可用列名: {df.columns.tolist()}")
        
        # 处理目标变量中的缺失值
        df = df.dropna(subset=[target_column])
        
        # 分离特征和目标变量
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        return X, y, df.columns.tolist()
        
    def create_preprocessing_pipeline(self):
        """创建数据预处理Pipeline：缺失值填充和特征标准化"""
        preprocessing_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        return preprocessing_pipeline
        
    def create_full_pipeline(self, params=None):
        """创建完整的预处理+模型Pipeline"""
        # 创建预处理Pipeline
        preprocessing_pipeline = self.create_preprocessing_pipeline()
        
        # 默认参数
        default_params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 3,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'subsample': 1.0,
            'random_state': 42,
            'loss': 'squared_error'
        }
        
        # 如果提供了自定义参数，合并它们
        if params:
            default_params.update(params)
            
        # 创建完整的Pipeline
        full_pipeline = Pipeline([
            ('preprocessing', preprocessing_pipeline),
            ('model', GradientBoostingRegressor(**default_params))
        ])
        
        return full_pipeline
        
    def train_model(self, X_train, y_train, params=None):
        """训练Gradient Boosting模型"""
        print("开始训练Gradient Boosting模型...")
        
        # 创建并拟合完整的Pipeline
        pipeline = self.create_full_pipeline(params)
        pipeline.fit(X_train, y_train)
        
        self.full_pipeline = pipeline
        print("模型训练完成!")
        return pipeline
        
    def cross_validation(self, X_train, y_train, params=None):
        """执行5折交叉验证，可选传入模型参数"""
        print("执行5折交叉验证...")
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        
        cv_results = {
            'r2': [],
            'mse': [],
            'rmse': [],
            'mae': [],
            'y_true': [],
            'y_pred': []
        }
        
        fold = 1
        for train_idx, val_idx in kf.split(X_train):
            print(f"交叉验证折 {fold}/5")
            X_fold_train, X_fold_val = X_train.iloc[train_idx] if hasattr(X_train, 'iloc') else X_train[train_idx], \
                                      X_train.iloc[val_idx] if hasattr(X_train, 'iloc') else X_train[val_idx]
            y_fold_train, y_fold_val = y_train.iloc[train_idx] if hasattr(y_train, 'iloc') else y_train[train_idx], \
                                      y_train.iloc[val_idx] if hasattr(y_train, 'iloc') else y_train[val_idx]
            
            # 创建带预处理的完整Pipeline
            fold_pipeline = self.create_full_pipeline(params)
            fold_pipeline.fit(X_fold_train, y_fold_train)
            
            # 预测
            y_pred_fold = fold_pipeline.predict(X_fold_val)
            
            # 计算指标
            r2 = r2_score(y_fold_val, y_pred_fold)
            mse = mean_squared_error(y_fold_val, y_pred_fold)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_fold_val, y_pred_fold)
            
            # 保存结果
            cv_results['r2'].append(r2)
            cv_results['mse'].append(mse)
            cv_results['rmse'].append(rmse)
            cv_results['mae'].append(mae)
            cv_results['y_true'].extend(y_fold_val)
            cv_results['y_pred'].extend(y_pred_fold)
            
            fold += 1
        
        # 计算平均指标
        mean_r2 = np.mean(cv_results['r2'])
        mean_mse = np.mean(cv_results['mse'])
        mean_rmse = np.mean(cv_results['rmse'])
        mean_mae = np.mean(cv_results['mae'])
        
        print(f"交叉验证完成，平均R²: {mean_r2:.4f}, 平均MSE: {mean_mse:.4f}")
        print(f"平均RMSE: {mean_rmse:.4f}, 平均MAE: {mean_mae:.4f}")
        
        return cv_results
        
    def predict(self, X):
        """使用训练好的模型进行预测"""
        if not self.full_pipeline:
            raise ValueError("模型尚未训练，请先调用train_model方法")
        
        return self.full_pipeline.predict(X)
        
    def save_model(self, model_path):
        """保存模型"""
        if not self.full_pipeline:
            raise ValueError("模型尚未训练，请先调用train_model方法")
        
        joblib.dump(self.full_pipeline, model_path)
        print(f"模型已保存至: {model_path}")
        
    def load_model(self, model_path):
        """加载模型"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")
        
        self.full_pipeline = joblib.load(model_path)
        print(f"模型已从: {model_path} 加载")
        
    def fine_tune(self, X_train, y_train, params=None):
        """使用新数据微调模型"""
        if not self.full_pipeline:
            raise ValueError("模型尚未加载，请先调用load_model方法")
        
        print("开始微调模型...")
        
        # 如果提供了新的参数，创建新的Pipeline
        if params:
            self.full_pipeline = self.create_full_pipeline(params)
        
        # 微调模型
        self.full_pipeline.fit(X_train, y_train)
        print("模型微调完成!")
        return self.full_pipeline
        
    def evaluate(self, X_test, y_test):
        """评估模型性能"""
        if not self.full_pipeline:
            raise ValueError("模型尚未训练，请先调用train_model方法")
        
        y_pred = self.full_pipeline.predict(X_test)
        
        # 计算评估指标
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"模型评估结果:")
        print(f"R2分数: {r2:.4f}")
        print(f"均方误差(MSE): {mse:.4f} MPa2")
        print(f"均方根误差(RMSE): {rmse:.4f} MPa")
        print(f"平均绝对误差(MAE): {mae:.4f} MPa")
        
        return {
            'r2': r2,
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'y_pred': y_pred
        }
