import streamlit as st
import pandera.pandas as pa
from backend import SCHEMAS, upload_file, read_file

st.set_page_config(page_title="File Upload", page_icon=":material/file_present:", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .empty-state {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 300px;
        font-size: 20px;
        color: #888;
        gap: 30px;
    }
    .arrow {
        font-size: 60px;
        color: #666;
        transform: rotate(-45deg);
    }
    </style>
""", unsafe_allow_html=True)

st.title("File Upload")

# Schema selection with better description
schema_options = {name: f"{config['display_name']} - {config['description']}" 
                  for name, config in SCHEMAS.items()}

selected_schema = st.selectbox(
    "Select the file type/schema you're uploading:",
    options=list(schema_options.keys()),
    format_func=lambda x: schema_options[x]
)

# File uploader
uploaded_file = st.file_uploader("Choose a file", label_visibility="collapsed")

if uploaded_file is None:
    # Empty state with arrow pointing to upload button
    st.markdown("""
        <div class="empty-state">
            <div>Upload a file to get started</div>
            <div class="arrow">↗</div>
        </div>
    """, unsafe_allow_html=True)
else:
    df = read_file(uploaded_file)
    schema: pa.DataFrameSchema = SCHEMAS[selected_schema]["schema"]
    required_cols = list(schema.columns.keys())
    extra_cols = [col for col in df.columns if col not in required_cols]
    
    if len(extra_cols) > 0:
        st.warning(f"⚠️ The following columns were ignored and removed: {', '.join(extra_cols)}")
    
    valid = False
    try:
        schema.validate(df, lazy=True)
        valid = True
    except pa.errors.SchemaErrors as e:
        failure_cases = e.failure_cases
        actions = []
        for _, row in failure_cases.iterrows():
            if row["check"] == "column_in_dataframe":
                actions.append(f"Add the column **'{row['failure_case']}'** to the Excel file.")
            elif row["check"].startswith("dtype"):
                actions.append(f"Change the data type of column **'{row['column']}'** to **{row['check'].split('(')[1].split(')')[0]}**.")
            elif "greater_than" in str(row["check"]):
                actions.append(f"Ensure all values in **'{row['column']}'** are greater than 0 (found {row['failure_case']}).")
            elif row["check"] == "not_nullable":
                actions.append(f"Fill in the empty values in column **'{row['column']}'**.")
            elif row["check"].startswith("isin"):
                actions.append(f"Column **'{row['column']}'** contains unexpected value **'{row['failure_case']}'**. Column **'{row['column']}'** must only include: {row['check'][5:-1]}")
        
        if actions:
            st.error("❌ The uploaded file does not match the required schema. Please fix the following issues and try again:")
            for action in set(actions):
                st.markdown(f"- {action}")
        else:
            st.error("❌ The file has schema errors. Please check your file.")
    except Exception as ex:
        st.error(f"❌ An unexpected error occurred: {ex}")
    
    if valid:
        st.success("✅ File validation successful!")
        
        # Show preview of first 5 rows
        st.subheader("Preview (first 5 rows)")
        st.dataframe(df[required_cols].head(5), use_container_width=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Submit to Databricks", use_container_width=True, type="primary"):
                with st.spinner("Uploading file..."):
                    upload_file(SCHEMAS[selected_schema]["file_name"], df[required_cols])
                    st.success("File uploaded successfully!")
                    st.balloons()
