from io import BytesIO
from databricks.sdk import WorkspaceClient
from datetime import datetime
import pandas as pd

def upload_file(file_name: str, file_data: pd.DataFrame):
    w = WorkspaceClient()

    catalog = ""
    schema = ""
    volume_name = ""

    file_name = file_name + "_" + datetime.now().strftime("%Y-%m-%d") + ".parquet"
    volume_file_path = f"/Volumes/{catalog}/{schema}/{volume_name}/{file_name}"
    w.files.upload(volume_file_path, BytesIO(file_data.to_parquet()), overwrite=True)
