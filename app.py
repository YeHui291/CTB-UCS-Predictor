import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from ucs_optimizer.core.optimizer import UCSOptimizer
from ucs_optimizer.core.lca_calculator import LCACalculator

# Page Configuration
st.set_page_config(
    page_title="金属矿山充填体强度与碳排放智能预测系统 V1.0.0｜Sustainable CTB Mixture Designer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Academic Style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Roboto Slab', serif;
    }
    
    .main {
        background-color: #f5f5f5;
    }
    
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .stButton>button {
        background-color: #1e3a5f;
        color: white;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2c5282;
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(30, 58, 95, 0.3);
    }
    
    .stHeader {
        color: #1e3a5f;
        font-weight: 700;
        margin-bottom: 20px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }
    
    .stSubheader {
        color: #2d3748;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .stMetric {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #3182ce;
    }
    
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        overflow: hidden;
    }
    
    .stRadio > div {
        padding: 10px 15px;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #e2e8f0;
        padding: 8px;
        font-family: 'Roboto Slab', serif;
    }
    
    .stFileUploader > div > div > button {
        border-radius: 6px;
        background-color: #f7fafc;
        border: 2px dashed #cbd5e0;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > button:hover {
        background-color: #edf2f7;
        border-color: #3182ce;
    }
    
    .stSlider > div > div > div > div {
        background-color: #3182ce;
    }
    
    .sidebar {
        background-color: #1a202c;
        color: #e2e8f0;
    }
    
    .sidebar .stTitle {
        color: #fff;
        font-weight: 700;
    }
    
    .sidebar .stRadio > div {
        background-color: #2d3748;
        color: #e2e8f0;
        border-radius: 6px;
        border: none;
    }
    
    .sidebar .stRadio > div:hover {
        background-color: #4a5568;
    }
    
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    
    .highlight {
        background-color: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 15px 20px;
        border-radius: 0 6px 6px 0;
        margin: 15px 0;
    }
    
    .success-message {
        background-color: #f0fff4;
        color: #276749;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 12px 0;
        border: 1px solid #c6f6d5;
    }
    
    .warning-message {
        background-color: #fffaf0;
        color: #744210;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 12px 0;
        border: 1px solid #feebc8;
    }
    
    .info-box {
        background-color: #f7fafc;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Page Title
st.title("金属矿山充填体强度与碳排放智能预测系统 V1.0.0｜Sustainable CTB Mixture Designer")
st.markdown("**Machine Learning-based UCS Prediction and Environmental Impact Assessment**")

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    selected_page = st.radio(
        "Select Function",
        ["Home", "Model Training", "Strength Prediction", "LCA Calculation", "Comprehensive Analysis"]
    )
    
    # Version Information
    st.markdown("---")
    st.markdown("**Version**")
    st.markdown("v1.0.0")
    
    # Usage Tips
    st.markdown("---")
    st.markdown("**Usage Tips**")
    st.markdown("- Upload data files for analysis")
    st.markdown("- Supports Excel format")
    st.markdown("- Manual parameter input available")

# Home Page
if selected_page == "Home":
    st.header("About 金属矿山充填体强度与碳排放智能预测系统 V1.0.0｜Sustainable CTB Mixture Designer")
    
    # Card Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Core Features")
        st.write("• Machine learning-based UCS prediction")
        st.write("• Environmental Impact Assessment (LCA)")
        st.write("• Complete analysis workflow")
        st.write("• Data visualization")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 Sample Data")
        st.write("• `sample_cement_data.xlsx` - Training dataset")
        st.write("• `sample_lci_data.xlsx` - LCA inventory data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.subheader("🚀 Quick Start")
    st.write("1. Upload your cement data file")
    st.write("2. Select the UCS column and train the model")
    st.write("3. Use the trained model for prediction")
    st.write("4. Calculate environmental impact indicators")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical Features
    st.subheader("🔧 Technical Features")
    features = {
        "Machine Learning Models": "Advanced ML algorithms for cement strength prediction",
        "Multi-parameter Analysis": "Comprehensive analysis with multiple features",
        "Environmental Assessment": "Calculate environmental impact indicators",
        "User-Friendly Interface": "Intuitive Streamlit web interface",
        "Data Visualization": "Rich charts and data presentation",
        "Flexible Input": "Support for file upload and manual input"
    }
    
    for feature, description in features.items():
        st.markdown(f"**{feature}**: {description}")
    
    # Contact Information
    st.markdown("---")
    st.subheader("📞 Contact Us")
    st.write("For questions or suggestions, please contact us.")

# Model Training Page
elif selected_page == "Model Training":
    st.header("Model Training")
    
    # Data Input Method
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 Data Input Method")
    data_input_method = st.radio(
        "Select input method",
        ["File Upload", "Manual Input"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if data_input_method == "File Upload":
        # File Upload Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 Upload Training Data")
        uploaded_file = st.file_uploader("Upload training data file", type=["xlsx"], key="train_uploader")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("File uploaded successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Read Data
            df = pd.read_excel(uploaded_file)
            use_uploaded_data = True
            
            # Initialize session state for column adjustment
            if 'columns_adjusted' not in st.session_state:
                st.session_state.columns_adjusted = False
            if 'adjusted_df' not in st.session_state:
                st.session_state.adjusted_df = None
            
            # Column Name Adjustment Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔧 Column Name Adjustment")
            
            # Show current column names
            st.write("Original Columns:")
            st.code(', '.join([str(col) for col in df.columns]))
            
            # Column name modification
            st.write("Adjust Column Names:")
            adjusted_columns = []
            for i, col in enumerate(df.columns):
                new_col = st.text_input(f"Column {i+1}: {col}", value=str(col), key=f"col_{i}")
                adjusted_columns.append(new_col)
            
            # Apply column name adjustment
            if st.button("✅ Apply Column Adjustment"):
                df.columns = adjusted_columns
                st.session_state.adjusted_df = df.copy()
                st.session_state.columns_adjusted = True
                st.success("Column names adjusted successfully!")
                st.write("New Columns:", df.columns.tolist())
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Use adjusted dataframe if available
            working_df = st.session_state.adjusted_df if st.session_state.columns_adjusted else df
            
            # UCS Column Selection Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎯 UCS Column Selection")
            
            # Auto-detect possible UCS columns
            possible_ucs_columns = []
            for col in working_df.columns:
                col_str = str(col).lower()
                if 'ucs' in col_str or 'strength' in col_str:
                    possible_ucs_columns.append(col)
            
            # Select UCS column
            if possible_ucs_columns:
                selected_ucs = st.selectbox(
                    "Select UCS column",
                    options=working_df.columns.tolist(),
                    index=working_df.columns.tolist().index(possible_ucs_columns[0]) if possible_ucs_columns[0] in working_df.columns else 0,
                    help="Select the column containing UCS values"
                )
            else:
                # If not detected, let user select from all columns
                selected_ucs = st.selectbox(
                    "Select UCS column",
                    options=working_df.columns.tolist(),
                    help="Select the column containing UCS values"
                )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Manual Input
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Manual Input for New Training Data")
        st.write("Enter new training data below:")
        
        # Load default dataset (in background, hidden from user)
        try:
            default_data_path = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_cement_data.xlsx")
            default_df = pd.read_excel(default_data_path)
        except Exception as e:
            default_df = pd.DataFrame()
        
        # Create empty input table
        user_input_df = pd.DataFrame({
            "Cu": [None],
            "Cc": [None],
            "TEMP": [None],
            "D10": [None],
            "SiO2": [None],
            "CaO": [None],
            "Al2O3": [None],
            "CT": [None],
            "CTR": [None],
            "MC": [None],
            "T": [None],
            "UCS": [None]
        })
        
        # Editable table for new data input
        st.write("**Enter New Data:**")
        user_df = st.data_editor(
            user_input_df,
            width='stretch',
            num_rows="dynamic",
            column_config={
                "Cu": st.column_config.NumberColumn("Cu (Curvature Coefficient)", min_value=0.0),
                "Cc": st.column_config.NumberColumn("Cc (Uniformity Coefficient)", min_value=0.0),
                "TEMP": st.column_config.NumberColumn("TEMP (Temperature °C)", min_value=0.0),
                "D10": st.column_config.NumberColumn("D10 (Effective Particle Size mm)", min_value=0.0),
                "SiO2": st.column_config.NumberColumn("SiO2 (%)", min_value=0.0),
                "CaO": st.column_config.NumberColumn("CaO (%)", min_value=0.0),
                "Al2O3": st.column_config.NumberColumn("Al2O3 (%)", min_value=0.0),
                "CT": st.column_config.NumberColumn("CT (Cement Type)", min_value=0.0),
                "CTR": st.column_config.NumberColumn("CTR (Cement-Tailings Ratio)", min_value=0.0, max_value=1.0),
                "MC": st.column_config.NumberColumn("MC (Mass Concentration %)", min_value=0.0, max_value=100.0),
                "T": st.column_config.NumberColumn("T (Curing Time days)", min_value=0.0),
                "UCS": st.column_config.NumberColumn("UCS (Unconfined Compressive Strength MPa)", min_value=0.0),
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
        use_uploaded_data = False
        
        # Merge default data with user input (hidden from user)
        user_df_clean = user_df.dropna(how='all')
        
        if len(user_df_clean) > 0:
            working_df = pd.concat([default_df, user_df_clean], ignore_index=True)
        else:
            working_df = default_df
        
        selected_ucs = "UCS"

        # Data Preview Card - only show user input data, not the merged data
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Your Input Data")
        edited_user_df = st.data_editor(user_df.dropna(how='all'), width='stretch')
        
        # Update working_df with edited user data
        if len(edited_user_df) > 0:
            working_df = pd.concat([default_df, edited_user_df], ignore_index=True)
        else:
            working_df = default_df
        
        # Data Statistics
        st.subheader("📈 Data Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Number of Samples", len(working_df))
        with col2:
            st.metric("Number of Features", len(working_df.columns) - 1)
        with col3:
            st.metric("UCS Column", selected_ucs)
        st.markdown('</div>', unsafe_allow_html=True)

        # Training Parameters Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚙️ Training Parameters")
        col1, col2 = st.columns(2)
        with col1:
            test_size = st.slider("Test Set Ratio", 0.1, 0.5, 0.2, help="Proportion of data used for model evaluation")
        with col2:
            random_state = st.number_input("Random Seed", 0, 1000, 42, help="Controls randomness of data splitting")
        st.markdown('</div>', unsafe_allow_html=True)

        # Train Button
        if st.button("🚀 Start Training"):
            with st.spinner("Training model..."):
                # Save working data (including hidden default data) to temporary file
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    tmp_path = tmp.name
                
                working_df.to_excel(tmp_path, index=False)
                
                optimizer = UCSOptimizer()
                # Train model
                model, metrics = optimizer.train(
                    data_path=tmp_path,
                    test_size=test_size,
                    random_state=random_state,
                    target_column=selected_ucs
                )
                
                # Clean up temporary file
                os.unlink(tmp_path)

            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("Model training completed!")
            st.markdown('</div>', unsafe_allow_html=True)

            # Training Results Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🏆 Training Results")
            
            # Display metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("R² Score", f"{metrics['r2']:.2f}")
            with col2:
                st.metric("MSE", f"{metrics['mse']:.2f}")
            with col3:
                st.metric("Training Samples", f"{int(len(edited_df) * (1 - test_size))}")
            with col4:
                st.metric("Test Samples", f"{int(len(edited_df) * test_size)}")
            
            # Model performance assessment
            if metrics['r2'] > 0.8:
                st.markdown("✅ Excellent model performance with high prediction accuracy")
            elif metrics['r2'] > 0.6:
                st.markdown("⚠️ Good model performance, ready for use")
            else:
                st.markdown("❌ Poor model performance, consider adding more data or adjusting parameters")
            st.markdown('</div>', unsafe_allow_html=True)

# Strength Prediction Page
elif selected_page == "Strength Prediction":
    st.header("Strength Prediction")
    
    # Prediction Method Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 Prediction Method")
    prediction_method = st.radio(
        "Select prediction method",
        ["File Upload", "Manual Input"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prediction_method == "File Upload":
        # File Upload Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 Upload Data")
        data_file = st.file_uploader("Upload prediction data file", type=["xlsx"], key="predict_uploader")
        
        if data_file:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("File uploaded successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Read Data
            df = pd.read_excel(data_file)
            
            # Display editable data table
            st.subheader("📊 Prediction Data (Editable)")
            edited_df = st.data_editor(df, width='stretch')
            
            # Predict Button
            if st.button("🚀 Start Prediction"):
                with st.spinner("Predicting..."):
                    # Save edited data to temporary file
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                        tmp_path = tmp.name
                    
                    edited_df.to_excel(tmp_path, index=False)
                    
                    optimizer = UCSOptimizer()
                    # Train model with sample data
                    sample_data = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_cement_data.xlsx")
                    model, metrics = optimizer.train(data_path=sample_data)
                    # Then predict
                    predictions = optimizer.predict(input_data=tmp_path)
                    
                    # Clean up temporary file
                    os.unlink(tmp_path)
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("Prediction completed!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display prediction results
                st.subheader("🏆 Prediction Results")
                st.dataframe(predictions)
                
                # Display prediction statistics
                st.subheader("📈 Prediction Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Number of Predictions", len(predictions))
                with col2:
                    st.metric("Average UCS", f"{predictions['Predicted UCS'].mean():.2f} MPa")
                with col3:
                    st.metric("Maximum UCS", f"{predictions['Predicted UCS'].max():.2f} MPa")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # Manual Input
        # Manual Input Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Manual Input of Features")
        
        # Feature inputs (11 features)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cu = st.number_input("Cu", min_value=0.0, value=12.7, help="Curvature Coefficient")
            cc = st.number_input("Cc", min_value=0.0, value=1.3, help="Uniformity Coefficient")
            tem = st.number_input("TEM", min_value=0.0, value=25.0, help="Temperature (°C)")
            d10 = st.number_input("D10", min_value=0.0, value=0.005, help="Effective Particle Size (mm)")
        
        with col2:
            sio2 = st.number_input("SiO2", min_value=0.0, value=29.11, help="Silicon Dioxide (%)")
            cao = st.number_input("CaO", min_value=0.0, value=32.65, help="Calcium Oxide (%)")
            al2o3 = st.number_input("Al2O3", min_value=0.0, value=0.37, help="Aluminum Oxide (%)")
            ct = st.number_input("CT", min_value=0.0, value=32.5, help="Cement Type")
        
        with col3:
            ctr = st.number_input("CTR", min_value=0.0, max_value=1.0, value=0.25, help="Cement-Tailings Ratio")
            mc = st.number_input("MC", min_value=0.0, max_value=100.0, value=76.0, help="Mass Concentration (%)")
            t = st.number_input("T", min_value=0.0, value=7.0, help="Curing Time (days)")
        
        # Predict Button
        if st.button("🚀 Start Prediction"):
            with st.spinner("Predicting..."):
                # Create input data
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
                
                # Save to temporary file
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    tmp_path = tmp.name
                
                input_data.to_excel(tmp_path, index=False)
                
                # Train model (using sample data)
                optimizer = UCSOptimizer()
                sample_data = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_cement_data.xlsx")
                model, metrics = optimizer.train(data_path=sample_data)
                
                # Perform prediction
                predictions = optimizer.predict(input_data=tmp_path)
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("Prediction completed!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display prediction results
            st.subheader("🏆 Prediction Results")
            st.dataframe(predictions)
            
            # Display predicted value
            predicted_ucs = predictions['Predicted UCS'].values[0]
            
            # Create prediction result card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Prediction Details")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Predicted UCS", f"{predicted_ucs:.2f} MPa")
            with col2:
                # Strength grade assessment
                if predicted_ucs > 5:
                    st.metric("Strength Grade", "High Strength")
                elif predicted_ucs >= 1:
                    st.metric("Strength Grade", "Medium Strength")
                else:
                    st.metric("Strength Grade", "Low Strength")
            
            # Display input parameters
            st.subheader("🔧 Input Parameters")
            st.dataframe(input_data)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# LCA Calculation Page
elif selected_page == "LCA Calculation":
    st.header("LCA Calculation")
    
    # Calculation Method - Move to top so users can select first
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 Calculation Method")
    calc_method = st.radio(
        "Select calculation method",
        options=["File Data", "Manual Input"],
        key="lca_calc_method"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if calc_method == "File Data":
        # File Upload Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 LCI Data Upload")
        lci_file = st.file_uploader("Upload LCI data file", type=["xlsx"], key="lci_uploader_1")
        
        if lci_file:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("File uploaded successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display data preview
            df = pd.read_excel(lci_file)
            st.subheader("📊 LCI Data Preview")
            st.dataframe(df.head())
            
            # Calculate Button
            if st.button("🚀 Start Calculation"):
                with st.spinner("Calculating LCA indicators..."):
                    lca_calculator = LCACalculator()
                    lca_calculator.load_lci_data(lci_file)
                    # Calculate with sample data
                    sample_df = pd.DataFrame({
                        "MC": [20, 25, 30],
                        "CTR": [0.1, 0.2, 0.3],
                        "UCS": [10, 15, 20]
                    })
                    lca_results = lca_calculator.calculate_lca(sample_df)
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("Calculation completed!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display results
                st.subheader("🏆 LCA Results")
                st.dataframe(lca_results)
                
                # Visualization
                st.subheader("📈 LCA Indicator Visualization")
                if not lca_results.empty:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lca_results.plot(kind='bar', ax=ax)
                    plt.xticks(rotation=45)
                    plt.title("Environmental Impact Comparison")
                    plt.tight_layout()
                    st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:  # Manual Input
        # Manual Input Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Manual Input of Parameters")
        
        # LCI Data Upload (optional, use default if not provided)
        st.subheader("📁 LCI Data (Optional)")
        lci_file = st.file_uploader("Upload LCI data file (optional, uses default if not provided)", 
                                   type=["xlsx"], key="lci_uploader_2")
        
        # Create empty input table
        input_df = pd.DataFrame({
            "MC": [20.0],
            "CTR": [0.1],
            "UCS": [10.0]
        })
        
        # Editable table for data input
        st.write("**Enter LCA Calculation Data:**")
        edited_df = st.data_editor(
            input_df,
            width='stretch',
            num_rows="dynamic",
            column_config={
                "MC": st.column_config.NumberColumn("MC (Mass Concentration %)", min_value=0.0, max_value=100.0),
                "CTR": st.column_config.NumberColumn("CTR (Cement-Tailings Ratio)", min_value=0.0, max_value=1.0),
                "UCS": st.column_config.NumberColumn("UCS (Unconfined Compressive Strength MPa)", min_value=0.0),
            }
        )
        
        # Calculate Button
        if st.button("🚀 Start Calculation"):
            # Filter out empty rows
            input_data = edited_df.dropna(how='all')
            
            if len(input_data) == 0:
                st.warning("Please enter at least one row of data!")
            else:
                with st.spinner("Calculating LCA indicators..."):
                    lca_calculator = LCACalculator()
                    
                    # Load LCI data - use uploaded file or default
                    if lci_file:
                        lca_calculator.load_lci_data(lci_file)
                    else:
                        # Load default LCI data
                        default_lci_path = os.path.join(os.path.dirname(__file__), "ucs_optimizer", "data", "sample_lci_data.xlsx")
                        if os.path.exists(default_lci_path):
                            lca_calculator.load_lci_data(default_lci_path)
                            st.info("Using default LCI data")
                        else:
                            st.error("Please upload an LCI data file or place sample_lci_data.xlsx in the data folder")
                            st.stop()
                    
                    # Calculate with manual input data
                    lca_results = lca_calculator.calculate_lca(input_data)
                    
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("Calculation completed!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display results
                st.subheader("🏆 LCA Results")
                st.dataframe(lca_results)
                
                # Display calculation statistics
                st.subheader("📊 Calculation Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Number of Calculations", len(lca_results))
                with col2:
                    if not lca_results.empty:
                        env_cols = ['carbon_per_MPa', 'energy_per_MPa']
                        avg_impact = lca_results[env_cols].sum(axis=1).mean()
                        st.metric("Average Environmental Impact", f"{avg_impact:.2f}")
                
                # Visualization
                st.subheader("📈 LCA Indicator Visualization")
                if not lca_results.empty:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lca_results.plot(kind='bar', ax=ax)
                    plt.xticks(rotation=45)
                    plt.title("Environmental Impact Comparison")
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                # Environmental Impact Assessment
                st.subheader("🌍 Environmental Impact Assessment")
                if not lca_results.empty:
                    env_cols = ['carbon_per_MPa', 'energy_per_MPa']
                    total_impact = lca_results[env_cols].sum(axis=1)
                    avg_impact = total_impact.mean()
                    
                    if avg_impact < 60:
                        st.markdown("✅ Low environmental impact")
                    elif avg_impact < 200:
                        st.markdown("⚠️ Medium environmental impact")
                    else:
                        st.markdown("❌ High environmental impact")
                        
                # Display input parameters
                st.subheader("🔧 Input Parameters")
                st.dataframe(input_data)
        st.markdown('</div>', unsafe_allow_html=True)

# Comprehensive Analysis Page
elif selected_page == "Comprehensive Analysis":
    st.header("Comprehensive Analysis")

    # ---------------- session_state 初始化：保存分析结果 ----------------
    for _key in (
        "comp_train_samples", "comp_test_samples", "comp_metrics",
        "comp_predictions", "comp_lca_results", "comp_strength_eval",
        "comp_env_eval", "comp_avg_ucs", "comp_avg_impact",
        "comp_is_manual",
    ):
        if _key not in st.session_state:
            st.session_state[_key] = None

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 Complete Analysis Workflow")

    # ---------------- 分析方式选择（radio 全局唯一 key） ----------------
    analysis_method = st.radio(
        "Analysis Method",
        options=["File Upload", "Manual Input"],
        key="comp_analysis_method",
    )

    # ---------------- 分析参数（slider / number_input 全局唯一 key） ----------------
    st.subheader("⚙️ Analysis Parameters")
    col_cp1, col_cp2 = st.columns(2)
    with col_cp1:
        test_size = st.slider(
            "Test Set Ratio", 0.1, 0.5, 0.2,
            key="comp_test_size",
            help="Proportion of data used for model evaluation",
        )
    with col_cp2:
        random_state = st.number_input(
            "Random Seed", 0, 1000, 42,
            key="comp_random_state",
            help="Controls randomness of data splitting",
        )

    cement_df_for_lca: pd.DataFrame | None = None
    lci_file = None

    # ==================== 方式一：文件上传 ====================
    if analysis_method == "File Upload":
        st.subheader("📁 Upload Data")
        cement_file = st.file_uploader(
            "Upload cement strength data file",
            type=["xlsx"],
            key="comp_cement_uploader",
        )
        lci_file = st.file_uploader(
            "Upload LCI data file",
            type=["xlsx"],
            key="comp_lci_uploader",
        )

        if cement_file is not None:
            st.subheader("Cement Data (Editable)")
            cement_raw = pd.read_excel(cement_file)
            edited_df = st.data_editor(cement_raw, use_container_width=True,
                                       key="comp_cement_data_editor")
            cement_df_for_lca = edited_df.copy()
            if lci_file is not None:
                st.success("Files uploaded successfully!")

    # ==================== 方式二：手动输入 ====================
    else:  # Manual Input
        st.subheader("📝 Manual Input of Cement Parameters")

        lci_file = st.file_uploader(
            "Upload LCI data file",
            type=["xlsx"],
            key="comp_lci_uploader_manual",
        )

        col_ca, col_cb, col_cc = st.columns(3)
        with col_ca:
            Cu  = st.number_input("Cu",  min_value=0.0, value=12.7,  key="comp_manual_Cu")
            Cc  = st.number_input("Cc",  min_value=0.0, value=1.3,   key="comp_manual_Cc")
            TEM = st.number_input("TEM", min_value=0.0, value=25.0,  key="comp_manual_TEM")
            D10 = st.number_input("D10", min_value=0.0, value=0.005, key="comp_manual_D10")
        with col_cb:
            SiO2  = st.number_input("SiO2",  min_value=0.0, value=29.11, key="comp_manual_SiO2")
            CaO   = st.number_input("CaO",   min_value=0.0, value=32.65, key="comp_manual_CaO")
            Al2O3 = st.number_input("Al2O3", min_value=0.0, value=0.37,  key="comp_manual_Al2O3")
            CT    = st.number_input("CT",    min_value=0.0, value=32.5,  key="comp_manual_CT")
        with col_cc:
            CTR = st.number_input("CTR", min_value=0.0, max_value=1.0, value=0.25, key="comp_manual_CTR")
            MC  = st.number_input("MC",  min_value=0.0, max_value=100.0, value=76.0, key="comp_manual_MC")
            T   = st.number_input("T",   min_value=0.0, value=7.0,  key="comp_manual_T")
            UCS = st.number_input("UCS", min_value=0.0, value=2.41, key="comp_manual_UCS")

        cement_df_for_lca = pd.DataFrame({
            "Cu": [Cu], "Cc": [Cc], "TEM": [TEM], "D10": [D10],
            "SiO2": [SiO2], "CaO": [CaO], "Al2O3": [Al2O3], "CT": [CT],
            "CTR": [CTR], "MC": [MC], "T": [T], "UCS": [UCS],
        })
        st.dataframe(cement_df_for_lca, use_container_width=True)
        if lci_file is not None:
            st.success("LCI data file uploaded successfully!")

    # ---------------- 执行分析按钮 ----------------
    ready_to_run = (
        cement_df_for_lca is not None and not cement_df_for_lca.empty
        and lci_file is not None
    )
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        run_clicked = st.button(
            "🚀 Start Comprehensive Analysis",
            key="comp_run_btn",
            disabled=not ready_to_run,
        )
    with col_btn2:
        if not ready_to_run:
            st.caption("请先上传水泥数据并上传 LCI 文件。")

    if run_clicked:
        import tempfile

        # 写入临时文件
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            cement_path = tmp.name
        cement_df_for_lca.to_excel(cement_path, index=False)

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            lci_path = tmp.name
        pd.read_excel(lci_file).to_excel(lci_path, index=False)

        try:
            is_manual = (analysis_method == "Manual Input")

            # ---- 执行分析：手动输入跳过训练，文件上传走全流程 ----
            if is_manual:
                with st.spinner("Running LCA assessment for manual input..."):
                    ucs_val = float(cement_df_for_lca["UCS"].values[0])
                    predictions = pd.DataFrame({"Predicted UCS": [ucs_val]})
                    metrics = {"r2": "N/A", "mse": "N/A"}
                    n_total = 1
            else:
                n_total = len(cement_df_for_lca)
                with st.spinner("Training model and running comprehensive analysis..."):
                    optimizer = UCSOptimizer()
                    model, metrics = optimizer.train(
                        data_path=cement_path,
                        test_size=test_size,
                        random_state=random_state,
                    )
                    predictions = optimizer.predict(input_data=cement_path)

            # ---- LCA 计算 ----
            lca_calc = LCACalculator()
            lca_calc.load_lci_data(lci_path)
            ucs_vals = predictions["Predicted UCS"].values
            _mc  = (cement_df_for_lca["MC"].values
                    if "MC" in cement_df_for_lca.columns
                    else [76.0] * len(ucs_vals))
            _ctr = (cement_df_for_lca["CTR"].values
                    if "CTR" in cement_df_for_lca.columns
                    else [0.25] * len(ucs_vals))
            lca_input = pd.DataFrame({"MC": _mc, "CTR": _ctr, "UCS": ucs_vals})
            lca_results = lca_calc.calculate_lca(lca_input)

            # ---- 强度评价（充填体阈值：<1低 / 1-5中 / >5高） ----
            avg_ucs = float(predictions["Predicted UCS"].mean())
            if avg_ucs > 5:
                strength_eval = "✅ High Strength"
            elif avg_ucs >= 1:
                strength_eval = "⚠️ Medium Strength"
            else:
                strength_eval = "❌ Low Strength"

            # ---- 环境评价（仅环境类指标 per MPa：<60低 / 60-200中 / >200高） ----
            if not lca_results.empty:
                env_cols = [c for c in ("carbon_per_MPa", "energy_per_MPa")
                            if c in lca_results.columns]
                avg_impact = (float(lca_results[env_cols].sum(axis=1).mean())
                              if env_cols else 0.0)
                if avg_impact < 60:
                    env_eval = "✅ Environmentally Friendly"
                elif avg_impact < 200:
                    env_eval = "⚠️ Medium Environmental Impact"
                else:
                    env_eval = "❌ High Environmental Impact"
            else:
                avg_impact = 0.0
                env_eval = "⚠️ Insufficient Data"

            # ---- 保存 session_state ----
            if is_manual:
                st.session_state.comp_train_samples = 0
                st.session_state.comp_test_samples = 0
            else:
                st.session_state.comp_train_samples = int(n_total * (1 - test_size))
                st.session_state.comp_test_samples  = int(n_total * test_size)
            st.session_state.comp_metrics = metrics
            st.session_state.comp_predictions = predictions
            st.session_state.comp_lca_results = lca_results
            st.session_state.comp_avg_ucs = avg_ucs
            st.session_state.comp_avg_impact = avg_impact
            st.session_state.comp_strength_eval = strength_eval
            st.session_state.comp_env_eval = env_eval
            st.session_state.comp_is_manual = is_manual

            if is_manual:
                st.info("Manual Input mode: model training skipped, UCS value used directly for LCA.")
            st.success("Comprehensive analysis completed!")

        except Exception as e:
            st.error(f"Analysis failed: {e}")
        finally:
            for p in (cement_path, lci_path):
                try:
                    if os.path.exists(p):
                        os.unlink(p)
                except Exception:
                    pass

    # ---------------- 结果展示（每次重渲染都从 session_state 读，不丢失） ----------------
    if st.session_state.comp_metrics is not None:
        metrics     = st.session_state.comp_metrics
        predictions = st.session_state.comp_predictions
        lca_results = st.session_state.comp_lca_results
        avg_ucs     = st.session_state.comp_avg_ucs
        avg_impact  = st.session_state.comp_avg_impact
        strength_eval = st.session_state.comp_strength_eval
        env_eval      = st.session_state.comp_env_eval
        is_manual     = st.session_state.comp_is_manual

        st.subheader("🏆 Analysis Results")

        # 1) 模型性能
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Model Performance")
        if is_manual:
            st.info("Model training skipped in Manual Input mode — R²/MSE not applicable.")
            c1, c2 = st.columns(2)
            c1.metric("R² Score", "N/A")
            c2.metric("MSE", "N/A")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("R² Score", f"{metrics['r2']:.2f}")
            c2.metric("MSE",      f"{metrics['mse']:.2f}")
            c3.metric("Training Samples", st.session_state.comp_train_samples)
            c4.metric("Test Samples",     st.session_state.comp_test_samples)
        st.markdown('</div>')

        # 2) 强度预测
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💪 Strength Prediction Results")
        st.dataframe(predictions, use_container_width=True)
        st.subheader("📈 Prediction Statistics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Number of Predictions", len(predictions))
        c2.metric("Average UCS", f"{predictions['Predicted UCS'].mean():.2f} MPa")
        c3.metric("Maximum UCS", f"{predictions['Predicted UCS'].max():.2f} MPa")
        c4.metric("Minimum UCS", f"{predictions['Predicted UCS'].min():.2f} MPa")
        st.markdown('</div>')

        # 3) LCA 结果
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌍 LCA Results")
        st.dataframe(lca_results, use_container_width=True)

        st.subheader("📊 LCA Indicator Visualization")
        if not lca_results.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            lca_results.plot(kind="bar", ax=ax)
            plt.xticks(rotation=45)
            plt.title("Environmental Impact Comparison")
            plt.tight_layout()
            st.pyplot(fig)

        st.subheader("🌱 Environmental Impact Assessment")
        if not lca_results.empty:
            if avg_impact < 60:
                st.markdown("✅ Low environmental impact")
            elif avg_impact < 200:
                st.markdown("⚠️ Medium environmental impact")
            else:
                st.markdown("❌ High environmental impact")
        st.markdown('</div>')

        # 4) 综合评价
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Comprehensive Assessment")
        c1, c2 = st.columns(2)
        c1.metric("Strength Assessment",      strength_eval)
        c2.metric("Environmental Assessment", env_eval)

        st.subheader("💡 Comprehensive Recommendations")
        if avg_ucs > 5 and avg_impact < 60:
            st.markdown("✅ Excellent performance: high strength with low environmental impact")
        elif avg_ucs >= 1 and avg_impact < 200:
            st.markdown("⚠️ Good performance: consider further optimization")
        else:
            st.markdown("❌ Recommend adjusting formulation parameters to improve strength or reduce environmental impact")
        st.markdown('</div>')

    st.markdown('</div>')

# Footer
st.markdown("""
---
**金属矿山充填体强度与碳排放智能预测系统 V1.0.0｜Sustainable CTB Mixture Designer** - Machine Learning-based UCS Prediction and Environmental Impact Assessment Tool
""")
