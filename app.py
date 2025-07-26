import streamlit as st
import pandera.pandas as pa
from io import BytesIO
from files import files
from uploader import upload_file
from utils import read_file

st.set_page_config(page_title="Upload de Arquivos", page_icon=":material/file_present:")

st.title("Upload de Arquivos")

file_type = st.selectbox("Selecione um arquivo", files.keys())

uploaded_file = st.file_uploader("Escolha um arquivo")

if uploaded_file is not None:
    df = read_file(uploaded_file)
    schema: pa.DataFrameSchema = files[file_type]["schema"]
    required_cols = list(schema.columns.keys())
    extra_cols = [col for col in df.columns if col not in required_cols]
    if len(extra_cols) > 0:
        st.warning(f"⚠️ As seguintes colunas foram ignoradas e removidas: {', '.join(extra_cols)}")
    valid = False
    try:
        schema.validate(df, lazy=True)
        valid = True
    except pa.errors.SchemaErrors as e:
        failure_cases = e.failure_cases
        actions = []
        for _, row in failure_cases.iterrows():
            if row["check"] == "column_in_dataframe":
                actions.append(f"Adicione a coluna **'{row['failure_case']}'** ao arquivo Excel.")
            elif row["check"].startswith("dtype"):
                actions.append(f"Mude o tipo da coluna **'{row['column']}'** para **{row['check'].split('(')[1].split(')')[0]}**.")
            elif "greater_than" in str(row["check"]):
                actions.append(f"Certifique-se que todos os valores em **'{row['column']}'** são maiores que 0 (encontrado {row['failure_case']}).")
            elif row["check"] == "not_nullable":
                actions.append(f"Preencha os valores vazios na coluna **'{row['column']}'**.")
            elif row["check"].startswith("isin"):
                actions.append(f"A coluna **'{row['column']}'** contém o valor inesperado **'{row['failure_case']}'**. A coluna **'{row['column']}'** deve incluir apenas: {row['check'][5:-1]}")
        if actions:
            st.error("❌ O arquivo enviado não corresponde ao esquema necessário. Por favor, corrija os seguintes problemas e tente novamente:")
            for action in set(actions):
                st.markdown(f"- {action}")
        else:
            st.error("❌ O arquivo tem erros de esquema. Por favor, verifique seu arquivo.")
    except Exception as ex:
        st.error(f"❌ Ocorreu um erro inesperado: {ex}")
    if valid:
        if st.button("Enviar"):
            with st.spinner("Enviando arquivo..."):
                upload_file(files[file_type]["file_name"], BytesIO(df[required_cols].to_parquet()), uploaded_file.name)
                st.success("Arquivo enviado com sucesso")



