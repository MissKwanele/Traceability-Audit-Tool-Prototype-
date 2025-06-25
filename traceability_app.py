import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import tempfile
from datetime import datetime

# Streamlit config
st.set_page_config(page_title="DOORS Traceability Audit Tool", layout="wide")
st.title("🔎 DOORS Traceability Audit Tool")

# Sidebar for DOORS Integration
st.sidebar.header("🔧 Options")
enable_mock_doors = st.sidebar.checkbox("Enable DOORS Integration (Mock)", value=False)

if enable_mock_doors:
    st.sidebar.subheader("Mock DOORS Settings")
    api_base_url = st.sidebar.text_input("DOORS API Base URL", "https://doors.example.com/api")
    auth_token = st.sidebar.text_input("API Token", type="password")
    start_date = st.sidebar.date_input("Start Date", datetime(2024, 12, 1))
    end_date = st.sidebar.date_input("End Date", datetime(2025, 6, 1))

    def connect_to_doors(api_base_url, auth_token):
        st.success(f"Connected to DOORS API at {api_base_url} with token {auth_token[:4]}***")
        return {"Authorization": f"Bearer {auth_token}"}

    def get_approved_requirements(start_date, end_date):
        sample_requirements = [
            {"id": "REQ-001", "name": "System shall log all access", "status": "Approved", "last_modified": "2024-11-05"},
            {"id": "REQ-002", "name": "System shall encrypt data", "status": "Approved", "last_modified": "2025-01-18"},
        ]
        start = datetime.strptime(str(start_date), "%Y-%m-%d")
        end = datetime.strptime(str(end_date), "%Y-%m-%d")
        return [r for r in sample_requirements if start <= datetime.strptime(r["last_modified"], "%Y-%m-%d") <= end]

    connect_to_doors(api_base_url, auth_token)
    approved_reqs = get_approved_requirements(start_date, end_date)
    st.subheader("📥 Approved Requirements from DOORS (Mock)")
    st.write(pd.DataFrame(approved_reqs))

# File upload
st.markdown("""
Upload your **requirements_links.csv** exported from IBM DOORS or your system.  
This tool will visualize requirement traceability, identify orphaned requirements, and generate a PDF audit report.
""")

uploaded_file = st.file_uploader("Upload requirements_links.csv", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        st.stop()

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    required_cols = {'SourceID', 'TargetID', 'LinkType', 'SourceType', 'TargetType'}
    if not required_cols.issubset(df.columns):
        st.error(f"Missing columns. Required: {required_cols}")
        st.stop()

    G = nx.DiGraph()
    for _, row in df.iterrows():
        src, tgt = row['SourceID'], row['TargetID']
        G.add_node(src, type=row['SourceType'])
        if pd.notna(tgt) and tgt != "":
            G.add_node(tgt, type=row['TargetType'])
            G.add_edge(src, tgt, type=row['LinkType'])

    orphans = [n for n in G.nodes if G.in_degree(n) == 0 and G.out_degree(n) == 0]

    st.subheader("📊 Traceability Summary")
    st.write(f"- Total requirements: **{G.number_of_nodes()}**")
    st.write(f"- Total trace links: **{G.number_of_edges()}**")
    st.write(f"- Orphaned requirements (no links): **{len(orphans)}**")
    if orphans:
        st.write(orphans)

    st.subheader("🔗 Traceability Graph")
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    edge_labels = {(u, v): d['type'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.axis('off')
    st.pyplot(plt)
    plt.close()

    class PDFReport(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Traceability Audit Report', ln=True, align='C')
            self.ln(10)
        def section_title(self, title):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, title, ln=True)
            self.ln(6)
        def section_body(self, text):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, text)
            self.ln(4)

    pdf = PDFReport()
    pdf.add_page()
    pdf.section_title("Summary")
    pdf.section_body(f"Total requirements in graph: {G.number_of_nodes()}")
    pdf.section_body(f"Total trace links: {G.number_of_edges()}")
    pdf.section_body(f"Orphaned requirements (count): {len(orphans)}")
    if orphans:
        pdf.section_body("Orphaned IDs:\n" + ", ".join(orphans))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(tmpfile.name, format='png')
        plt.close()
        pdf.image(tmpfile.name, x=10, w=pdf.w - 20)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output = io.BytesIO(pdf_bytes)

    st.subheader("📥 Download Audit Report")
    st.download_button(
        label="Download Traceability Report PDF",
        data=pdf_output,
        file_name="traceability_report.pdf",
        mime="application/pdf"
    )
else:
    st.info("Please upload your `requirements_links.csv` file to begin.")

