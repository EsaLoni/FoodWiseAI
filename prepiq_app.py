import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

APP = "PrepIQ"
TAG = "Smart demand forecasting for low-waste kitchens"
GREEN, LEAF, ORANGE, RED, CREAM = "#0E3B2E", "#2E9E5B", "#F28C28", "#D1495B", "#FBF7F0"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

LOGO = """<svg width="{s}" height="{s}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2E9E5B"/>
<stop offset="1" stop-color="#0E3B2E"/></linearGradient></defs>
<rect width="64" height="64" rx="16" fill="url(#g)"/>
<circle cx="32" cy="30" r="17" fill="#FBF7F0"/><circle cx="32" cy="30" r="11" fill="none" stroke="#0E3B2E" stroke-width="2" opacity=".35"/>
<path d="M18 33 L26 33 L29 25 L34 38 L38 29 L46 29" fill="none" stroke="#F28C28" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M14 51 H50" stroke="#FBF7F0" stroke-width="3" stroke-linecap="round" opacity=".85"/></svg>"""


def logo(s=56):
    return LOGO.format(s=s)


st.set_page_config(page_title=f"{APP} | Demand Intelligence", page_icon="🍽️", layout="wide")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] {{font-family:'Inter',sans-serif;}}
h1,h2,h3,.hero-t,.kv,.brand {{font-family:'Poppins',sans-serif !important;}}
.block-container {{padding-top:1.4rem;max-width:1250px;}}
.hero {{display:flex;gap:22px;align-items:center;padding:26px 30px;border-radius:22px;margin-bottom:20px;
 background:linear-gradient(120deg,{GREEN} 0%,#1B5E43 65%,{LEAF} 130%);color:#fff;}}
.hero-t {{font-size:36px;font-weight:800;margin:0;line-height:1.1;color:#fff;}}
.hero-s {{color:#D6EBDD;font-size:16px;margin-top:6px;max-width:680px;}}
.pill {{display:inline-block;background:rgba(255,255,255,.14);border-radius:999px;padding:4px 12px;font-size:13px;margin:10px 8px 0 0;}}
.kpi {{background:{CREAM};border:1px solid #E7DFD0;border-radius:14px;padding:14px 16px;}}
.kv {{font-size:26px;font-weight:700;color:{GREEN};}} .kl {{font-size:13px;color:#6B6B5E;}}
.note {{background:#FFF4E5;border-left:4px solid {ORANGE};padding:10px 14px;border-radius:8px;font-size:14px;margin:8px 0;}}
.rec {{background:linear-gradient(120deg,{LEAF},{GREEN});color:#fff;border-radius:18px;padding:22px 26px;}}
.rec .big {{font-family:'Poppins',sans-serif;font-size:40px;font-weight:800;margin:0;}}
[data-testid="stSidebar"] {{background:#F3F0E8;}}
.brand {{font-size:22px;font-weight:800;color:{GREEN};margin:0;}} .tag {{font-size:12.5px;color:#6B6B5E;margin:0;}}
</style>""", unsafe_allow_html=True)


def kpi(col, value, label):
    col.markdown(f'<div class="kpi"><div class="kv">{value}</div><div class="kl">{label}</div></div>',
                 unsafe_allow_html=True)


def style(fig, h=380):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", font=dict(family="Inter"), title_font=dict(family="Poppins", size=16))
    return fig


# ============================================================
# DATA
# ============================================================
FILES = dict(data="foodwise_model_data.csv", eval="forecast_evaluation.csv",
             menu="menu_performance.csv", err="high_demand_error_analysis.csv")


def find(name):
    for folder in (".", "data"):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            return p
    return None


missing = [f for f in FILES.values() if find(f) is None]
if missing:
    st.markdown(f'<div class="hero"><div>{logo(70)}</div><div><p class="hero-t">{APP}</p>'
                f'<div class="hero-s">{TAG}</div></div></div>', unsafe_allow_html=True)
    st.error("Missing data files: " + ", ".join(f"`{m}`" for m in missing) +
             ". Run the notebook's save cells and place the files next to this app (or in a `data/` folder).")
    st.stop()


@st.cache_data(show_spinner="Loading sales history...")
def load_data():
    cols = ["date", "restaurant_id", "restaurant_name", "city", "state", "menu_item_id", "menu_item_name",
            "category", "unit_price", "quantity", "day_of_week", "month", "year", "avg_temp_f",
            "precip_inches", "is_weekend", "is_holiday", "is_promotion"]
    df = pd.read_csv(find(FILES["data"]), usecols=cols, parse_dates=["date"])
    for c in ["restaurant_id", "restaurant_name", "city", "state", "menu_item_id", "menu_item_name",
              "category", "day_of_week"]:
        df[c] = df[c].astype("category")
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


@st.cache_data
def load_other():
    return (pd.read_csv(find(FILES["eval"])), pd.read_csv(find(FILES["menu"])),
            pd.read_csv(find(FILES["err"])))


df_all = load_data()
evaluation, menu_perf, err = load_other()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f'<div style="display:flex;gap:12px;align-items:center;">{logo(46)}<div>'
                f'<p class="brand">{APP}</p><p class="tag">{TAG}</p></div></div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Filters")
    y0, y1 = int(df_all["year"].min()), int(df_all["year"].max())
    years = st.slider("Years", y0, y1, (y0, y1))
    rest_names = sorted(df_all["restaurant_name"].unique())
    rests = st.multiselect("Restaurants", rest_names, placeholder="All restaurants")
    cats = st.multiselect("Menu categories", sorted(df_all["category"].unique()), placeholder="All categories")
    st.caption("Filters apply to the Overview and Demand Drivers tabs.")

df = df_all[df_all["year"].between(*years)]
if rests:
    df = df[df["restaurant_name"].isin(rests)]
if cats:
    df = df[df["category"].isin(cats)]

# ============================================================
# HERO
# ============================================================
st.markdown(f"""<div class="hero"><div>{logo(88)}</div><div>
<p class="hero-t">{APP}</p>
<div class="hero-s">Forecast item-level demand, spot high-demand days before they happen, and plan food prep
with less guesswork and less waste.</div>
<span class="pill">{len(df_all):,} sales records</span><span class="pill">{df_all["restaurant_id"].nunique()} restaurants</span>
<span class="pill">{df_all["menu_item_id"].nunique()} menu items</span><span class="pill">{y0}-{y1}</span></div></div>""",
            unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.tabs(["Overview", "Demand Drivers", "Forecast Accuracy", "High-Demand Alerts", "Prep Planner"])

# ============================================================
# 1. OVERVIEW
# ============================================================
with t1:
    if df.empty:
        st.warning("No data for the selected filters.")
    else:
        c = st.columns(5)
        kpi(c[0], f"{df['quantity'].sum():,.0f}", "Units sold")
        kpi(c[1], f"${df['revenue'].sum():,.0f}", "Estimated revenue")
        kpi(c[2], f"{df['quantity'].mean():.1f}", "Avg units per item-day")
        promo = df.groupby("is_promotion", observed=True)["quantity"].mean()
        up = (promo.get(1, np.nan) / promo.get(0, np.nan) - 1) * 100
        kpi(c[3], f"{up:+.1f}%" if pd.notna(up) else "n/a", "Promotion uplift")
        wk = df.groupby("is_weekend", observed=True)["quantity"].mean()
        wu = (wk.get(1, np.nan) / wk.get(0, np.nan) - 1) * 100
        kpi(c[4], f"{wu:+.1f}%" if pd.notna(wu) else "n/a", "Weekend uplift")
        st.write("")

        a, b = st.columns(2)
        m = df.groupby(["year", "month"], observed=True)["quantity"].mean().reset_index()
        m["Month"] = m["month"].map(lambda x: MONTHS[int(x) - 1])
        fig = px.line(m, x="Month", y="quantity", color="year", markers=True,
                      category_orders={"Month": MONTHS}, title="Average demand by month",
                      color_discrete_sequence=px.colors.sequential.Greens[2:])
        a.plotly_chart(style(fig), use_container_width=True)

        d = df.groupby("day_of_week", observed=True)["quantity"].mean().reindex(DAYS).reset_index()
        fig = px.bar(d, x="day_of_week", y="quantity", title="Average demand by weekday",
                     color="quantity", color_continuous_scale=["#BFE3CD", GREEN])
        fig.update_layout(coloraxis_showscale=False, xaxis_title=None)
        b.plotly_chart(style(fig), use_container_width=True)

        a, b = st.columns(2)
        cat = df.groupby("category", observed=True)["quantity"].sum().sort_values().reset_index()
        fig = px.bar(cat, x="quantity", y="category", orientation="h", title="Total units by category",
                     color_discrete_sequence=[LEAF])
        a.plotly_chart(style(fig), use_container_width=True)
        top = (df.groupby(["menu_item_id", "menu_item_name"], observed=True)["quantity"].sum()
               .nlargest(10).sort_values().reset_index())
        top["item"] = top["menu_item_id"].astype(str) + " " + top["menu_item_name"].astype(str)
        fig = px.bar(top, x="quantity", y="item", orientation="h", title="Top 10 items by units",
                     color_discrete_sequence=[ORANGE])
        b.plotly_chart(style(fig), use_container_width=True)

        summary = (df.groupby(["restaurant_name", "category"], observed=True)
                   .agg(units=("quantity", "sum"), revenue=("revenue", "sum"), avg_units=("quantity", "mean"))
                   .round(2).reset_index())
        st.download_button("Download filtered summary (CSV)", summary.to_csv(index=False),
                           "prepiq_summary.csv")

# ============================================================
# 2. DEMAND DRIVERS
# ============================================================
with t2:
    st.markdown('<div class="note">These charts show <b>association</b>, not proven cause and effect. '
                'Restaurant, item mix and season also influence demand.</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("No data for the selected filters.")
    else:
        base = df["quantity"].mean()
        rows = []
        for col, label in [("is_promotion", "Promotion"), ("is_holiday", "Holiday"), ("is_weekend", "Weekend")]:
            g = df.groupby(col, observed=True)["quantity"].mean()
            if 0 in g.index and 1 in g.index:
                rows.append((label, (g[1] / g[0] - 1) * 100))
        if rows:
            up = pd.DataFrame(rows, columns=["Factor", "Uplift %"])
            fig = px.bar(up, x="Factor", y="Uplift %", text=up["Uplift %"].map(lambda v: f"{v:+.1f}%"),
                         title="Average demand uplift vs. normal days", color_discrete_sequence=[LEAF])
            st.plotly_chart(style(fig, 330), use_container_width=True)

        a, b = st.columns(2)
        tmp = df.assign(temp=pd.cut(df["avg_temp_f"], [0, 20, 40, 60, 70, 85, 130],
                                    labels=["<20F", "20-40F", "40-60F", "60-70F", "70-85F", "85F+"], include_lowest=True))
        t = tmp.groupby("temp", observed=True)["quantity"].mean().reset_index()
        a.plotly_chart(style(px.bar(t, x="temp", y="quantity", title="Demand by temperature band",
                                    color_discrete_sequence=[ORANGE])), use_container_width=True)
        rn = df.assign(rain=pd.cut(df["precip_inches"], [-0.01, 0, 0.1, 0.5, 1, np.inf],
                                   labels=["None", "Light", "Moderate", "Heavy", "Very heavy"]))
        r = rn.groupby("rain", observed=True)["quantity"].mean().reset_index()
        b.plotly_chart(style(px.bar(r, x="rain", y="quantity", title="Demand by rainfall level",
                                    color_discrete_sequence=["#3A86C8"])), use_container_width=True)

        heat = df.pivot_table(index="day_of_week", columns="month", values="quantity", aggfunc="mean",
                              observed=True).reindex(DAYS)
        heat.columns = [MONTHS[int(m) - 1] for m in heat.columns]
        fig = px.imshow(heat, aspect="auto", color_continuous_scale="YlGn", title="Average demand: weekday x month")
        st.plotly_chart(style(fig, 360), use_container_width=True)

# ============================================================
# 3. FORECAST ACCURACY
# ============================================================
with t3:
    st.subheader("Model comparison (2025 hold-out)")
    st.caption("Models were trained on 2021-2024 and tested on 2025. Values are from your notebook run.")
    comp = pd.DataFrame({"Model": ["Decision Tree (baseline)", "Gradient Boosting"],
                         "MAE": [4.63, 4.19], "RMSE": [9.00, 8.50], "R2": [0.750, 0.776]})
    c = st.columns(3)
    kpi(c[0], "4.19", "Gradient Boosting MAE (units)")
    kpi(c[1], "8.50", "Gradient Boosting RMSE (units)")
    kpi(c[2], "0.776", "Gradient Boosting R2")
    st.write("")
    a, b = st.columns([2, 3])
    a.dataframe(comp, hide_index=True, use_container_width=True)
    mf = comp.melt("Model", ["MAE", "RMSE"], var_name="Metric", value_name="Value")
    b.plotly_chart(style(px.bar(mf, x="Metric", y="Value", color="Model", barmode="group",
                                color_discrete_sequence=["#9DB8A8", GREEN], title="Error (lower is better)"), 300),
                   use_container_width=True)

    a, b = st.columns(2)
    smp = evaluation.sample(min(5000, len(evaluation)), random_state=42)
    lim = float(np.percentile(smp["actual_quantity"], 99))
    fig = px.scatter(smp, x="actual_quantity", y="predicted_quantity", opacity=.3,
                     title="Actual vs predicted (5,000-row sample)", color_discrete_sequence=[LEAF])
    fig.add_shape(type="line", x0=0, y0=0, x1=lim, y1=lim, line=dict(color=RED, dash="dash"))
    fig.update_xaxes(range=[0, lim]); fig.update_yaxes(range=[0, lim])
    a.plotly_chart(style(fig), use_container_width=True)
    fig = px.histogram(evaluation[evaluation["error"].between(-40, 40)], x="error", nbins=60,
                       title="Forecast error distribution (actual - predicted)", color_discrete_sequence=[ORANGE])
    b.plotly_chart(style(fig), use_container_width=True)

    st.subheader("Accuracy by menu item")
    st.caption("WAPE = total absolute error / total actual units. Under 10% is low, 10-20% moderate, above 20% high.")
    cnt = menu_perf["forecast_status"].value_counts().reset_index()
    cnt.columns = ["Status", "Items"]
    a, b = st.columns([2, 3])
    fig = px.pie(cnt, names="Status", values="Items", hole=.55, title="Items by forecast status",
                 color="Status", color_discrete_map={"Low Error": LEAF, "Moderate Error": ORANGE, "High Error": RED})
    a.plotly_chart(style(fig, 320), use_container_width=True)
    show = menu_perf[["menu_item_id", "actual_avg", "predicted_avg", "MAE", "WAPE_percent", "forecast_status"]]
    b.dataframe(show.sort_values("WAPE_percent", ascending=False).round(2), hide_index=True,
                use_container_width=True, height=320)

# ============================================================
# 4. HIGH-DEMAND ALERTS
# ============================================================
with t4:
    st.subheader("High-demand alert system")
    st.caption("A record counts as high demand when more than 100 units are sold. Move the threshold to trade "
               "false alarms against missed events.")
    prob = err["predicted_probability"].to_numpy()
    act = err["actual_high_demand"].to_numpy().astype(bool)
    thr = st.slider("Alert threshold (probability)", 0.10, 0.99, 0.90, 0.01,
                    help="Your notebook's final model used 0.90.")


    def stats(t):
        p = prob >= t
        tp, fp, fn = int((p & act).sum()), int((p & ~act).sum()), int((~p & act).sum())
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        return tp, fp, fn, pr, rc, (2 * pr * rc / (pr + rc) if pr + rc else 0.0)


    tp, fp, fn, pr, rc, f1 = stats(thr)
    c = st.columns(5)
    kpi(c[0], f"{pr:.1%}", "Precision (alerts that were real)")
    kpi(c[1], f"{rc:.1%}", "Recall (real events caught)")
    kpi(c[2], f"{f1:.3f}", "F1 score")
    kpi(c[3], f"{tp + fp:,}", "Alerts raised")
    kpi(c[4], f"{fn:,}", "Missed events")
    st.write("")

    a, b = st.columns(2)
    cm = pd.DataFrame([[int((~(prob >= thr) & ~act).sum()), fp], [fn, tp]],
                      index=["Actual normal", "Actual high"], columns=["Predicted normal", "Predicted high"])
    a.plotly_chart(style(px.imshow(cm, text_auto=",", color_continuous_scale="Greens",
                                   title="Confusion matrix"), 330), use_container_width=True)
    ts = np.round(np.arange(0.1, 1.0, 0.05), 2)
    curve = pd.DataFrame([(t, *stats(t)[3:5]) for t in ts], columns=["Threshold", "Precision", "Recall"])
    fig = go.Figure()
    fig.add_scatter(x=curve["Threshold"], y=curve["Precision"], name="Precision", line=dict(color=ORANGE, width=3))
    fig.add_scatter(x=curve["Threshold"], y=curve["Recall"], name="Recall", line=dict(color=GREEN, width=3))
    fig.add_vline(x=thr, line_dash="dash", line_color="#888")
    fig.update_layout(title="Precision and recall by threshold")
    b.plotly_chart(style(fig, 330), use_container_width=True)

    work = err.assign(pred=(prob >= thr))
    work["outcome"] = np.select([work.pred & work.actual_high_demand.astype(bool),
                                 work.pred & ~work.actual_high_demand.astype(bool),
                                 ~work.pred & work.actual_high_demand.astype(bool)],
                                ["Correct alert", "False alarm", "Missed event"], "Normal")
    g = st.radio("Break down by", ["menu_item_id", "restaurant_id"], horizontal=True,
                 format_func=lambda x: "Menu item" if x == "menu_item_id" else "Restaurant")
    br = (work[work.outcome != "Normal"].groupby([g, "outcome"]).size().unstack(fill_value=0)
          .assign(total=lambda d: d.sum(axis=1)).nlargest(12, "total").drop(columns="total").reset_index())
    fig = px.bar(br, x=g, y=[c for c in ["Correct alert", "False alarm", "Missed event"] if c in br],
                 barmode="stack", title="Where alerts succeed and fail (top 12)",
                 color_discrete_map={"Correct alert": LEAF, "False alarm": ORANGE, "Missed event": RED})
    fig.update_layout(legend_title=None, yaxis_title="Records")
    st.plotly_chart(style(fig, 340), use_container_width=True)

    st.markdown("**Largest missed events at this threshold**")
    st.dataframe(work[work.outcome == "Missed event"].nlargest(15, "quantity")
                 [["date", "restaurant_id", "menu_item_id", "quantity", "predicted_probability"]]
                 .round(3), hide_index=True, use_container_width=True)
    st.markdown('<div class="note">The model flags high demand, not waste. Measuring waste reduction needs '
                'prepared quantities and discarded-food data.</div>', unsafe_allow_html=True)

# ============================================================
# 5. PREP PLANNER
# ============================================================
with t5:
    st.subheader("Prep planner")
    st.markdown('<div class="note">This planner uses <b>historical averages</b> for the chosen restaurant, item and '
                'weekday, adjusted by that item\'s own promotion and holiday uplift. It does not call the trained '
                'model.</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    rn_ = c1.selectbox("Restaurant", rest_names)
    items = (df_all[df_all["restaurant_name"] == rn_][["menu_item_id", "menu_item_name"]].drop_duplicates()
             .assign(label=lambda d: d["menu_item_id"].astype(str) + " - " + d["menu_item_name"].astype(str))
             .sort_values("label"))
    item_label = c2.selectbox("Menu item", items["label"])
    day = c3.selectbox("Day", DAYS, index=4)
    d1, d2, d3 = st.columns(3)
    promo_on = d1.toggle("Promotion running")
    hol_on = d2.toggle("Public holiday")
    buffer = d3.slider("Safety buffer", 0, 30, 10, format="%d%%")

    item_id = item_label.split(" - ")[0]
    sub = df_all[(df_all["restaurant_name"] == rn_) & (df_all["menu_item_id"] == item_id)]
    recent = sub[sub["year"] >= sub["year"].max() - 1]
    base = recent[(recent["day_of_week"] == day) & (recent["is_promotion"] == 0) & (recent["is_holiday"] == 0)]["quantity"]
    if len(base) < 5:
        st.warning("Not enough history for this combination.")
    else:
        def lift(col):
            g = recent.groupby(col, observed=True)["quantity"].agg(["mean", "size"])
            return g.loc[1, "mean"] / g.loc[0, "mean"] if {0, 1} <= set(g.index) and g.loc[1, "size"] >= 5 else 1.0


        exp = base.mean() * (lift("is_promotion") if promo_on else 1) * (lift("is_holiday") if hol_on else 1)
        rec = exp * (1 + buffer / 100)
        hi = base.quantile(.9) * exp / base.mean()
        a, b = st.columns([2, 3])
        a.markdown(f'<div class="rec"><div style="opacity:.85">Recommended prep quantity</div>'
                   f'<p class="big">{rec:,.0f} units</p><div style="opacity:.9">Expected {exp:,.0f} + {buffer}% buffer. '
                   f'Busy-day (90th percentile) level: about {hi:,.0f}.</div></div>', unsafe_allow_html=True)
        wd = (recent[(recent["is_promotion"] == 0) & (recent["is_holiday"] == 0)]
              .groupby("day_of_week", observed=True)["quantity"].mean().reindex(DAYS).reset_index())
        wd["sel"] = np.where(wd["day_of_week"] == day, "Selected", "Other")
        fig = px.bar(wd, x="day_of_week", y="quantity", color="sel", title="Typical demand by weekday (this item)",
                     color_discrete_map={"Selected": ORANGE, "Other": "#BFE3CD"})
        fig.update_layout(showlegend=False, xaxis_title=None)
        b.plotly_chart(style(fig, 300), use_container_width=True)

st.divider()
st.caption(f"{APP} | {TAG} | Built from the FoodWise AI analysis notebook")
