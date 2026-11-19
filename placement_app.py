import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from datetime import datetime, date
import json

# ──────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Placement Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Navy/Charcoal Theme with Custom CSS
st.markdown("""
<style>
/* ────────────────── ROOT VARIABLES ────────────────── */
:root {
    --bg-primary: #0a0f1a;
    --bg-secondary: #111827;
    --bg-card: #1e293b;
    --bg-card-hover: #253147;
    --bg-input: #0f172a;
    --border-primary: #2d3d56;
    --border-accent: #3b82f6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-violet: #8b5cf6;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.3);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.3);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.3);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ────────────────── GLOBAL RESET ────────────────── */
.stApp {
    background: linear-gradient(135deg, #0a0f1a 0%, #111827 50%, #0f172a 100%);
    color: var(--text-primary);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary);
}

/* ────────────────── SIDEBAR ────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border-right: 1px solid var(--border-primary);
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 4px;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 12px 16px !important;
    border-radius: var(--radius-md) !important;
    transition: var(--transition) !important;
    border: 1px solid transparent !important;
    margin: 2px 8px !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-card) !important;
    border-color: var(--border-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stRadioValueContainer"] > div {
    background: var(--accent-blue) !important;
    color: white !important;
    border-radius: var(--radius-md) !important;
    border: none !important;
    box-shadow: var(--shadow-md) !important;
}

/* ────────────────── TYPOGRAPHY ────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

h1 { font-size: 1.75rem !important; }
h2 { font-size: 1.375rem !important; }
h3 { font-size: 1.125rem !important; }

.stMarkdown, .stText, p {
    color: var(--text-secondary) !important;
}

/* ────────────────── METRIC CARDS ────────────────── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px 24px !important;
    box-shadow: var(--shadow-md) !important;
    transition: var(--transition) !important;
}

[data-testid="metric-container"]:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-lg) !important;
    transform: translateY(-2px) !important;
}

[data-testid="metric-container"] > div:first-child {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="metric-container"] > div:last-child {
    color: var(--text-primary) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ────────────────── BUTTONS ────────────────── */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--accent-blue) 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary button style */
.stButton > button[kind="secondary"] {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-primary) !important;
    color: var(--text-secondary) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--bg-card) !important;
    border-color: var(--border-accent) !important;
    color: var(--text-primary) !important;
}

/* ────────────────── INPUTS ────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
    font-size: 0.875rem !important;
    transition: var(--transition) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ────────────────── DATAFRAME / TABLES ────────────────── */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-md) !important;
}

[data-testid="stDataFrame"] table {
    color: var(--text-primary) !important;
}

[data-testid="stDataFrame"] th {
    background: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid var(--border-primary) !important;
}

[data-testid="stDataFrame"] td {
    padding: 12px 16px !important;
    border-bottom: 1px solid var(--border-primary) !important;
    font-size: 0.875rem !important;
}

[data-testid="stDataFrame"] tr:hover td {
    background: var(--bg-card-hover) !important;
}

/* ────────────────── TABS ────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: var(--bg-secondary) !important;
    padding: 4px !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-primary) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 20px !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    transition: var(--transition) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: var(--bg-card) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent-blue) !important;
    color: white !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ────────────────── EXPANDER ────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.streamlit-expanderContent {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-primary) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

/* ────────────────── FORM ────────────────── */
.stForm {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: var(--radius-lg) !important;
    padding: 24px !important;
    box-shadow: var(--shadow-md) !important;
}

.stForm > div {
    gap: 16px !important;
}

/* ────────────────── ALERTS ────────────────── */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
    box-shadow: var(--shadow-md) !important;
}

.stAlert[data-baseweb="notification"][kind="success"] {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
    border-left: 4px solid var(--accent-emerald) !important;
    color: var(--accent-emerald) !important;
}

.stAlert[data-baseweb="notification"][kind="error"] {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.15) 0%, rgba(244, 63, 94, 0.05) 100%) !important;
    border-left: 4px solid var(--accent-rose) !important;
    color: var(--accent-rose) !important;
}

.stAlert[data-baseweb="notification"][kind="warning"] {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
    border-left: 4px solid var(--accent-amber) !important;
    color: var(--accent-amber) !important;
}

.stAlert[data-baseweb="notification"][kind="info"] {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%) !important;
    border-left: 4px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
}

/* ────────────────── CUSTOM KPI CARDS ────────────────── */
.kpi-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent-color);
}

.kpi-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 4px;
}

.kpi-delta {
    font-size: 0.75rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* ────────────────── DIVIDERS ────────────────── */
hr, .stDivider {
    border-color: var(--border-primary) !important;
    opacity: 0.5 !important;
}

/* ────────────────── SCROLLBAR ────────────────── */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--border-accent);
}

/* ────────────────── RESPONSIVE ────────────────── */
@media (max-width: 768px) {
    .kpi-value { font-size: 1.75rem !important; }
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATABASE CONNECTION
# ──────────────────────────────────────────────
@st.cache_resource
def get_engine():
    db = st.secrets["mysql"]

    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=db["user"],
        password=db["password"],
        host=db["host"],
        port=int(db["port"]),
        database=db["database"]
    )

    return create_engine(url, pool_pre_ping=True, pool_recycle=3600)

def fetch_data(engine, query: str, params: dict = None) -> pd.DataFrame:
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(query), conn, params=params or {})
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()


def execute_write(engine, query: str, params: dict) -> bool:
    try:
        with engine.begin() as conn:
            conn.execute(text(query), params)
        return True
    except Exception as e:
        st.error(f"Write operation failed: {e}")
        return False


def call_procedure(engine, proc_name: str, args: list) -> tuple:
    """Call a stored procedure and return (success, message, output)"""
    try:
        with engine.begin() as conn:
            # Build CALL statement with placeholders
            placeholders = ', '.join([f'@{proc_name}_arg_{i}' for i in range(len(args))])
            call_stmt = f"CALL {proc_name}({placeholders})"

            # Set user variables
            for i, arg in enumerate(args):
                if isinstance(arg, str):
                    conn.execute(text(f"SET @{proc_name}_arg_{i} = :val"), {"val": arg})
                elif arg is None:
                    conn.execute(text(f"SET @{proc_name}_arg_{i} = NULL"))
                else:
                    conn.execute(text(f"SET @{proc_name}_arg_{i} = :val"), {"val": arg})

            # Execute the call
            conn.execute(text(call_stmt))

            # Try to get OUT parameters (for procedures with OUT params)
            # This is MySQL specific - OUT params are returned as result sets or user vars
            return True, "Procedure executed successfully", None
    except Exception as e:
        return False, str(e), None


def call_function(engine, func_name: str, args: list) -> any:
    """Call a stored function and return the result"""
    try:
        with engine.connect() as conn:
            placeholders = ', '.join([f':arg{i}' for i in range(len(args))])
            query = f"SELECT {func_name}({placeholders}) as result"
            params = {f'arg{i}': arg for i, arg in enumerate(args)}
            result = conn.execute(text(query), params).scalar()
            return result
    except Exception as e:
        st.error(f"Function call failed: {e}")
        return None

# ──────────────────────────────────────────────
# SIDEBAR - CONNECTION & NAVIGATION
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 24px 16px 16px; text-align: center; border-bottom: 1px solid var(--border-primary); margin-bottom: 16px;">
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">
            Placement<span style="color: var(--accent-blue);">Hub</span>
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px;">
            Enterprise Management
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("✅ Cloud MySQL Connected", icon="✅")
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

    st.divider()

    # Navigation
    NAV_SECTIONS = [
        ("📊", "Dashboard"),
        ("👨‍🎓", "Students"),
        ("🏫", "Departments"),
        ("🏢", "Companies"),
        ("👔", "Recruiters"),
        ("💼", "Job Postings"),
        ("📝", "Applications"),
        ("🎤", "Interviews"),
        ("🤝", "Offers"),
        ("✅", "Placements"),
        ("🛠️", "Skills"),
        ("💻", "SQL Console"),
    ]

    nav_labels = [f"{icon}  {label}" for icon, label in NAV_SECTIONS]
    nav_keys = [label for _, label in NAV_SECTIONS]

    selected_idx = st.radio(
        "Navigation",
        options=range(len(nav_labels)),
        format_func=lambda i: nav_labels[i],
        key="nav_radio",
        label_visibility="collapsed"
    )

    section = nav_keys[selected_idx]

    st.divider()

    # Quick stats in sidebar
    st.markdown("### Quick Stats")
    try:
        for table, label in [("STUDENT", "Students"), ("COMPANY", "Companies"), ("JOB", "Jobs"), ("PLACEMENT", "Placements")]:
            count = fetch_data(engine, f"SELECT COUNT(*) as c FROM `{table}`").iloc[0]['c']
            st.markdown(f"""
            <div style="padding: 8px 12px; background: var(--bg-card); border: 1px solid var(--border-primary); border-radius: var(--radius-md); margin: 4px 0;">
                <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">{label}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary);">{count:,}</div>
            </div>
            """, unsafe_allow_html=True)
    except:
        pass

# ──────────────────────────────────────────────
# HELPER: RENDER KPI CARD
# ──────────────────────────────────────────────
def render_kpi_card(label: str, value: str, delta: str = None, accent: str = "#3b82f6", delta_color: str = None):
    delta_html = ""
    if delta:
        color = delta_color or ("var(--accent-emerald)" if not delta.startswith("-") else "var(--accent-rose)")
        delta_html = f'<div class="kpi-delta" style="color: {color};">{delta}</div>'

    st.markdown(f"""
    <div class="kpi-card" style="--accent-color: {accent};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECTION: DASHBOARD
# ──────────────────────────────────────────────
if section == "Dashboard":
    st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)
    st.caption("Enterprise Placement & Recruitment Management System — Real-time Analytics")

    # ───── KPI ROW ─────
    try:
        total_students = fetch_data(engine, "SELECT COUNT(*) as c FROM `STUDENT`").iloc[0]['c']
        total_companies = fetch_data(engine, "SELECT COUNT(*) as c FROM `COMPANY`").iloc[0]['c']
        total_jobs = fetch_data(engine, "SELECT COUNT(*) as c FROM `JOB`").iloc[0]['c']
        total_placements = fetch_data(engine, "SELECT COUNT(*) as c FROM `PLACEMENT`").iloc[0]['c']
        placement_pct = (total_placements / total_students * 100) if total_students > 0 else 0
        total_applications = fetch_data(engine, "SELECT COUNT(*) as c FROM `APPLICATION`").iloc[0]['c']
    except Exception as e:
        st.error(f"Failed to load dashboard metrics: {e}")
        total_students = total_companies = total_jobs = total_placements = placement_pct = total_applications = 0

    kpi_cols = st.columns(5)
    with kpi_cols[0]:
        render_kpi_card("Total Students", f"{total_students:,}", accent="#3b82f6")
    with kpi_cols[1]:
        render_kpi_card("Companies", f"{total_companies:,}", accent="#06b6d4")
    with kpi_cols[2]:
        render_kpi_card("Active Jobs", f"{total_jobs:,}", accent="#8b5cf6")
    with kpi_cols[3]:
        render_kpi_card("Placements", f"{total_placements:,}", f"{placement_pct:.1f}%", accent="#10b981", delta_color="#10b981")
    with kpi_cols[4]:
        render_kpi_card("Applications", f"{total_applications:,}", accent="#f59e0b")

    st.divider()

    # ───── CHARTS ROW ─────
    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        st.markdown("### Application Status Distribution")
        try:
            status_df = fetch_data(engine, """
                SELECT status, COUNT(*) as total
                FROM APPLICATION
                GROUP BY status
                ORDER BY total DESC
            """)
            if not status_df.empty:
                fig = px.pie(
                    status_df, values='total', names='status',
                    hole=0.55,
                    color_discrete_sequence=['#3b82f6', '#06b6d4', '#8b5cf6', '#10b981', '#f59e0b', '#f43f5e', '#64748b']
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#f1f5f9',
                    font_size=12,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=10, b=10, l=10, r=10),
                )
                fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No application data available")
        except Exception as e:
            st.error(f"Chart error: {e}")

    with chart_col2:
        st.markdown("### Department Placement %")
        try:
            dept_df = fetch_data(engine, """
                SELECT d.department_name,
                       COUNT(DISTINCT s.student_id) as total_students,
                       COUNT(DISTINCT p.student_id) as placed_students
                FROM DEPARTMENT d
                LEFT JOIN STUDENT s ON d.department_id = s.department_id
                LEFT JOIN PLACEMENT p ON s.student_id = p.student_id
                GROUP BY d.department_id, d.department_name
                ORDER BY placed_students DESC
            """)
            if not dept_df.empty:
                dept_df['placement_pct'] = (dept_df['placed_students'] / dept_df['total_students'] * 100).round(1)
                fig = px.bar(
                    dept_df, x='placement_pct', y='department_name',
                    orientation='h',
                    color='placement_pct',
                    color_continuous_scale=['#1e3a8a', '#3b82f6', '#06b6d4', '#10b981'],
                    text='placement_pct'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#f1f5f9',
                    font_size=11,
                    showlegend=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    xaxis=dict(title="Placement %", gridcolor='#2d3d56'),
                    yaxis=dict(title="", gridcolor='#2d3d56'),
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=10)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No department data")
        except Exception as e:
            st.error(f"Chart error: {e}")

    # ───── SALARY ANALYTICS ─────
    st.markdown("### Salary Analytics")
    sal_col1, sal_col2, sal_col3 = st.columns(3)
    try:
        avg_salary = fetch_data(engine, """
            SELECT ROUND(AVG(o.offered_salary), 2) as avg_sal
            FROM OFFER o
            WHERE o.status = 'Accepted'
        """).iloc[0]['avg_sal'] or 0
        max_salary = fetch_data(engine, """
            SELECT MAX(o.offered_salary) as max_sal
            FROM OFFER o
            WHERE o.status = 'Accepted'
        """).iloc[0]['max_sal'] or 0
        min_salary = fetch_data(engine, """
            SELECT MIN(o.offered_salary) as min_sal
            FROM OFFER o
            WHERE o.status = 'Accepted'
        """).iloc[0]['min_sal'] or 0

        with sal_col1:
            render_kpi_card("Avg Package", f"₹{avg_salary:,.0f}", accent="#3b82f6")
        with sal_col2:
            render_kpi_card("Highest", f"₹{max_salary:,.0f}", accent="#8b5cf6")
        with sal_col3:
            render_kpi_card("Lowest", f"₹{min_salary:,.0f}", accent="#f59e0b")
    except:
        pass

    # ───── RECENT ACTIVITY ─────
    recent_col1, recent_col2 = st.columns(2)
    with recent_col1:
        st.markdown("### Recent Applications")
        try:
            recent_apps = fetch_data(engine, """
                SELECT a.application_id, s.student_name, j.job_title, c.company_name, a.status, a.application_date
                FROM APPLICATION a
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                ORDER BY a.application_date DESC
                LIMIT 10
            """)
            st.dataframe(recent_apps, use_container_width=True, hide_index=True)
        except:
            st.info("No recent applications")

    with recent_col2:
        st.markdown("### Recent Job Postings")
        try:
            recent_jobs = fetch_data(engine, """
                SELECT j.job_id, j.job_title, c.company_name, j.location, j.salary, j.minimum_cgpa, j.vacancies
                FROM JOB j
                JOIN COMPANY c ON j.company_id = c.company_id
                ORDER BY j.job_id DESC
                LIMIT 10
            """)
            st.dataframe(recent_jobs, use_container_width=True, hide_index=True)
        except:
            st.info("No recent jobs")

# ──────────────────────────────────────────────
# SECTION: STUDENTS
# ──────────────────────────────────────────────
elif section == "Students":
    st.markdown("<h1>Students</h1>", unsafe_allow_html=True)
    st.caption("Manage student records, registrations, and profiles")

    # Fetch departments for dropdown
    try:
        departments = fetch_data(engine, "SELECT department_id, department_name FROM DEPARTMENT ORDER BY department_name")
        dept_map = dict(zip(departments['department_id'], departments['department_name']))
        dept_ids = departments['department_id'].tolist()
    except:
        dept_map = {}
        dept_ids = []

    # ───── TABS ─────
    tab_list, tab_register, tab_update, tab_delete = st.tabs(["📋 All Students", "➕ Register", "✏️ Update", "🗑️ Delete"])

    # ─── TAB 1: LIST ───
    with tab_list:
        st.markdown("### Student Records")
        search = st.text_input("Search", placeholder="Search by name, email, or ID...", key="student_search")

        try:
            students_df = fetch_data(engine, """
                SELECT s.student_id, s.student_name, s.email, s.phone, s.cgpa, s.graduation_year,
                       d.department_name, s.linkedin_profile
                FROM STUDENT s
                JOIN DEPARTMENT d ON s.department_id = d.department_id
                ORDER BY s.student_id
            """)

            filtered = students_df.copy()
            if search.strip():
                term = search.strip().lower()
                mask = (
                    filtered['student_name'].str.lower().str.contains(term, na=False) |
                    filtered['email'].str.lower().str.contains(term, na=False) |
                    filtered['student_id'].astype(str).str.contains(term, na=False)
                )
                filtered = filtered[mask]

            st.markdown(f"**Showing {len(filtered)} of {len(students_df)} students**")
            st.dataframe(filtered, use_container_width=True, hide_index=True)

            # Export button
            csv = filtered.to_csv(index=False)
            st.download_button(
                "📥 Export CSV",
                csv,
                f"students_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Failed to load students: {e}")

    # ─── TAB 2: REGISTER ───
    with tab_register:
        st.markdown("### Register New Student")
        with st.form("register_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="John Doe")
                email = st.text_input("Email Address *", placeholder="john@college.edu")
                phone = st.text_input("Phone Number", placeholder="+91 98765 43210")
            with col2:
                cgpa = st.number_input("CGPA *", min_value=0.0, max_value=10.0, value=8.0, step=0.01, format="%.2f")
                year = st.number_input("Graduation Year *", min_value=2020, max_value=2035, value=2026, step=1)
                dept_id = st.selectbox("Department *", dept_ids, format_func=lambda x: dept_map.get(x, x))

            linkedin = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/username")

            submitted = st.form_submit_button("Register Student", type="primary", use_container_width=True)
            if submitted:
                if not name.strip() or not email.strip():
                    st.error("Name and email are required.")
                elif "@" not in email or "." not in email:
                    st.error("Enter a valid email address.")
                else:
                    success = execute_write(engine, """
                        INSERT INTO STUDENT (student_name, email, phone, cgpa, graduation_year, department_id, linkedin_profile)
                        VALUES (:name, :email, :phone, :cgpa, :year, :dept_id, :linkedin)
                    """, {
                        "name": name.strip(), "email": email.strip(), "phone": phone.strip() or None,
                        "cgpa": cgpa, "year": int(year), "dept_id": dept_id, "linkedin": linkedin.strip() or None
                    })
                    if success:
                        st.success("✅ Student registered successfully!")
                        st.rerun()

    # ─── TAB 3: UPDATE ───
    with tab_update:
        st.markdown("### Update Student")
        try:
            students_df = fetch_data(engine, "SELECT student_id, student_name FROM STUDENT ORDER BY student_id")
            if students_df.empty:
                st.info("No students available.")
            else:
                selected_id = st.selectbox(
                    "Select Student",
                    students_df['student_id'].tolist(),
                    format_func=lambda x: f"{x} - {students_df.loc[students_df.student_id == x, 'student_name'].iloc[0]}",
                    key="update_student_select"
                )

                record = fetch_data(engine, "SELECT * FROM STUDENT WHERE student_id = :id", {"id": selected_id}).iloc[0]

                with st.form("update_student_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name", value=record['student_name'])
                        email = st.text_input("Email", value=record['email'])
                        phone = st.text_input("Phone", value=record['phone'] or "")
                    with col2:
                        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(record['cgpa']), step=0.01, format="%.2f")
                        year = st.number_input("Graduation Year", min_value=2020, max_value=2035, value=int(record['graduation_year']), step=1)
                        dept_id = st.selectbox("Department", dept_ids, index=dept_ids.index(int(record['department_id'])), format_func=lambda x: dept_map.get(x, x))

                    linkedin = st.text_input("LinkedIn Profile", value=record['linkedin_profile'] or "")

                    submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
                    if submitted:
                        if not name.strip() or not email.strip():
                            st.error("Name and email are required.")
                        elif "@" not in email or "." not in email:
                            st.error("Enter a valid email address.")
                        else:
                            success = execute_write(engine, """
                                UPDATE STUDENT SET
                                    student_name = :name, email = :email, phone = :phone,
                                    cgpa = :cgpa, graduation_year = :year,
                                    department_id = :dept_id, linkedin_profile = :linkedin
                                WHERE student_id = :sid
                            """, {
                                "name": name.strip(), "email": email.strip(), "phone": phone.strip() or None,
                                "cgpa": cgpa, "year": int(year), "dept_id": dept_id,
                                "linkedin": linkedin.strip() or None, "sid": selected_id
                            })
                            if success:
                                st.success("✅ Student updated successfully!")
                                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    # ─── TAB 4: DELETE ───
    with tab_delete:
        st.markdown("### Delete Student")
        st.warning("⚠️ Deleting a student is permanent and may be blocked by foreign key constraints.")
        try:
            students_df = fetch_data(engine, "SELECT student_id, student_name FROM STUDENT ORDER BY student_id")
            if students_df.empty:
                st.info("No students available.")
            else:
                selected_id = st.selectbox(
                    "Select Student to Delete",
                    students_df['student_id'].tolist(),
                    format_func=lambda x: f"{x} - {students_df.loc[students_df.student_id == x, 'student_name'].iloc[0]}",
                    key="delete_student_select"
                )
                selected_name = students_df.loc[students_df.student_id == selected_id, 'student_name'].iloc[0]
                st.write(f"Selected: **{selected_name}** (ID: {selected_id})")

                confirm = st.checkbox("I understand this permanently deletes the student.", key="delete_confirm")
                if st.button("🗑️ Delete Student", type="primary", use_container_width=True, disabled=not confirm):
                    success = execute_write(engine, "DELETE FROM STUDENT WHERE student_id = :sid", {"sid": selected_id})
                    if success:
                        st.success("✅ Student deleted!")
                        st.rerun()
                    else:
                        st.error("Deletion blocked — student has related records (applications, interviews, placements).")
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: DEPARTMENTS
# ──────────────────────────────────────────────
elif section == "Departments":
    st.markdown("<h1>Departments</h1>", unsafe_allow_html=True)
    st.caption("Manage academic departments")

    tab_list, tab_add, tab_edit = st.tabs(["📋 All Departments", "➕ Add", "✏️ Edit"])

    with tab_list:
        st.markdown("### Departments")
        try:
            dept_df = fetch_data(engine, """
                SELECT d.department_id, d.department_name,
                       COUNT(s.student_id) as student_count
                FROM DEPARTMENT d
                LEFT JOIN STUDENT s ON d.department_id = s.department_id
                GROUP BY d.department_id, d.department_name
                ORDER BY d.department_id
            """)
            st.dataframe(dept_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_add:
        with st.form("add_dept_form"):
            name = st.text_input("Department Name *")
            submitted = st.form_submit_button("Add Department", type="primary")
            if submitted and name.strip():
                execute_write(engine, "INSERT INTO DEPARTMENT (department_name) VALUES (:name)", {"name": name.strip()})
                st.success("✅ Department added!")
                st.rerun()

    with tab_edit:
        try:
            depts = fetch_data(engine, "SELECT * FROM DEPARTMENT ORDER BY department_id")
            if depts.empty:
                st.info("No departments.")
            else:
                sel = st.selectbox("Select Department", depts['department_id'].tolist(),
                                   format_func=lambda x: f"{x} - {depts.loc[depts.department_id==x,'department_name'].iloc[0]}")
                rec = depts[depts.department_id == sel].iloc[0]
                with st.form("edit_dept_form"):
                    new_name = st.text_input("Department Name", value=rec['department_name'])
                    if st.form_submit_button("Update", type="primary"):
                        execute_write(engine, "UPDATE DEPARTMENT SET department_name = :name WHERE department_id = :id",
                                      {"name": new_name.strip(), "id": sel})
                        st.success("✅ Updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: COMPANIES
# ──────────────────────────────────────────────
elif section == "Companies":
    st.markdown("<h1>Companies</h1>", unsafe_allow_html=True)
    st.caption("Manage recruiting companies")

    tab_list, tab_add, tab_edit = st.tabs(["📋 All Companies", "➕ Add", "✏️ Edit"])

    with tab_list:
        try:
            comp_df = fetch_data(engine, """
                SELECT c.company_id, c.company_name, c.industry, c.location,
                       COUNT(DISTINCT r.recruiter_id) as recruiters,
                       COUNT(DISTINCT j.job_id) as jobs
                FROM COMPANY c
                LEFT JOIN RECRUITER r ON c.company_id = r.company_id
                LEFT JOIN JOB j ON c.company_id = j.company_id
                GROUP BY c.company_id, c.company_name, c.industry, c.location
                ORDER BY c.company_id
            """)
            st.dataframe(comp_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_add:
        with st.form("add_comp_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Company Name *")
                industry = st.text_input("Industry")
            with col2:
                location = st.text_input("Location")
            if st.form_submit_button("Add Company", type="primary") and name.strip():
                execute_write(engine, "INSERT INTO COMPANY (company_name, industry, location) VALUES (:name, :industry, :location)",
                              {"name": name.strip(), "industry": industry.strip() or None, "location": location.strip() or None})
                st.success("✅ Company added!")
                st.rerun()

    with tab_edit:
        try:
            comps = fetch_data(engine, "SELECT * FROM COMPANY ORDER BY company_id")
            if comps.empty:
                st.info("No companies.")
            else:
                sel = st.selectbox("Select Company", comps['company_id'].tolist(),
                                   format_func=lambda x: f"{x} - {comps.loc[comps.company_id==x,'company_name'].iloc[0]}")
                rec = comps[comps.company_id == sel].iloc[0]
                with st.form("edit_comp_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Company Name", value=rec['company_name'])
                        industry = st.text_input("Industry", value=rec['industry'] or "")
                    with col2:
                        location = st.text_input("Location", value=rec['location'] or "")
                    if st.form_submit_button("Update", type="primary"):
                        execute_write(engine, "UPDATE COMPANY SET company_name=:name, industry=:ind, location=:loc WHERE company_id=:id",
                                      {"name": name.strip(), "ind": industry.strip() or None, "loc": location.strip() or None, "id": sel})
                        st.success("✅ Updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: RECRUITERS
# ──────────────────────────────────────────────
elif section == "Recruiters":
    st.markdown("<h1>Recruiters</h1>", unsafe_allow_html=True)
    st.caption("Manage company recruiters")

    try:
        companies = fetch_data(engine, "SELECT company_id, company_name FROM COMPANY ORDER BY company_name")
        comp_map = dict(zip(companies['company_id'], companies['company_name']))
        comp_ids = companies['company_id'].tolist()
    except:
        comp_map = {}
        comp_ids = []

    tab_list, tab_add, tab_edit = st.tabs(["📋 All Recruiters", "➕ Add", "✏️ Edit"])

    with tab_list:
        try:
            rec_df = fetch_data(engine, """
                SELECT r.recruiter_id, r.recruiter_name, r.email, r.phone, c.company_name
                FROM RECRUITER r
                JOIN COMPANY c ON r.company_id = c.company_id
                ORDER BY r.recruiter_id
            """)
            st.dataframe(rec_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_add:
        with st.form("add_rec_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Recruiter Name *")
                email = st.text_input("Email *")
            with col2:
                phone = st.text_input("Phone")
                comp_id = st.selectbox("Company *", comp_ids, format_func=lambda x: comp_map.get(x, x))
            if st.form_submit_button("Add Recruiter", type="primary") and name.strip() and email.strip():
                execute_write(engine, "INSERT INTO RECRUITER (recruiter_name, email, phone, company_id) VALUES (:name, :email, :phone, :cid)",
                              {"name": name.strip(), "email": email.strip(), "phone": phone.strip() or None, "cid": comp_id})
                st.success("✅ Recruiter added!")
                st.rerun()

    with tab_edit:
        try:
            recs = fetch_data(engine, "SELECT * FROM RECRUITER ORDER BY recruiter_id")
            if recs.empty:
                st.info("No recruiters.")
            else:
                sel = st.selectbox("Select Recruiter", recs['recruiter_id'].tolist(),
                                   format_func=lambda x: f"{x} - {recs.loc[recs.recruiter_id==x,'recruiter_name'].iloc[0]}")
                rec = recs[recs.recruiter_id == sel].iloc[0]
                with st.form("edit_rec_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Name", value=rec['recruiter_name'])
                        email = st.text_input("Email", value=rec['email'])
                    with col2:
                        phone = st.text_input("Phone", value=rec['phone'] or "")
                        comp_id = st.selectbox("Company", comp_ids, index=comp_ids.index(int(rec['company_id'])), format_func=lambda x: comp_map.get(x, x))
                    if st.form_submit_button("Update", type="primary"):
                        execute_write(engine, "UPDATE RECRUITER SET recruiter_name=:name, email=:email, phone=:phone, company_id=:cid WHERE recruiter_id=:id",
                                      {"name": name.strip(), "email": email.strip(), "phone": phone.strip() or None, "cid": comp_id, "id": sel})
                        st.success("✅ Updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: JOB POSTINGS
# ──────────────────────────────────────────────
elif section == "Job Postings":
    st.markdown("<h1>Job Postings</h1>", unsafe_allow_html=True)
    st.caption("Manage job opportunities and requirements")

    try:
        companies = fetch_data(engine, "SELECT company_id, company_name FROM COMPANY ORDER BY company_name")
        recruiters = fetch_data(engine, "SELECT recruiter_id, recruiter_name FROM RECRUITER ORDER BY recruiter_name")
        comp_map = dict(zip(companies['company_id'], companies['company_name']))
        rec_map = dict(zip(recruiters['recruiter_id'], recruiters['recruiter_name']))
        comp_ids = companies['company_id'].tolist()
        rec_ids = recruiters['recruiter_id'].tolist()
    except:
        comp_map = {}; rec_map = {}; comp_ids = []; rec_ids = []

    tab_list, tab_add, tab_edit, tab_skills = st.tabs(["📋 All Jobs", "➕ Add Job", "✏️ Edit", "🔧 Skills"])

    with tab_list:
        try:
            job_df = fetch_data(engine, """
                SELECT j.job_id, j.job_title, j.job_type, j.location, j.minimum_cgpa, j.salary, j.vacancies,
                       c.company_name, r.recruiter_name
                FROM JOB j
                JOIN COMPANY c ON j.company_id = c.company_id
                JOIN RECRUITER r ON j.recruiter_id = r.recruiter_id
                ORDER BY j.job_id DESC
            """)
            st.dataframe(job_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_add:
        with st.form("add_job_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Job Title *")
                jtype = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship", "Contract"])
                location = st.text_input("Location")
            with col2:
                min_cgpa = st.number_input("Minimum CGPA *", min_value=0.0, max_value=10.0, value=7.0, step=0.01, format="%.2f")
                salary = st.number_input("Annual Salary (₹) *", min_value=0, value=600000, step=50000)
                vacancies = st.number_input("Vacancies *", min_value=1, value=1, step=1)

            comp_id = st.selectbox("Company *", comp_ids, format_func=lambda x: comp_map.get(x, x))
            rec_id = st.selectbox("Recruiter *", rec_ids, format_func=lambda x: rec_map.get(x, x))

            if st.form_submit_button("Post Job", type="primary") and title.strip():
                execute_write(engine, """
                    INSERT INTO JOB (job_title, job_type, location, minimum_cgpa, salary, vacancies, company_id, recruiter_id)
                    VALUES (:title, :jtype, :loc, :mcgpa, :sal, :vac, :cid, :rid)
                """, {"title": title.strip(), "jtype": jtype, "loc": location.strip() or None,
                      "mcgpa": min_cgpa, "sal": salary, "vac": vacancies, "cid": comp_id, "rid": rec_id})
                st.success("✅ Job posted!")
                st.rerun()

    with tab_edit:
        try:
            jobs = fetch_data(engine, "SELECT job_id, job_title FROM JOB ORDER BY job_id DESC")
            if jobs.empty:
                st.info("No jobs.")
            else:
                sel = st.selectbox("Select Job", jobs['job_id'].tolist(),
                                   format_func=lambda x: f"{x} - {jobs.loc[jobs.job_id==x,'job_title'].iloc[0]}")
                rec = fetch_data(engine, "SELECT * FROM JOB WHERE job_id = :id", {"id": sel}).iloc[0]
                with st.form("edit_job_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input("Job Title", value=rec['job_title'])
                        jtype = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship", "Contract"],
                                             index=["Full-time", "Part-time", "Internship", "Contract"].index(rec['job_type']))
                        location = st.text_input("Location", value=rec['location'] or "")
                    with col2:
                        min_cgpa = st.number_input("Minimum CGPA", min_value=0.0, max_value=10.0, value=float(rec['minimum_cgpa']), step=0.01, format="%.2f")
                        salary = st.number_input("Salary", min_value=0, value=int(rec['salary']), step=50000)
                        vacancies = st.number_input("Vacancies", min_value=1, value=int(rec['vacancies']), step=1)

                    comp_id = st.selectbox("Company", comp_ids, index=comp_ids.index(int(rec['company_id'])), format_func=lambda x: comp_map.get(x, x))
                    rec_id = st.selectbox("Recruiter", rec_ids, index=rec_ids.index(int(rec['recruiter_id'])), format_func=lambda x: rec_map.get(x, x))

                    if st.form_submit_button("Update Job", type="primary"):
                        execute_write(engine, """
                            UPDATE JOB SET job_title=:title, job_type=:jtype, location=:loc,
                                minimum_cgpa=:mcgpa, salary=:sal, vacancies=:vac,
                                company_id=:cid, recruiter_id=:rid
                            WHERE job_id=:jid
                        """, {"title": title.strip(), "jtype": jtype, "loc": location.strip() or None,
                              "mcgpa": min_cgpa, "sal": salary, "vac": vacancies,
                              "cid": comp_id, "rid": rec_id, "jid": sel})
                        st.success("✅ Job updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_skills:
        st.markdown("### Manage Job Skill Requirements")
        try:
            jobs = fetch_data(engine, "SELECT job_id, job_title FROM JOB ORDER BY job_id")
            skills = fetch_data(engine, "SELECT skill_id, skill_name FROM SKILL ORDER BY skill_name")
            if jobs.empty or skills.empty:
                st.info("Add jobs and skills first.")
            else:
                job_sel = st.selectbox("Select Job", jobs['job_id'].tolist(),
                                       format_func=lambda x: f"{x} - {jobs.loc[jobs.job_id==x,'job_title'].iloc[0]}")

                # Show current skills
                curr = fetch_data(engine, """
                    SELECT js.skill_id, s.skill_name, js.required_level
                    FROM JOB_SKILL js JOIN SKILL s ON js.skill_id = s.skill_id
                    WHERE js.job_id = :jid
                """, {"jid": job_sel})
                st.markdown("**Current Requirements:**")
                st.dataframe(curr, use_container_width=True, hide_index=True)

                # Add skill
                with st.form("add_job_skill_form"):
                    skill_id = st.selectbox("Skill", skills['skill_id'].tolist(),
                                           format_func=lambda x: f"{skills.loc[skills.skill_id==x,'skill_name'].iloc[0]}")
                    level = st.selectbox("Required Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
                    if st.form_submit_button("Add Skill"):
                        execute_write(engine, "INSERT INTO JOB_SKILL (job_id, skill_id, required_level) VALUES (:jid, :sid, :lvl)",
                                      {"jid": job_sel, "sid": skill_id, "lvl": level})
                        st.success("✅ Skill added!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: APPLICATIONS
# ──────────────────────────────────────────────
elif section == "Applications":
    st.markdown("<h1>Applications</h1>", unsafe_allow_html=True)
    st.caption("Track and manage student job applications")

    tab_list, tab_apply, tab_status = st.tabs(["📋 All Applications", "➕ Apply", "🔄 Status"])

    with tab_list:
        st.markdown("### All Applications")
        search = st.text_input("Search", placeholder="Search by student, job, company...", key="app_search")
        status_filter = st.selectbox("Filter by Status", ["All", "Applied", "Under Review", "Shortlisted", "Rejected", "Selected", "Withdrawn"])

        try:
            query = """
                SELECT a.application_id, a.application_date, a.status,
                       s.student_id, s.student_name, s.email, s.cgpa,
                       j.job_id, j.job_title, j.location,
                       c.company_name,
                       d.department_name
                FROM APPLICATION a
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                JOIN DEPARTMENT d ON s.department_id = d.department_id
            """
            apps_df = fetch_data(engine, query)

            filtered = apps_df.copy()
            if search.strip():
                term = search.strip().lower()
                mask = (
                    filtered['student_name'].str.lower().str.contains(term, na=False) |
                    filtered['email'].str.lower().str.contains(term, na=False) |
                    filtered['job_title'].str.lower().str.contains(term, na=False) |
                    filtered['company_name'].str.lower().str.contains(term, na=False)
                )
                filtered = filtered[mask]

            if status_filter != "All":
                filtered = filtered[filtered['status'] == status_filter]

            st.markdown(f"**Showing {len(filtered)} of {len(apps_df)} applications**")
            st.dataframe(filtered, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_apply:
        st.markdown("### Apply for Job")
        try:
            students = fetch_data(engine, "SELECT student_id, student_name, cgpa FROM STUDENT ORDER BY student_name")
            jobs = fetch_data(engine, """
                SELECT j.job_id, j.job_title, j.minimum_cgpa, j.vacancies,
                       c.company_name
                FROM JOB j
                JOIN COMPANY c ON j.company_id = c.company_id
                WHERE j.vacancies > 0
                ORDER BY j.job_title
            """)

            with st.form("apply_form"):
                student_id = st.selectbox("Student *", students['student_id'].tolist(),
                                          format_func=lambda x: f"{x} - {students.loc[students.student_id==x,'student_name'].iloc[0]} (CGPA: {students.loc[students.student_id==x,'cgpa'].iloc[0]})")
                job_id = st.selectbox("Job *", jobs['job_id'].tolist(),
                                      format_func=lambda x: f"{x} - {jobs.loc[jobs.job_id==x,'job_title'].iloc[0]} ({jobs.loc[jobs.job_id==x,'company_name'].iloc[0]})")
                if st.form_submit_button("Submit Application", type="primary"):
                    # Check eligibility
                    student_cgpa = students.loc[students.student_id==student_id,'cgpa'].iloc[0]
                    job_min_cgpa = jobs.loc[jobs.job_id==job_id,'minimum_cgpa'].iloc[0]
                    if student_cgpa < job_min_cgpa:
                        st.error(f"Student CGPA ({student_cgpa}) below minimum required ({job_min_cgpa})")
                    else:
                        success = execute_write(engine, """
                            INSERT INTO APPLICATION (student_id, job_id, application_date, status)
                            VALUES (:sid, :jid, CURDATE(), 'Applied')
                        """, {"sid": student_id, "jid": job_id})
                        if success:
                            st.success("✅ Application submitted!")
                            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_status:
        st.markdown("### Update Application Status")
        try:
            apps = fetch_data(engine, """
                SELECT a.application_id, a.status, s.student_name, j.job_title
                FROM APPLICATION a
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                ORDER BY a.application_date DESC
            """)
            if apps.empty:
                st.info("No applications.")
            else:
                sel = st.selectbox("Select Application", apps['application_id'].tolist(),
                                   format_func=lambda x: f"{x} - {apps.loc[apps.application_id==x,'student_name'].iloc[0]} - {apps.loc[apps.application_id==x,'job_title'].iloc[0]}")
                curr_status = apps[apps.application_id == sel].iloc[0]['status']

                with st.form("status_form"):
                    new_status = st.selectbox("New Status",
                        ["Applied", "Under Review", "Shortlisted", "Rejected", "Selected", "Withdrawn"],
                        index=["Applied", "Under Review", "Shortlisted", "Rejected", "Selected", "Withdrawn"].index(curr_status))
                    if st.form_submit_button("Update Status", type="primary"):
                        execute_write(engine, "UPDATE APPLICATION SET status = :status WHERE application_id = :aid",
                                      {"status": new_status, "aid": sel})
                        st.success("✅ Status updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: INTERVIEWS
# ──────────────────────────────────────────────
elif section == "Interviews":
    st.markdown("<h1>Interviews</h1>", unsafe_allow_html=True)
    st.caption("Manage interview rounds and results")

    tab_list, tab_schedule, tab_results = st.tabs(["📋 All Interviews", "📅 Schedule", "📊 Results"])

    with tab_list:
        try:
            int_df = fetch_data(engine, """
                SELECT i.interview_id, i.round_no, i.interview_date, i.result,
                       a.application_id, s.student_name, j.job_title, c.company_name
                FROM INTERVIEW i
                JOIN APPLICATION a ON i.application_id = a.application_id
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                ORDER BY i.interview_date DESC
            """)
            st.dataframe(int_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_schedule:
        try:
            apps = fetch_data(engine, """
                SELECT a.application_id, s.student_name, j.job_title, c.company_name
                FROM APPLICATION a
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                WHERE a.status IN ('Shortlisted', 'Selected', 'Under Review')
                ORDER BY a.application_date DESC
            """)
            with st.form("schedule_form"):
                app_id = st.selectbox("Application *", apps['application_id'].tolist(),
                                      format_func=lambda x: f"{x} - {apps.loc[apps.application_id==x,'student_name'].iloc[0]} - {apps.loc[apps.application_id==x,'job_title'].iloc[0]}")
                round_no = st.number_input("Round Number *", min_value=1, value=1)
                int_date = st.date_input("Interview Date *", value=date.today())
                if st.form_submit_button("Schedule Interview", type="primary"):
                    execute_write(engine, """
                        INSERT INTO INTERVIEW (application_id, round_no, interview_date, result)
                        VALUES (:aid, :rnd, :dt, 'Scheduled')
                    """, {"aid": app_id, "rnd": round_no, "dt": int_date})
                    st.success("✅ Interview scheduled!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_results:
        st.markdown("### Record Interview Result")
        try:
            pending = fetch_data(engine, """
                SELECT i.interview_id, i.round_no, i.interview_date,
                       s.student_name, j.job_title, c.company_name
                FROM INTERVIEW i
                JOIN APPLICATION a ON i.application_id = a.application_id
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                WHERE i.result IN ('Scheduled', 'Pending')
                ORDER BY i.interview_date
            """)
            if pending.empty:
                st.info("No pending interviews.")
            else:
                sel = st.selectbox("Select Interview", pending['interview_id'].tolist(),
                                   format_func=lambda x: f"{x} - {pending.loc[pending.interview_id==x,'student_name'].iloc[0]} - Round {pending.loc[pending.interview_id==x,'round_no'].iloc[0]}")
                with st.form("result_form"):
                    result = st.selectbox("Result", ["Pass", "Fail", "Pending"])
                    if st.form_submit_button("Save Result", type="primary"):
                        execute_write(engine, "UPDATE INTERVIEW SET result = :res WHERE interview_id = :iid",
                                      {"res": result, "iid": sel})
                        st.success("✅ Result recorded!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: OFFERS
# ──────────────────────────────────────────────
elif section == "Offers":
    st.markdown("<h1>Offers</h1>", unsafe_allow_html=True)
    st.caption("Manage employment offers")

    tab_list, tab_create, tab_update = st.tabs(["📋 All Offers", "➕ Create Offer", "✏️ Update"])

    with tab_list:
        try:
            off_df = fetch_data(engine, """
                SELECT o.offer_id, o.offer_date, o.offered_salary, o.status,
                       a.application_id, s.student_name, j.job_title, c.company_name
                FROM OFFER o
                JOIN APPLICATION a ON o.application_id = a.application_id
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                ORDER BY o.offer_date DESC
            """)
            st.dataframe(off_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_create:
        try:
            selected_apps = fetch_data(engine, """
                SELECT a.application_id, s.student_name, j.job_title, c.company_name
                FROM APPLICATION a
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                WHERE a.status = 'Selected' AND a.application_id NOT IN (SELECT application_id FROM OFFER)
                ORDER BY a.application_date DESC
            """)
            if selected_apps.empty:
                st.info("No selected applications without offers.")
            else:
                with st.form("create_offer_form"):
                    app_id = st.selectbox("Application *", selected_apps['application_id'].tolist(),
                                          format_func=lambda x: f"{x} - {selected_apps.loc[selected_apps.application_id==x,'student_name'].iloc[0]} - {selected_apps.loc[selected_apps.application_id==x,'job_title'].iloc[0]}")
                    salary = st.number_input("Offered Salary (₹) *", min_value=0, value=600000, step=50000)
                    if st.form_submit_button("Create Offer", type="primary"):
                        execute_write(engine, """
                            INSERT INTO OFFER (application_id, offer_date, offered_salary, status)
                            VALUES (:aid, CURDATE(), :sal, 'Pending')
                        """, {"aid": app_id, "sal": salary})
                        st.success("✅ Offer created!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_update:
        try:
            offers = fetch_data(engine, """
                SELECT o.offer_id, o.offered_salary, o.status, s.student_name, j.job_title
                FROM OFFER o
                JOIN APPLICATION a ON o.application_id = a.application_id
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                ORDER BY o.offer_id DESC
            """)
            if offers.empty:
                st.info("No offers.")
            else:
                sel = st.selectbox("Select Offer", offers['offer_id'].tolist(),
                                   format_func=lambda x: f"{x} - {offers.loc[offers.offer_id==x,'student_name'].iloc[0]} - ₹{offers.loc[offers.offer_id==x,'offered_salary'].iloc[0]:,.0f}")
                rec = offers[offers.offer_id == sel].iloc[0]
                with st.form("update_offer_form"):
                    salary = st.number_input("Offered Salary", min_value=0, value=int(rec['offered_salary']), step=50000)
                    status = st.selectbox("Status", ["Pending", "Accepted", "Rejected", "Expired"],
                                          index=["Pending", "Accepted", "Rejected", "Expired"].index(rec['status']))
                    if st.form_submit_button("Update Offer", type="primary"):
                        execute_write(engine, "UPDATE OFFER SET offered_salary = :sal, status = :stat WHERE offer_id = :oid",
                                      {"sal": salary, "stat": status, "oid": sel})
                        st.success("✅ Offer updated!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: PLACEMENTS
# ──────────────────────────────────────────────
elif section == "Placements":
    st.markdown("<h1>Placements</h1>", unsafe_allow_html=True)
    st.caption("Final placement records")

    tab_list, tab_create = st.tabs(["📋 All Placements", "➕ Record Placement"])

    with tab_list:
        try:
            plc_df = fetch_data(engine, """
                SELECT p.placement_id, p.joining_date, p.placement_status,
                       s.student_id, s.student_name, s.email,
                       c.company_name, j.job_title,
                       o.offered_salary
                FROM PLACEMENT p
                JOIN STUDENT s ON p.student_id = s.student_id
                JOIN OFFER o ON p.offer_id = o.offer_id
                JOIN APPLICATION a ON o.application_id = a.application_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                ORDER BY p.placement_id DESC
            """)
            st.dataframe(plc_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab_create:
        st.warning("⚠️ Placement requires a valid accepted offer. Student must not already have a placement.")
        try:
            accepted = fetch_data(engine, """
                SELECT o.offer_id, o.offered_salary, s.student_id, s.student_name, j.job_title, c.company_name
                FROM OFFER o
                JOIN APPLICATION a ON o.application_id = a.application_id
                JOIN STUDENT s ON a.student_id = s.student_id
                JOIN JOB j ON a.job_id = j.job_id
                JOIN COMPANY c ON j.company_id = c.company_id
                WHERE o.status = 'Accepted'
                  AND o.offer_id NOT IN (SELECT offer_id FROM PLACEMENT)
                  AND a.student_id NOT IN (SELECT student_id FROM PLACEMENT)
                ORDER BY o.offer_date DESC
            """)
            if accepted.empty:
                st.info("No eligible accepted offers for placement.")
            else:
                with st.form("create_placement_form"):
                    offer_id = st.selectbox("Offer *", accepted['offer_id'].tolist(),
                                            format_func=lambda x: f"{x} - {accepted.loc[accepted.offer_id==x,'student_name'].iloc[0]} - {accepted.loc[accepted.offer_id==x,'job_title'].iloc[0]} ({accepted.loc[accepted.offer_id==x,'company_name'].iloc[0]})")
                    join_date = st.date_input("Joining Date *", value=date.today() + pd.DateOffset(days=30))
                    status = st.selectbox("Placement Status", ["Confirmed", "Joined", "Deferred", "Cancelled"])
                    if st.form_submit_button("Record Placement", type="primary"):
                        success = execute_write(engine, """
                            INSERT INTO PLACEMENT (student_id, offer_id, joining_date, placement_status)
                            VALUES (:sid, :oid, :jd, :stat)
                        """, {"sid": accepted.loc[accepted.offer_id==offer_id,'student_id'].iloc[0],
                              "oid": offer_id, "jd": join_date, "stat": status})
                        if success:
                            st.success("✅ Placement recorded!")
                            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: SKILLS
# ──────────────────────────────────────────────
elif section == "Skills":
    st.markdown("<h1>Skills</h1>", unsafe_allow_html=True)
    st.caption("Manage skills and student proficiencies")

    tab_skills, tab_student_skills = st.tabs(["🛠️ Skills Catalog", "👨‍🎓 Student Skills"])

    with tab_skills:
        tab_list, tab_add = st.tabs(["📋 All Skills", "➕ Add Skill"])

        with tab_list:
            try:
                sk_df = fetch_data(engine, """
                    SELECT s.skill_id, s.skill_name,
                           COUNT(DISTINCT ss.student_id) as student_count,
                           COUNT(DISTINCT js.job_id) as job_count
                    FROM SKILL s
                    LEFT JOIN STUDENT_SKILL ss ON s.skill_id = ss.skill_id
                    LEFT JOIN JOB_SKILL js ON s.skill_id = js.skill_id
                    GROUP BY s.skill_id, s.skill_name
                    ORDER BY s.skill_name
                """)
                st.dataframe(sk_df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Error: {e}")

        with tab_add:
            with st.form("add_skill_form"):
                name = st.text_input("Skill Name *")
                if st.form_submit_button("Add Skill", type="primary") and name.strip():
                    execute_write(engine, "INSERT INTO SKILL (skill_name) VALUES (:name)", {"name": name.strip()})
                    st.success("✅ Skill added!")
                    st.rerun()

    with tab_student_skills:
        try:
            students = fetch_data(engine, "SELECT student_id, student_name FROM STUDENT ORDER BY student_name")
            skills = fetch_data(engine, "SELECT skill_id, skill_name FROM SKILL ORDER BY skill_name")

            with st.form("add_student_skill_form"):
                col1, col2 = st.columns(2)
                with col1:
                    student_id = st.selectbox("Student *", students['student_id'].tolist(),
                                              format_func=lambda x: f"{x} - {students.loc[students.student_id==x,'student_name'].iloc[0]}")
                with col2:
                    skill_id = st.selectbox("Skill *", skills['skill_id'].tolist(),
                                            format_func=lambda x: f"{skills.loc[skills.skill_id==x,'skill_name'].iloc[0]}")
                proficiency = st.selectbox("Proficiency *", ["Beginner", "Intermediate", "Advanced", "Expert"])

                if st.form_submit_button("Add Student Skill", type="primary"):
                    execute_write(engine, """
                        INSERT INTO STUDENT_SKILL (student_id, skill_id, proficiency)
                        VALUES (:sid, :skid, :prof)
                    """, {"sid": student_id, "skid": skill_id, "prof": proficiency})
                    st.success("✅ Student skill added!")
                    st.rerun()

            # Show existing
            st.markdown("### Current Student Skills")
            ss_df = fetch_data(engine, """
                SELECT ss.student_id, s.student_name, sk.skill_name, ss.proficiency
                FROM STUDENT_SKILL ss
                JOIN STUDENT s ON ss.student_id = s.student_id
                JOIN SKILL sk ON ss.skill_id = sk.skill_id
                ORDER BY s.student_name, sk.skill_name
            """)
            st.dataframe(ss_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────────────────────────
# SECTION: SQL CONSOLE
# ──────────────────────────────────────────────
elif section == "SQL Console":
    st.markdown("<h1>SQL Query Console</h1>", unsafe_allow_html=True)
    st.caption("Execute read-only SQL queries against placement_management database")

    # Example queries
    with st.expander("💡 Example Queries"):
        examples = {
            "Student Placement Stats": """SELECT s.student_name, d.department_name, s.cgpa,
    j.job_title, c.company_name, o.offered_salary, p.placement_status
FROM STUDENT s
JOIN DEPARTMENT d ON s.department_id = d.department_id
LEFT JOIN PLACEMENT p ON s.student_id = p.student_id
LEFT JOIN OFFER o ON p.offer_id = o.offer_id
LEFT JOIN APPLICATION a ON o.application_id = a.application_id
LEFT JOIN JOB j ON a.job_id = j.job_id
LEFT JOIN COMPANY c ON j.company_id = c.company_id
WHERE p.placement_id IS NOT NULL
ORDER BY o.offered_salary DESC;""",
            "Company Hiring Stats": """SELECT c.company_name, c.industry, c.location,
    COUNT(DISTINCT j.job_id) as jobs_posted,
    COUNT(DISTINCT a.application_id) as applications_received,
    COUNT(DISTINCT o.offer_id) as offers_made,
    COUNT(DISTINCT p.placement_id) as placements
FROM COMPANY c
LEFT JOIN JOB j ON c.company_id = j.company_id
LEFT JOIN APPLICATION a ON j.job_id = a.job_id
LEFT JOIN OFFER o ON a.application_id = o.application_id
LEFT JOIN PLACEMENT p ON o.offer_id = p.offer_id
GROUP BY c.company_id, c.company_name, c.industry, c.location
ORDER BY placements DESC;""",
            "Skill Gap Analysis": """SELECT j.job_title, s.skill_name, js.required_level
FROM JOB_SKILL js
JOIN JOB j ON js.job_id = j.job_id
JOIN SKILL s ON js.skill_id = s.skill_id
WHERE NOT EXISTS (
    SELECT 1 FROM STUDENT_SKILL ss
    WHERE ss.skill_id = js.skill_id
)
ORDER BY j.job_id, s.skill_name;""",
            "Department Placement %": """SELECT d.department_name,
    COUNT(DISTINCT s.student_id) as total_students,
    COUNT(DISTINCT p.student_id) as placed_students,
    ROUND(COUNT(DISTINCT p.student_id) * 100.0 / COUNT(DISTINCT s.student_id), 2) as placement_pct
FROM DEPARTMENT d
LEFT JOIN STUDENT s ON d.department_id = s.department_id
LEFT JOIN PLACEMENT p ON s.student_id = p.student_id
GROUP BY d.department_id, d.department_name
ORDER BY placement_pct DESC;"""
        }

        for title, query in examples.items():
            st.markdown(f"**{title}**")
            st.code(query, language="sql")

    st.divider()

    # Query input
    query = st.text_area(
        "SQL Query",
        value="SELECT * FROM STUDENT LIMIT 10;",
        height=200,
        key="sql_query_input",
        help="Enter a single read-only SQL statement (SELECT, SHOW, DESCRIBE, EXPLAIN)"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_btn = st.button("▶ Run Query", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("Clear", use_container_width=True)

    if clear_btn:
        st.rerun()

    if run_btn:
        cleaned = query.strip().rstrip(";").strip()
        first_word = cleaned.split()[0].upper() if cleaned else ""
        allowed = {"SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN", "WITH"}

        if not cleaned:
            st.warning("Enter a query.")
        elif first_word not in allowed or ";" in cleaned:
            st.error("Only one read-only SQL statement allowed (SELECT, SHOW, DESCRIBE, EXPLAIN, WITH).")
        else:
            try:
                with st.spinner("Executing..."):
                    result = fetch_data(engine, cleaned)

                st.success(f"✅ Query executed. {len(result)} rows returned.")

                # Show results
                st.dataframe(result, use_container_width=True, hide_index=True)

                # Download
                if len(result) > 0:
                    csv = result.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"SQL Error: {e}")

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align: center; padding: 16px; color: var(--text-muted); font-size: 0.8rem;">
    Placement Management System &nbsp;|&nbsp; MySQL 8.0 &nbsp;|&nbsp; Python + Streamlit &nbsp;|&nbsp; Enterprise Edition
</div>
""", unsafe_allow_html=True)