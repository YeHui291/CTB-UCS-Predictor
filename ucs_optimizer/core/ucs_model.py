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
        
    def load_data(self, file_path, target_column=None):
        """加载数据（支持文件路径和Streamlit文件对象）
        
        Args:
            file_path: 文件路径或Streamlit文件对象
            target_column: 手动指定的目标列名
        """
        print("\n=== 数据加载开始 ===")
        print(f"目标列: {target_column}")
        
        # 首先尝试 header=0（最常见的情况）
        try:
            if hasattr(file_path, 'read'):
                file_path.seek(0)
                df = pd.read_excel(file_path, engine='openpyxl', header=0)
            else:
                df = pd.read_excel(file_path, engine='openpyxl', header=0)
            
            # 清理列名
            df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
            
            # 检查是否有 Unnamed 列
            unnamed_count = sum(1 for col in df.columns if str(col).startswith('Unnamed'))
            print(f"[INFO] Header=0 读取成功")
            print(f"[INFO] 列名: {df.columns.tolist()}")
            print(f"[INFO] 数据形状: {df.shape}")
            print(f"[INFO] Unnamed列数量: {unnamed_count}")
            
            # 如果 Unnamed 列太多，尝试其他 header
            if unnamed_count > len(df.columns) / 2:
                print(f"[WARNING] Unnamed列过多，尝试其他header设置")
                raise Exception("Unnamed列过多")
            
        except Exception as e:
            print(f"[INFO] Header=0 读取失败，尝试其他方式...")
            
            # 尝试多种方式读取文件，确保列名正确识别
            best_df = None
            best_columns = []
            best_header = None
            
            # 尝试不设置header，让pandas自动处理
            print("[INFO] 尝试不设置header...")
            try:
                if hasattr(file_path, 'read'):
                    file_path.seek(0)
                    df_temp = pd.read_excel(file_path, engine='openpyxl', header=None)
                else:
                    df_temp = pd.read_excel(file_path, engine='openpyxl', header=None)
                
                # 尝试将第一行作为列名
                if len(df_temp) > 0:
                    first_row = df_temp.iloc[0].tolist()
                    df_temp.columns = first_row
                    df_temp = df_temp[1:]
                    print(f"[INFO] 将第一行作为列名: {first_row}")
                    
                    # 清理列名
                    df_temp.columns = [str(col).strip() if isinstance(col, (str, int, float)) else col for col in df_temp.columns]
                    
                    # 检查列名质量
                    non_unnamed_count = sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed'))
                    print(f"[INFO] 找到 {non_unnamed_count} 个有效列名")
                    
                    if non_unnamed_count > len(best_columns):
                        best_df = df_temp.copy()
                        best_columns = df_temp.columns.tolist()
                        best_header = "first_row"
            except Exception as e1:
                print(f"[ERROR] 不设置header失败: {e1}")
            
            # 尝试不同的header设置
            for header in [0, 1, 2, 3, 4, 5]:
                try:
                    if hasattr(file_path, 'read'):
                        file_path.seek(0)
                    else:
                        pass
                        
                    if hasattr(file_path, 'read'):
                        file_path.seek(0)
                        df_temp = pd.read_excel(file_path, engine='openpyxl', header=header)
                    else:
                        df_temp = pd.read_excel(file_path, engine='openpyxl', header=header)
                    
                    # 清理列名
                    df_temp.columns = [col.strip() if isinstance(col, str) else col for col in df_temp.columns]
                    
                    # 检查列名质量
                    non_unnamed_count = sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed'))
                    print(f"[INFO] Header={header} 找到 {non_unnamed_count} 个有效列名")
                    
                    if non_unnamed_count > len(best_columns):
                        best_df = df_temp.copy()
                        best_columns = df_temp.columns.tolist()
                        best_header = header
                        
                except Exception as e2:
                    print(f"[ERROR] Header={header} 读取失败: {e2}")
                    continue
            
            # 如果找到了较好的列名，使用它
            if best_df is not None:
                df = best_df
                print(f"[SUCCESS] 使用 header={best_header} 的列名: {best_columns}")
            else:
                raise Exception("无法找到有效的列名")
        
        # 清理列名（去除空格和特殊字符）
        df.columns = [str(col).strip() if isinstance(col, (str, int, float)) else col for col in df.columns]
        print(f"[INFO] 最终列名: {df.columns.tolist()}")
        print(f"[INFO] 数据形状: {df.shape}")
        print(f"=== 数据加载结束 ===\n")
        
        # 使用AI辅助识别列名
        if target_column is not None:
            target_column = self._ai_column_recognition(df, target_column)
        else:
            # 自动检测UCS列
            target_column = self._ai_detect_ucs_column(df)
        
        # 处理目标变量中的缺失值
        df = df.dropna(subset=[target_column])
        
        # 分离特征和目标变量
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        return X, y, df.columns.tolist()
    
    def _ai_column_recognition(self, df, target_column):
        """使用AI辅助识别列名
        
        Args:
            df: 数据框
            target_column: 目标列名
            
        Returns:
            识别到的目标列名
        """
        # 0. 打印详细调试信息
        print(f"\n=== AI 列名识别开始 ===")
        print(f"目标列: {target_column}")
        print(f"可用列名: {df.columns.tolist()}")
        print(f"数据形状: {df.shape}")
        
        # 1. 尝试精确匹配
        if target_column in df.columns:
            print(f"[SUCCESS] 精确匹配成功: {target_column}")
            print(f"=== AI 列名识别结束 ===\n")
            return target_column
        
        # 2. 尝试不区分大小写匹配
        for col in df.columns:
            if str(col).lower() == str(target_column).lower():
                print(f"[SUCCESS] 不区分大小写匹配成功: {col}")
                print(f"=== AI 列名识别结束 ===\n")
                return col
        
        # 3. 尝试部分匹配
        for col in df.columns:
            col_str = str(col).lower()
            target_str = str(target_column).lower()
            if target_str in col_str:
                print(f"[SUCCESS] 部分匹配成功: {col}")
                print(f"=== AI 列名识别结束 ===\n")
                return col
        
        # 4. 尝试常用UCS列名
        possible_columns = [
            'UCS', 'UCS (MPa)', 'UCS (Mpa)', '抗压强度', '抗压强度值', 'UCS值', '强度', '水泥强度',
            'ucs', 'Ucs', 'strength', 'Strength', 'compressive strength', 'Compressive Strength',
            '抗压强度(MPa)', 'UCS值(MPa)', '抗压强度值(MPa)', '强度值', 'cement strength',
            'Cement Strength', 'compressive', 'Compressive', 'strength value', 'Strength Value',
            '抗压', '压强', '压力', 'strength', 'compressive', '固化强度', '硬化强度'
        ]
        
        for col in possible_columns:
            if col in df.columns:
                print(f"[SUCCESS] 常用列名匹配成功: {col}")
                print(f"=== AI 列名识别结束 ===\n")
                return col
        
        # 5. 尝试部分匹配常用列名
        for col in df.columns:
            col_str = str(col).lower()
            if any(keyword in col_str for keyword in ['ucs', '抗压', '强度', 'strength', 'compressive', '压强', '压力']):
                print(f"[SUCCESS] 部分匹配常用列名成功: {col}")
                print(f"=== AI 列名识别结束 ===\n")
                return col
        
        # 6. 基于数据特征的智能识别
        best_match = None
        highest_score = 0
        
        print("\n--- 基于数据特征的智能识别 ---")
        for col in df.columns:
            # 计算列与UCS的匹配分数
            score = self._calculate_column_score(str(col))
            
            # 同时考虑数据特征
            if df[col].dtype in [np.float64, np.int64]:
                # 尝试计算统计值
                try:
                    col_min = df[col].min()
                    col_max = df[col].max()
                    col_mean = df[col].mean()
                    col_std = df[col].std()
                    
                    print(f"列 '{col}': 类型={df[col].dtype}, 最小值={col_min:.2f}, 最大值={col_max:.2f}, 平均值={col_mean:.2f}")
                    
                    # UCS值通常在0-100之间
                    if 0 <= col_min and col_max <= 100:
                        score += 0.3
                        print(f"  +0.3 分数: 值范围合适")
                    
                    # UCS值通常为正数
                    if col_min >= 0:
                        score += 0.2
                        print(f"  +0.2 分数: 值为正数")
                    
                    # UCS值通常有一定的范围
                    if col_max - col_min > 5:
                        score += 0.1
                        print(f"  +0.1 分数: 值范围足够大")
                    
                    # UCS值通常有一定的波动性
                    if col_std > 0.5:
                        score += 0.1
                        print(f"  +0.1 分数: 值有波动性")
                except Exception as e:
                    print(f"列 '{col}': 计算统计值失败: {e}")
            else:
                print(f"列 '{col}': 类型={df[col].dtype} (非数值类型)")
            
            print(f"  总分: {score:.2f}")
            
            if score > highest_score:
                highest_score = score
                best_match = col
        
        if best_match:
            print(f"\n[SUCCESS] 基于数据特征的智能识别成功: {best_match} (分数: {highest_score:.2f})")
            print(f"=== AI 列名识别结束 ===\n")
            return best_match
        
        # 7. 尝试所有数值列
        numeric_columns = []
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                numeric_columns.append(col)
        
        print(f"\n--- 尝试数值列 ---")
        print(f"找到 {len(numeric_columns)} 个数值列: {numeric_columns}")
        
        if numeric_columns:
            # 选择最后一个数值列（通常UCS在最后）
            best_match = numeric_columns[-1]
            print(f"[SUCCESS] 选择最后一个数值列: {best_match}")
            print(f"=== AI 列名识别结束 ===\n")
            return best_match
        
        # 8. 尝试所有列，不管类型
        print(f"\n--- 尝试所有列 ---")
        print(f"总列数: {len(df.columns)}")
        
        if len(df.columns) > 0:
            # 选择最后一列
            best_match = df.columns[-1]
            print(f"[SUCCESS] 选择最后一列: {best_match}")
            print(f"=== AI 列名识别结束 ===\n")
            return best_match
        
        print(f"=== AI 列名识别失败 ===\n")
        raise ValueError(f"指定的目标列 '{target_column}' 不存在于数据中。可用列名: {df.columns.tolist()}")
    
    def _ai_detect_ucs_column(self, df):
        """使用AI自动检测UCS列
        
        Args:
            df: 数据框
            
        Returns:
            检测到的UCS列名
        """
        # 0. 打印调试信息
        print("[INFO] 尝试自动检测UCS列")
        print(f"可用列名: {df.columns.tolist()}")
        
        # 1. 尝试常用UCS列名
        possible_columns = [
            'UCS', 'UCS (MPa)', 'UCS (Mpa)', '抗压强度', '抗压强度值', 'UCS值', '强度', '水泥强度',
            'ucs', 'Ucs', 'strength', 'Strength', 'compressive strength', 'Compressive Strength',
            '抗压强度(MPa)', 'UCS值(MPa)', '抗压强度值(MPa)', '强度值', 'cement strength',
            'Cement Strength', 'compressive', 'Compressive', 'strength value', 'Strength Value'
        ]
        
        for col in possible_columns:
            if col in df.columns:
                print(f"[SUCCESS] 常用列名匹配成功: {col}")
                return col
        
        # 2. 尝试部分匹配
        for col in df.columns:
            col_str = str(col).lower()
            if any(keyword in col_str for keyword in ['ucs', '抗压', '强度', 'strength', 'compressive']):
                print(f"[SUCCESS] 部分匹配常用列名成功: {col}")
                return col
        
        # 3. 基于数据特征的智能识别
        best_match = None
        highest_score = 0
        
        for col in df.columns:
            # 计算列与UCS的匹配分数
            score = self._calculate_column_score(str(col))
            
            # 同时考虑数据特征
            if df[col].dtype in [np.float64, np.int64]:
                # 尝试计算统计值
                try:
                    col_min = df[col].min()
                    col_max = df[col].max()
                    col_mean = df[col].mean()
                    
                    # UCS值通常在0-100之间
                    if 0 <= col_min and col_max <= 100:
                        score += 0.3
                    
                    # UCS值通常为正数
                    if col_min >= 0:
                        score += 0.2
                    
                    # UCS值通常有一定的范围
                    if col_max - col_min > 5:
                        score += 0.1
                except:
                    pass
            
            if score > highest_score:
                highest_score = score
                best_match = col
        
        if best_match:
            print(f"[SUCCESS] 基于数据特征的智能识别成功: {best_match} (分数: {highest_score})")
            return best_match
        
        # 4. 尝试所有数值列
        numeric_columns = []
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                numeric_columns.append(col)
        
        if numeric_columns:
            # 选择最后一个数值列（通常UCS在最后）
            best_match = numeric_columns[-1]
            print(f"[SUCCESS] 选择最后一个数值列: {best_match}")
            return best_match
        
        # 5. 尝试所有列，不管类型
        if len(df.columns) > 0:
            # 选择最后一列
            best_match = df.columns[-1]
            print(f"[SUCCESS] 选择最后一列: {best_match}")
            return best_match
        
        raise ValueError(f"数据中未找到UCS相关列，请检查数据文件。可用列名: {df.columns.tolist()}")
    
    def _calculate_column_score(self, column_name):
        """计算列名与UCS的匹配分数
        
        Args:
            column_name: 列名
            
        Returns:
            匹配分数
        """
        score = 0
        col_str = column_name.lower()
        
        # 关键词匹配
        ucs_keywords = ['ucs', '抗压', '强度', 'strength', 'compressive']
        for keyword in ucs_keywords:
            if keyword in col_str:
                score += 0.2
        
        # 单位匹配
        unit_keywords = ['mpa', '兆帕', '压强', '压力']
        for keyword in unit_keywords:
            if keyword in col_str:
                score += 0.1
        
        return score
        
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
