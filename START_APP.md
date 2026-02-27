# How to Start the Compliance Discovery Questionnaire

## Quick Start (Recommended)

Open your terminal and run:

```bash
cd "/Users/nkotakis/Code Repository/desktop-tutorial"
./start.sh
```

That's it! The script will start both the backend and frontend servers.

---

## Manual Start (Alternative)

If you prefer to start services manually or the script doesn't work:

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd "/Users/nkotakis/Code Repository/desktop-tutorial/backend"
python3 -m compliance_discovery.api_server
```

You should see:
```
Loading NIST 800-53 Moderate Baseline controls...
Loaded 177 controls
Generating discovery questions...
Generated questions for 177 controls
Loaded MCP data for 177 controls
 * Running on http://127.0.0.1:5001
```

### Step 2: Start the Frontend Server

Open a **new terminal** (keep the backend running) and run:

```bash
cd "/Users/nkotakis/Code Repository/desktop-tutorial/frontend"
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5174/
```

---

## Access the Application

Once both servers are running, open your browser and go to:

**http://localhost:5174**

---

## Verify Everything is Working

### Check Backend Health
```bash
curl http://localhost:5001/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-26T..."
}
```

### Check Frontend
Open http://localhost:5174 in your browser. You should see:
- Compliance Discovery Tool interface
- Sidebar with Dashboard, Questionnaire, Settings
- Export button on the far left

---

## What's New

✅ **AWS Managed Controls Added**
- All 177 controls now have implementation guides
- Customer responsibility controls include:
  - AWS Config rules
  - Security Hub controls
  - Control Tower rules
  - Detailed implementation guidance

✅ **Export Button**
- Vertical "EXPORT" button on far left
- Click to open modal with export options
- Formats: Excel, PDF, JSON, YAML

✅ **Progress Button Removed**
- Redundant with Dashboard, now removed from sidebar

---

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:

**Backend (port 5001):**
```bash
lsof -ti:5001 | xargs kill -9
```

**Frontend (port 5174):**
```bash
lsof -ti:5174 | xargs kill -9
```

Then restart the servers.

### Backend Not Loading Data

If the backend starts but doesn't load controls:
```bash
cd "/Users/nkotakis/Code Repository/desktop-tutorial/backend"
ls -la compliance_discovery/aws_controls_mcp_data.json
```

The file should exist and be ~500KB. If missing, contact support.

### Frontend Build Errors

If npm fails:
```bash
cd "/Users/nkotakis/Code Repository/desktop-tutorial/frontend"
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## Stop the Application

### Using start.sh
Press `Ctrl+C` in the terminal where you ran `./start.sh`

### Manual Stop
Press `Ctrl+C` in each terminal window (backend and frontend)

Or kill processes:
```bash
lsof -ti:5001 | xargs kill -9  # Backend
lsof -ti:5174 | xargs kill -9  # Frontend
```

---

## Application Details

- **Backend**: Python Flask API on port 5001
- **Frontend**: React TypeScript with Vite on port 5174
- **Database**: SQLite (sessions.db)
- **Total Controls**: 177 (NIST 800-53 Moderate Baseline)
- **AWS Implementation Guides**: All 177 controls
- **Export Formats**: Excel (.xlsx), PDF (fillable), JSON, YAML

---

## Need Help?

Check these files for more information:
- `QUICKSTART_COMPLIANCE.md` - Detailed setup guide
- `COMPLIANCE_IMPLEMENTATION_SUMMARY.md` - Feature overview
- `AWS_MANAGED_CONTROLS_ADDED.md` - Latest updates
