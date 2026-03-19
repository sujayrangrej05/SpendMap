<div align="center">

```
$$$$$$\                                      $$\       $$\      $$\                     
$$  __$$\                                     $$ |      $$$\    $$$ |                    
$$ /  \__| $$$$$$\   $$$$$$\  $$$$$$$\   $$$$$$$ |      $$$$\  $$$$ | $$$$$$\   $$$$$$\  
\$$$$$$\  $$  __$$\ $$  __$$\ $$  __$$ \ $$  __$$ |      $$\$$\$$ $$ | \____$$\ $$  __$$\ 
 \____$$\ $$ /  $$ |$$$$$$$$ |$$ |  $$ |$$ /  $$ |      $$ \$$$  $$ | $$$$$$$ |$$ /  $$ |
$$\   $$ |$$ |  $$ |$$   ____|$$ |  $$ |$$ |  $$ |      $$ |\$  /$$ |$$  __$$ |$$ |  $$ |
\$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |  $$ |\$$$$$$$ |      $$ | \_/ $$ |\$$$$$$$ |$$$$$$$  |
 \______/ $$  ____/  \_______|\__|  \__| \_______|      \__|     \__| \_______|$$  ____/ 
          $$ |                                                                 $$ |      
          $$ |                                                                 $$ |      
          \__|                                                                 \__| 
```

### UPI Market Intelligence · Personal Finance Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Plotly Dash](https://img.shields.io/badge/Plotly-Dash-3D4DB7?style=flat-square&logo=plotly&logoColor=white)](https://dash.plotly.com)
[![Data](https://img.shields.io/badge/Data-NPCI%20%2B%20Personal-orange?style=flat-square)](/)
[![Charts](https://img.shields.io/badge/Charts-10%2B%20interactive-brightgreen?style=flat-square)](/)

**Two datasets. One unified dashboard. India's UPI market trends + your personal spending story — fully interactive, dark-themed, zero configuration.**

</div>

---

## What's inside

**Section 1 — India UPI Market (2021)**
Live charts built on NPCI public data covering 69 payment apps, 654 data points, all 12 months.

**Section 2 — Personal Finance (2023)**
Your real transaction data visualised — daily heatmap, category split, income vs spending, day-of-week patterns.

---

## Charts at a glance

| Chart | Type | Dataset |
|---|---|---|
| Monthly UPI volume & value growth | Dual-axis bar + line | NPCI |
| App market share | Donut | NPCI |
| Top 10 apps by total volume | Horizontal bar | NPCI |
| Top 5 apps monthly race | Multi-line | NPCI |
| Monthly income vs spending | Grouped bar + net line | Personal |
| Spending by category | Donut | Personal |
| Daily spend heatmap (full year) | Heatmap calendar | Personal |
| Avg spend by day of week | Bar | Personal |

---

## Quick start

```bash
pip install plotly dash pandas numpy
python3 app.py
# Open http://localhost:8050
```

---

## Dataset sources

**UPI Apps 2021** — `UPI_apps_transaction_data_in_2021.csv`
Original source: NPCI (National Payments Corporation of India) public statistics.
Available on Kaggle: [UPI apps 2021-22](https://www.kaggle.com/datasets/ramjasmaurya/upi-apps-transactions-in-2021)

**Personal Transactions** — `MyTransaction.csv`
Real bank statement export (Jan–Dec 2023). Categories: Food, Misc, Shopping, Salary, Rent, Transport.

---

---

## 📊 Results
<img width="1813" height="450" alt="newplot" src="https://github.com/user-attachments/assets/ea042bc2-9004-41ea-a286-415096a9eb15" />
<img width="1813" height="450" alt="newplot (1)" src="https://github.com/user-attachments/assets/8df3a987-7e08-4fe3-b4d0-04a77194ca00" />
<img width="1813" height="450" alt="newplot (3)" src="https://github.com/user-attachments/assets/6c0f8e73-7e0e-4952-a865-6a8146c666cc" />
<img width="1813" height="450" alt="newplot (4)" src="https://github.com/user-attachments/assets/99e8f1a6-9790-4177-ac74-718d4d2a5239" />
<img width="1813" height="450" alt="newplot (5)" src="https://github.com/user-attachments/assets/c8ed148c-c0ac-42d9-9103-616790209b98" />
<img width="1813" height="450" alt="newplot (6)" src="https://github.com/user-attachments/assets/4f16d100-b23d-42a0-a975-7481b2f639e9" />
<img width="1813" height="450" alt="newplot (7)" src="https://github.com/user-attachments/assets/7a46c7cf-9e98-4686-b9d2-0ae9a3cca4aa" />
<img width="1813" height="450" alt="newplot (2)" src="https://github.com/user-attachments/assets/54b4c2fc-ce2f-4fcb-adbf-b7242c77d0ed" />

---

## Stack

`Python` · `Plotly` · `Gradio` · `Pandas` · `NumPy`

---

<div align="center">
Built by Sujay Rangrej 
</div>
