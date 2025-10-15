# Databricks Data Sharing Workspace Provisioning

This project provisions Databricks workspaces for data sharing scenarios using [**StackQL**](https://github.com/stackql/stackql) and [**stackql-deploy**](https://stackql-deploy.io/).

## About StackQL and stackql-deploy

**StackQL** is an open-source DevOps framework that uses SQL to query, provision, and manage cloud and SaaS resources. It provides a unified interface to interact with cloud providers through their APIs using familiar SQL syntax.

**stackql-deploy** is an Infrastructure as Code (IaC) framework built on top of StackQL that enables:
- **Declarative infrastructure management** using SQL-based templates
- **Multi-cloud support** with consistent syntax across providers
- **State management** without external state files
- **Real-time querying** of cloud resources alongside provisioning

## Project Structure

This workspace provisioning contains two infrastructure stacks:

```
workspace_provisioning/
├── README.md                     # This file
├── provider_workspace/           # Data provider workspace infrastructure
│   ├── stackql_manifest.yml
│   └── resources/
└── recipient_workspace/          # Data recipient workspace infrastructure
    ├── stackql_manifest.yml
    └── resources/
```

Each workspace creates:
- AWS IAM roles and policies for cross-account access
- S3 buckets with appropriate policies for Databricks workspace storage
- Databricks workspace with Unity Catalog metastore
- Storage credentials and external locations for data access
- Network configurations and security groups

## Prerequisites

### AWS Account Setup
- An active AWS account with administrative permissions
- AWS CLI configured with appropriate credentials

### Databricks Account Setup
1. **Enable Databricks on AWS Marketplace**: Subscribe to the Databricks offering
2. **Complete Databricks initial setup**: Create your Databricks account
3. **Collect account identifiers**:
   - **Databricks Account ID**: Available in the Databricks console
   - **Databricks AWS Account ID**: Found in cross-account role configuration
4. **Create service principal**: Go to Account Console → User Management → Service Principals

### Local Development Setup
- Python 3.8+ with virtual environment support
- Install stackql-deploy: `pip install stackql-deploy`

## Environment Variables

Set the following environment variables for both provider and recipient workspaces:

```bash
# AWS Configuration
export AWS_REGION='us-east-1'                                    # Your AWS region
export AWS_ACCOUNT_ID='123456789012'                             # Your AWS account ID
export AWS_ACCESS_KEY_ID='your-aws-access-key'                   # AWS credentials (optional)
export AWS_SECRET_ACCESS_KEY='your-aws-secret'                   # AWS credentials (optional)

# Databricks Configuration
export DATABRICKS_ACCOUNT_ID='your-databricks-account-id'        # From Databricks console
export DATABRICKS_AWS_ACCOUNT_ID='databricks-aws-account-id'     # From cross-account setup
export DATABRICKS_CLIENT_ID='your-service-principal-client-id'   # Service principal client ID
export DATABRICKS_CLIENT_SECRET='your-service-principal-secret'  # Service principal secret
```

## Deploying Provider Workspace

### 1. Deploy Infrastructure

```bash
stackql-deploy build \
provider_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

### 2. Test Deployment

```bash
stackql-deploy test \
provider_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

### 3. Teardown (When Done)

```bash
stackql-deploy teardown \
provider_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

## Deploying Recipient Workspace

### 1. Deploy Infrastructure

```bash
stackql-deploy build \
recipient_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

### 2. Test Deployment

```bash
stackql-deploy test \
recipient_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

### 3. Teardown (When Done)

```bash
stackql-deploy teardown \
recipient_workspace dev \
-e AWS_REGION=${AWS_REGION} \
-e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} \
-e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} \
-e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

## Common Commands

### Dry Run (Preview Changes)
Add `--dry-run` to any build command to preview without making changes:

```bash
stackql-deploy build provider_workspace dev --dry-run -e AWS_REGION=${AWS_REGION} # ... other env vars
```

### Show Queries
Add `--show-queries` to see the actual SQL queries being executed:

```bash
stackql-deploy build provider_workspace dev --show-queries -e AWS_REGION=${AWS_REGION} # ... other env vars
```

### Deploy Both Workspaces
To set up a complete data sharing environment, deploy both workspaces:

```bash
# Deploy provider workspace first
stackql-deploy build provider_workspace dev -e AWS_REGION=${AWS_REGION} -e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} -e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} -e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}

# Then deploy recipient workspace
stackql-deploy build recipient_workspace dev -e AWS_REGION=${AWS_REGION} -e AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID} -e DATABRICKS_ACCOUNT_ID=${DATABRICKS_ACCOUNT_ID} -e DATABRICKS_AWS_ACCOUNT_ID=${DATABRICKS_AWS_ACCOUNT_ID}
```

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Verify environment variables and service principal permissions
2. **Resource Conflicts**: Ensure unique resource names across environments
3. **Deployment Failures**: Run with `--dry-run` first to validate configuration

### Getting Help
- **StackQL Documentation**: [https://stackql.io/docs](https://stackql.io/docs)
- **stackql-deploy Guide**: [https://github.com/stackql/stackql-deploy](https://github.com/stackql/stackql-deploy)

## Important Notes

⚠️ **Cost Management**: Remember to teardown resources when done to avoid ongoing charges.

⚠️ **Security**: Never commit credentials to version control. Use environment variables or secure credential management.

---

*This infrastructure enables Databricks data sharing scenarios using SQL-based Infrastructure as Code with StackQL.*