# Instructions for DBApps Spreadsheet Uploader

## Project Overview

This is a Streamlit-based file validation and upload application that:
- Validates CSV and Excel files against predefined schemas using Pandera
- Uploads validated files to Databricks Unity Catalog volumes
- Provides an intuitive UI for business analysts to ensure data quality

## Tech Stack

- **Frontend**: Streamlit for the web UI
- **Backend**: Python with Databricks SDK
- **Validation**: Pandera for schema validation
- **Storage**: Databricks Unity Catalog volumes
- **File Formats**: CSV and Excel (.xlsx)

## Code Architecture

### app.py
- Contains the Streamlit UI logic
- Handles user interactions for file selection and upload
- Displays validation results and data previews
- Keep UI code separate from business logic

### backend.py
- Contains all business logic and configuration
- **SCHEMAS dictionary**: Central configuration for all file schemas
- **read_file()**: Handles file reading (CSV/Excel)
- **upload_file()**: Manages Databricks volume uploads
- Always add new file schemas to the SCHEMAS dictionary

## Coding Guidelines

1. **Schema Configuration**: When adding new file types, always define them in the `SCHEMAS` dictionary in backend.py with:
   - `display_name`: User-friendly name for the UI
   - `description`: Clear explanation of the file's purpose
   - `schema`: Pandera schema with column definitions and validation rules
   - `file_name`: Base name for storing the file

2. **Error Handling**: Provide clear, actionable error messages that help users understand what went wrong and how to fix it

3. **Databricks Integration**:
   - Use `WorkspaceClient()` for Databricks SDK connections
   - For local testing, use `WorkspaceClient(profile="profile_name")`
   - When deployed, rely on inherited permissions
   - Always specify catalog, schema, and volume_name

4. **Validation**: Use Pandera schemas to define:
   - Required columns
   - Data types
   - Nullable constraints
   - Custom validation rules

5. **Code Style**:
   - Keep functions focused and single-purpose
   - Use descriptive variable names
   - Add docstrings to functions
   - Follow PEP 8 style guidelines

## Common Tasks

### Adding a New File Schema
1. Define the Pandera schema with expected columns
2. Add entry to SCHEMAS dictionary in backend.py
3. Test with example files in the example_data/ directory

### Modifying Validation Rules
- Update the Pandera schema in the SCHEMAS dictionary
- Ensure error messages are clear and actionable

### Updating Databricks Configuration
- Modify catalog, schema, and volume_name variables in backend.py
- Update WorkspaceClient configuration if needed

## Testing

- Use the example_data/ directory for test files
- Include both valid and invalid examples to test validation
- Test locally with `streamlit run app.py` before deploying

## Deployment

- Application deploys as a Databricks App
- Configuration in app.yaml
- Service principal needs: USE CATALOG, USE SCHEMA, READ VOLUME, WRITE VOLUME permissions

## References

- [Databricks Apps Cookbook](https://apps-cookbook.dev/docs/streamlit/volumes/volumes_upload)
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html)

