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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    }
    
    .stHeader {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .stSubheader {
        color: #34495e;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .stMetric {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    
    .stDataFrame {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .stRadio > div {
        padding: 12px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        padding: 8px;
    }
    
    .stFileUploader > div > div > button {
        border-radius: 8px;
        background-color: #ecf0f1;
        border: 2px dashed #bdc3c7;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > button:hover {
        background-color: #e8f4f8;
        border-color: #3498db;
    }
    
    .stSlider > div > div > div > div {
        background-color: #3498db;
    }
    
    .sidebar {
        background-color: #2c3e50;
        color: white;
    }
    
    .sidebar .stTitle {
        color: white;
        font-weight: 700;
    }
    
    .sidebar .stRadio > div {
        background-color: #34495e;
        color: white;
        border-radius: 8px;
    }
    
    .sidebar .stRadio > div:hover {
        background-color: #3d566e;
    }
    
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .highlight {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("⚡ UCS Optimizer")
st.markdown("**智能水泥强度预测和环境影响评估工具**")

# 侧边栏导航
with st.sidebar:
    st.title("功能导航")
    selected_page = st.radio(
        "选择功能",
        ["首页", "模型训练", "强度预测", "LCA 计算", "完整分析"]
    )
    
    # 添加版本信息
    st.markdown("---")
    st.markdown("**版本信息**")
    st.markdown("v1.0.0")
    
    # 添加使用提示
    st.markdown("---")
    st.markdown("**使用提示**")
    st.markdown("- 上传数据文件进行分析")
    st.markdown("- 支持 Excel 格式文件")
    st.markdown("- 可手动输入参数进行预测")

# 首页
if selected_page == "首页":
    st.header("UCS Optimizer 简介")
    
    # 添加卡片式布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 核心功能")
        st.write("• 智能水泥强度预测模型")
        st.write("• 环境影响评估 (LCA)")
        st.write("• 完整的分析流程")
        st.write("• 数据可视化展示")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 示例数据")
        st.write("• `sample_cement_data.xlsx` - 水泥强度训练数据")
        st.write("• `sample_lci_data.xlsx` - LCA 计算数据")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.subheader("🚀 快速开始")
    st.write("1. 上传您的水泥数据文件")
    st.write("2. 选择 UCS 列并训练模型")
    st.write("3. 使用训练好的模型进行预测")
    st.write("4. 计算环境影响指标")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 添加技术特点
    st.subheader("🔧 技术特点")
    features = {
        "机器学习模型": "使用先进的机器学习算法预测水泥强度",
        "多参数分析": "支持多种特征变量的综合分析",
        "环境影响评估": "计算水泥生产的环境影响指标",
        "用户友好界面": "直观的 Streamlit 网页界面",
        "数据可视化": "丰富的图表和数据展示",
        "灵活的输入方式": "支持文件上传和手动输入"
    }
    
    for feature, description in features.items():
        st.markdown(f"**{feature}**: {description}")
    
    # 添加联系信息
    st.markdown("---")
    st.subheader("📞 联系我们")
    st.write("如有任何问题或建议，请联系我们。")

# 模型训练页面
elif selected_page == "模型训练":
    st.header("模型训练")
    
    # 文件上传卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📁 数据上传")
    uploaded_file = st.file_uploader("上传训练数据文件", type=["xlsx"], key="train_uploader")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.success("文件上传成功！")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 读取数据
        df = pd.read_excel(uploaded_file)
        
        # UCS列设置卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 UCS列设置")
        
        # 自动检测可能的UCS列
        possible_ucs_columns = []
        for col in df.columns:
            col_str = str(col).lower()
            if 'ucs' in col_str or '抗压' in col_str or '强度' in col_str or 'strength' in col_str:
                possible_ucs_columns.append(col)
        
        # 选择UCS列
        if possible_ucs_columns:
            selected_ucs = st.selectbox(
                "选择UCS列",
                options=df.columns.tolist(),
                index=df.columns.tolist().index(possible_ucs_columns[0]) if possible_ucs_columns[0] in df.columns else 0,
                help="从检测到的列中选择包含UCS值的列"
            )
        else:
            # 如果没有检测到，让用户从所有列中选择
            selected_ucs = st.selectbox(
                "选择UCS列",
                options=df.columns.tolist(),
                help="从所有列中选择包含UCS值的列"
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # 列名调整卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔧 列名调整")
        
        # 显示当前列名
        st.write("当前列名：")
        st.code(', '.join([str(col) for col in df.columns]))
        
        # 提供列名修改功能
        st.write("调整列名：")
        adjusted_columns = []
        for i, col in enumerate(df.columns):
            new_col = st.text_input(f"列 {i+1}：{col}", value=str(col), key=f"col_{i}")
            adjusted_columns.append(new_col)
        
        # 应用列名调整
        if st.button("✅ 应用列名调整"):
            df.columns = adjusted_columns
            st.success("列名调整成功！")
            st.write("新列名：", df.columns.tolist())
        st.markdown('</div>', unsafe_allow_html=True)

        # 数据预览卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 训练数据（可编辑）")
        edited_df = st.data_editor(df, use_container_width=True)
        
        # 显示数据统计信息
        st.subheader("📈 数据统计")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("样本数量", len(df))
        with col2:
            st.metric("特征数量", len(df.columns) - 1)
        with col3:
            st.metric("UCS列", selected_ucs)
        st.markdown('</div>', unsafe_allow_html=True)

        # 训练参数卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚙️ 训练参数")
        col1, col2 = st.columns(2)
        with col1:
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, help="用于评估模型的测试数据比例")
        with col2:
            random_state = st.number_input("随机种子", 0, 1000, 42, help="控制数据分割的随机性")
        st.markdown('</div>', unsafe_allow_html=True)

        # 训练按钮
        if st.button("🚀 开始训练"):
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
                    random_state=random_state,
                    target_column=selected_ucs
                )
                
                # 清理临时文件
                os.unlink(tmp_path)

            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("模型训练完成！")
            st.markdown('</div>', unsafe_allow_html=True)

            # 训练结果卡片
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🏆 训练结果")
            
            # 使用列显示指标
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("R² 评分", f"{metrics['r2']:.2f}")
            with col2:
                st.metric("均方误差", f"{metrics['mse']:.2f}")
            with col3:
                st.metric("训练样本", f"{int(len(edited_df) * (1 - test_size))}")
            with col4:
                st.metric("测试样本", f"{int(len(edited_df) * test_size)}")
            
            # 添加模型性能说明
            if metrics['r2'] > 0.8:
                st.markdown("✅ 模型性能优秀，预测准确度高")
            elif metrics['r2'] > 0.6:
                st.markdown("⚠️ 模型性能良好，可以使用")
            else:
                st.markdown("❌ 模型性能较差，建议增加数据或调整参数")
            st.markdown('</div>', unsafe_allow_html=True)

# 强度预测页面
elif selected_page == "强度预测":
    st.header("强度预测")
    
    # 预测方式选择卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 预测方式")
    prediction_method = st.radio(
        "选择预测方式",
        ["文件上传", "手动输入"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prediction_method == "文件上传":
        # 文件上传卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 数据上传")
        data_file = st.file_uploader("上传预测数据文件", type=["xlsx"], key="predict_uploader")
        
        if data_file:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("文件上传成功！")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 读取数据
            df = pd.read_excel(data_file)
            
            # 显示可编辑的数据表格
            st.subheader("📊 预测数据（可编辑）")
            edited_df = st.data_editor(df, use_container_width=True)
            
            # 预测按钮
            if st.button("🚀 开始预测"):
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
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("预测完成！")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 显示预测结果
                st.subheader("🏆 预测结果")
                st.dataframe(predictions)
                
                # 显示预测统计信息
                st.subheader("📈 预测统计")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("预测样本数", len(predictions))
                with col2:
                    st.metric("平均UCS", f"{predictions['Predicted UCS'].mean():.2f} MPa")
                with col3:
                    st.metric("最大UCS", f"{predictions['Predicted UCS'].max():.2f} MPa")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # 手动输入
        # 手动输入卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 手动输入特征变量")
        
        # 特征变量输入（11个特征）
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cu = st.number_input("Cu", min_value=0.0, value=12.7, help="曲率系数")
            cc = st.number_input("Cc", min_value=0.0, value=1.3, help="不均匀系数")
            tem = st.number_input("TEM", min_value=0.0, value=25.0, help="温度 (°C)")
            d10 = st.number_input("D10", min_value=0.0, value=0.005, help="有效粒径 (mm)")
        
        with col2:
            sio2 = st.number_input("SiO2", min_value=0.0, value=29.11, help="二氧化硅含量 (%)")
            cao = st.number_input("CaO", min_value=0.0, value=32.65, help="氧化钙含量 (%)")
            al2o3 = st.number_input("Al2O3", min_value=0.0, value=0.37, help="氧化铝含量 (%)")
            ct = st.number_input("CT", min_value=0.0, value=32.5, help="水泥类型")
        
        with col3:
            ctr = st.number_input("CTR", min_value=0.0, max_value=1.0, value=0.25, help="水泥-尾矿比")
            mc = st.number_input("MC", min_value=0.0, max_value=100.0, value=76.0, help="质量浓度 (%)")
            t = st.number_input("T", min_value=0.0, value=7.0, help="固化时间 (天)")
        
        # 预测按钮
        if st.button("🚀 开始预测"):
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
                
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("预测完成！")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示预测结果
            st.subheader("🏆 预测结果")
            st.dataframe(predictions)
            
            # 显示预测值
            predicted_ucs = predictions['Predicted UCS'].values[0]
            
            # 创建预测结果卡片
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 预测详情")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("预测 UCS 值", f"{predicted_ucs:.2f} MPa")
            with col2:
                # 强度等级评估
                if predicted_ucs >= 25:
                    st.metric("强度等级", "高强度")
                elif predicted_ucs >= 15:
                    st.metric("强度等级", "中等强度")
                else:
                    st.metric("强度等级", "低强度")
            
            # 显示输入参数
            st.subheader("🔧 输入参数")
            st.dataframe(input_data)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# LCA 计算页面
elif selected_page == "LCA 计算":
    st.header("LCA 计算")
    
    # 文件上传卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📁 LCI 数据上传")
    lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"], key="lci_uploader_1")
    
    if lci_file:
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.success("文件上传成功！")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示数据预览
        df = pd.read_excel(lci_file)
        st.subheader("📊 LCI 数据预览")
        st.dataframe(df.head())
        
        # 计算方式选择
        st.subheader("🔄 计算方式")
        calc_method = st.radio(
            "选择计算方式",
            options=["文件数据", "手动输入"],
            key="lca_calc_method"
        )
        
        if calc_method == "文件数据":
            # 计算按钮
            if st.button("🚀 开始计算"):
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
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("计算完成！")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 显示计算结果
                st.subheader("🏆 LCA 计算结果")
                st.dataframe(lca_results)
                
                # 可视化
                st.subheader("📈 LCA 指标可视化")
                if not lca_results.empty:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lca_results.plot(kind='bar', ax=ax)
                    plt.xticks(rotation=45)
                    plt.title("环境影响指标对比")
                    plt.tight_layout()
                    st.pyplot(fig)
        
        else:  # 手动输入
            st.subheader("🎯 手动输入计算参数")
            
            # 输入参数
            col1, col2, col3 = st.columns(3)
            
            with col1:
                mc1 = st.number_input("MC 1", min_value=0.0, value=20.0, help="质量浓度 (%)")
                ctr1 = st.number_input("CTR 1", min_value=0.0, max_value=1.0, value=0.1, help="水泥-尾矿比")
                ucs1 = st.number_input("UCS 1", min_value=0.0, value=10.0, help="抗压强度 (MPa)")
            
            with col2:
                mc2 = st.number_input("MC 2", min_value=0.0, value=25.0, help="质量浓度 (%)")
                ctr2 = st.number_input("CTR 2", min_value=0.0, max_value=1.0, value=0.2, help="水泥-尾矿比")
                ucs2 = st.number_input("UCS 2", min_value=0.0, value=15.0, help="抗压强度 (MPa)")
            
            with col3:
                mc3 = st.number_input("MC 3", min_value=0.0, value=30.0, help="质量浓度 (%)")
                ctr3 = st.number_input("CTR 3", min_value=0.0, max_value=1.0, value=0.3, help="水泥-尾矿比")
                ucs3 = st.number_input("UCS 3", min_value=0.0, value=20.0, help="抗压强度 (MPa)")
            
            # 计算按钮
            if st.button("🚀 开始计算"):
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
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("计算完成！")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 显示计算结果
                st.subheader("🏆 LCA 计算结果")
                st.dataframe(lca_results)
                
                # 可视化
                st.subheader("📈 LCA 指标可视化")
                if not lca_results.empty:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lca_results.plot(kind='bar', ax=ax)
                    plt.xticks(rotation=45)
                    plt.title("环境影响指标对比")
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                # 环境影响评估
                st.subheader("🌍 环境影响评估")
                if not lca_results.empty:
                    total_impact = lca_results.sum(axis=1)
                    avg_impact = total_impact.mean()
                    
                    if avg_impact < 10:
                        st.markdown("✅ 环境影响较小")
                    elif avg_impact < 20:
                        st.markdown("⚠️ 环境影响中等")
                    else:
                        st.markdown("❌ 环境影响较大")
    st.markdown('</div>', unsafe_allow_html=True)

# 完整分析页面
elif selected_page == "完整分析":
    st.header("完整分析")
    
    # 完整分析卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 完整分析流程")
    
    # 上传数据文件
    st.subheader("📁 数据上传")
    cement_file = st.file_uploader("上传水泥强度数据文件", type=["xlsx"], key="cement_uploader_1")
    lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"], key="lci_uploader_1")
    
    if cement_file and lci_file:
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.success("文件上传成功！")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 分析参数设置
        st.subheader("⚙️ 分析参数")
        col1, col2 = st.columns(2)
        with col1:
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, help="用于评估模型的测试数据比例")
        with col2:
            random_state = st.number_input("随机种子", 0, 1000, 42, help="控制数据分割的随机性")
        
        # 开始分析按钮
        if st.button("🚀 开始完整分析"):
            with st.spinner("正在进行完整分析..."):
                # 保存文件到临时位置
                import tempfile
                import os
                
                # 保存水泥强度数据
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    cement_path = tmp.name
                df_cement = pd.read_excel(cement_file)
                df_cement.to_excel(cement_path, index=False)
                
                # 保存 LCI 数据
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    lci_path = tmp.name
                df_lci = pd.read_excel(lci_file)
                df_lci.to_excel(lci_path, index=False)
                
                # 1. 训练模型
                optimizer = UCSOptimizer()
                model, metrics = optimizer.train(
                    data_path=cement_path,
                    test_size=test_size,
                    random_state=random_state
                )
                
                # 2. 预测强度
                predictions = optimizer.predict(input_data=cement_path)
                
                # 3. 计算 LCA
                lca_calculator = LCACalculator()
                lca_calculator.load_lci_data(lci_path)
                # 提取预测结果中的 UCS 值
                ucs_values = predictions['Predicted UCS'].values
                # 创建 LCA 计算所需的数据
                lca_input = pd.DataFrame({
                    "MC": df_cement['MC'] if 'MC' in df_cement.columns else [76.0] * len(ucs_values),
                    "CTR": df_cement['CTR'] if 'CTR' in df_cement.columns else [0.25] * len(ucs_values),
                    "UCS": ucs_values
                })
                lca_results = lca_calculator.calculate_lca(lca_input)
                
                # 清理临时文件
                os.unlink(cement_path)
                os.unlink(lci_path)
                
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("完整分析完成！")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 显示分析结果
            st.subheader("🏆 分析结果")
            
            # 1. 模型性能
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 模型性能")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("R² 评分", f"{metrics['r2']:.2f}")
            with col2:
                st.metric("均方误差", f"{metrics['mse']:.2f}")
            with col3:
                st.metric("训练样本", f"{int(len(df_cement) * (1 - test_size))}")
            with col4:
                st.metric("测试样本", f"{int(len(df_cement) * test_size)}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 2. 强度预测结果
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("💪 强度预测结果")
            st.dataframe(predictions)
            
            # 预测统计
            st.subheader("📈 预测统计")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("预测样本数", len(predictions))
            with col2:
                st.metric("平均UCS", f"{predictions['Predicted UCS'].mean():.2f} MPa")
            with col3:
                st.metric("最大UCS", f"{predictions['Predicted UCS'].max():.2f} MPa")
            with col4:
                st.metric("最小UCS", f"{predictions['Predicted UCS'].min():.2f} MPa")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 3. LCA 计算结果
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🌍 LCA 计算结果")
            st.dataframe(lca_results)
            
            # LCA 可视化
            st.subheader("📊 LCA 指标可视化")
            if not lca_results.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                lca_results.plot(kind='bar', ax=ax)
                plt.xticks(rotation=45)
                plt.title("环境影响指标对比")
                plt.tight_layout()
                st.pyplot(fig)
            
            # 环境影响评估
            st.subheader("🌱 环境影响评估")
            if not lca_results.empty:
                total_impact = lca_results.sum(axis=1)
                avg_impact = total_impact.mean()
                
                if avg_impact < 10:
                    st.markdown("✅ 环境影响较小")
                elif avg_impact < 20:
                    st.markdown("⚠️ 环境影响中等")
                else:
                    st.markdown("❌ 环境影响较大")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 4. 综合评估
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎯 综合评估")
            
            # 强度评估
            avg_ucs = predictions['Predicted UCS'].mean()
            if avg_ucs >= 25:
                strength_eval = "✅ 高强度"
            elif avg_ucs >= 15:
                strength_eval = "⚠️ 中等强度"
            else:
                strength_eval = "❌ 低强度"
            
            # 环境影响评估
            if not lca_results.empty:
                avg_impact = lca_results.sum(axis=1).mean()
                if avg_impact < 10:
                    env_eval = "✅ 环境友好"
                elif avg_impact < 20:
                    env_eval = "⚠️ 环境影响中等"
                else:
                    env_eval = "❌ 环境影响较大"
            else:
                env_eval = "⚠️ 环境评估数据不足"
            
            # 显示评估结果
            col1, col2 = st.columns(2)
            with col1:
                st.metric("强度评估", strength_eval)
            with col2:
                st.metric("环境评估", env_eval)
            
            # 综合建议
            st.subheader("💡 综合建议")
            if avg_ucs >= 25 and avg_impact < 10:
                st.markdown("✅ 该配方表现优秀，强度高且环境影响小")
            elif avg_ucs >= 15 and avg_impact < 20:
                st.markdown("⚠️ 该配方表现良好，可以考虑进一步优化")
            else:
                st.markdown("❌ 建议调整配方参数，提高强度或减少环境影响")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 分析方式选择
    analysis_method = st.radio(
        "分析方式",
        options=["文件上传", "手动输入"],
        key="analysis_method"
    )
    
    if analysis_method == "文件上传":
        # 上传数据文件
        cement_file = st.file_uploader("上传水泥数据文件", type=["xlsx"], key="cement_uploader_2")
        lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"], key="lci_uploader_2")
        
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
        lci_file = st.file_uploader("上传 LCI 数据文件", type=["xlsx"], key="lci_uploader_3")
        
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
