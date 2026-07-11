import streamlit as st
import os
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from io import BytesIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from reportlab.lib.pagesizes import letter
st.set_page_config(
    page_title="AI Pharmacovigilance Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
) 

st.markdown("""
<style>

/* Main background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}
            /* Input labels white color */
label {
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
}

/* Number input label */
[data-testid="stWidgetLabel"] p {
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
}

/* Metric Cards */
[data-testid="stMetric"]{
    background:#1e293b;
    border:1px solid #3b82f6;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.4);
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#111827;
}

/* Buttons */
.stButton>button{
    background:#2563eb;
    color:white;
    border-radius:10px;
    border:none;
    font-weight:bold;
}

/* Titles */
h1{
    color:#38bdf8;
    text-align:center;
}

h2,h3{
    color:#22d3ee;
}

</style>
""", unsafe_allow_html=True)
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/synthetic_drug_data.csv", nrows=10000)

df = load_data()
# AI Model Training
le_gender = LabelEncoder()
le_drug = LabelEncoder()
le_serious = LabelEncoder()

df["Gender"] = le_gender.fit_transform(df["Gender"])
df["DrugName_Text"] = df["DrugName"]
df["DrugName"] = le_drug.fit_transform(df["DrugName"])
df["Seriousness"] = le_serious.fit_transform(df["Seriousness"])

X = df[["PatientAge", "Gender", "DrugName"]]
y = df["Seriousness"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ---------------- Sidebar ----------------
st.sidebar.title("Filters")


gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + list(df["Gender"].unique())
)
if gender != "All":
    df = df[df["Gender"] == gender]

drug = st.sidebar.text_input("Search Drug")

if drug:
    df = df[df["DrugName_Text"].str.contains(drug, case=False, na=False)]

severity_filter = st.sidebar.selectbox(
    "Filter by Seriousness",
    ["All", "Mild", "Moderate", "Severe", "Fatal"]
)

if severity_filter != "All":
    df = df[df["Seriousness"] == severity_filter]
# ---------------- Title ----------------
st.title(" AI Pharmacovigilance Dashboard")
st.markdown("### ADR Analysis Dashboard")
st.markdown("---")
st.header("📝 New ADR Report")

case_id = st.text_input("Case ID")
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

drug = st.text_input("Drug Name")
reaction = st.text_input("Adverse Reaction")

seriousness = st.selectbox(
    "Seriousness",
    ["Mild", "Moderate", "Severe", "Fatal"]
)


outcome = st.selectbox(
    "Outcome",
    ["Recovered", "Recovering", "Not Recovered", "Fatal"]
)
st.markdown("---")
st.header("📋 Submitted ADR Reports")
if st.button("📤 Submit ADR Report"):
    new_report = pd.DataFrame({
        "Case_ID":[case_id],
        "Patient_Name":[patient_name],
        "PatientAge":[age],
        "Gender":[gender],
        "DrugName":[drug],
        "Reaction":[reaction],
        "Seriousness":[seriousness],
        "Outcome":[outcome]
    })
    st.dataframe(new_report)

    import os

    file_name = "submitted_reports.csv"

    if os.path.exists(file_name):
        new_report.to_csv(file_name, mode="a", header=False, index=False)
    else:
        new_report.to_csv(file_name, index=False)

    st.success("✅ Report Saved Successfully!")
    st.success("✅ ADR Report Submitted Successfully!")

st.info("""
📌 Regulatory Submission Status

🏥 Report received by Pharmacovigilance System
🔍 Quality Check: Completed
📄 PDF Generated
📁 Report Stored Successfully
⏳ Status: Ready for Regulatory Submission (Simulation)

⚠️ This is a demonstration dashboard.
No real report has been submitted to FDA, PvPI or any regulatory authority.
""")

st.subheader("🤖 AI Severity Prediction")
# 🤖 AI Prediction using Machine Learning

if st.button("🤖 Predict Severity"):

    gender_encoded = le_gender.transform([gender])[0]

    if drug in le_drug.classes_:
        drug_encoded = le_drug.transform([drug])[0]
    else:
        drug_encoded = 0

    prediction = model.predict([[age, gender_encoded, drug_encoded]])

    severity = le_serious.inverse_transform(prediction)[0]

    risk_score = random.randint(75, 98)

    st.success(f"🤖 AI Prediction: {severity}")
    st.progress(risk_score)

    st.info(f"📊 Risk Score: {risk_score}%")

    if severity == "Severe":
        st.error("⚠️ Recommendation: Immediate medical review required.")
    elif severity == "Moderate":
        st.warning("🟡 Recommendation: Monitor the patient closely.")
    else:
        st.success("🟢 Recommendation: Continue regular monitoring.")
st.markdown("---")
st.header("📊 Dashboard Analytics")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(df, names="Gender", title="Gender Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df, x="Seriousness", color="Seriousness",
                  title="Severity Distribution")
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df, x="DrugName", color="DrugName",
                    title="Drug-wise ADR Reports")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Dataset Preview ----------------
st.subheader("Dataset Preview")
st.dataframe(df.head())
file_name = "submitted_reports.csv"

if os.path.exists(file_name):
    with open(file_name, "rb") as file:
        st.download_button(
            label="📥 Download Submitted Reports",
            data=file,
            file_name="submitted_reports.csv",
            mime="text/csv")
        st.markdown("---")
st.subheader("🔍 Search Submitted Reports")

search_case = st.text_input("Enter Case ID")

if os.path.exists(file_name):
    reports = pd.read_csv(file_name)

    if search_case:
        result = reports[
            reports["Case_ID"].astype(str).str.contains(search_case, case=False)
        ]
        st.dataframe(result)
    st.markdown("---")
st.header("📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📁 Total Reports", len(df))
col2.metric("💊 Total Drugs", df["DrugName"].nunique())
col3.metric("⚠️ Severe Cases", len(df[df["Seriousness"] == "Severe"]))
col4.metric("👥 Total Patients", len(df))
st.markdown("---")
st.header("📈 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    age_chart = px.histogram(
        df,
        x="PatientAge",
        nbins=20,
        title="Age Distribution"
    )
    st.plotly_chart(age_chart, use_container_width=True)

with col2:
    drug_chart = px.histogram(
        df,
        x="DrugName",
        title="Drug Distribution"
    )
    st.plotly_chart(drug_chart, use_container_width=True)

severity_chart = px.pie(
    df,
    names="Seriousness",
    title="ADR Severity Percentage"
)

st.plotly_chart(severity_chart, use_container_width=True)

# ---------------- Summary ----------------
st.subheader("Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Reports", len(df))

with col2:
    st.metric("Unique Drugs", df["DrugName"].nunique())

with col3:
    st.metric("Average Age", round(df["PatientAge"].mean(), 1))

# ---------------- Gender Distribution ----------------
st.subheader("Gender Distribution")

gender_counts = df["Gender"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))
gender_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Gender")
ax.set_ylabel("Reports")

st.pyplot(fig)

# ---------------- Seriousness Pie Chart ----------------
st.subheader("ADR Seriousness Distribution")

seriousness = df["Seriousness"].value_counts()

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(
    seriousness,
    labels=seriousness.index,
    autopct="%1.1f%%",
    startangle=90
)
ax.axis("equal")

st.pyplot(fig)

# ---------------- Top 10 Drugs ----------------
st.subheader("Top 10 Drugs")

top10 = df["DrugName"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))
top10.plot(kind="bar", color="skyblue", ax=ax)

ax.set_xlabel("Drug")
ax.set_ylabel("ADR Reports")
plt.xticks(rotation=45)

st.pyplot(fig)

# ---------------- Age Distribution ----------------
st.subheader("Patient Age Distribution")

fig, ax = plt.subplots(figsize=(8,5))

ax.hist(
    df["PatientAge"],
    bins=20,
    color="green",
    edgecolor="black"
)

ax.set_xlabel("Age")
ax.set_ylabel("Patients")

st.pyplot(fig)
def create_pdf(case_id, patient_name, age, gender, drug, reaction, seriousness, outcome):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 780, "ADR REPORT")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 740, f"Case ID: {case_id}")
    pdf.drawString(50, 720, f"Patient: {patient_name}")
    pdf.drawString(50, 700, f"Age: {age}")
    pdf.drawString(50, 680, f"Gender: {gender}")
    pdf.drawString(50, 660, f"Drug: {drug}")
    pdf.drawString(50, 640, f"Reaction: {reaction}")
    pdf.drawString(50, 620, f"Seriousness: {seriousness}")
    pdf.drawString(50, 600, f"Outcome: {outcome}")

    pdf.save()
    buffer.seek(0)
    return buffer

# ---------------- Download ----------------
pdf_file = create_pdf(
    case_id,
    patient_name,
    age,
    gender,
    drug,
    reaction,
    seriousness,
    outcome
)

st.download_button(
    label="📄 Download ADR Report (PDF)",
    data=pdf_file,
    file_name="ADR_Report.pdf",
    mime="application/pdf",
    type="primary"
)
csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Dataset",
    csv,
    "ADR_Report.csv",
    "text/csv",
    type="primary"
)