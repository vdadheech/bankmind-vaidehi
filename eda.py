"""
eda.py — Exploratory Data Analysis for UCI Bank Marketing Dataset
VITB AI Innovators Hub · Track A
Run: python eda.py
Outputs: prints stats + saves 4 PNG charts to ./charts/
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import warnings

warnings.filterwarnings("ignore")
os.makedirs("charts", exist_ok=True)

# ── 1. Load data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — Loading data")
print("=" * 60)

df = pd.read_csv("bank-full.csv", sep=";")
print(f"Shape          : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Columns        : {list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values :\n{df.isnull().sum()}")

# ── 2. Target distribution ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2 — Target variable (y) distribution")
print("=" * 60)

y_counts = df["y"].value_counts()
y_pct    = df["y"].value_counts(normalize=True) * 100
print(y_counts.to_string())
print(f"\nSubscription rate : {y_pct['yes']:.2f}%")
print(f"Class imbalance   : {y_counts['no'] / y_counts['yes']:.1f}× more 'no' than 'yes'")
print("\n→ Class imbalance means raw accuracy is misleading.")
print("  A model predicting 'no' for everyone gets ~88% accuracy but zero utility.")
print("  Prefer F1-score, precision-recall, and ROC-AUC for evaluation.")

# Encode target for numeric operations
df["subscribed"] = (df["y"] == "yes").astype(int)

# ── 3. Q1 — Subscription rate by job ─────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — Q1: Subscription rate by job type")
print("=" * 60)

job_stats = (
    df.groupby("job")["subscribed"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "subscribers", "count": "total"})
    .assign(rate=lambda x: x["subscribers"] / x["total"] * 100)
    .sort_values("rate", ascending=False)
)
print(job_stats.to_string())
print(f"\nHighest: {job_stats.index[0]}  ({job_stats['rate'].iloc[0]:.1f}%)")
print(f"Lowest : {job_stats.index[-1]} ({job_stats['rate'].iloc[-1]:.1f}%)")

# Plot
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#3b82f6" if r == job_stats["rate"].max() else "#1e3a5f"
          for r in job_stats["rate"]]
bars = ax.barh(job_stats.index[::-1], job_stats["rate"][::-1], color=colors[::-1])
for bar, val in zip(bars, job_stats["rate"][::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=8, color="#e2e8f0")
ax.set_xlabel("Subscription Rate (%)", color="#94a3b8")
ax.set_title("Q1: Subscription Rate by Job Type", color="#e2e8f0", pad=12)
ax.set_facecolor("#0d1117"); fig.set_facecolor("#0d1117")
ax.tick_params(colors="#64748b"); ax.spines[:].set_visible(False)
plt.tight_layout()
plt.savefig("charts/q1_job_subscription_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved → charts/q1_job_subscription_rate.png")

# ── 4. Q2 — Balance vs subscription ──────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — Q2: Account balance vs subscription")
print("=" * 60)

yes_bal = df[df["y"] == "yes"]["balance"]
no_bal  = df[df["y"] == "no"]["balance"]
print(f"Median balance (subscribed)    : €{yes_bal.median():,.0f}")
print(f"Median balance (not subscribed): €{no_bal.median():,.0f}")

q2 = df[df["balance"] < df["balance"].quantile(0.99)].copy()
q2["balance_bin"] = pd.qcut(q2["balance"], q=8, duplicates="drop")
bal_stats = (
    q2.groupby("balance_bin", observed=True)["subscribed"]
    .agg(["sum", "count"])
    .assign(rate=lambda x: x["sum"] / x["count"] * 100)
    .reset_index()
)
bal_stats["bin_label"] = bal_stats["balance_bin"].apply(
    lambda x: f"€{x.left:,.0f}–{x.right:,.0f}"
)

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(range(len(bal_stats)), bal_stats["rate"], color="#3b82f6", alpha=0.8)
ax.plot(range(len(bal_stats)), bal_stats["rate"], color="#f59e0b",
        marker="o", linewidth=2, markersize=6)
ax.set_xticks(range(len(bal_stats)))
ax.set_xticklabels(bal_stats["bin_label"], rotation=30, ha="right", fontsize=7.5, color="#64748b")
ax.set_ylabel("Subscription Rate (%)", color="#94a3b8")
ax.set_title("Q2: Subscription Rate by Account Balance Decile", color="#e2e8f0", pad=12)
ax.set_facecolor("#0d1117"); fig.set_facecolor("#0d1117")
ax.tick_params(colors="#64748b"); ax.spines[:].set_visible(False)
plt.tight_layout()
plt.savefig("charts/q2_balance_subscription_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved → charts/q2_balance_subscription_rate.png")

# ── 5. Q3 — Age group vs subscription ────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5 — Q3: Subscription rate by age group")
print("=" * 60)

df["age_group"] = pd.cut(
    df["age"], bins=[17, 30, 45, 60, 100],
    labels=["18–30", "31–45", "46–60", "60+"]
)
age_stats = (
    df.groupby("age_group", observed=True)["subscribed"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "subs", "count": "total"})
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
)
print(age_stats.to_string())

fig, ax1 = plt.subplots(figsize=(7, 4))
ax2 = ax1.twinx()
labels = age_stats.index.astype(str)
x = np.arange(len(labels))
ax1.bar(x, age_stats["total"], color="#1e3a5f", label="Customers")
ax1.bar(x, age_stats["subs"],  color="#3b82f6", label="Subscribers")
ax2.plot(x, age_stats["rate"], color="#f59e0b", marker="o",
         linewidth=2.5, markersize=8, label="Rate %")
for xi, (_, row) in zip(x, age_stats.iterrows()):
    ax2.text(xi, row["rate"] + 0.4, f"{row['rate']:.1f}%", ha="center",
             fontsize=9, color="#f59e0b")
ax1.set_xticks(x); ax1.set_xticklabels(labels, color="#64748b")
ax1.set_ylabel("Customers", color="#94a3b8")
ax2.set_ylabel("Sub Rate %", color="#f59e0b")
ax1.set_title("Q3: Subscription Rate by Age Group", color="#e2e8f0", pad=12)
ax1.set_facecolor("#0d1117"); fig.set_facecolor("#0d1117")
ax1.tick_params(colors="#64748b"); ax2.tick_params(colors="#f59e0b")
ax1.spines[:].set_visible(False); ax2.spines[:].set_visible(False)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, facecolor="#1e293b",
           labelcolor="#94a3b8", loc="upper right", fontsize=8)
plt.tight_layout()
plt.savefig("charts/q3_age_subscription_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved → charts/q3_age_subscription_rate.png")

# ── 6. Q4 — Housing loan vs subscription ─────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6 — Q4: Housing loan vs subscription")
print("=" * 60)

housing_stats = (
    df.groupby("housing")["subscribed"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "subs", "count": "total"})
    .assign(rate=lambda x: x["subs"] / x["total"] * 100)
)
print(housing_stats.to_string())
delta = (housing_stats.loc["no", "rate"] - housing_stats.loc["yes", "rate"])
print(f"\nCustomers WITHOUT housing loan subscribe {delta:.1f}pp more often.")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
# Bar chart
ax = axes[0]
bars = ax.bar(["No Housing Loan", "Has Housing Loan"],
              housing_stats["rate"].values,
              color=["#22c55e", "#ef4444"])
for bar, val in zip(bars, housing_stats["rate"].values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", fontsize=11, color="#e2e8f0")
ax.set_ylabel("Subscription Rate (%)", color="#94a3b8")
ax.set_title("Q4: Housing Loan vs No Loan", color="#e2e8f0", pad=10)
ax.set_facecolor("#0d1117"); ax.tick_params(colors="#64748b")
ax.spines[:].set_visible(False)

# Cross-tab
ax2 = axes[1]
cross = df.groupby(["housing", "loan"])["subscribed"].mean() * 100
cross = cross.unstack()
im = ax2.imshow(cross.values, cmap="Blues", aspect="auto")
ax2.set_xticks([0, 1]); ax2.set_xticklabels(["No Personal Loan", "Has Personal Loan"], color="#64748b")
ax2.set_yticks([0, 1]); ax2.set_yticklabels(["No Housing Loan", "Has Housing Loan"], color="#64748b")
for i in range(2):
    for j in range(2):
        ax2.text(j, i, f"{cross.values[i, j]:.1f}%", ha="center", va="center",
                 color="white", fontweight="bold", fontsize=12)
ax2.set_title("Sub Rate: Housing × Personal Loan", color="#e2e8f0", pad=10)
ax2.set_facecolor("#0d1117")
fig.set_facecolor("#0d1117")
plt.tight_layout()
plt.savefig("charts/q4_housing_loan_subscription_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved → charts/q4_housing_loan_subscription_rate.png")

print("\n" + "=" * 60)
print("EDA COMPLETE — all 4 charts saved to ./charts/")
print("=" * 60)
