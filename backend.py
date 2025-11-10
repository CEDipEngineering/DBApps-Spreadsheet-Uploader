from io import BytesIO
from datetime import datetime
import pandas as pd
import pandera.pandas as pa
from databricks.sdk import WorkspaceClient
from streamlit.runtime.uploaded_file_manager import UploadedFile


# File schema configurations
SCHEMAS = {
    "Sales Data": {
        "display_name": "Sales Data",
        "description": "Daily sales transactions with seller, product, and quantity information",
        "schema": pa.DataFrameSchema({
            "data": pa.Column(pa.DateTime, nullable=False),
            "vendedor": pa.Column(str, nullable=False),
            "produto": pa.Column(str, pa.Check.isin(["Paracetamol", "Ibuprofeno", "Tadalafila"]), nullable=False),
            "quantidade": pa.Column(pa.Int64, pa.Check.ge(0), nullable=False),
            "valor": pa.Column(pa.Float, pa.Check.ge(0), nullable=False),
        }),
        "file_name": "sales",
    }
}


def read_file(file: UploadedFile) -> pd.DataFrame:
    ext = file.name.split(".")[1]
    if ext == "csv":
        return pd.read_csv(file)
    elif ext == "xlsx":
        return pd.read_excel(file)


def upload_file(file_name: str, file_data: pd.DataFrame):
    w = WorkspaceClient()
    
    # Configure the target Databricks volume
    catalog = ""
    schema = ""
    volume_name = ""
    
    file_name = f"{file_name}_{datetime.now().strftime('%Y-%m-%d')}.parquet"
    volume_file_path = f"/Volumes/{catalog}/{schema}/{volume_name}/{file_name}"
    w.files.upload(volume_file_path, BytesIO(file_data.to_parquet()), overwrite=True)

