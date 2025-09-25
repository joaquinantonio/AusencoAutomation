# Automation (Grok + Python) 
**Three runnable automation demos, designed for non-IT participants, with or without API keys.**  
Scenarios covered:
1) **Finance** — Draft a monthly report from a GL CSV (highlights, variance table, risks).  
2) **HR** — Answer HR policy questions from provided policy text with **citations**.  
3) **Procurement** — Summarize contract text into a structured **contracts register**.

This kit supports two modes:
- **DRY RUN (default)** — No internet or API token required. Uses deterministic, heuristic logic to produce realistic outputs. Great for workshops and offline demos.
- **LIVE** — With a valid **xAI Grok** API token, the same scripts call the Grok API for AI-generated outputs while keeping the **same JSON shapes**.

---

## 🧭 Repository layout
```
automation_kit/
├─ run_finance.py           # Entry: Finance scenario
├─ run_hr.py                # Entry: HR policy Q&A scenario
├─ run_procurement.py       # Entry: Procurement contract summary scenario
├─ config/
│  ├─ finance.json          # Config for Finance scenario
│  ├─ hr.json               # Config for HR scenario
│  └─ proc.json             # Config for Procurement scenario
├─ sample_data/             # Redacted/fictional workshop inputs
│  ├─ gl_aug.csv            # Finance GL data (account, actual, budget)
│  ├─ hr_policy.txt         # HR policy excerpt
│  ├─ contract_A.txt        # Short contract text
│  └─ contract_B.txt        # Short contract text
├─ app/
│  ├─ llm/
│  │  └─ client.py          # Grok client (used only in LIVE mode)
│  ├─ schemas/
│  │  └─ finance.py         # Dataclasses for finance report
│  └─ services/
│     ├─ finance.py         # Core finance logic (DRY RUN + LIVE paths)
│     ├─ hr.py              # Core HR logic (DRY RUN + LIVE paths)
│     └─ procurement.py     # Core procurement logic (DRY RUN + LIVE paths)
├─ out/                     # Outputs are written here (created on first run)
├─ README.md                # This file
├─ requirements.txt         # Minimal dependencies (LIVE mode)
└─ .env.sample              # Example env variables
```

> **Tip:** The `app/` folder contains the reusable logic. The `run_*.py` scripts are thin entry points meant for workshops.

---

## 🧩 What each scenario produces
- **Finance** → `out/finance_report_YYYY-MM.json` (period, highlights[], variance_table[], risks[])  
  and `out/finance_variances_YYYY-MM.csv` (top variance rows).
- **HR** → `out/hr_qna_log.csv` with columns: question | answer | citations.
- **Procurement** → `out/contracts_register.csv` with columns: parties | term | renewal | payment | obligations | risks.

All outputs use **structured JSON** internally, so they’re easy to integrate with Sheets/DBs or Webhooks later.

---

## 🛠️ Prerequisites
- **Python 3.9+** (3.10–3.12 recommended).  
- **Internet access** only if running in **LIVE** mode with a Grok token.  
- OS: works on **macOS** and **Windows**.

Optional but recommended:
- A modern editor/IDE (PyCharm Community/Professional, VS Code).

---

## 📦 Setup (terminals / command line)

### macOS / Linux
```bash
# 1) Navigate into the project folder
cd automation_kit

# 2) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies (only needed for LIVE mode; safe to install anyway)
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
# 1) Navigate into the project folder
cd automation_kit

# 2) Create and activate a virtual environment
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install dependencies (only needed for LIVE mode; safe to install anyway)
pip install -r requirements.txt
```

> If execution policy blocks activation in PowerShell, run:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (then re-open PowerShell).

---

## 🚦 Running the demos (DRY RUN vs LIVE)

### DRY RUN (default) — **No API token required**
DRY RUN generates deterministic outputs using local heuristics. Perfect for workshops when network or tokens aren’t available.

**macOS / Linux**
```bash
cd automation_kit
source .venv/bin/activate
export DRY_RUN=true

python run_finance.py
python run_hr.py
python run_procurement.py
```

**Windows (PowerShell)**
```powershell
cd automation_kit
.\.venv\Scripts\Activate.ps1
$env:DRY_RUN = "true"

python run_finance.py
python run_hr.py
python run_procurement.py
```

Outputs will appear in the `out/` folder.

### LIVE — **Using a Grok API token**
When you have a valid **xAI Grok** API token, switch to LIVE mode:

**macOS / Linux**
```bash
cd automation_kit
source .venv/bin/activate
export DRY_RUN=false
export XAI_API_KEY=YOUR_XAI_GROK_TOKEN

python run_finance.py
python run_hr.py
python run_procurement.py
```

**Windows (PowerShell)**
```powershell
cd automation_kit
.\.venv\Scripts\Activate.ps1
$env:DRY_RUN = "false"
$env:XAI_API_KEY = "YOUR_XAI_GROK_TOKEN"

python run_finance.py
python run_hr.py
python run_procurement.py
```

**What changes between modes?**
- **DRY RUN:** No network calls. Finance highlights/risks derived from CSV math & heuristics; HR answers are built from best-matching policy lines; Procurement summaries use regex/keyword heuristics.
- **LIVE:** `app/llm/client.py` calls the Grok **/v1/chat/completions** endpoint. The same service functions request **structured JSON** via a response schema and validate the result before writing outputs.

**Security tip:** Treat real data as sensitive. Use redacted samples for demos. Never commit tokens; use env vars or secret managers.

---

## ⚙️ Configuration files (what to change)

### `config/finance.json`
```json
{
  "period": "2025-08",
  "input_path": "sample_data/gl_aug.csv",
  "outputs": {
    "json_path": "out/finance_report_2025-08.json",
    "csv_append_path": "out/finance_variances_2025-08.csv"
  }
}
```
- **period**: Label for the report period (string).  
- **input_path**: Path to a CSV containing `account,actual,budget`.  
- **outputs.json_path**: Where to write the structured report (JSON).  
- **outputs.csv_append_path**: Where to write the top variance rows (CSV).

**Use your own data:** point `input_path` to your GL/P&L CSV. The script computes `variance_pct` locally, then (LIVE) may request a narrative/structure from Grok using the same numbers.

---

### `config/hr.json`
```json
{
  "policy_path": "sample_data/hr_policy.txt",
  "questions": [
    "How many days of annual leave am I entitled to?",
    "What is the claim submission deadline?"
  ],
  "outputs": {
    "log_path": "out/hr_qna_log.csv"
  }
}
```
- **policy_path**: A text file containing the HR policy excerpts.  
- **questions[]**: The questions to answer in this batch run.  
- **outputs.log_path**: CSV log path (question, answer, citations).

**Use your own policy:** replace `policy_path` with your policy text. In LIVE mode the script prompts Grok **“Answer only from provided excerpts; otherwise say ‘Not in policy.’”**

---

### `config/proc.json`
```json
{
  "contracts": [
    "sample_data/contract_A.txt",
    "sample_data/contract_B.txt"
  ],
  "outputs": {
    "register_path": "out/contracts_register.csv"
  }
}
```
- **contracts[]**: Paths to plain-text contracts (for the workshop). You can paste text out of a PDF as a start.  
- **outputs.register_path**: Destination CSV for the contract register.

**Using PDFs later:** swap in a PDF-to-text step (e.g., `pdfplumber`) before calling the summarizer. The LIVE mode still expects clean text as input to the model.

---

## 🧪 Alternate configs via environment variables
Each runner supports an override env var to point at a different config file:

- `FINANCE_CONFIG=/path/to/your_finance.json`  
- `HR_CONFIG=/path/to/your_hr.json`  
- `PROC_CONFIG=/path/to/your_proc.json`

**Example (macOS/Linux):**
```bash
export DRY_RUN=true
export FINANCE_CONFIG=config/finance.json
python run_finance.py
```

**Example (Windows PowerShell):**
```powershell
$env:DRY_RUN = "true"
$env:HR_CONFIG = "config/hr.json"
python run_hr.py
```

---

## 🧑‍💻 Running in **PyCharm** (step-by-step)
1. **Open** the `automation_kit` folder as a project.  
2. **Create a virtualenv:** *File ▸ Settings ▸ Project ▸ Python Interpreter ▸ Add Interpreter ▸ Virtualenv* (choose Python 3.9+).  
3. **Install dependencies:** open the “Python Packages” tab, search **requests**, install (or use terminal `pip install -r requirements.txt`).  
4. **Mark Sources Root:** right-click the `app/` folder → *Mark Directory As ▸ Sources Root* (ensures imports like `from app.services...` work).  
5. **Create Run/Debug Configurations:** *Run ▸ Edit Configurations ▸ + ▸ Python*  
   - **Script path:** `run_finance.py` (repeat for `run_hr.py`, `run_procurement.py`)  
   - **Working directory:** project root (`automation_kit`)  
   - **Environment variables:**  
     - DRY RUN: `DRY_RUN=true`  
     - LIVE later: `DRY_RUN=false; XAI_API_KEY=YOUR_TOKEN`  
     - Optional: `FINANCE_CONFIG=...`, `HR_CONFIG=...`, `PROC_CONFIG=...`  
6. Click **Run**. Check outputs in the `out/` folder.

---

## 🧑‍💻 Running in **VS Code** (step-by-step)
1. **Open folder**: `automation_kit`.  
2. **Install Python extension** (ms-python.python).  
3. **Select interpreter**: `Ctrl/Cmd+Shift+P ▸ Python: Select Interpreter ▸ .venv`.  
4. **Create venv** in Terminal if you haven’t already:  
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`  
   - Windows: `py -3 -m venv .venv ; .\.venv\Scripts\Activate.ps1`  
   - Install deps: `pip install -r requirements.txt`  
5. **Set environment variables**:  
   - Create a `.env` file in project root with lines like:  
     ```
     DRY_RUN=true
     # DRY_RUN=false
     # XAI_API_KEY=YOUR_XAI_GROK_TOKEN
     ```
   - VS Code automatically loads `.env` for Run/Debug.  
6. **Run**: open `run_finance.py` and press **Run ▸ Start Debugging** (F5), or run from the Terminal:
   - `python run_finance.py`  
   - `python run_hr.py`  
   - `python run_procurement.py`

> Optional: Create `.vscode/launch.json` for pre-set configurations using the selected interpreter.

---

## 🧩 How the code is structured (under the hood)
- **DRY RUN path** — Each `app/services/*.py` function first tries a local, deterministic routine:
  - Finance computes `variance_pct` and synthesizes highlights/risks from heuristics.
  - HR extracts “best lines” using keyword overlap and builds a concise answer + citations.
  - Procurement uses light regex rules to populate the summary fields.
- **LIVE path** — If `DRY_RUN=false` and `XAI_API_KEY` is set:
  - `app/llm/client.py` constructs a request to **xAI Grok** `/v1/chat/completions`.
  - The service passes a **JSON schema** via `response_format` so the model returns strict JSON.
  - The script validates and writes the results to `out/`.

This design keeps **inputs/outputs stable** between modes so your downstream automations don’t change.

---

## 🧰 Customizing prompts or outputs (advanced)
### Example 1 — Finance: change the **tone** and **add a new field** (`recommendations[]`)

**Goal:** Ask Grok to return a short executive tone and include a new `recommendations` array in the JSON.

**Edit in** `app/services/finance.py` (LIVE path only):
```python
messages = [
    {
        "role": "system",
        "content": (
            "You are a finance analyst. "
            "Return ONLY JSON matching the schema. "
            "Use concise executive tone (<= 12 words per highlight)."
        ),
    },
    {
        "role": "user",
        "content": json.dumps({"period": period, "gl": var_rows}),
    },
]

schema = {
  "type": "json_schema",
  "json_schema": {
    "name": "FinanceReport",
    "schema": {
      "type": "object",
      "required": ["period", "highlights", "variance_table", "risks", "recommendations"],
      "properties": {
        "period": {"type": "string"},
        "highlights": {"type": "array", "items": {"type": "string"}},
        "variance_table": {"type": "array", "items": {
          "type": "object",
          "required": ["account","actual","budget","variance_pct"],
          "properties": {
            "account": {"type":"string"},
            "actual": {"type":"number"},
            "budget": {"type":"number"},
            "variance_pct": {"type":"number"}
          }
        }},
        "risks": {"type": "array", "items": {"type": "string"}},
        "recommendations": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

**What changes?**
- The model will keep highlights very short.
- The output JSON will include `recommendations` (e.g., “Trim marketing by 5% next month”).  
- Your downstream code can now read `result["recommendations"]` safely.

> **Tip:** In DRY RUN, the kit won’t auto-generate `recommendations`. If you need them offline too,
> add a small heuristic list in the DRY RUN branch near where highlights/risks are built.


### Example 2 — HR: enforce **citations** and a templated answer

**Goal:** Require at least one citation when the answer is not “Not in policy.”

**Edit in** `app/services/hr.py` (LIVE path only):
```python
messages = [
    {
        "role": "system",
        "content": (
            "Answer ONLY from the provided policy excerpts. "
            "If unknown, reply 'Not in policy.' "
            "Return JSON {answer, citations[]} where citations are exact lines used. "
            "If answer != 'Not in policy.', citations MUST contain at least 1 item. "
            "Style: one-sentence answer; no extra commentary."
        )
    },
    {"role": "user", "content": f"Policy excerpts:\n{excerpts}\n\nQuestion: {question}"}
]
```
**Validation idea:** after parsing JSON, add a simple check:
```python
if data["answer"] != "Not in policy." and len(data.get("citations", [])) == 0:
    raise ValueError("Model returned an answer without citations.")
```

**What changes?**
- Answers are short and always come with a citation line when policy covers it.
- Any hallucinated answers without citations will be caught and routed to a human.


### Example 3 — Procurement: request **normalized fields** and **risk levels**

**Goal:** Ask for a proper ISO date for renewal and a risk level per item.

**Edit in** `app/services/procurement.py` (LIVE path only):
```python
messages = [
    {"role": "system", "content": (
        "Summarize the contract into structured JSON. "
        "If a renewal deadline can be inferred, include renewal_date_iso in YYYY-MM-DD. "
        "Classify each risk as 'low' | 'medium' | 'high'."
    )},
    {"role": "user", "content": text[:15000]}
]

schema = {
  "type": "json_schema",
  "json_schema": {
    "name": "ContractSummary",
    "schema": {
      "type": "object",
      "required": ["parties","term","renewal","payment","obligations","risks","renewal_date_iso"],
      "properties": {
        "parties": {"type":"array","items":{"type":"string"}},
        "term": {"type":"string"},
        "renewal": {"type":"string"},
        "payment": {"type":"string"},
        "obligations": {"type":"array","items":{"type":"string"}},
        "risks": {"type":"array","items": {
          "type":"object",
          "required": ["text","level"],
          "properties": {
            "text": {"type":"string"},
            "level": {"type":"string","enum":["low","medium","high"]}
          }
        }},
        "renewal_date_iso": {"type":"string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
      }
    }
  }
}
```
**What changes?**
- You can sort by `renewal_date_iso` and filter risks by severity immediately.
- If the model can’t infer a date, it should leave an empty string or omit the field (adjust `required` if you prefer).
- In **LIVE** mode, edit the messages inside each service file under `app/services/` (search for `messages = [...]`).  
- You can tighten the **system prompts** (e.g., “Answer only from excerpts; do not fabricate”) or expand schemas to include more fields.  
- Keep an eye on **token budgets** if you paste long texts (especially contracts). Truncate or chunk if needed.

---

## 🧯 Troubleshooting
- **`ModuleNotFoundError: app ...`** — Mark `app/` as *Sources Root* (PyCharm) or ensure you run from the project root so relative imports resolve.  
- **No files under `out/`** — Check your working directory and permissions; the scripts write to relative paths.  
- **LIVE mode fails** — Verify `DRY_RUN=false`, `XAI_API_KEY` is set, and internet access/proxy rules allow `https://api.x.ai`.  
- **Windows activation error** — See the PowerShell execution policy tip above.  
- **CSV/paths not found** — Update `config/*.json` to point at your files, or place data in `sample_data/`.

---

## 🔐 Data & governance guidance
- Use **redacted** samples in workshops.  
- Log what you must for audit (inputs, outputs) but avoid storing sensitive free text.  
- For HR, prefer the pattern **“Answer only from provided policy excerpts.”**  
- Introduce **human-in-the-loop** steps for approvals before publishing summaries/reports.

---

## ➕ Where to go next (optional)
- Expose FastAPI endpoints (e.g., `/finance/report`, `/hr/ask`, `/proc/summary`) so **Zapier** can call your Python with Webhooks.  
- Replace the Procurement text loader with PDF parsing (e.g., `pdfplumber`).  
- Persist outputs to a database (SQLite/Postgres) instead of CSV.  
- Add scheduling (APScheduler) for periodic runs.

---

## ✅ Quick checklist
- [ ] Create venv and activate  
- [ ] `pip install -r requirements.txt`  
- [ ] **DRY RUN:** set `DRY_RUN=true` and run the three scripts  
- [ ] **LIVE:** set `DRY_RUN=false` and `XAI_API_KEY=...` then re-run  
- [ ] Edit `config/*.json` to point at your data and desired output paths
