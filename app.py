import os
import warnings
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import gradio as gr

warnings.filterwarnings('ignore')

# ── Colour palette ────────────────────────────────────────────────────────────
BG       = '#0d0f12'
SURFACE  = '#151820'
BORDER   = '#252a35'
TEXT     = '#d4d9e8'
MUTED    = '#5a6275'
ACCENT   = '#4a9eff'
PURPLE   = '#9b7ff4'
GREEN    = '#2ecc71'
AMBER    = '#f0a500'
RED      = '#e74c3c'
TEAL     = '#1abc9c'
PINK     = '#e056b0'

APP_COLORS = [ACCENT, PURPLE, GREEN, AMBER, RED, TEAL, PINK,
              '#f39c12', '#16a085', '#8e44ad', '#2980b9', '#c0392b']

PAPER_STYLE = dict(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
                   font=dict(color=TEXT, family='IBM Plex Mono, monospace', size=11))

def axis_style(title='', show_grid=True):
    return dict(title=title, color=MUTED, showgrid=show_grid,
                gridcolor=BORDER, zeroline=False, tickfont=dict(size=10, color=MUTED))

# ── Dashboard generation ────────────────────────────────────────────────────────

def generate_dashboard(txn_path: str | None = None):
    """Generate all KPIs, Plotly figures, and yearly summaries.
    If ``txn_path`` is ``None`` the default ``MyTransaction.csv`` is used.
    Returns a dictionary containing markdown strings for KPIs, a dict of yearly
    markdown summaries, and Plotly Figure objects.
    """
    # Load static UPI data
    upi_path = os.path.join(os.path.dirname(__file__), 'UPI_apps_transaction_data_in_2021.csv')
    upi = pd.read_csv(upi_path)
    upi.columns = upi.columns.str.strip()

    # Load personal transaction data
    if txn_path is None:
        txn_path = os.path.join(os.path.dirname(__file__), 'MyTransaction.csv')
    txn = pd.read_csv(txn_path).dropna(how='all')
    txn['Date'] = pd.to_datetime(txn['Date'], dayfirst=True, errors='coerce')
    txn = txn.dropna(subset=['Date'])
    txn['Month']     = txn['Date'].dt.month
    txn['MonthName'] = txn['Date'].dt.strftime('%b')
    txn['MonthYear'] = txn['Date'].dt.strftime('%b %Y')
    txn['DayOfWeek'] = txn['Date'].dt.day_name()
    txn['Week']      = txn['Date'].dt.isocalendar().week.astype(int)
    txn['DayOfYear'] = txn['Date'].dt.dayofyear

    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    MONTH_MAP = {i+1: m for i, m in enumerate(MONTHS)}

    # ------ UPI pre‑computations ------
    monthly_upi = upi.groupby('Month')[['Volume (Mn)', 'Value (Cr)']].sum().reset_index()
    monthly_upi['MonthName'] = monthly_upi['Month'].map(MONTH_MAP)

    top10 = (upi.groupby('UPI Banks')['Volume (Mn)'].sum()
               .sort_values(ascending=False).head(10).reset_index())

    top5_names = top10['UPI Banks'].head(5).tolist()
    share = upi.groupby('UPI Banks')['Volume (Mn)'].sum()
    top5_vals = share[top5_names]
    others = pd.Series({'Others': share[~share.index.isin(top5_names)].sum()})
    pie_data = pd.concat([top5_vals, others]).reset_index()
    pie_data.columns = ['App', 'Volume']

    top5_monthly = (upi[upi['UPI Banks'].isin(top5_names)]
                    .groupby(['Month','UPI Banks'])['Volume (Mn)'].sum().reset_index())
    top5_monthly['MonthName'] = top5_monthly['Month'].map(MONTH_MAP)

    # ------ Personal finance pre‑computations ------
    monthly_spend = txn.groupby('Month').agg(
        Withdrawal=('Withdrawal','sum'),
        Deposit=('Deposit','sum'),
        Txns=('Withdrawal','count')
    ).reset_index()
    monthly_spend['MonthName'] = monthly_spend['Month'].map(MONTH_MAP)
    monthly_spend['Net'] = monthly_spend['Deposit'] - monthly_spend['Withdrawal']

    cat_spend = (txn[txn['Withdrawal'] > 0]
                 .groupby('Category')['Withdrawal'].sum()
                 .sort_values(ascending=False).reset_index())

    daily = txn[txn['Withdrawal'] > 0].groupby('Date')['Withdrawal'].sum().reset_index()
    daily['Week']      = daily['Date'].dt.isocalendar().week.astype(int)
    daily['DayOfWeek'] = daily['Date'].dt.weekday  # 0=Mon
    daily['MonthName'] = daily['Date'].dt.strftime('%b')

    dow_avg = (txn[txn['Withdrawal']>0]
               .groupby('DayOfWeek')['Withdrawal'].mean()
               .reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))

    # ------ KPI calculations ------
    total_upi_vol   = monthly_upi['Volume (Mn)'].sum()
    total_upi_val   = monthly_upi['Value (Cr)'].sum()
    upi_growth      = ((monthly_upi['Volume (Mn)'].iloc[-1] / monthly_upi['Volume (Mn)'].iloc[0]) - 1) * 100
    phonePe_share   = (top10[top10['UPI Banks']=='PhonePe']['Volume (Mn)'].values[0] / total_upi_vol) * 100

    total_spent     = txn['Withdrawal'].sum()
    total_received  = txn['Deposit'].sum()
    net_savings     = total_received - total_spent
    highest_month   = monthly_spend.loc[monthly_spend['Withdrawal'].idxmax(), 'MonthName']
    top_category    = cat_spend.iloc[0]['Category'] if not cat_spend.empty else 'N/A'

    # ------ Yearly spending analysis ------
    txn['Year'] = txn['Date'].dt.year
    yearly = txn.groupby('Year').agg(
        spent=('Withdrawal','sum'),
        received=('Deposit','sum')
    ).reset_index()
    yearly['net'] = yearly['received'] - yearly['spent']
    yearly_md = {}
    for _, row in yearly.iterrows():
        yr = str(int(row['Year']))
        md = f"**Year {yr}**\n- Total spent: ₹{row['spent']:,.0f}\n- Total received: ₹{row['received']:,.0f}\n- Net savings: ₹{row['net']:,.0f}"
        yearly_md[yr] = md
    year_options = list(yearly_md.keys())

    # ------ Large KPI HTML (for separate boxes) ------
    upi_kpi_html = f"""
<div class='kpi-large'>
Total volume: {total_upi_vol:,.0f} Mn<br>
Total value: ₹{total_upi_val/100000:.2f}L Cr<br>
YoY growth: +{upi_growth:.0f}%<br>
PhonePe share: {phonePe_share:.1f}%<br>
Apps tracked: 69
</div>
"""
    personal_kpi_html = f"""
<div class='kpi-large'>
Total spent: ₹{total_spent:,.0f}<br>
Total received: ₹{total_received:,.0f}<br>
Net savings: ₹{net_savings:,.0f}<br>
Highest month: {highest_month}<br>
Top category: {top_category}
</div>
"""

    # ------ Plot building functions ------

    # ------ Money Management Recommendations ------
    # Compute simple offline recommendations based on transaction patterns
    # 1. Emergency fund (3× average monthly spend)
    avg_monthly_spend = monthly_spend['Withdrawal'].mean()
    emergency_fund = avg_monthly_spend * 3
    # 2. Savings target (20% of total income)
    savings_target = total_received * 0.20
    # 3. Category spending percentages
    cat_analysis = cat_spend.copy()
    if total_spent > 0:
        cat_analysis['pct'] = cat_analysis['Withdrawal'] / total_spent * 100
    else:
        cat_analysis['pct'] = 0
    high_spend = cat_analysis[cat_analysis['pct'] > 20]
    # 4. Build recommendation markdown
    rec_lines = []
    rec_lines.append("### Money Management Recommendations")
    rec_lines.append(f"- **Emergency Fund**: Aim for at least **₹{emergency_fund:,.0f}** (≈ three months of average spending) saved in an easily accessible account.")
    rec_lines.append(f"- **Savings Goal**: Target saving **20%** of your income, i.e., **₹{savings_target:,.0f}** per year.")
    if not high_spend.empty:
        rec_lines.append("- **High‑Spending Categories (>20% of total spend):**")
        for _, row in high_spend.iterrows():
            cat = row['Category']
            pct = row['pct']
            rec_lines.append(f"  - **{cat}** accounts for **{pct:.1f}%** of spending. Consider reviewing expenses here.")
    else:
        rec_lines.append("- No single expense category exceeds 20% of total spend.")
    rec_lines.append("- **Budget Rule**: A simple 50/30/20 split (50% needs, 30% wants, 20% savings) can help you allocate income effectively.")
    recommendations_md = "\n".join(rec_lines)
    # ------ Plot building functions ------
    def make_upi_growth():
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[MONTH_MAP[m] for m in monthly_upi['Month']],
            y=monthly_upi['Volume (Mn)'],
            name='Volume (Mn txns)',
            marker_color=ACCENT,
            marker_opacity=0.85,
            yaxis='y'
        ))
        fig.add_trace(go.Scatter(
            x=[MONTH_MAP[m] for m in monthly_upi['Month']],
            y=monthly_upi['Value (Cr)'],
            name='Value (₹ Cr)',
            mode='lines+markers',
            line=dict(color=AMBER, width=2),
            marker=dict(size=6, color=AMBER),
            yaxis='y2'
        ))
        fig.update_layout(
            **PAPER_STYLE,
            yaxis=dict(**axis_style('Volume (Mn)')),
            yaxis2=dict(**axis_style('Value (₹ Cr)', False), overlaying='y', side='right'),
            xaxis=axis_style(),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10, color=MUTED)),
            margin=dict(l=50, r=60, t=20, b=40),
            hovermode='x unified',
            barmode='group'
        )
        return fig

    def make_market_share():
        colors = [ACCENT, PURPLE, GREEN, AMBER, RED, MUTED]
        fig = go.Figure(go.Pie(
            labels=pie_data['App'],
            values=pie_data['Volume'],
            hole=0.55,
            marker_colors=colors,
            textinfo='label+percent',
            textfont=dict(size=10, color=TEXT),
            hovertemplate='<b>%{label}</b><br>%{value:.0f} Mn txns<br>%{percent}<extra></extra>',
        ))
        fig.update_layout(
            **PAPER_STYLE,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(text='Market\nShare', x=0.5, y=0.5,
                              font=dict(size=13, color=TEXT), showarrow=False)]
        )
        return fig

    def make_top10_bar():
        fig = go.Figure(go.Bar(
            x=top10['Volume (Mn)'],
            y=top10['UPI Banks'],
            orientation='h',
            marker=dict(
                color=top10['Volume (Mn)'],
                colorscale=[[0, BORDER], [1, ACCENT]],
                showscale=False
            ),
            text=top10['Volume (Mn)'].apply(lambda x: f'{x:,.0f} Mn'),
            textposition='outside',
            textfont=dict(size=10, color=MUTED),
            hovertemplate='<b>%{y}</b><br>%{x:.0f} Mn transactions<extra></extra>'
        ))
        fig.update_layout(
            **PAPER_STYLE,
            xaxis=axis_style('Total Volume 2021 (Mn)'),
            yaxis=dict(**axis_style(), autorange='reversed'),
            margin=dict(l=160, r=80, t=20, b=40)
        )
        return fig

    def make_top5_monthly():
        fig = go.Figure()
        for i, app in enumerate(top5_names):
            df = top5_monthly[top5_monthly['UPI Banks'] == app]
            fig.add_trace(go.Scatter(
                x=[MONTH_MAP[m] for m in df['Month']],
                y=df['Volume (Mn)'],
                name=app.replace(' App','').replace(' Apps','').replace(' Payments Bank',''),
                mode='lines+markers',
                line=dict(color=APP_COLORS[i], width=2),
                marker=dict(size=5, color=APP_COLORS[i]),
                hovertemplate=f'<b>{app}</b><br>%{{x}}: %{{y:.0f}} Mn<extra></extra>'
            ))
        fig.update_layout(
            **PAPER_STYLE,
            xaxis=axis_style(),
            yaxis=axis_style('Volume (Mn txns)'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10, color=MUTED),
                        orientation='h', y=-0.2),
            margin=dict(l=50, r=20, t=20, b=80),
            hovermode='x unified'
        )
        return fig

    def make_monthly_spend():
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_spend['MonthName'],
            y=monthly_spend['Withdrawal'],
            name='Spent',
            marker_color=RED,
            marker_opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Spent: ₹%{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=monthly_spend['MonthName'],
            y=monthly_spend['Deposit'],
            name='Received',
            marker_color=GREEN,
            marker_opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Received: ₹%{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=monthly_spend['MonthName'],
            y=monthly_spend['Net'],
            name='Net',
            mode='lines+markers',
            line=dict(color=AMBER, width=2, dash='dot'),
            marker=dict(size=6),
            hovertemplate='Net: ₹%{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            **PAPER_STYLE,
            barmode='group',
            xaxis=axis_style(),
            yaxis=axis_style('Amount (₹)'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10, color=MUTED),
                        orientation='h', y=-0.2),
            margin=dict(l=60, r=20, t=20, b=80),
            hovermode='x unified'
        )
        return fig

    def make_category_donut():
        cat_clean = cat_spend[cat_spend['Category'] != 'Salary']
        colors = [RED, AMBER, PURPLE, TEAL, ACCENT, GREEN, PINK]
        fig = go.Figure(go.Pie(
            labels=cat_clean['Category'],
            values=cat_clean['Withdrawal'],
            hole=0.55,
            marker_colors=colors[:len(cat_clean)],
            textinfo='label+percent',
            textfont=dict(size=11, color=TEXT),
            hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>'
        ))
        fig.update_layout(
            **PAPER_STYLE,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(text='Spend<br>Split', x=0.5, y=0.5,
                          font=dict(size=13, color=TEXT), showarrow=False)]
        )
        return fig

    def make_daily_heatmap():
        hmap = daily.copy()
        hmap['DayLabel'] = hmap['Date'].dt.strftime('%a')
        hmap['WeekNum']  = (hmap['Date'] - hmap['Date'].min()).dt.days // 7
        pivot = hmap.pivot_table(index='DayOfWeek', columns='WeekNum',
                                  values='Withdrawal', aggfunc='sum').fillna(0)
        week_labels = []
        for w in pivot.columns:
            dates_in_week = hmap[hmap['WeekNum'] == w]['Date']
            if len(dates_in_week):
                week_labels.append(dates_in_week.iloc[0].strftime('%d %b'))
            else:
                week_labels.append('')
        day_labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=week_labels,
            y=day_labels,
            colorscale=[[0, SURFACE], [0.3, '#1a3a5c'], [0.7, ACCENT], [1, '#ffffff']],
            hovertemplate='Week of %{x}<br>%{y}<br>₹%{z:,.0f}<extra></extra>',
            showscale=True,
            colorbar=dict(thickness=10, len=0.8,
                          tickfont=dict(size=9, color=MUTED),
                          title=dict(text='₹', font=dict(color=MUTED, size=10)))
        ))
        fig.update_layout(
            **PAPER_STYLE,
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(color=MUTED, tickfont=dict(size=10, color=TEXT),
                       showgrid=False, zeroline=False),
            margin=dict(l=40, r=60, t=10, b=20)
        )
        return fig

    def make_dow_bar():
        fig = go.Figure(go.Bar(
            x=dow_avg.index,
            y=dow_avg.values,
            marker=dict(
                color=dow_avg.values,
                colorscale=[[0, BORDER], [1, PURPLE]],
                showscale=False
            ),
            text=[f'₹{v:,.0f}' for v in dow_avg.values],
            textposition='outside',
            textfont=dict(size=10, color=MUTED),
            hovertemplate='<b>%{x}</b><br>Avg spend: ₹%{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            **PAPER_STYLE,
            xaxis=axis_style(),
            yaxis=axis_style('Avg spend (₹)'),
            margin=dict(l=50, r=20, t=20, b=40)
        )
        return fig

    # Return all artifacts
    return {
        "kpi_upi_md": upi_kpi_html,
        "kpi_personal_md": personal_kpi_html,
        "upi_growth": make_upi_growth(),
        "market_share": make_market_share(),
        "top10_bar": make_top10_bar(),
        "top5_monthly": make_top5_monthly(),
        "monthly_spend": make_monthly_spend(),
        "category_donut": make_category_donut(),
        "daily_heatmap": make_daily_heatmap(),
        "dow_bar": make_dow_bar(),
        "recommendations_md": recommendations_md,
        "year_options": year_options,
        "yearly_summary": yearly_md,

    }

# ── Gradio UI ────────────────────────────────────────────────────────────────

# Load custom CSS from the assets folder
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
custom_css = ''
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        custom_css = f.read()

with gr.Blocks(css=custom_css) as demo:
    # Header with animation
    gr.HTML("""<h1 id='header' style='color:#4a9eff; font-family:\"IBM Plex Sans\",sans-serif; margin-bottom:10px;'>SpendMap — UPI Intelligence Dashboard</h1>""")
    # File uploader & analyse button
    with gr.Row():
        txn_upload = gr.File(label="Upload your personal transaction CSV (optional)", file_types=[".csv"], interactive=True)
        analyse_btn = gr.Button("Analyse")
    # KPI boxes (hidden until analysis)
    kpi_upi_md = gr.Markdown(visible=False)
    kpi_personal_md = gr.Markdown(visible=False)
    # Yearly spending dropdown and summary (hidden until analysis)
    year_dropdown = gr.Dropdown(label="Select Year", choices=[], visible=False)
    year_state = gr.State()
    year_summary_md = gr.Markdown(visible=False)
    # Tabs with accordions for progressive reveal
    with gr.Tabs():
        with gr.TabItem("UPI Overview"):
            # KPI box
            with gr.Accordion("Key Metrics"):
                kpi_upi_md
            # Charts
            with gr.Accordion("Growth & Market Share"):
                upi_growth_plot = gr.Plot()
                market_share_plot = gr.Plot()
            with gr.Accordion("Top 10 & Top 5 Monthly"):
                top10_bar_plot = gr.Plot()
                top5_monthly_plot = gr.Plot()
        with gr.TabItem("Personal Finance"):
            with gr.Accordion("Key Metrics"):
                kpi_personal_md
                with gr.Accordion("Yearly Spending"):
                    year_dropdown
                    year_summary_md
            with gr.Accordion("Monthly Income vs Spending & Category"):
                monthly_spend_plot = gr.Plot()
                category_donut_plot = gr.Plot()
            with gr.Accordion("Heatmap & Day‑of‑Week"):
                daily_heatmap_plot = gr.Plot()
                dow_bar_plot = gr.Plot()
                # Recommendations accordion
                recommendations_md = gr.Markdown(visible=False)

    def run_analysis(txn_file):
        result = generate_dashboard(txn_file)
        # Prepare dropdown update
        dropdown_update = gr.update(choices=result["year_options"], visible=True)
        # Return KPI markdowns, plots, dropdown, state, and an empty summary placeholder
        return (
            gr.update(value=result["kpi_upi_md"], visible=True),
            gr.update(value=result["kpi_personal_md"], visible=True),
            result["upi_growth"],
            result["market_share"],
            result["top10_bar"],
            result["top5_monthly"],
            result["monthly_spend"],
            result["category_donut"],
            result["daily_heatmap"],
            result["dow_bar"],
            # Recommendations markdown
            gr.update(value=result["recommendations_md"], visible=True),
            dropdown_update,
            result["yearly_summary"],
            gr.update(value="", visible=False)
        )



    def update_year_summary(selected_year, yearly_dict):
        if not selected_year:
            return gr.update(value="", visible=False)
        md = yearly_dict.get(selected_year, "")
        return gr.update(value=md, visible=True)

    # Bind button click
    analyse_btn.click(fn=run_analysis, inputs=txn_upload,
                      outputs=[kpi_upi_md, kpi_personal_md,
                               upi_growth_plot, market_share_plot,
                               top10_bar_plot, top5_monthly_plot,
                               monthly_spend_plot, category_donut_plot,
                               daily_heatmap_plot, dow_bar_plot,
                               recommendations_md,
                               year_dropdown, year_state, year_summary_md])

    # Bind year dropdown change
    year_dropdown.change(fn=update_year_summary, inputs=[year_dropdown, year_state], outputs=year_summary_md)



if __name__ == "__main__":
    demo.launch()
