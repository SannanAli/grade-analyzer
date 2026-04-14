import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Student Grade Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Grade Analyzer")
st.markdown("Upload a CSV of student scores to get instant analysis, charts, and a summary report.")

# ── Helper functions ─────────────────────────────────────────
def assign_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

def grade_color(grade):
    return {"A": "#27AE60", "B": "#2980B9", "C": "#F39C12", "D": "#E67E22", "F": "#E74C3C"}[grade]

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    pass_mark = st.slider("Passing score threshold", 40, 70, 60, step=5)
    show_names = st.checkbox("Show student names in table", value=True)
    st.markdown("---")
    st.markdown("**Sample CSV format:**")
    st.code("Name,Score\nAlice,85\nBob,72\nCarol,91")
    st.markdown("---")

    # Download sample CSV
    sample = pd.DataFrame({
        "Name": ["Alice", "Bob", "Carol", "David", "Emma",
                 "Faisal", "Grace", "Hassan", "Iris", "James",
                 "Khalid", "Layla", "Mohammed", "Nora", "Omar"],
        "Score": [85, 72, 91, 55, 88, 63, 76, 44, 95, 67,
                  82, 70, 58, 93, 77]
    })
    csv_sample = sample.to_csv(index=False).encode("utf-8")
    st.download_button("Download sample CSV", csv_sample, "sample_grades.csv", "text/csv")

# ── File Upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is None:
    st.info("No file uploaded yet. Download the sample CSV from the sidebar to try it out.")
    st.stop()

# ── Load Data ─────────────────────────────────────────────────
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

# Validate columns
if "Score" not in df.columns:
    st.error("Your CSV must have a column named 'Score'.")
    st.stop()

df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
df.dropna(subset=["Score"], inplace=True)
df["Score"] = df["Score"].clip(0, 100)
df["Grade"] = df["Score"].apply(assign_grade)
df["Status"] = df["Score"].apply(lambda s: "Pass" if s >= pass_mark else "Fail")

# ── Metric Cards ──────────────────────────────────────────────
st.markdown("### Summary")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Students", len(df))
col2.metric("Average Score", f"{df['Score'].mean():.1f}")
col3.metric("Highest Score", f"{df['Score'].max():.0f}")
col4.metric("Lowest Score", f"{df['Score'].min():.0f}")
pass_rate = (df["Status"] == "Pass").mean() * 100
col5.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Grade Distribution")
    grade_counts = df["Grade"].value_counts().reindex(["A", "B", "C", "D", "F"], fill_value=0)
    colors = [grade_color(g) for g in grade_counts.index]
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    fig1.patch.set_facecolor("#0E1117")
    ax1.set_facecolor("#0E1117")
    bars = ax1.bar(grade_counts.index, grade_counts.values, color=colors, edgecolor="none", width=0.5)
    ax1.set_xlabel("Grade", color="white")
    ax1.set_ylabel("Number of Students", color="white")
    ax1.tick_params(colors="white")
    for spine in ax1.spines.values(): spine.set_visible(False)
    for bar, val in zip(bars, grade_counts.values):
        if val > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     str(val), ha="center", color="white", fontsize=11)
    st.pyplot(fig1)

with col_right:
    st.markdown("#### Score Distribution")
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    fig2.patch.set_facecolor("#0E1117")
    ax2.set_facecolor("#0E1117")
    ax2.hist(df["Score"], bins=10, range=(0, 100), color="#3498DB", edgecolor="#0E1117")
    ax2.axvline(pass_mark, color="#E74C3C", linestyle="--", linewidth=1.5, label=f"Pass mark ({pass_mark})")
    ax2.axvline(df["Score"].mean(), color="#F1C40F", linestyle="--", linewidth=1.5, label=f"Average ({df['Score'].mean():.1f})")
    ax2.set_xlabel("Score", color="white")
    ax2.set_ylabel("Number of Students", color="white")
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values(): spine.set_visible(False)
    legend = ax2.legend(facecolor="#1A252F", labelcolor="white", fontsize=9)
    st.pyplot(fig2)

# ── Pass / Fail Pie ───────────────────────────────────────────
st.markdown("#### Pass vs Fail")
pass_counts = df["Status"].value_counts()
fig3, ax3 = plt.subplots(figsize=(4, 2.5))
fig3.patch.set_facecolor("#0E1117")
ax3.pie(pass_counts.values,
        labels=pass_counts.index,
        colors=["#27AE60", "#E74C3C"][:len(pass_counts)],
        autopct="%1.1f%%",
        textprops={"color": "white"},
        startangle=90)
st.pyplot(fig3)

st.markdown("---")

# ── Student Table ─────────────────────────────────────────────
st.markdown("### Student Results")
display_df = df.copy()
if not show_names and "Name" in display_df.columns:
    display_df = display_df.drop(columns=["Name"])

st.dataframe(
    display_df.style.applymap(
        lambda v: f"color: {grade_color(v)}" if v in ["A","B","C","D","F"] else "",
        subset=["Grade"]
    ).applymap(
        lambda v: "color: #27AE60" if v == "Pass" else "color: #E74C3C",
        subset=["Status"]
    ),
    use_container_width=True
)

# ── Download Report ───────────────────────────────────────────
st.markdown("---")
st.markdown("### Download Report")
report_csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download full report as CSV", report_csv, "grade_report.csv", "text/csv")
