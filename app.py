import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ucs_optimizer.core.optimizer import UCSOptimizer
from ucs_optimizer.core.lca_calculator import LCACalculator

# 设置页面配置
st.set_page_config(
    page_title="UCS Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stHeader {
        color: #1a1a2e;
        font-weight: bold;
    }
    .stSubheader {
        color: #16213e;
    }
    .stMetric {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stRadio > div {
        padding: 8px;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stNumberInput > div > div > input {
        border-radius: 4px;
    }
    .stFileUploader > div > div > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("⚡ UCS Optimizer")
st.markdown("**水泥强度预测和环境影响评估工具**")

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
        
        # 读取数据
        df = pd.read_excel(uploaded_file)
        
        # 检查是否包含 UCS 相关列
        ucs_columns = ['UCS', 'UCS (MPa)', 'UCS (Mpa)', '抗压强度', '抗压强度值', 'UCS值', '强度', '水泥强度']
        has_ucs = any(col in df.columns for col in ucs_columns)
        
        if not has_ucs:
            st.error(f"数据中未找到UCS相关列，请检查数据文件。可用列名: {df.columns.tolist()}")
        else:
            # 显示可编辑的数据表格
            st.subheader("训练数据（可编辑）")
            edited_df = st.data_editor(df, use_container_width=True)

            # 训练参数
            st.subheader("训练参数")
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2)
            random_state = st.number_input("随机种子", 0, 1000, 42)

            # 训练按钮
            if st.button("开始训练"):
                with st.spinner("正在训练模型..."):
                    # 保存编辑后的数据到临时文件
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                        tmp_path = tmp.name
                    
                    edited_df.to_excel(tmp_path, index=False)
                    
                    optimizer = UCSOptimizer()
                    # 训练模型
                    model, metrics = optimizer.train(
                        data_path=tmp_path,
                        test_size=test_size,
                        random_state=random_state
                    )
                    
                    # 清理临时文件
                    os.unlink(tmp_path)

                st.success("模型训练完成！")

                # 显示训练结果
                st.subheader("训练结果")
                st.write(f"R² 评分: {metrics['r2']:.2f}")
                st.write(f"均方误差: {metrics['mse']:.2f}")

# 强度预测页面
elif selected_page == "强度预测":
    st.header("强度预测")
    
    # 预测方式选择
    prediction_method = st.radio(
        "选择预测方式",
        ["文件上传", "手动输入"]
    )
    
    if prediction_method == "文件上传":
        # 上传预测数据
        data_file = st.file_uploader("上传预测数据文件", type=["xlsx"])
        
        if data_file:
            st.success("文件上传成功！")
            
            # 读取数据
            df = pd.read_excel(data_file)
            
            # 显示可编辑的数据表格
            st.subheader("预测数据（可编辑）")
            edited_df = st.data_editor(df, use_container_width=True)
            
            # 预测按钮
            if st.button("开始预测"):
                with st.spinner("正在预测..."):
                    # 保存编辑后的数据到临时文件
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                        tmp_path = tmp.name
                    
                    edited_df.to_excel(tmp_path, index=False)
                    
                    optimizer = UCSOptimizer()
                    # 使用示例数据训练模型
                    import os
                    sample_data = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_cement_data.xlsx")
                    model, metrics = optimizer.train(data_path=sample_data)
                    # 然后预测
                    predictions = optimizer.predict(input_data=tmp_path)
                    
                    # 清理临时文件
                    os.unlink(tmp_path)
                    
                st.success("预测完成！")
                
                # 显示预测结果
                st.subheader("预测结果")
                st.dataframe(predictions)
    
    else:  # 手动输入
        st.subheader("手动输入特征变量")
        
        # 特征变量输入（11个特征）
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cu = st.number_input("Cu", min_value=0.0, value=12.7)
            cc = st.number_input("Cc", min_value=0.0, value=1.3)
            tem = st.number_input("TEM", min_value=0.0, value=25.0)
            d10 = st.number_input("D10", min_value=0.0, value=0.005)
        
        with col2:
            sio2 = st.number_input("SiO2", min_value=0.0, value=29.11)
            cao = st.number_input("CaO", min_value=0.0, value=32.65)
            al2o3 = st.number_input("Al2O3", min_value=0.0, value=0.37)
            ct = st.number_input("CT", min_value=0.0, value=32.5)
        
        with col3:
            ctr = st.number_input("CTR", min_value=0.0, max_value=1.0, value=0.25)
            mc = st.number_input("MC", min_value=0.0, max_value=100.0, value=76.0)
            t = st.number_input("T", min_value=0.0, value=7.0)
        
        # 预测按钮
        if st.button("开始预测"):
            with st.spinner("正在预测..."):
                # 创建输入数据
                input_data = pd.DataFrame({
                    "Cu": [cu],
                    "Cc": [cc],
                    "TEM": [tem],
                    "D10": [d10],
                    "SiO2": [sio2],
                    "CaO": [cao],
                    "Al2O3": [al2o3],
                    "CT": [ct],
                    "CTR": [ctr],
                    "MC": [mc],
                    "T": [t]
                })
                
                # 保存为临时文件
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    tmp_path = tmp.name
                
                input_data.to_excel(tmp_path, index=False)
                
                # 训练模型（使用示例数据）
                optimizer = UCSOptimizer()
                # 使用示例数据训练模型
                import os
                sample_data = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_cement_data.xlsx")
                model, metrics = optimizer.train(data_path=sample_data)
                
                # 进行预测
                predictions = optimizer.predict(input_data=tmp_path)
                
                # 清理临时文件
                os.unlink(tmp_path)
                
            st.success("预测完成！")
            
            # 显示预测结果
            st.subheader("预测结果")
            st.dataframe(predictions)
            
            # 显示预测值
            predicted_ucs = predictions['Predicted UCS'].values[0]
            st.metric("预测 UCS 值", f"{predicted_ucs:.2f} MPa")

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
        
        # 计算方式选择
        calc_method = st.radio(
            "计算方式",
            options=["文件数据", "手动输入"],
            key="lca_calc_method"
        )
        
        if calc_method == "文件数据":
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
        
        else:  # 手动输入
            st.subheader("手动输入计算参数")
            
            # 输入参数
            col1, col2, col3 = st.columns(3)
            
            with col1:
                mc1 = st.number_input("MC 1", min_value=0.0, value=20.0)
                ctr1 = st.number_input("CTR 1", min_value=0.0, max_value=1.0, value=0.1)
                ucs1 = st.number_input("UCS 1", min_value=0.0, value=10.0)
            
            with col2:
                mc2 = st.number_input("MC 2", min_value=0.0, value=25.0)
                ctr2 = st.number_input("CTR 2", min_value=0.0, max_value=1.0, value=0.2)
                ucs2 = st.number_input("UCS 2", min_value=0.0, value=15.0)
            
            with col3:
                mc3 = st.number_input("MC 3", min_value=0.0, value=30.0)
                ctr3 = st.number_input("CTR 3", min_value=0.0, max_value=1.0, value=0.3)
                ucs3 = st.number_input("UCS 3", min_value=0.0, value=20.0)
            
            # 计算按钮
            if st.button("开始计算"):
                with st.spinner("正在计算 LCA 指标..."):
                    lca_calculator = LCACalculator()
                    lca_calculator.load_lci_data(lci_file)
                    # 使用手动输入数据进行计算
                    input_df = pd.DataFrame({
                        "MC": [mc1, mc2, mc3],
                        "CTR": [ctr1, ctr2, ctr3],
                        "UCS": [ucs1, ucs2, ucs3]
                    })
                    lca_results = lca_calculator.calculate_lca(input_df)
                    
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
    
    # 分析方式选择
    analysis_method = st.radio(
        "分析方式",
        options=["文件上传", "手动输入"],
        key="analysis_method"
    )
    
    if analysis_method == "文件上传":
        # 上传数据文件
        cement_file = st.file_uploader("上传水泥数据文件", type=["xlsx"])
        lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"])
        
        if cement_file and lci_file:
            st.success("文件上传成功！")
            
            # 读取水泥数据
            df = pd.read_excel(cement_file)
            
            # 显示可编辑的数据表格
            st.subheader("水泥数据（可编辑）")
            edited_df = st.data_editor(df, use_container_width=True)
            
            # 分析参数
            st.subheader("分析参数")
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2)
            random_state = st.number_input("随机种子", 0, 1000, 42)
            
            # 分析按钮
            if st.button("开始完整分析"):
                with st.spinner("正在进行完整分析..."):
                    # 保存编辑后的数据到临时文件
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                        tmp_path = tmp.name
                    
                    edited_df.to_excel(tmp_path, index=False)
                    
                    optimizer = UCSOptimizer()
                    # 先训练模型
                    model, metrics = optimizer.train(
                        data_path=tmp_path,
                        test_size=test_size,
                        random_state=random_state
                    )
                    # 加载 LCI 数据
                    optimizer.load_lci_data(lci_file)
                    # 运行完整分析
                    lca_results, lca_metrics = optimizer.run_full_analysis(
                        data_file=tmp_path
                    )
                    
                    # 清理临时文件
                    os.unlink(tmp_path)
                    
                st.success("分析完成！")
                
                # 显示分析结果
                st.subheader("分析结果")
                st.write("### LCA 计算结果")
                st.dataframe(lca_results.head())
    
    else:  # 手动输入
        st.subheader("手动输入分析参数")
        
        # 上传 LCI 数据文件（仍然需要）
        lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"])
        
        if lci_file:
            st.success("LCI 数据文件上传成功！")
            
            # 手动输入水泥数据
            st.subheader("水泥数据")
            
            # 输入参数
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cu = st.number_input("Cu", min_value=0.0, value=12.7)
                cc = st.number_input("Cc", min_value=0.0, value=1.3)
                tem = st.number_input("TEM", min_value=0.0, value=25.0)
                d10 = st.number_input("D10", min_value=0.0, value=0.005)
            
            with col2:
                sio2 = st.number_input("SiO2", min_value=0.0, value=29.11)
                cao = st.number_input("CaO", min_value=0.0, value=32.65)
                al2o3 = st.number_input("Al2O3", min_value=0.0, value=0.37)
                ct = st.number_input("CT", min_value=0.0, value=32.5)
            
            with col3:
                ctr = st.number_input("CTR", min_value=0.0, max_value=1.0, value=0.25)
                mc = st.number_input("MC", min_value=0.0, max_value=100.0, value=76.0)
                t = st.number_input("T", min_value=0.0, value=7.0)
                ucs = st.number_input("UCS", min_value=0.0, value=2.41)
            
            # 分析参数
            st.subheader("分析参数")
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2)
            random_state = st.number_input("随机种子", 0, 1000, 42)
            
            # 分析按钮
            if st.button("开始完整分析"):
                with st.spinner("正在进行完整分析..."):
                    # 创建输入数据
                    input_data = pd.DataFrame({
                        "Cu": [cu],
                        "Cc": [cc],
                        "TEM": [tem],
                        "D10": [d10],
                        "SiO2": [sio2],
                        "CaO": [cao],
                        "Al2O3": [al2o3],
                        "CT": [ct],
                        "CTR": [ctr],
                        "MC": [mc],
                        "T": [t],
                        "UCS": [ucs]
                    })
                    
                    # 保存为临时文件
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                        tmp_path = tmp.name
                    
                    input_data.to_excel(tmp_path, index=False)
                    
                    # 执行分析
                    optimizer = UCSOptimizer()
                    # 先训练模型
                    model, metrics = optimizer.train(
                        data_path=tmp_path,
                        test_size=test_size,
                        random_state=random_state
                    )
                    # 加载 LCI 数据
                    optimizer.load_lci_data(lci_file)
                    # 运行完整分析
                    lca_results, lca_metrics = optimizer.run_full_analysis(
                        data_file=tmp_path
                    )
                    
                    # 清理临时文件
                    os.unlink(tmp_path)
                    
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
