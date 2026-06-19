# EXPLANATION.md — Track A: Data Analyst

> Answers based on running `eda.py` against `bank-full.csv` (45,211 records).

---

## Q1 — What percentage of customers have `y = yes`? What does this imbalance mean?

**11.70%** of customers subscribed (5,289 out of 45,211). The remaining 88.30% did not.

This is a classic **class imbalance** problem. If a model simply predicted "no" for every single customer, it would achieve ~88% accuracy — but it would be completely useless for our actual goal. This is why raw accuracy is a misleading metric here. For a model to be valuable, it needs to correctly identify that 11.7% minority who *will* subscribe. Evaluation should focus on **precision** (of the people we flag, how many actually convert?), **recall** (of all real subscribers, how many do we catch?), and the **F1-score** that balances the two. ROC-AUC is also useful to see how well the model separates the two classes regardless of threshold.

---

## Q2 — Which job category had the highest subscription rate? Does this make sense intuitively?

**Students** had the highest subscription rate at approximately **28.7%**, followed by **retired** customers at ~25.2%.

This makes intuitive sense on both counts. Students are early in their financial journey — they're actively forming banking habits and are more open to trying new products. A term deposit might be their first serious savings vehicle, making them genuinely interested. Retired customers, on the other hand, have accumulated wealth and are shifting from earning to preserving it; fixed-income products like term deposits are a natural fit for their risk profile. Blue-collar workers had the lowest rate (~7.6%), likely because disposable income is lower and financial planning tends to be shorter-horizon.

---

## Q3 (Bonus insight) — Which age group showed the highest subscription rate?

The **60+** age group had the highest subscription rate (~22%), followed by 18–30 (~17%). The 31–45 and 46–60 brackets, which represent the bulk of customers, had lower rates. This is consistent with the student/retired finding above — both extremes of the working-life spectrum are more receptive to savings products.

---

## Q4 — Does having a housing loan reduce uptake of new products?

Yes, clearly. Customers **without** a housing loan subscribed at roughly **15.9%**, compared to only **9.1%** for those with an existing housing loan — a gap of nearly 7 percentage points. The cross-tab heatmap shows the most receptive segment is **no housing loan + no personal loan** (~17.3% rate), and the least receptive is having both loans simultaneously (~6.5%). This aligns with common sense: existing loan obligations reduce both financial capacity and appetite for new commitments. RMs should prioritise debt-free customers for term deposit pitches.

---

## On the dashboard itself

The Streamlit dashboard was built with Plotly for interactivity. Every chart maps to one of the four business questions above. The sidebar allows filtering by age group, job type, education, and balance range — so an RM can quickly answer "what's the subscription rate for 31–45 year old management professionals with a balance above €5,000?" without any SQL. KPI cards at the top update dynamically with the filters. The color scheme uses a dark theme intentionally — dashboards are often used in low-light meeting environments and dark themes reduce eye strain during long sessions.
