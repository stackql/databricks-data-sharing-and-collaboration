# D2O Demo - Setup Checklist ✅

Use this checklist to verify your D2O Delta Sharing demo is ready to run.

## Provider Setup (Do First)

### Step 1: Provider Notebook
- [ ] Opened provider notebook in Databricks
  - Location: `provider-notebooks/Module 2.../2.3 DEMO Implementing D2O Delta Sharing.ipynb`
- [ ] Ran all cells successfully
- [ ] Share created: `external_retail`
- [ ] Recipient created: `partner_co`
- [ ] Access granted to recipient
- [ ] Activation link displayed

### Step 2: Credentials
- [ ] Downloaded credential file from activation link
- [ ] Saved as: `.creds/config.share`
- [ ] File contains JSON with:
  - [ ] `bearerToken`
  - [ ] `endpoint`
  - [ ] `expirationTime`
- [ ] Token expiration date is in the future
- [ ] File is in `.gitignore` (already configured)

## Recipient Setup (Do Second)

### Step 3: Prerequisites
- [ ] Docker Desktop installed
- [ ] Docker Desktop is running
- [ ] Port 8888 is available
- [ ] PowerShell (Windows) or Bash (Linux/Mac) available

### Step 4: Files Present
- [ ] `run-d2o-demo.ps1` exists (Windows)
- [ ] `run-d2o-demo.sh` exists (Linux/Mac)
- [ ] `Dockerfile` exists
- [ ] `external_jupyter_notebooks/d2o_example.ipynb` exists
- [ ] `.creds/config.share` exists

### Step 5: Run the Demo
- [ ] Executed run script: `.\run-d2o-demo.ps1` or `./run-d2o-demo.sh`
- [ ] Script output shows:
  - [ ] "✓ Docker is running"
  - [ ] "✓ Found config.share"
  - [ ] "✓ Docker image built successfully"
  - [ ] "✓ Container started successfully"
  - [ ] "http://localhost:8888" displayed

### Step 6: Access Jupyter
- [ ] Opened browser to: http://localhost:8888
- [ ] Jupyter Lab loaded successfully
- [ ] File browser shows: `d2o_example.ipynb`
- [ ] Opened the notebook

### Step 7: Run Notebook
- [ ] Cell 1: Libraries imported successfully
- [ ] Cell 2: Credentials loaded, client initialized
- [ ] Cell 3: Shares listed (should see `external_retail`)
- [ ] Cell 4: Schemas listed (should see `retail`)
- [ ] Cell 5: Tables listed (should see `customers` and `sales_transactions`)
- [ ] Cell 6: Customer data loaded
- [ ] Cell 7: Sales data loaded
- [ ] Cell 8: Summary statistics displayed
- [ ] Cell 9: Sales visualizations displayed
- [ ] Cell 10: Customer demographics displayed
- [ ] Cell 11: Merged analysis completed
- [ ] Cell 12: Summary displayed

## Verification

### Data Checks
- [ ] Customer records count > 0
- [ ] Sales records count > 0
- [ ] No authentication errors
- [ ] No connection errors
- [ ] Visualizations render correctly

### Docker Checks
- [ ] Container is running: `docker ps | findstr d2o-demo`
- [ ] No errors in logs: `docker logs d2o-demo`
- [ ] Jupyter Lab accessible

## Troubleshooting

If any checkbox above is unchecked, refer to the corresponding section:

| Issue | See |
|-------|-----|
| Provider setup issues | Provider notebook errors |
| config.share missing | Step 2 in this checklist |
| Docker not running | Docker Desktop |
| Port 8888 in use | Kill other Jupyter instances |
| Authentication errors | Verify token not expired |
| Connection errors | Check network/firewall |
| Notebook errors | EXPECTED-OUTPUT.md |
| General issues | README-D2O-DEMO.md → Troubleshooting |

## Success Criteria

Your demo is ready when:
- ✅ All checkboxes above are checked
- ✅ No error messages in script output
- ✅ No errors in notebook execution
- ✅ All visualizations display correctly
- ✅ Data loads in < 10 seconds per table

## Quick Test Script

Run this to verify Docker and config:

```powershell
# Windows PowerShell
Write-Host "Checking Docker..."
docker version
Write-Host "`nChecking config.share..."
Test-Path .\.creds\config.share
Write-Host "`nChecking port 8888..."
netstat -an | findstr :8888
```

```bash
# Linux/Mac
echo "Checking Docker..."
docker version
echo -e "\nChecking config.share..."
ls -l .creds/config.share
echo -e "\nChecking port 8888..."
lsof -i :8888
```

## Pre-Demo Checklist (for Presenters)

Before presenting to an audience:

### 15 Minutes Before
- [ ] Run through entire setup once
- [ ] Verify all cells execute without errors
- [ ] Clear all cell outputs (for fresh demo)
- [ ] Close extra browser tabs
- [ ] Set browser zoom to 100%

### 5 Minutes Before
- [ ] Stop container: `docker stop d2o-demo`
- [ ] Prepare to run script live
- [ ] Have documentation open in separate window
- [ ] Test screen sharing

### During Demo
- [ ] Run script: `.\run-d2o-demo.ps1`
- [ ] While building, explain architecture
- [ ] Open Jupyter when container ready
- [ ] Run cells one by one with explanations
- [ ] Highlight key visualizations

### After Demo
- [ ] Stop container if needed
- [ ] Answer questions (see Q&A section in DEMO-SUMMARY.md)
- [ ] Share documentation links

## Post-Demo Cleanup (Optional)

If you want to completely clean up:

```bash
# Stop container
docker stop d2o-demo

# Remove container
docker rm d2o-demo

# Remove image (optional - will need to rebuild)
docker rmi d2o-delta-sharing-demo

# Remove credentials (optional - will need to regenerate)
# rm .creds/config.share
```

## Next Steps After Success

Once all checkboxes are complete:

1. ✅ **Experiment** - Modify the notebook, add new visualizations
2. ✅ **Learn More** - Read ARCHITECTURE-D2O.md for deep dive
3. ✅ **Try OIDC** - Set up OIDC federation (more secure)
4. ✅ **Integrate BI Tools** - Use same config.share with Power BI
5. ✅ **Production Deploy** - Set up automated pipelines

## Documentation Quick Links

- **[START-HERE.md](START-HERE.md)** - Navigation guide
- **[README-D2O-DEMO.md](README-D2O-DEMO.md)** - Full instructions
- **[QUICKSTART-D2O.md](QUICKSTART-D2O.md)** - Commands reference
- **[EXPECTED-OUTPUT.md](EXPECTED-OUTPUT.md)** - What you should see
- **[DEMO-SUMMARY.md](DEMO-SUMMARY.md)** - Complete overview

---

**All checked? Congratulations! 🎉 Your D2O demo is ready!**

Ready to run: `.\run-d2o-demo.ps1` → http://localhost:8888

---
**Last Updated:** October 2025
