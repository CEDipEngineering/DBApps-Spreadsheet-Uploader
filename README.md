# Spreadsheet File Uploader

This project was developed to prevent data quality issues in dashboards and pipelines that depend on files uploaded by business analysts. It uses Streamlit to provide an intuitive user interface for file uploads and automatically validates whether uploaded files comply with the formats expected by downstream systems. It also uses Databricks to store the files in a volume.

## About This Project

This is an English translation and enhanced version of Pedro Ramos's excellent [uploader_carga_fria](https://github.com/Databricks-BR/uploader_carga_fria) repository. The original project provided a solid foundation for validating and uploading cold load files to Databricks Unity Catalog volumes.

**Enhancements in this version:**
- Complete English translation (code, comments, documentation, and example files)
- Refactored backend with improved schema configuration structure
- Enhanced UI with better user guidance and data preview
- Simplified codebase with consolidated backend logic
- Improved documentation and extensibility

This project follows patterns from the [Databricks Apps Cookbook](https://apps-cookbook.dev/docs/streamlit/volumes/volumes_upload) for working with Unity Catalog volumes in Streamlit applications.

## Environment Setup

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate the virtual environment: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Project Structure and Variables / Parameters to Edit

### app.py

Streamlit application that builds the user interface for file uploads and validation.

### backend.py

Contains all backend logic including:
- **SCHEMAS dictionary**: Configure file schemas with display names, descriptions, and validation rules
- **read_file()**: Reads uploaded CSV or Excel files into DataFrames
- **upload_file()**: Uploads validated files to Databricks volumes

To add a new file schema, add an entry to the `SCHEMAS` dictionary with:
- `display_name`: User-friendly name shown in the UI
- `description`: Brief description of what the file contains
- `schema`: Pandera schema defining the expected columns and validation rules
- `file_name`: Base name for the saved file

**Configuration needed:**
1. **WorkspaceClient()**: For local testing, configure the workspace profile:
   - `databricks auth login` => Registers the profile on your machine
   - `WorkspaceClient(profile="<profile name>")` => Connects using your credentials
   - When deployed on Databricks, no configuration needed (inherits user permissions)

2. **catalog, schema, and volume_name**: Must point to your Databricks volume

## Running the Application

To run the application locally:

```bash
streamlit run app.py
```

## Features

- **File Upload Interface**: Simple and intuitive file upload interface built with Streamlit
- **Schema Validation**: Automatically validates uploaded files against predefined schemas
- **Error Reporting**: Provides clear, actionable error messages when validation fails
- **Databricks Integration**: Seamlessly uploads validated files to Databricks volumes
- **Multiple File Formats**: Supports CSV and Excel (.xlsx) files

## How It Works

1. User selects a file type/schema from the dropdown menu
2. User uploads a file (CSV or Excel)
3. The application validates the file structure against the expected schema
4. If validation passes, a preview of the first 5 rows is displayed
5. User can submit the validated file to be uploaded to Databricks
6. If validation fails, user receives detailed feedback about what needs to be corrected

## Deploying to Databricks

This application can be deployed as a Databricks App. The `app.yaml` configuration file is provided for deployment.

### Required Permissions

Your app service principal needs the following permissions:
- `USE CATALOG` on the catalog of the volume
- `USE SCHEMA` on the schema of the volume
- `READ VOLUME` and `WRITE VOLUME` on the volume

See the [Databricks documentation on privileges for volume operations](https://apps-cookbook.dev/docs/streamlit/volumes/volumes_upload#permissions) for more information.

## References

- [Databricks Apps Cookbook - Upload a file](https://apps-cookbook.dev/docs/streamlit/volumes/volumes_upload)
- [Original project by Pedro Ramos](https://github.com/Databricks-BR/uploader_carga_fria)
- [Pandera - Data Validation Library](https://pandera.readthedocs.io/)
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html)

## Contributing

Feel free to open issues or submit pull requests with improvements!

## Credits

Original concept and implementation by [Pedro Ramos](https://github.com/Databricks-BR/uploader_carga_fria). This version includes translations, refactoring, and UI enhancements.
