import argparse
import os
import sys
from ..core.optimizer import UCSOptimizer


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='UCS Optimizer - 水泥强度预测和环境影响评估工具')
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 训练命令
    train_parser = subparsers.add_parser('train', help='训练UCS预测模型')
    train_parser.add_argument('--data', required=True, help='训练数据文件路径')
    train_parser.add_argument('--lci', help='生命周期清单文件路径')
    train_parser.add_argument('--output', default='results', help='结果保存目录')
    
    # 微调命令
    fine_tune_parser = subparsers.add_parser('fine-tune', help='使用新数据微调模型')
    fine_tune_parser.add_argument('--model', required=True, help='预训练模型文件路径')
    fine_tune_parser.add_argument('--data', required=True, help='微调数据文件路径')
    fine_tune_parser.add_argument('--output', default='results', help='结果保存目录')
    
    # 预测命令
    predict_parser = subparsers.add_parser('predict', help='使用模型预测UCS值')
    predict_parser.add_argument('--model', required=True, help='模型文件路径')
    predict_parser.add_argument('--data', required=True, help='预测数据文件路径')
    predict_parser.add_argument('--output', default='results', help='结果保存目录')
    
    # LCA计算命令
    lca_parser = subparsers.add_parser('lca', help='计算LCA指标')
    lca_parser.add_argument('--data', required=True, help='数据文件路径')
    lca_parser.add_argument('--lci', help='生命周期清单文件路径')
    lca_parser.add_argument('--output', default='results', help='结果保存目录')
    
    # 完整分析命令
    analyze_parser = subparsers.add_parser('analyze', help='运行完整分析流程')
    analyze_parser.add_argument('--data', required=True, help='数据文件路径')
    analyze_parser.add_argument('--lci', help='生命周期清单文件路径')
    analyze_parser.add_argument('--model', help='预训练模型文件路径（可选）')
    analyze_parser.add_argument('--output', default='results', help='结果保存目录')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    # 创建优化器实例
    optimizer = UCSOptimizer()
    
    # 设置结果目录
    output_dir = os.path.abspath(args.output)
    optimizer.set_result_directory(output_dir)
    
    try:
        if args.command == 'train':
            # 训练模型
            print('开始训练UCS预测模型...')
            if args.lci:
                optimizer.load_lci_data(args.lci)
            optimizer.train_ucs_model(args.data)
            # 保存模型
            model_path = os.path.join(output_dir, 'ucs_model.pkl')
            optimizer.save_model(model_path)
            print(f'模型已保存至: {model_path}')
            
        elif args.command == 'fine-tune':
            # 微调模型
            print('开始微调UCS预测模型...')
            optimizer.load_ucs_model(args.model)
            optimizer.fine_tune_ucs_model(args.data)
            # 保存微调后的模型
            model_path = os.path.join(output_dir, 'ucs_model_fine_tuned.pkl')
            optimizer.save_model(model_path)
            print(f'微调后的模型已保存至: {model_path}')
            
        elif args.command == 'predict':
            # 预测UCS值
            print('开始预测UCS值...')
            optimizer.load_ucs_model(args.model)
            
            # 加载数据
            import pandas as pd
            df = pd.read_excel(args.data)
            
            # 提取特征
            target_column = 'UCS (Mpa)'
            if target_column not in df.columns:
                possible_columns = ['UCS', 'UCS (MPa)', '抗压强度']
                for col in possible_columns:
                    if col in df.columns:
                        target_column = col
                        break
            
            X = df.drop(target_column, axis=1) if target_column in df.columns else df
            
            # 预测
            predictions = optimizer.predict_ucs(X)
            df['Predicted UCS'] = predictions
            
            # 保存结果
            output_file = os.path.join(output_dir, 'predictions.xlsx')
            df.to_excel(output_file, index=False)
            print(f'预测结果已保存至: {output_file}')
            
        elif args.command == 'lca':
            # 计算LCA指标
            print('开始计算LCA指标...')
            if args.lci:
                optimizer.load_lci_data(args.lci)
            
            # 加载数据
            import pandas as pd
            df = pd.read_excel(args.data)
            
            # 计算LCA
            lca_results = optimizer.calculate_lca(df)
            
            # 保存结果
            output_file = os.path.join(output_dir, 'lca_results.xlsx')
            lca_results.to_excel(output_file, index=False)
            print(f'LCA计算结果已保存至: {output_file}')
            
        elif args.command == 'analyze':
            # 运行完整分析
            print('开始运行完整分析...')
            optimizer.run_full_analysis(
                args.data,
                lci_file=args.lci,
                model_path=args.model
            )
            
        else:
            print('请指定命令，使用 --help 查看可用命令')
            sys.exit(1)
            
    except Exception as e:
        print(f'错误: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
