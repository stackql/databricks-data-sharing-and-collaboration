"""
Delta Sharing External Client Example
======================================

This script demonstrates how to access Delta Shared data from outside Databricks
using the delta-sharing Python library.

Prerequisites:
--------------
1. Obtain the credential file (.share) from the provider
   - Provider will send you a download URL
   - Save the file as 'config.share' in the same directory as this script
   
2. Install required packages:
   pip install delta-sharing pandas

Usage:
------
python external_client_example.py
"""

import delta_sharing
import pandas as pd
from pathlib import Path

# Path to your credential file
# Replace this with the actual path to your .share file
CREDENTIAL_FILE = "config.share"

def main():
    """Main function to demonstrate Delta Sharing client usage."""
    
    print("=" * 70)
    print("Delta Sharing External Client Demo")
    print("=" * 70)
    
    # Check if credential file exists
    if not Path(CREDENTIAL_FILE).exists():
        print(f"\n❌ ERROR: Credential file not found: {CREDENTIAL_FILE}")
        print("\nPlease:")
        print("1. Download the .share file from the URL provided by your data provider")
        print("2. Save it as 'config.share' in the same directory as this script")
        print("3. Run this script again")
        return
    
    try:
        # Create a SharingClient
        print(f"\n📁 Loading credential file: {CREDENTIAL_FILE}")
        client = delta_sharing.SharingClient(CREDENTIAL_FILE)
        
        # List all shares available to you
        print("\n📊 Available Shares:")
        shares = client.list_shares()
        for share in shares:
            print(f"  - {share.name}")
        
        # List all schemas in the first share
        if shares:
            share_name = shares[0].name
            print(f"\n📂 Schemas in share '{share_name}':")
            schemas = client.list_schemas(delta_sharing.Share(name=share_name))
            for schema in schemas:
                print(f"  - {schema.name}")
            
            # List all tables in the first schema
            if schemas:
                schema_name = schemas[0].name
                print(f"\n📋 Tables in schema '{schema_name}':")
                tables = client.list_tables(
                    delta_sharing.Schema(name=schema_name, share=share_name)
                )
                for table in tables:
                    print(f"  - {table.name}")
                
                # Query data from the first table
                if tables:
                    table = tables[0]
                    print(f"\n🔍 Querying data from '{table.name}':")
                    print("-" * 70)
                    
                    # Method 1: Load as Pandas DataFrame
                    table_url = f"{CREDENTIAL_FILE}#{share_name}.{schema_name}.{table.name}"
                    df = delta_sharing.load_as_pandas(table_url)
                    
                    print(f"\n📊 Table Schema:")
                    print(df.dtypes)
                    
                    print(f"\n📊 Row Count: {len(df)}")
                    
                    print(f"\n📊 Sample Data (first 10 rows):")
                    print(df.head(10).to_string())
                    
                    # Method 2: Using filters (if supported)
                    print("\n" + "=" * 70)
                    print("Advanced: Filtering Example")
                    print("=" * 70)
                    print("\nYou can also use SQL-like operations with Pandas:")
                    print("  filtered_df = df[df['column_name'] > 100]")
                    print("  grouped_df = df.groupby('category').sum()")
                    print("  merged_df = pd.merge(df1, df2, on='key_column')")
                    
                    # Display basic statistics
                    print(f"\n📈 Basic Statistics:")
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        print(df[numeric_cols].describe().to_string())
                    else:
                        print("  No numeric columns found")
        
        print("\n" + "=" * 70)
        print("✅ Demo completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("- Verify the credential file is valid and not expired")
        print("- Check network connectivity to the Delta Sharing server")
        print("- Ensure you have the required permissions")
        print("- Contact your data provider for assistance")

if __name__ == "__main__":
    main()


# Additional Examples:
# --------------------

def example_filtering():
    """Example: Filter data before loading."""
    client = delta_sharing.SharingClient(CREDENTIAL_FILE)
    table_url = f"{CREDENTIAL_FILE}#share.schema.table"
    
    # Load only specific columns
    df = delta_sharing.load_as_pandas(
        table_url,
        # Note: Column filtering may not be supported by all Delta Sharing servers
    )
    return df


def example_version_history():
    """Example: Access historical versions (if supported)."""
    client = delta_sharing.SharingClient(CREDENTIAL_FILE)
    table_url = f"{CREDENTIAL_FILE}#share.schema.table"
    
    # Load data from a specific version
    # Note: Time travel support depends on provider configuration
    # df = delta_sharing.load_as_pandas(table_url, version=5)
    pass


def example_export_to_csv():
    """Example: Export shared data to local CSV."""
    table_url = f"{CREDENTIAL_FILE}#share.schema.table"
    df = delta_sharing.load_as_pandas(table_url)
    df.to_csv("exported_data.csv", index=False)
    print("Data exported to exported_data.csv")


# Integration Examples:
# ---------------------

def example_powerbi_connection():
    """
    Power BI Connection:
    1. Open Power BI Desktop
    2. Get Data > More > Database > Delta Sharing (Preview)
    3. Browse to your .share credential file
    4. Select the tables you want to import
    5. Load or Transform data as needed
    """
    pass


def example_tableau_connection():
    """
    Tableau Connection:
    1. Open Tableau Desktop
    2. Connect > To a Server > More > Delta Sharing
    3. Browse to your .share credential file
    4. Select the tables you want to analyze
    5. Start building visualizations
    """
    pass
