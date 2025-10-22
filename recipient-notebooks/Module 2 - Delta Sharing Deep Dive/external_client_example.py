#!/usr/bin/env python3
"""
Delta Sharing External Client Example

This script demonstrates how to access Delta Sharing data from a standalone
Python application without requiring a Databricks workspace.

Prerequisites:
    pip install delta-sharing pandas

Usage:
    python external_client_example.py --credential /path/to/config.share

Security Notes:
    - Never commit credential files to version control
    - Store credentials securely (encrypted storage, credential managers)
    - Use environment variables for credential paths in production
    - Rotate credentials if compromised
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import delta_sharing
    import pandas as pd
except ImportError as e:
    print(f"Error: Required package not found. {e}")
    print("Install required packages: pip install delta-sharing pandas")
    sys.exit(1)


class DeltaSharingClient:
    """Wrapper class for Delta Sharing operations"""
    
    def __init__(self, credential_file: str):
        """
        Initialize Delta Sharing client
        
        Args:
            credential_file: Path to the Delta Sharing credential file (.share)
        
        Raises:
            FileNotFoundError: If credential file doesn't exist
            ValueError: If credential file is invalid
        """
        self.credential_file = credential_file
        self._validate_credential_file()
        self.client = delta_sharing.SharingClient(credential_file)
        
    def _validate_credential_file(self):
        """Validate that credential file exists and has valid structure"""
        if not os.path.exists(self.credential_file):
            raise FileNotFoundError(
                f"Credential file not found: {self.credential_file}\n"
                "Please download the credential file from your activation link."
            )
        
        try:
            with open(self.credential_file, 'r') as f:
                config = json.load(f)
            
            required_fields = ['shareCredentialsVersion', 'endpoint', 'bearerToken']
            missing = [field for field in required_fields if field not in config]
            
            if missing:
                raise ValueError(
                    f"Invalid credential file. Missing fields: {missing}"
                )
                
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid credential file format. Expected JSON."
            )
    
    def list_shares(self) -> List[delta_sharing.Share]:
        """
        List all shares available to this recipient
        
        Returns:
            List of Share objects
        """
        return self.client.list_shares()
    
    def list_schemas(self, share_name: str) -> List[delta_sharing.Schema]:
        """
        List schemas in a share
        
        Args:
            share_name: Name of the share
            
        Returns:
            List of Schema objects
        """
        share = delta_sharing.Share(share_name)
        return self.client.list_schemas(share)
    
    def list_tables(self, share_name: str, schema_name: str) -> List[delta_sharing.Table]:
        """
        List tables in a schema
        
        Args:
            share_name: Name of the share
            schema_name: Name of the schema
            
        Returns:
            List of Table objects
        """
        schema = delta_sharing.Schema(share_name, schema_name)
        return self.client.list_tables(schema)
    
    def load_table_as_pandas(
        self,
        share_name: str,
        schema_name: str,
        table_name: str,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Load a shared table into a pandas DataFrame
        
        Args:
            share_name: Name of the share
            schema_name: Name of the schema
            table_name: Name of the table
            limit: Optional limit on number of rows to load
            
        Returns:
            pandas DataFrame containing the table data
        """
        table_url = f"{self.credential_file}#{share_name}.{schema_name}.{table_name}"
        
        if limit:
            return delta_sharing.load_as_pandas(table_url, limit=limit)
        else:
            return delta_sharing.load_as_pandas(table_url)
    
    def get_table_version(
        self,
        share_name: str,
        schema_name: str,
        table_name: str
    ) -> int:
        """
        Get the current version of a shared table
        
        Args:
            share_name: Name of the share
            schema_name: Name of the schema
            table_name: Name of the table
            
        Returns:
            Current table version number
        """
        table_url = f"{self.credential_file}#{share_name}.{schema_name}.{table_name}"
        return delta_sharing.get_table_version(table_url)
    
    def print_share_summary(self):
        """Print a summary of available shares, schemas, and tables"""
        print("\n" + "="*70)
        print("DELTA SHARING - AVAILABLE DATA")
        print("="*70)
        
        shares = self.list_shares()
        print(f"\nTotal Shares: {len(shares)}\n")
        
        for share in shares:
            print(f"📦 Share: {share.name}")
            
            schemas = self.list_schemas(share.name)
            print(f"   └─ Schemas: {len(schemas)}")
            
            for schema in schemas:
                print(f"      └─ Schema: {schema.name}")
                
                tables = self.list_tables(share.name, schema.name)
                print(f"         └─ Tables: {len(tables)}")
                
                for table in tables:
                    print(f"            └─ 📊 {table.name}")
            print()


def analyze_customer_data(client: DeltaSharingClient, share_name: str, schema_name: str):
    """
    Example analysis: Load and analyze customer and sales data
    
    Args:
        client: DeltaSharingClient instance
        share_name: Name of the share
        schema_name: Name of the schema
    """
    print("\n" + "="*70)
    print("ANALYSIS: CUSTOMER AND SALES DATA")
    print("="*70)
    
    # Load customers table
    print("\n📥 Loading customers data...")
    customers_df = client.load_table_as_pandas(share_name, schema_name, "customers")
    print(f"✓ Loaded {len(customers_df)} customers")
    print(f"   Columns: {', '.join(customers_df.columns.tolist())}")
    
    # Load sales transactions
    print("\n📥 Loading sales transactions...")
    sales_df = client.load_table_as_pandas(share_name, schema_name, "sales_transactions")
    print(f"✓ Loaded {len(sales_df)} transactions")
    print(f"   Columns: {', '.join(sales_df.columns.tolist())}")
    
    # Perform analysis
    print("\n" + "-"*70)
    print("ANALYSIS RESULTS")
    print("-"*70)
    
    # 1. Customer segments
    print("\n1. Customer Distribution by Segment:")
    segment_counts = customers_df['customer_segment'].value_counts()
    for segment, count in segment_counts.items():
        print(f"   {segment}: {count} customers")
    
    # 2. Merge data for deeper analysis
    merged_df = pd.merge(
        sales_df,
        customers_df[['customer_id', 'customer_name', 'customer_segment', 'country']],
        on='customer_id',
        how='left'
    )
    
    # 3. Sales by segment
    print("\n2. Total Sales by Customer Segment:")
    segment_sales = merged_df.groupby('customer_segment')['total_amount'].agg(['sum', 'count', 'mean'])
    segment_sales.columns = ['Total Sales', 'Transaction Count', 'Avg Transaction']
    segment_sales = segment_sales.sort_values('Total Sales', ascending=False)
    print(segment_sales.to_string())
    
    # 4. Sales by region
    print("\n3. Total Sales by Region:")
    region_sales = merged_df.groupby('region')['total_amount'].sum().sort_values(ascending=False)
    print(region_sales.to_string())
    
    # 5. Top customers
    print("\n4. Top 5 Customers by Total Sales:")
    top_customers = merged_df.groupby('customer_name')['total_amount'].sum().sort_values(ascending=False).head(5)
    for idx, (customer, amount) in enumerate(top_customers.items(), 1):
        print(f"   {idx}. {customer}: ${amount:,.2f}")
    
    # 6. Product performance
    print("\n5. Top 5 Products by Sales:")
    top_products = merged_df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head(5)
    for idx, (product, amount) in enumerate(top_products.items(), 1):
        print(f"   {idx}. {product}: ${amount:,.2f}")
    
    # 7. Summary statistics
    print("\n6. Overall Summary:")
    print(f"   Total Revenue: ${merged_df['total_amount'].sum():,.2f}")
    print(f"   Average Transaction: ${merged_df['total_amount'].mean():,.2f}")
    print(f"   Total Transactions: {len(merged_df)}")
    print(f"   Unique Customers: {merged_df['customer_id'].nunique()}")
    print(f"   Unique Products: {merged_df['product_name'].nunique()}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Delta Sharing External Client Example",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all available data
    python external_client_example.py --credential config.share --list
    
    # Run customer analysis
    python external_client_example.py --credential config.share --analyze
    
    # Use environment variable for credential path
    export DELTA_SHARING_CREDENTIAL=/path/to/config.share
    python external_client_example.py --analyze
        """
    )
    
    parser.add_argument(
        '--credential',
        type=str,
        default=os.getenv('DELTA_SHARING_CREDENTIAL'),
        help='Path to Delta Sharing credential file (.share)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available shares, schemas, and tables'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Run example customer and sales analysis'
    )
    
    parser.add_argument(
        '--share',
        type=str,
        default='external_retail',
        help='Share name for analysis (default: external_retail)'
    )
    
    parser.add_argument(
        '--schema',
        type=str,
        default='retail',
        help='Schema name for analysis (default: retail)'
    )
    
    args = parser.parse_args()
    
    # Validate credential file
    if not args.credential:
        print("Error: No credential file specified.")
        print("Use --credential flag or set DELTA_SHARING_CREDENTIAL environment variable")
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize client
        print(f"🔐 Connecting to Delta Sharing...")
        print(f"   Credential file: {args.credential}")
        client = DeltaSharingClient(args.credential)
        print("✓ Connected successfully")
        
        # Execute requested action
        if args.list or (not args.list and not args.analyze):
            # Default action: list available data
            client.print_share_summary()
        
        if args.analyze:
            analyze_customer_data(client, args.share, args.schema)
        
        print("\n" + "="*70)
        print("✓ COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()