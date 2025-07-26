import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

def read_file(file: UploadedFile) -> pd.DataFrame:
    ext = file.name.split(".")[1]
    if ext == "csv":
        df = pd.read_csv(file)
    elif ext == "xlsx":
        df = pd.read_excel(file)
    return df