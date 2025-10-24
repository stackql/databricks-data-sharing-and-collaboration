# D2O Delta Sharing Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATABRICKS WORKSPACE                        │
│                         (Provider Side)                         │
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                    │
│  │ Unity Catalog│         │ Delta Sharing│                    │
│  │              │         │   Service    │                    │
│  │ ┌──────────┐ │         │              │                    │
│  │ │  Share   │ │◄────────┤ - Manages    │                    │
│  │ │external_ │ │         │   recipients │                    │
│  │ │ retail   │ │         │ - Issues     │                    │
│  │ │          │ │         │   tokens     │                    │
│  │ │ Tables:  │ │         │ - Tracks     │                    │
│  │ │• customers│ │         │   access     │                    │
│  │ │• sales_  │ │         └──────────────┘                    │
│  │ │  trans.  │ │                                              │
│  │ └──────────┘ │                                              │
│  │              │                                              │
│  │ ┌──────────┐ │                                              │
│  │ │Recipient │ │                                              │
│  │ │partner_co│ │                                              │
│  │ │(Token)   │ │                                              │
│  │ └──────────┘ │                                              │
│  └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS + Bearer Token
                              │ Delta Sharing Protocol (REST API)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER CONTAINER                             │
│                     (Recipient Side)                            │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │                   Jupyter Lab                          │    │
│  │                 (http://localhost:8888)                │    │
│  └───────────────────────────────────────────────────────┘    │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────┐     │
│  │            d2o_example.ipynb                          │     │
│  │                                                       │     │
│  │  1. Load credentials from env var                    │     │
│  │  2. Connect to Delta Share                           │     │
│  │  3. List shares/schemas/tables                       │     │
│  │  4. Query data with pandas                           │     │
│  │  5. Analyze & visualize                              │     │
│  └───────────────────────────────────────────────────────┘     │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────┐     │
│  │         Python Libraries                              │     │
│  │  • delta-sharing (client library)                    │     │
│  │  • pandas (data manipulation)                        │     │
│  │  • seaborn (visualization)                           │     │
│  │  • matplotlib (plotting)                             │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
│  Environment Variable:                                          │
│  DELTA_SHARING_CONFIG = {                                      │
│    "endpoint": "https://...",                                  │
│    "bearerToken": "xxx...",                                    │
│    "expirationTime": "2026-01-20..."                           │
│  }                                                              │
│                                                                 │
│  Volume Mount:                                                  │
│  ./external_jupyter_notebooks → /workspace                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌─────────────┐                                    ┌─────────────┐
│  Provider   │                                    │  Recipient  │
│ (Databricks)│                                    │   (Docker)  │
└──────┬──────┘                                    └──────┬──────┘
       │                                                   │
       │ 1. CREATE RECIPIENT partner_co                   │
       ├──────────────────────────────────────────────────┤
       │                                                   │
       │ 2. Generate bearer token & activation link       │
       │    (Token expires: 2026-01-20)                   │
       │                                                   │
       │ 3. GRANT SELECT ON SHARE external_retail         │
       │    TO RECIPIENT partner_co                       │
       │                                                   │
       │ 4. Share config.share securely ─────────────────>│
       │    (via activation link or direct transfer)      │
       │                                                   │
       │                                                   │ 5. Load config
       │                                                   │
       │ 6. Request: List shares                          │
       │<──────────────────────────────────────────────────│
       │    (Headers: Authorization: Bearer xxx...)       │
       │                                                   │
       │ 7. Response: [external_retail]                   │
       ├─────────────────────────────────────────────────>│
       │                                                   │
       │ 8. Request: Get table metadata                   │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │ 9. Response: Schema + presigned URLs             │
       ├─────────────────────────────────────────────────>│
       │                                                   │
       │                                                   │ 10. Read data
       │                                                   │     from cloud
       │                                                   │     storage
       │                                                   │
       │ (All access logged in Unity Catalog)             │
       │                                                   │
```

## Data Access Pattern

```
┌──────────────────────────────────────────────────────────────┐
│                     Cloud Storage                             │
│                  (S3 / ADLS / GCS)                           │
│                                                               │
│  Delta Lake Files:                                            │
│  ├── customers/                                               │
│  │   ├── _delta_log/                                         │
│  │   ├── part-00000.parquet ◄──────────┐                    │
│  │   └── part-00001.parquet             │                    │
│  │                                       │                    │
│  └── sales_transactions/                 │                    │
│      ├── _delta_log/                     │                    │
│      ├── part-00000.parquet ◄────────────┼───────┐           │
│      └── part-00001.parquet              │       │           │
└──────────────────────────────────────────┼───────┼───────────┘
                                           │       │
              ┌────────────────────────────┘       │
              │ Presigned URLs                     │
              │ (short-lived)                      │
              │                                    │
    ┌─────────▼────────────────┐       ┌──────────▼──────────┐
    │  Delta Sharing Service   │       │   Recipient Client  │
    │  (Databricks)            │       │   (docker-sharing)  │
    │                          │       │                     │
    │  • Validates token       │       │  • Requests data    │
    │  • Checks permissions    │◄──────┤  • Reads directly   │
    │  • Returns presigned URLs│       │    from storage     │
    │  • Logs access           │       │  • No data copy     │
    └──────────────────────────┘       └─────────────────────┘
```

## Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
└─────────────────────────────────────────────────────────────┘

1. AUTHENTICATION
   └── Bearer Token (long-lived but expirable)
       └── Included in every API request
       └── Can be rotated by provider

2. AUTHORIZATION
   └── Unity Catalog Permissions
       └── GRANT SELECT ON SHARE TO RECIPIENT
       └── Fine-grained table-level access
       └── Optional: Dynamic views for row/column filtering

3. NETWORK SECURITY
   └── HTTPS/TLS for all communications
   └── Optional: IP access lists
   └── Presigned URLs with short expiration

4. AUDIT & COMPLIANCE
   └── All access logged in Unity Catalog
   └── Track: who, what, when
   └── Integrate with SIEM systems

5. DATA PROTECTION
   └── No data duplication
   └── Read-only access
   └── Data stays in provider's cloud
   └── Optional: Encryption at rest

┌─────────────────────────────────────────────────────────────┐
│              Alternative: OIDC Federation                    │
│  (More secure - uses short-lived JWT tokens)                │
│                                                               │
│  Provider IdP ──JWT──> Recipient ──JWT──> Delta Sharing     │
│  (Okta, Entra)         (validates)        (validates JWT)   │
│                                                               │
│  Benefits:                                                    │
│  • Short-lived tokens (minutes)                              │
│  • MFA support                                               │
│  • Centralized identity management                           │
│  • No bearer token to manage                                │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Options

```
┌──────────────────────────────────────────────────────────┐
│              Recipient Deployment Models                  │
└──────────────────────────────────────────────────────────┘

Option 1: Docker (This Demo)
┌─────────────────────┐
│  Docker Container   │
│  • Jupyter Lab      │
│  • Interactive      │
│  • Development      │
└─────────────────────┘

Option 2: Python Script
┌─────────────────────┐
│  Python Process     │
│  • Automated ETL    │
│  • Scheduled jobs   │
│  • Data pipelines   │
└─────────────────────┘

Option 3: BI Tool
┌─────────────────────┐
│  Power BI / Tableau │
│  • Visual analytics │
│  • Dashboards       │
│  • Business users   │
└─────────────────────┘

Option 4: Apache Spark
┌─────────────────────┐
│  Spark Cluster      │
│  • Large scale      │
│  • Distributed      │
│  • High performance │
└─────────────────────┘

Option 5: Cloud Function
┌─────────────────────┐
│  Lambda / Function  │
│  • Serverless       │
│  • Event-driven     │
│  • Auto-scaling     │
└─────────────────────┘
```

## Data Flow Example

```
User Query in Jupyter:
  customers_df = delta_sharing.load_as_pandas(table_url)

       │
       ▼
┌────────────────────────┐
│ 1. Parse table URL     │
│    share.schema.table  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 2. Send HTTP request   │
│    to Delta Sharing    │
│    endpoint            │
│    + Bearer token      │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 3. Provider validates: │
│    • Token valid?      │
│    • Access granted?   │
│    • Table exists?     │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 4. Return metadata +   │
│    presigned URLs to   │
│    Parquet files       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 5. Client downloads    │
│    Parquet files from  │
│    cloud storage       │
│    (S3/ADLS/GCS)       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 6. Parse Parquet and   │
│    return pandas       │
│    DataFrame           │
└────────────────────────┘
```

---
**See also:** `README-D2O-DEMO.md` for setup instructions
