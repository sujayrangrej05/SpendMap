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

## Stack

`Python` · `Plotly` · `Gradio` · `Pandas` · `NumPy`

---

<div align="center">
Built by Sujay Rangrej 
</div>
