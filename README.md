# 🔎 DOORS Traceability Audit Tool (WIP)

This is a **prototype web-based tool** built to support **requirements traceability audits** for projects managed using **IBM DOORS Next** (or similar systems). It is designed to assist **Software Quality Assurance Representatives (SQARs)** and project stakeholders by verifying and visualizing how requirements are linked across all system levels.

---

## 📌 Status: Work in Progress 🚧

This app is an early-stage prototype.

- ✅ CSV file upload and parsing implemented
- ✅ Traceability graph visualization and orphan detection
- ✅ PDF audit report generation
- 🔜 API integration with IBM DOORS Next via OSLC (pending)
- 🔜 Internal deployment options under evaluation (security review)

---

## 💡 What It Does

- Accepts a `requirements_links.csv` file exported from DOORS
- Builds a directed graph showing requirement relationships
- Identifies and reports **orphaned requirements** (unlinked)
- Generates a downloadable **PDF audit report**
- Runs entirely via a web browser (built with Streamlit)

---

## 🚀 Try the App

👉 [Launch the App](https://your-username-your-app.streamlit.app)  
*No login required — just upload a CSV and explore.*

> ⚠️ This public app is for demo/testing only. For production use, internal deployment is recommended.

---

## 📁 Expected CSV Format

The uploaded file should contain the following columns:

| Column       | Description                              |
|--------------|------------------------------------------|
| SourceID     | The ID of the source requirement         |
| TargetID     | The ID of the target (linked) requirement|
| LinkType     | The type of link (e.g. "satisfies", "derives") |
| SourceType   | Type/category of the source (e.g. "System") |
| TargetType   | Type/category of the target              |

---

## 📷 Screenshots

![Traceability Graph Example](./assets/sample_graph.png)

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) – App framework
- [pandas](https://pandas.pydata.org/) – Data handling
- [networkx](https://networkx.org/) – Graph analysis
- [matplotlib](https://matplotlib.org/) – Graph plotting
- [fpdf](https://pyfpdf.github.io/) – PDF report generation

---

## 🔒 Security Considerations

This app is currently hosted on Streamlit Cloud.  
If company policy prohibits public cloud use, the code can be deployed internally using:

- Company-hosted Streamlit server
- Docker container
- Dash, Flask, or other internal web stack

---

## ✅ Next Steps

- [ ] Connect to IBM DOORS Next using OSLC APIs
- [ ] Auto-fetch and validate requirements for specific projects
- [ ] Add project filters, search, and improved UI
- [ ] Integrate authentication and role-based access (if internalized)

---

## 🙋 Contact & Contributions

For questions, suggestions, or contributions, please contact:

**Nonkululeko Ntshele**  
Software Quality Assurance  
📧 SAAB Grintek Defense

---

