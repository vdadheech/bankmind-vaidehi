# Bankmind-Vaidehi Dadheech

**VITB AI Innovators Hub · Track A — Data Analyst**

An interactive Streamlit dashboard that surfaces insights from the UCI Bank Marketing Dataset for Relationship Managers.

---

## What's in this repo

| File | Purpose |
|---|---|
| `app.py` | Streamlit dashboard — 4 business questions, interactive filters |
| `eda.py` | Standalone EDA script — prints stats + saves charts to `./charts/` |
| `EXPLANATION.md` | Required answers (written after running the code) |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

### 1. Clone and install
```bash
git clone https://github.com/yourusername/bankmind-yourname
cd bankmind-yourname
pip install -r requirements.txt
```

### 2. Download the dataset
Download `bank-full.csv` from the [UCI Bank Marketing Dataset](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing) and place it in the **root of the repo** (same folder as `app.py`).

```
bankmind-yourname/
├── app.py
├── eda.py
├── bank-full.csv   ← place it here
├── EXPLANATION.md
└── requirements.txt
```

### 3. Run EDA (optional, generates charts)
```bash
python eda.py
# Charts saved to ./charts/
```

### 4. Launch the dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Dashboard Features

- **4 business questions** answered with interactive Plotly charts
- **Sidebar filters**: age group, job type, education, balance range
- **KPI cards** that update dynamically with filters
- **Raw data explorer** at the bottom

### Business questions answered:
1. Which job types have the highest subscription rate?
2. Is there a pattern between account balance and likelihood to subscribe?
3. How does subscription rate differ across age groups (18–30, 31–45, 46–60, 60+)?
4. Does having an existing housing loan reduce uptake of new products?

---

## Live Demo
🔗 *[Add your deployment link here — Streamlit Cloud, HuggingFace Spaces, etc.]*

---

## Tech Stack
- Python 3.9+
- Pandas · NumPy · Matplotlib
- Plotly · Streamlit
