# D2O Demo - Expected Output Examples

This document shows what you should expect to see when running the D2O Delta Sharing demo.

## Running the Container

### PowerShell Output
```powershell
PS C:\LocalGitRepos\databricks\databricks-data-sharing-and-collaboration> .\run-d2o-demo.ps1

========================================
D2O Delta Sharing Demo - Docker Setup
========================================

Checking Docker...
✓ Docker is running
✓ Found config.share
✓ Loaded credentials

Building Docker image...
[+] Building 45.2s (8/8) FINISHED
✓ Docker image built successfully

Cleaning up existing containers...
✓ Cleanup complete

Starting Docker container...
✓ Container started successfully

Waiting for Jupyter Lab to start...

========================================
SUCCESS! Container is running
========================================

Jupyter Lab is accessible at:
  http://localhost:8888

The notebook 'd2o_example.ipynb' is available in the workspace.

To view container logs:
  docker logs d2o-demo

To stop the container:
  docker stop d2o-demo

To remove the container:
  docker rm d2o-demo
```

## Jupyter Lab

### Browser View
When you open http://localhost:8888, you should see:

```
┌─────────────────────────────────────────────────────────┐
│  Jupyter Lab                                     × ⎕ −  │
├─────────────────────────────────────────────────────────┤
│  File  Edit  View  Run  Kernel  Tabs  Settings  Help   │
├──────────────┬──────────────────────────────────────────┤
│              │                                           │
│  📁 workspace│  🎯 Launcher                             │
│    📓 d2o_   │                                           │
│      example │  Notebook                                │
│      .ipynb  │  ┌──────────┐                            │
│              │  │ Python 3 │                            │
│              │  └──────────┘                            │
│              │                                           │
└──────────────┴──────────────────────────────────────────┘
```

## Notebook Execution

### Cell 1: Import Libraries

**Code:**
```python
import delta_sharing
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os
import warnings

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

print("✓ Libraries imported successfully")
print(f"Delta Sharing version: {delta_sharing.__version__}")
print(f"Pandas version: {pd.__version__}")
```

**Expected Output:**
```
✓ Libraries imported successfully
Delta Sharing version: 1.0.3
Pandas version: 2.1.0
```

### Cell 2: Load Credentials

**Code:**
```python
config_json = os.environ.get('DELTA_SHARING_CONFIG')
# ... [rest of code]
```

**Expected Output:**
```
✓ Credentials loaded successfully
Endpoint: https://nvirginia.cloud.databricks.com/api/2.0/delta-sharing/metastores/1dcd4d81-7ba5-4618-95dc-00bda50dac97
Token expires: 2026-01-20T03:36:52.591Z
✓ Delta Sharing client initialized
```

### Cell 3: List Shares

**Code:**
```python
shares = client.list_shares()
print(f"✓ Found {len(shares)} share(s)\n")
for share in shares:
    print(f"Share: {share.name}")
```

**Expected Output:**
```
✓ Found 1 share(s)

Share: external_retail
  ID: external_retail
```

### Cell 4: List Schemas

**Expected Output:**
```
Working with share: external_retail

✓ Found 1 schema(s)

Schema: retail
  Share: external_retail
```

### Cell 5: List Tables

**Expected Output:**
```
Working with schema: retail

✓ Found 2 table(s)

1. Table: customers
   Share: external_retail
   Schema: retail

2. Table: sales_transactions
   Share: external_retail
   Schema: retail
```

### Cell 6: Query Customers

**Expected Output:**
```
Loading customers table...
✓ Loaded 1000 customer records

Data shape: (1000, 6)

Column names:
['customer_id', 'name', 'email', 'segment', 'region', 'signup_date']

First few records:
```

| customer_id | name          | email                | segment   | region | signup_date |
|------------|---------------|----------------------|-----------|--------|-------------|
| 1          | John Smith    | john.smith@email.com | Premium   | North  | 2023-01-15  |
| 2          | Jane Doe      | jane.doe@email.com   | Standard  | South  | 2023-02-20  |
| 3          | Bob Johnson   | bob.j@email.com      | Premium   | East   | 2023-01-10  |
| 4          | Alice Brown   | alice.b@email.com    | Basic     | West   | 2023-03-05  |
| 5          | Charlie Davis | charlie.d@email.com  | Premium   | North  | 2023-01-25  |

### Cell 7: Query Sales Transactions

**Expected Output:**
```
Loading sales transactions table...
✓ Loaded 5000 transaction records

Data shape: (5000, 5)

Column names:
['transaction_id', 'customer_id', 'amount', 'product_category', 'transaction_date']

First few records:
```

| transaction_id | customer_id | amount | product_category | transaction_date |
|---------------|-------------|--------|------------------|------------------|
| 1             | 123         | 149.99 | Electronics      | 2024-01-15       |
| 2             | 456         | 29.99  | Books            | 2024-01-16       |
| 3             | 789         | 299.99 | Clothing         | 2024-01-16       |
| 4             | 123         | 79.99  | Home             | 2024-01-17       |
| 5             | 234         | 199.99 | Electronics      | 2024-01-18       |

### Cell 8: Summary Statistics

**Expected Output:**
```
============================================================
CUSTOMER DATA SUMMARY
============================================================

Total customers: 1,000

Customer info:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000 entries, 0 to 999
Data columns (total 6 columns):
 #   Column        Non-Null Count  Dtype         
---  ------        --------------  -----         
 0   customer_id   1000 non-null   int64         
 1   name          1000 non-null   object        
 2   email         1000 non-null   object        
 3   segment       1000 non-null   object        
 4   region        1000 non-null   object        
 5   signup_date   1000 non-null   datetime64[ns]

============================================================
SALES DATA SUMMARY
============================================================

Total transactions: 5,000
Total revenue: $749,950.00
Average transaction: $149.99
Max transaction: $499.99
Min transaction: $9.99

Sales data info:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5000 entries, 0 to 4999
Data columns (total 5 columns):
 #   Column            Non-Null Count  Dtype         
---  ------            --------------  -----         
 0   transaction_id    5000 non-null   int64         
 1   customer_id       5000 non-null   int64         
 2   amount            5000 non-null   float64       
 3   product_category  5000 non-null   object        
 4   transaction_date  5000 non-null   datetime64[ns]
```

### Cell 9: Sales Visualizations

**Expected Output:**

A 2x2 grid of plots displaying:

```
┌───────────────────────────────────────────────────────┐
│        Sales Data Analysis Dashboard                  │
├──────────────────────┬────────────────────────────────┤
│                      │                                │
│  Distribution of     │  Transaction Amount           │
│  Transaction Amounts │  Box Plot                     │
│                      │                                │
│  [Histogram with     │  [Box plot showing            │
│   bell curve]        │   median, quartiles,          │
│                      │   outliers]                    │
│                      │                                │
├──────────────────────┼────────────────────────────────┤
│                      │                                │
│  Transactions        │  Top 10 Customers by          │
│  Over Time           │  Transaction Count            │
│                      │                                │
│  [Line graph showing │  [Horizontal bar chart        │
│   daily trend]       │   showing top customers]      │
│                      │                                │
└──────────────────────┴────────────────────────────────┘

✓ Visualizations created successfully
```

### Cell 10: Customer Demographics

**Expected Output:**

A 1x2 grid showing:

```
┌───────────────────────────────────────────────────────┐
│        Customer Demographics Analysis                 │
├──────────────────────┬────────────────────────────────┤
│                      │                                │
│  Top 10 segment      │  region Distribution           │
│  Distribution        │  (Pie Chart)                   │
│                      │                                │
│  [Bar chart showing  │  [Pie chart showing           │
│   Premium: 450       │   North: 30%                  │
│   Standard: 350      │   South: 25%                  │
│   Basic: 200]        │   East: 25%                   │
│                      │   West: 20%]                  │
│                      │                                │
└──────────────────────┴────────────────────────────────┘

✓ Customer demographics visualizations created
```

### Cell 11: Advanced Analysis

**Expected Output:**

```
✓ Merged dataset created with 5000 records

Merged columns: ['transaction_id', 'customer_id', 'amount', 'product_category', 
'transaction_date', 'name', 'email', 'segment', 'region', 'signup_date']

Revenue Analysis by segment:

            Total Revenue  Avg Transaction  Transaction Count
Premium         449,925.00           149.98              3,000
Standard        224,962.50           149.98              1,500
Basic            75,062.50           150.13                500

[Two bar charts showing revenue by segment]
```

### Cell 12: Summary

**Expected Output:**

```
🎉 Demo Complete!

In this notebook, we successfully demonstrated D2O (Databricks-to-Open) 
Delta Sharing as a recipient:

✅ What we accomplished:
1. Loaded credentials from environment variable
2. Connected to the Delta Sharing endpoint
3. Listed available shares, schemas, and tables
4. Queried shared data using pandas
5. Performed data analysis and generated summary statistics
6. Created multiple visualizations using seaborn and matplotlib
7. Merged datasets for advanced analytics

... [rest of summary text]
```

## Docker Logs

To view container logs:
```bash
docker logs d2o-demo
```

**Expected Log Output:**
```
[I 2025-10-24 10:30:45.123 ServerApp] jupyterlab | extension was successfully linked.
[I 2025-10-24 10:30:45.234 ServerApp] Writing Jupyter server cookie secret to /root/.local/share/jupyter/runtime/jupyter_cookie_secret
[I 2025-10-24 10:30:45.456 ServerApp] Serving notebooks from local directory: /workspace
[I 2025-10-24 10:30:45.456 ServerApp] Jupyter Server 2.7.0 is running at:
[I 2025-10-24 10:30:45.456 ServerApp] http://hostname:8888/lab
[I 2025-10-24 10:30:45.456 ServerApp]     http://127.0.0.1:8888/lab
[I 2025-10-24 10:30:45.456 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

## Stopping the Demo

```bash
PS> docker stop d2o-demo
d2o-demo

PS> docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## Troubleshooting Examples

### Port Already in Use

**Error:**
```
Error response from daemon: driver failed programming external connectivity on endpoint d2o-demo: 
Bind for 0.0.0.0:8888 failed: port is already allocated.
```

**Solution:**
```bash
# Find what's using port 8888
netstat -ano | findstr :8888

# Stop that process or change the port in run-d2o-demo.ps1
```

### Token Expired

**Error in Notebook:**
```python
Exception: HTTPError: 401 Client Error: Unauthorized for url: https://...
```

**Solution:**
1. Check token expiration in config.share
2. Rotate token in Databricks UI
3. Download new config.share
4. Restart container: `.\run-d2o-demo.ps1`

### Cannot Connect to Share

**Error in Notebook:**
```python
Exception: ConnectionError: HTTPSConnectionPool(host='...', port=443): 
Max retries exceeded with url: /api/2.0/delta-sharing/...
```

**Solution:**
1. Check network connectivity
2. Verify endpoint URL in config.share
3. Check firewall/proxy settings
4. Verify recipient has been granted access

## Performance Notes

**Expected Timing:**
- Container build (first time): 2-5 minutes
- Container start: 5-10 seconds
- Jupyter Lab ready: 3-5 seconds
- Load 1000 customer records: 1-3 seconds
- Load 5000 transaction records: 2-5 seconds
- Generate visualizations: 2-5 seconds per chart

**Factors affecting performance:**
- Network bandwidth to Databricks
- Size of shared tables
- Complexity of queries
- Docker resource allocation

---
**See also:**
- `README-D2O-DEMO.md` - Full setup guide
- `QUICKSTART-D2O.md` - Quick reference
- `ARCHITECTURE-D2O.md` - System architecture
