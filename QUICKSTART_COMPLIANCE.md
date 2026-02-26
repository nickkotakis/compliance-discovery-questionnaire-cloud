# Quick Start Guide - Compliance Discovery Questionnaire

Get up and running with the Compliance Discovery Questionnaire in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Internet connection (to download NIST data)

## Step 1: Install Dependencies

### Backend
```bash
pip install -r requirements.txt
```

### Frontend
```bash
npm install
```

## Step 2: Start the API Server

```bash
python compliance_discovery/api_server.py
```

**Expected output:**
```
Starting Compliance Discovery API Server...
Initializing data...
Loading NIST 800-53 Moderate Baseline controls...
Loaded 325 controls
Generating discovery questions...
Generated questions for 325 controls
Server ready!
 * Running on http://127.0.0.1:5000
```

**Note:** First startup takes 10-30 seconds to download NIST data.

## Step 3: Start the Frontend

In a new terminal:

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 4: Access the Application

Open your browser and navigate to:

**http://localhost:5173/compliance**

## What You'll See

1. **Controls List**: All 325 NIST 800-53 Moderate Baseline controls
2. **Family Filter**: Dropdown to filter by control family (AC, AU, CM, etc.)
3. **Control Cards**: Click to expand and see details
4. **Questions**: 8-10 discovery questions per control
5. **AWS Hints**: AWS implementation guidance
6. **Session Management**: Create sessions to track responses

## Quick Tour

### Browse Controls
- Scroll through the list of controls
- Use the family filter to narrow down
- Click any control to expand

### Answer Questions
- Expand a control
- Read the questions
- Type your responses in the text areas
- Responses auto-save when you leave the field

### Create a Session
1. Click "New Session" button
2. Enter customer name (e.g., "Example Bank")
3. Enter analyst name (e.g., "John Doe")
4. Click "Create Session"
5. Session ID appears at the top
6. All responses are tracked in this session

### Export Template
1. Click "Export Template" button
2. JSON file downloads with all controls and questions
3. Complete offline and import later (future feature)

## Example Workflow

1. **Start a new session**
   - Click "New Session"
   - Enter "Example Bank" and "Jane Smith"
   - Click "Create Session"

2. **Browse Access Control (AC) family**
   - Select "AC" from family filter
   - See ~20 AC controls

3. **Assess AC-1 (Policy and Procedures)**
   - Click AC-1 to expand
   - Read the 9 questions
   - Answer each question
   - Note AWS hints for implementation

4. **Continue with other controls**
   - Work through each control in the family
   - Responses auto-save to your session

5. **Export your work**
   - Click "Export Template" to save progress
   - Or continue in the next session

## Troubleshooting

### API Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Controls Not Loading

**Error:** "Failed to load controls" in browser

**Solution:**
1. Check API server is running on port 5000
2. Look for errors in API server terminal
3. Verify internet connection (needed for NIST data)

### Slow Initial Load

**Issue:** API takes 30+ seconds to start

**Explanation:** This is normal! The system downloads and parses 325 controls from NIST GitHub on first load. Subsequent requests are fast.

### Port Already in Use

**Error:** `Address already in use: 5000`

**Solution:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python compliance_discovery/api_server.py --port 5001
```

## Testing the Installation

Run the example script to verify everything works:

```bash
python example_compliance_usage.py
```

**Expected output:**
```
================================================================================
Compliance Discovery Questionnaire - Example Usage
================================================================================

Step 1: Parsing NIST 800-53 Moderate Baseline...
--------------------------------------------------------------------------------
✓ Successfully loaded 325 controls

Example controls:
  • AC-1: Policy and Procedures
    Family: AC
    Parameters: 2
    Enhancements: 0

...
```

## Next Steps

1. **Read the full documentation**: `COMPLIANCE_INTEGRATION_README.md`
2. **Review the design**: `.kiro/specs/compliance-discovery-questionnaire/design.md`
3. **Explore the API**: Try the endpoints with curl or Postman
4. **Customize questions**: Modify `question_generator.py`
5. **Add framework mappings**: Implement NIST CSF, GLBA, SOX, FFIEC

## API Quick Reference

### Get All Controls
```bash
curl http://localhost:5000/api/controls
```

### Get Control Details
```bash
curl http://localhost:5000/api/controls/AC-1
```

### Create Session
```bash
curl -X POST http://localhost:5000/api/session \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Example Bank","analyst_name":"John Doe","frameworks":["NIST 800-53"]}'
```

### Export Template
```bash
curl http://localhost:5000/api/export > template.json
```

## Support

For issues or questions:
1. Check `COMPLIANCE_INTEGRATION_README.md` troubleshooting section
2. Review API server logs for errors
3. Verify all dependencies are installed
4. Ensure ports 5000 and 5173 are available

## Success!

You're now ready to use the Compliance Discovery Questionnaire! 🎉

Start assessing your NIST 800-53 compliance by browsing controls and answering questions.
