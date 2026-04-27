import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ucs_optimizer.core.optimizer import UCSOptimizer
from ucs_optimizer.core.lca_calculator import LCACalculator

# 页面标题
st.title("UCS Optimizer - 水泥强度预测和环境影响评估")

# 侧边栏导航
with st.sidebar:
    st.title("功能导航")
    selected_page = st.radio(
        "选择功能",
        ["首页", "模型训练", "强度预测", "LCA 计算", "完整分析"]
    )

# 首页
if selected_page == "首页":
    st.header("UCS Optimizer 简介")
    st.write("""
    UCS Optimizer 是一个用于水泥强度预测和环境影响评估的工具。
    它可以帮助您：
    - 训练水泥强度预测模型
    - 预测水泥的抗压强度
    - 计算环境影响指标 (LCA)
    - 进行完整的分析流程
    """)
    
    st.subheader("示例数据")
    st.write("项目提供了以下示例数据：")
    st.markdown("- `sample_cement_data.xlsx` - 水泥强度训练数据")
    st.markdown("- `sample_lci_data.xlsx` - LCA 计算数据")

# 模型训练页面
elif selected_page == "模型训练":
    st.header("模型训练")
    
    # 文件上传
    uploaded_file = st.file_uploader("上传训练数据文件", type=["xlsx"])
    
    if uploaded_file is not None:
        st.success("文件上传成功！")
        
        # 显示数据预览
        df = pd.read_excel(uploaded_file)
        st.subheader("数据预览")
        st.dataframe(df.head())

        # 训练参数
        st.subheader("训练参数")
        test_size = st.slider("测试集比例", 0.1, 0.5, 0.2)
        random_state = st.number_input("随机种子", 0, 1000, 42)

        # 训练按钮
        if st.button("开始训练"):
            with st.spinner("正在训练模型..."):
                optimizer = UCSOptimizer()
                # 训练模型
                model, metrics = optimizer.train(
                    data_path=uploaded_file,
                    test_size=test_size,
                    random_state=random_state
                )

            st.success("模型训练完成！")

            # 显示训练结果
            st.subheader("训练结果")
            st.write(f"R² 评分: {metrics['r2']:.2f}")
            st.write(f"均方误差: {metrics['mse']:.2f}")

# 强度预测页面
elif selected_page == "强度预测":
    st.header("强度预测")
    
    # 上传预测数据
    data_file = st.file_uploader("上传预测数据文件", type=["xlsx"])
    
    if data_file:
        st.success("文件上传成功！")
        
        # 显示数据预览
        df = pd.read_excel(data_file)
        st.subheader("预测数据预览")
        st.dataframe(df.head())
        
        # 预测按钮
        if st.button("开始预测"):
            with st.spinner("正在预测..."):
                optimizer = UCSOptimizer()
                # 先训练一个模型
                model, metrics = optimizer.train(data_path=data_file)
                # 然后预测
                predictions = optimizer.predict(input_data=data_file)
                
            st.success("预测完成！")
            
            # 显示预测结果
            st.subheader("预测结果")
            st.dataframe(predictions)

# LCA 计算页面
elif selected_page == "LCA 计算":
    st.header("LCA 计算")
    
    # 上传 LCI 数据
    lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"])
    
    if lci_file:
        st.success("文件上传成功！")
        
        # 显示数据预览
        df = pd.read_excel(lci_file)
        st.subheader("LCI 数据预览")
        st.dataframe(df.head())
        
        # 计算按钮
        if st.button("开始计算"):
            with st.spinner("正在计算 LCA 指标..."):
                lca_calculator = LCACalculator()
                lca_calculator.load_lci_data(lci_file)
                # 使用示例数据进行计算
                sample_df = pd.DataFrame({
                    "MC": [20, 25, 30],
                    "CTR": [0.1, 0.2, 0.3],
                    "UCS": [10, 15, 20]
                })
                lca_results = lca_calculator.calculate_lca(sample_df)
                
            st.success("计算完成！")
            
            # 显示计算结果
            st.subheader("LCA 计算结果")
            st.dataframe(lca_results)
            
            # 可视化
            st.subheader("LCA 指标可视化")
            if not lca_results.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                lca_results.plot(kind='bar', ax=ax)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)

# 完整分析页面
elif selected_page == "完整分析":
    st.header("完整分析")
    
    # 上传数据文件
    cement_file = st.file_uploader("上传水泥数据文件", type=["xlsx"])
    lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"])
    
    if cement_file and lci_file:
        st.success("文件上传成功！")
        
        # 分析参数
        st.subheader("分析参数")
        test_size = st.slider("测试集比例", 0.1, 0.5, 0.2)
        random_state = st.number_input("随机种子", 0, 1000, 42)
        
        # 分析按钮
        if st.button("开始完整分析"):
            with st.spinner("正在进行完整分析..."):
                optimizer = UCSOptimizer()
                # 先训练模型
                model, metrics = optimizer.train(
                    data_path=cement_file,
                    test_size=test_size,
                    random_state=random_state
                )
                # 加载 LCI 数据
                optimizer.load_lci_data(lci_file)
                # 运行完整分析
                lca_results, lca_metrics = optimizer.run_full_analysis(
                    data_file=cement_file
                )
                
            st.success("分析完成！")
            
            # 显示分析结果
            st.subheader("分析结果")
            st.write("### LCA 计算结果")
            st.dataframe(lca_results.head())

# 页脚
st.markdown("""
---
**UCS Optimizer** - 水泥强度预测和环境影响评估工具
""")
