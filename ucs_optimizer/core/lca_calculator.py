import pandas as pd
import os
import re

class LCACalculator:
    def __init__(self):
        self.carbon_cement = 0.82    # kg CO2 / kg 水泥
        self.energy_cement = 115    # kWh / ton 水泥
        self.cost_cement = 0.084    # $ / kg 水泥
        self.cost_water = 0.001     # $ / kg 水
        
    def load_lci_data(self, lci_file):
        """加载生命周期清单数据"""
        # 检查是否为文件对象（Streamlit上传的文件）
        if hasattr(lci_file, 'read'):
            # 对于文件对象，直接读取
            lci_df = pd.read_excel(lci_file, engine='openpyxl')
        else:
            # 对于文件路径，检查是否存在
            if os.path.exists(lci_file):
                lci_df = pd.read_excel(lci_file, engine='openpyxl')
            else:
                # 如果文件不存在，使用默认值
                print('生命周期清单文件不存在，使用默认值')
                return
        
        print(f'生命周期清单文件列名: {list(lci_df.columns)}')
        
        # 尝试不同的列名组合
        try:
            # 使用英文列名
            material_col = 'Materials/curving condition'
            cost_col = 'Cost（＄ /kg）'
            carbon_col = 'Carbon footprint（kg/kg）'
            energy_col = 'Energy consumption（kWh/t）'
            
            # 打印所有材料类型，以便调试
            print(f'生命周期清单中的材料类型: {list(lci_df[material_col].unique())}')
            
            # 尝试不同的水泥名称
            cement_names = ['Cement', '水泥', 'cement', 'CEMENT']
            cement_found = False
            for cement_name in cement_names:
                cement_rows = lci_df[lci_df[material_col] == cement_name]
                if len(cement_rows) > 0:
                    cement_lci = cement_rows.iloc[0]
                    
                    # 提取纯数字值（去除文献引用）
                    def extract_numeric(value):
                        match = re.search(r'[-+]?\d*\.?\d+', str(value))
                        if match:
                            return float(match.group())
                        return None
                    
                    self.carbon_cement = extract_numeric(cement_lci[carbon_col])
                    self.energy_cement = extract_numeric(cement_lci[energy_col])
                    self.cost_cement = extract_numeric(cement_lci[cost_col])
                    
                    if all([self.carbon_cement, self.energy_cement, self.cost_cement]):
                        cement_found = True
                        print(f'找到水泥数据: {cement_name}')
                        break
                    else:
                        print(f'水泥数据提取失败，尝试下一个名称')
            
            if not cement_found:
                raise Exception('未找到水泥数据')
            
            # 尝试不同的水名称
            water_names = ['Water', '水', 'water', 'WATER']
            water_found = False
            for water_name in water_names:
                water_rows = lci_df[lci_df[material_col] == water_name]
                if len(water_rows) > 0:
                    water_lci = water_rows.iloc[0]
                    
                    # 提取纯数字值
                    def extract_numeric(value):
                        match = re.search(r'[-+]?\d*\.?\d+', str(value))
                        if match:
                            return float(match.group())
                        return None
                    
                    self.cost_water = extract_numeric(water_lci[cost_col])
                    
                    if self.cost_water is not None:
                        water_found = True
                        print(f'找到水数据: {water_name}')
                        break
                    else:
                        print(f'水数据提取失败，尝试下一个名称')
            
            if not water_found:
                raise Exception('未找到水数据')
            
            print('生命周期清单数据读取成功')
            print(f'水泥碳排放系数: {self.carbon_cement} kg CO2/kg')
            print(f'水泥能耗系数: {self.energy_cement} kWh/ton')
            print(f'水泥成本: {self.cost_cement} $/kg')
            print(f'水成本: {self.cost_water} $/kg')
        except Exception as e:
            print(f'读取生命周期清单数据失败: {e}，使用默认值')
            # 保持默认值
    
    def calculate_lca(self, df, total_mass=1000):
        """计算LCA指标"""
        print('开始LCA计算...')
        
        # 1. 各材料质量
        df["固体质量_kg"] = total_mass * df["MC"] / 100
        # 修正后的水泥质量计算逻辑
        df["水泥质量_kg"] = df["固体质量_kg"] * df["CTR"] / (1 + df["CTR"])
        df["尾矿质量_kg"] = df["固体质量_kg"] - df["水泥质量_kg"]
        df["水质量_kg"] = total_mass - df["固体质量_kg"]
        
        # 2. 环境影响 & 成本
        df["总碳足迹_kgCO2"] = df["水泥质量_kg"] * self.carbon_cement
        df["总能耗_kWh"] = df["水泥质量_kg"] * self.energy_cement / 1000
        df["总成本_USD"] = df["水泥质量_kg"] * self.cost_cement + df["水质量_kg"] * self.cost_water
        
        # 3. 强度归一化指标（论文标准）
        if 'UCS' in df.columns:
            # 过滤掉UCS值为0的样本
            ucs_col = 'UCS'
            initial_count = len(df)
            df = df[df[ucs_col] > 0]
            filtered_count = len(df)
            if initial_count > filtered_count:
                print(f'过滤掉 {initial_count - filtered_count} 个UCS值为0的样本')
            
            df["碳足迹_per_MPa"] = df["总碳足迹_kgCO2"] / df[ucs_col]
            df["能耗_per_MPa"] = df["总能耗_kWh"] / df[ucs_col]
            df["成本_per_MPa"] = df["总成本_USD"] / df[ucs_col]
        elif 'UCS (Mpa)' in df.columns:
            # 过滤掉UCS值为0的样本
            ucs_col = 'UCS (Mpa)'
            initial_count = len(df)
            df = df[df[ucs_col] > 0]
            filtered_count = len(df)
            if initial_count > filtered_count:
                print(f'过滤掉 {initial_count - filtered_count} 个UCS值为0的样本')
            
            df["碳足迹_per_MPa"] = df["总碳足迹_kgCO2"] / df[ucs_col]
            df["能耗_per_MPa"] = df["总能耗_kWh"] / df[ucs_col]
            df["成本_per_MPa"] = df["总成本_USD"] / df[ucs_col]
        else:
            print('未找到UCS列，无法计算归一化指标')
        
        print('LCA计算完成！')
        return df
    
    def get_lca_metrics(self, df):
        """获取LCA指标统计信息"""
        if not df.empty:
            metrics = {
                '平均水泥质量': df["水泥质量_kg"].mean(),
                '平均总碳足迹': df["总碳足迹_kgCO2"].mean(),
                '平均总能耗': df["总能耗_kWh"].mean(),
                '平均总成本': df["总成本_USD"].mean()
            }
            
            if '碳足迹_per_MPa' in df.columns:
                metrics.update({
                    '平均碳足迹_per_MPa': df["碳足迹_per_MPa"].mean(),
                    '平均能耗_per_MPa': df["能耗_per_MPa"].mean(),
                    '平均成本_per_MPa': df["成本_per_MPa"].mean()
                })
            
            return metrics
        else:
            return {}
