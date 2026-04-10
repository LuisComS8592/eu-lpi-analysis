# EU Logistics Performance Index Analysis

[🚀 Access the web application](https://eu-lpi-analysis.streamlit.app)

Detailed analysis of the logistics performance of European Union countries based on the Logistics Performance Index (LPI). This interactive application allows users to explore data, perform statistical analyses, and multicriteria rankings (TOPSIS, DEA/BoD).
---

## Table of Contents

- [About](#about)
- [App Acess](#app-acess)
- [Features](#features)
- [Technologies](#technologies)
- [Installation and Local Usage](#installation-and-local-usage)
- [Project Structure](#project-structure)
- [License](#license)
- [Contact](#contact)

---

## About

This project is the result of a Research Project titled "Assessment of Logistics Performance in European Union Countries based on the Logistics Performance Index". The main objective is to provide a tool for analyzing and ranking EU countries according to logistics indicators using World Bank data.

The application, developed in Python with Streamlit, integrates statistical and multicriteria methods to facilitate data-driven understanding and decision-making.

---

## App Access

Access the application online with no installation required:

👉 [https://eu-lpi-analysis.streamlit.app](https://eu-lpi-analysis.streamlit.app)

---

## Features

- Interactive exploration of Logistics Performance Index (LPI) data.
- Detailed descriptive statistical analysis.
- Ranking using the TOPSIS method, configurable by criteria and weights.
- Efficiency assessment via Data Envelopment Analysis (DEA) / Benefit of the Doubt (BoD) model.
- Dynamic graphical visualizations and results export.
- Intuitive and responsive web interface via Streamlit.

---

## Technologies

- Python 3.10+
- Pandas, NumPy, SciPy, scikit-learn
- Streamlit for the interactive interface
- Matplotlib, Seaborn, and Plotly for visualizations
- cvxpy for the DEA model
- Other dependencies detailed in `requirements.txt`

---

## Installation and Local Usage

To run the application locally:

1. Clone the repository:o

```
git clone https://github.com/your-username/eu-lpi-analysis.git
cd eu-lpi-analysis
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Run the application:

```
streamlit run app.py
```

5. Open in your browser:

```
http://localhost:8501
```

## Project Structure

```
eu-lpi-analysis/
│
├── data/                  # Raw and processed data
├── src/                   # Source code
│   ├── models/            # TOPSIS, DEA, etc. implementation
│   ├── plots/             # Visualization functions
│   └── utils/             # Helper utilities
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
└── LICENSE                # License file
```

## License
Distributed under the MIT License. See the `LICENSE` file for details.

## Contact
Luis Enrique Krulikowski | [LinkedIn](linkedin.com/in/luis-krulikowski)
