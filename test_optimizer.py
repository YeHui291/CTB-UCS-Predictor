#!/usr/bin/env python
# 测试UCS Optimizer功能

import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ucs_optimizer.core.optimizer import UCSOptimizer

def test_optimizer():
    """测试UCS Optimizer的基本功能"""
    print("开始测试UCS Optimizer...")
    
    # 初始化优化器
    optimizer = UCSOptimizer()
    optimizer.set_result_directory('test_results')
    
    # 测试数据文件路径
    data_file = 'data/sample_cement_data.xlsx'
    lci_file = 'data/sample_lci_data.xlsx'
    
    try:
        # 运行完整分析
        print("\n1. 运行完整分析...")
        lca_results, lca_metrics = optimizer.run_full_analysis(
            data_file,
            lci_file=lci_file
        )
        
        print("\n2. 保存模型...")
        model_path = 'test_results/ucs_model.pkl'
        optimizer.save_model(model_path)
        print(f'模型已保存至: {model_path}')
        
        print("\n3. 加载模型...")
        optimizer.load_ucs_model(model_path)
        print("模型加载成功！")
        
        print("\n4. 测试预测功能...")
        import pandas as pd
        df = pd.read_excel(data_file)
        X = df.drop('UCS', axis=1)
        predictions = optimizer.predict_ucs(X)
        print(f'预测结果: {predictions[:5]}...')
        
        print("\n5. 测试LCA计算功能...")
        lca_results = optimizer.calculate_lca(df)
        print(f'LCA计算结果行数: {len(lca_results)}')
        print(f'LCA指标列: {list(lca_results.columns)}')
        
        print("\n测试完成！所有功能运行正常。")
        
    except Exception as e:
        print(f'测试失败: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_optimizer()
