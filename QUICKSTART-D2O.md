# D2O Delta Sharing Demo - Quick Reference

## 🚀 Quick Start Commands

### Build Docker Image
```bash
docker build -t d2o-delta-sharing-demo .
```

### Run the Demo (PowerShell - Windows)
```powershell
$configContent = Get-Content .\.creds\config.share -Raw
docker run -d --name d2o-demo -p 8888:8888 -e DELTA_SHARING_CONFIG="$configContent" -v "${PWD}\external_jupyter_notebooks:/workspace" d2o-delta-sharing-demo
```

### Run the Demo (Bash - Linux/Mac)
```bash
CONFIG_CONTENT=$(cat .creds/config.share)
docker run -d --name d2o-demo -p 8888:8888 -e DELTA_SHARING_CONFIG="$CONFIG_CONTENT" -v "$(pwd)/external_jupyter_notebooks:/workspace" d2o-delta-sharing-demo
```

### Access Jupyter Lab
```
http://localhost:8888
```

## 📋 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Provider Notebook | `provider-notebooks/Module 2.../2.3 DEMO...` | Creates share & recipient |
| Recipient Notebook | `external_jupyter_notebooks/d2o_example.ipynb` | Demos data access |
| Credentials | `.creds/config.share` | Bearer token (DO NOT COMMIT) |
| Dockerfile | `./Dockerfile` | Container definition |
| Run Scripts | `./run-d2o-demo.*` | Launch scripts |

## 🔧 Docker Commands

```bash
# View logs
docker logs d2o-demo

# Stop container
docker stop d2o-demo

# Remove container
docker rm d2o-demo

# View running containers
docker ps

# Clean everything and rebuild
docker stop d2o-demo; docker rm d2o-demo; docker rmi d2o-delta-sharing-demo
```

## 📊 Demo Flow

```
1. Provider: Run Databricks notebook
   ↓
2. Provider: Download config.share → .creds/
   ↓
3. Recipient: Run ./run-d2o-demo.ps1
   ↓
4. Recipient: Open http://localhost:8888
   ↓
5. Recipient: Run d2o_example.ipynb
   ↓
6. Recipient: View data & visualizations
```

## 🎯 What the Demo Shows

✅ Connect to Delta Share  
✅ List available shares  
✅ Query customers table  
✅ Query sales transactions  
✅ Generate summary statistics  
✅ Create visualizations:
  - Sales distribution
  - Time series
  - Customer demographics
  - Revenue analysis

## 🔐 Security Checklist

- [ ] config.share is in `.creds/` directory
- [ ] `.creds/` is in `.gitignore`
- [ ] Token expiration date is checked
- [ ] Activation link shared securely (if needed)
- [ ] Container runs in isolated network
- [ ] No credentials in notebook code

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Docker not running | Start Docker Desktop |
| Port 8888 in use | Stop other Jupyter instances |
| config.share not found | Run provider notebook first |
| Token expired | Rotate token in Databricks |
| Cannot connect | Check network/token validity |

## 📦 Container Details

**Image:** `d2o-delta-sharing-demo`  
**Container Name:** `d2o-demo`  
**Port:** `8888:8888`  
**Volume:** `./external_jupyter_notebooks:/workspace`  
**Env Var:** `DELTA_SHARING_CONFIG`

## 🔄 Typical Workflow

### First Time Setup
1. Run provider notebook in Databricks
2. Download config.share
3. Save to `.creds/config.share`
4. Run `./run-d2o-demo.ps1`
5. Open browser to localhost:8888
6. Run demo notebook

### Subsequent Runs
1. Run `./run-d2o-demo.ps1` (auto-rebuilds)
2. Open browser to localhost:8888
3. Run demo notebook

### Token Expired
1. Rotate token in Databricks UI
2. Download new config.share
3. Restart container: `.\run-d2o-demo.ps1`

## 💡 Tips

- **Persist changes:** Notebook changes are saved to your local filesystem
- **Multiple demos:** Change container name & port to run multiple instances
- **Production use:** Replace bearer token with OIDC federation
- **BI tools:** Use same config.share with Power BI, Tableau, etc.
- **Automation:** Schedule Python scripts using delta-sharing library

## 📚 Learn More

- Full documentation: `README-D2O-DEMO.md`
- Provider notebook: See provider-notebooks folder
- Delta Sharing docs: https://docs.databricks.com/delta-sharing/

---
**Quick help:** Check `README-D2O-DEMO.md` for detailed instructions
