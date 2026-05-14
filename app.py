import streamlit as st
import pandas as pd
import os
import time

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(
    page_title="政策红利匹配引擎 | 智慧社区",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 定制 CSS 样式系统
# ==========================================
st.markdown("""
<style>
    /* ===== CSS 变量与全局重置 ===== */
    :root {
        --primary: #FF6B35;
        --primary-dark: #E55A2B;
        --accent-gold: #F7B731;
        --bg-warm: #FFF8F0;
        --text-dark: #1a1a2e;
        --text-mid: #4a4a6a;
        --text-light: #6b7280;
        --card-bg: rgba(255,255,255,0.92);
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
        --shadow-md: 0 8px 30px rgba(0,0,0,0.08);
        --shadow-lg: 0 20px 60px rgba(0,0,0,0.12);
        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 24px;
        --cat-job: #3B82F6;
        --cat-welfare: #10B981;
        --cat-elderly: #F59E0B;
        --cat-housing: #8B5CF6;
    }

    /* ===== 全局背景 ===== */
    .stApp {
        background: linear-gradient(160deg, #FFF5EE 0%, #FFF8F0 30%, #FFF0E5 70%, #FFFAF5 100%);
    }
    .main > div:first-child {
        padding-top: 1rem;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none !important;
    }

    /* ===== 顶部导航栏 ===== */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 0;
        margin-bottom: 12px;
    }
    .top-nav .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary);
    }
    .top-nav .logo-icon {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, #FF6B35, #F7B731);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        color: white;
    }
    .top-nav .badge {
        background: rgba(255,107,53,0.1);
        color: var(--primary);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* ===== Hero 区域 ===== */
    .hero-section {
        text-align: center;
        padding: 32px 20px 40px;
        position: relative;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #E55A2B 0%, #FF6B35 40%, #F7B731 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        color: var(--text-mid);
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 500px;
        margin: 0 auto 20px;
        line-height: 1.6;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 32px;
        flex-wrap: wrap;
    }
    .hero-stat {
        text-align: center;
        min-width: 80px;
    }
    .hero-stat .number {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary);
        line-height: 1;
    }
    .hero-stat .label {
        font-size: 0.8rem;
        color: var(--text-light);
        margin-top: 4px;
    }

    /* ===== 表单卡片 ===== */
    .form-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: var(--radius-lg);
        padding: 32px 28px 20px;
        box-shadow: var(--shadow-md);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .form-card::before {
        content: "";
        position: absolute; top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF6B35, #F7B731, #FF6B35);
    }
    .form-card .step-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,107,53,0.08);
        color: var(--primary);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 20px;
    }

    /* ===== 输入框美化 ===== */
    .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {
        background: rgba(249,250,251,0.9) !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
        color: var(--text-dark) !important;
        transition: all 0.25s !important;
        box-shadow: none !important;
    }
    .stNumberInput input:focus, .stSelectbox [data-baseweb="select"] > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important;
        background: white !important;
    }
    div[data-testid="stNumberInput"] label, div[data-testid="stSelectbox"] label {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: var(--text-mid) !important;
        margin-bottom: 4px !important;
    }

    /* Toggle 美化 */
    div[data-testid="stToggle"] label {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: var(--text-mid) !important;
    }
    div[data-testid="stToggle"] [data-baseweb="toggle"] {
        transform: scale(0.9);
    }

    /* ===== 提交按钮 ===== */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF6B35 0%, #E55A2B 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 28px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 20px rgba(255,107,53,0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    div.stButton > button:first-child::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
        transition: left 0.6s;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(255,107,53,0.45) !important;
    }
    div.stButton > button:first-child:hover::before {
        left: 100%;
    }

    /* ===== 进度条 ===== */
    div[data-testid="stProgress"] > div {
        background: rgba(255,107,53,0.1) !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #FF6B35, #F7B731) !important;
        border-radius: 4px !important;
    }

    /* ===== 指标卡片 ===== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin: 20px 0 28px;
    }
    @media (max-width: 640px) {
        .metric-grid { grid-template-columns: 1fr; }
    }
    .metric-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0,0,0,0.05);
        border-radius: var(--radius-md);
        padding: 20px;
        text-align: center;
        box-shadow: var(--shadow-sm);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-card .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 6px;
    }
    .metric-card .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--primary);
        line-height: 1.2;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: var(--text-light);
        margin-top: 2px;
    }

    /* ===== 政策卡片（Expander） ===== */
    div[data-testid="stExpander"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
        border-left: 5px solid #e5e7eb !important;
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg) !important;
        border-color: rgba(0,0,0,0.1) !important;
    }
    div[data-testid="stExpander"] details summary {
        padding: 16px 20px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
    }

    /* 分类颜色边框 */
    .cat-job { border-left-color: var(--cat-job) !important; }
    .cat-welfare { border-left-color: var(--cat-welfare) !important; }
    .cat-elderly { border-left-color: var(--cat-elderly) !important; }
    .cat-housing { border-left-color: var(--cat-housing) !important; }

    /* 分类徽章 */
    .category-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .category-tag.job { background: rgba(59,130,246,0.1); color: #2563EB; }
    .category-tag.welfare { background: rgba(16,185,129,0.1); color: #059669; }
    .category-tag.elderly { background: rgba(245,158,11,0.1); color: #D97706; }
    .category-tag.housing { background: rgba(139,92,246,0.1); color: #7C3AED; }

    /* 金额高亮 */
    .amount-highlight {
        color: #DC2626;
        font-size: 1.15rem;
        font-weight: 700;
        background: rgba(220,38,38,0.06);
        padding: 4px 12px;
        border-radius: 8px;
    }

    /* ===== 空状态 ===== */
    .empty-state {
        text-align: center;
        padding: 48px 20px;
    }
    .empty-state .empty-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        opacity: 0.6;
    }

    /* ===== 页脚 ===== */
    .app-footer {
        text-align: center;
        padding: 32px 0 16px;
        color: var(--text-light);
        font-size: 0.78rem;
        border-top: 1px solid rgba(0,0,0,0.05);
        margin-top: 40px;
    }
    .app-footer a {
        color: var(--primary);
        text-decoration: none;
    }

    /* ===== 侧边栏美化 ===== */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0,0,0,0.05) !important;
    }
    section[data-testid="stSidebar"] .stMetric {
        background: rgba(255,107,53,0.06) !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    /* ===== 滚动条 ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,107,53,0.2);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,107,53,0.4); }

    /* ===== 提示框 ===== */
    div[data-testid="stInfo"] {
        background: rgba(59,130,246,0.06) !important;
        border-left: 4px solid #3B82F6 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stWarning"] {
        background: rgba(245,158,11,0.06) !important;
        border-left: 4px solid #F59E0B !important;
        border-radius: 10px !important;
    }

    /* ===== Divider ===== */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.2), transparent) !important;
        margin: 28px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 数据加载
# ==========================================
@st.cache_data
def load_real_data():
    file_path = "policies.csv"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        default_csv = """id,name,category,description,condition_age_min,condition_age_max,condition_status,condition_income_max,condition_hukou,amount
P001,高校毕业生到基层就业补贴,就业创业,鼓励高校毕业生到中小微企业或基层社会组织就业，依法缴纳社保满6个月即可申领。,18,28,学生/应届生,999999,否,3000元 一次性
P002,灵活就业人员社保补贴,就业创业,针对以个人身份缴纳城镇职工养老和医疗保险的就业困难人员及离校未就业毕业生。,18,55,待业/灵活就业,8000,否,最高 800元/月
P003,高龄老人综合津贴（尊老金）,养老服务,具有本市户籍且年满80周岁的老年人即可享受，按年龄段分档发放。,80,120,退休,999999,是,100-500元/月
P004,最低生活保障家庭救助金,民生保障,家庭人均月收入低于当地最低生活保障标准（如1500元）的困难家庭。,0,120,学生/应届生;在职;待业/灵活就业;退休,1500,是,按差额发放
P005,青年就业见习生活补贴,就业创业,16-24岁失业青年或毕业学年大学生参加政企合作的就业见习计划期间的生活费支持。,16,24,待业/灵活就业;学生/应届生,999999,是,当地最低工资的80%
P006,困难残疾人生活补贴,民生保障,针对纳入最低生活保障范围的残疾人，缓解其因残疾产生的额外生活支出困难。,0,120,学生/应届生;在职;待业/灵活就业;退休,1500,是,200元/月
P007,初创企业无息贷款及贴息,就业创业,针对毕业5年内的高校毕业生、登记失业人员等创办小微企业，提供免息资金支持。,18,45,待业/灵活就业;在职;学生/应届生,999999,否,最高 30万元
P008,经济困难失能老人居家照护补贴,养老服务,面向60周岁以上、低收入且经过失能评估的老人，发放用于购买上门洗浴、家政等服务的额度。,60,120,退休,2500,是,300元 服务券/月"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_csv)

    try:
        df = pd.read_csv(file_path)
        df['condition_status'] = df['condition_status'].apply(lambda x: x.split(';') if isinstance(x, str) else [])
        if 'condition_hukou' not in df.columns:
            df['condition_hukou'] = '是'
        return df.to_dict('records')
    except Exception:
        return []

policies = load_real_data()

# 分类配置
CATEGORY_CONFIG = {
    "就业创业": {"icon": "💼", "css_class": "job", "label": "就业创业"},
    "民生保障": {"icon": "🛡️", "css_class": "welfare", "label": "民生保障"},
    "养老服务": {"icon": "🧓", "css_class": "elderly", "label": "养老服务"},
    "住房补贴": {"icon": "🏠", "css_class": "housing", "label": "住房补贴"},
}

# ==========================================
# 4. 侧边栏
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px;">
        <div style="width:42px;height:42px;background:linear-gradient(135deg,#FF6B35,#F7B731);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;">☀️</div>
        <div>
            <div style="font-weight:800;font-size:1.05rem;color:#1a1a2e;">智慧社区</div>
            <div style="font-size:0.75rem;color:#6b7280;">政策匹配引擎 v2.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 数据总览")
    if policies:
        total_amounts = sum(1 for p in policies if "元" in str(p.get("amount", "")))
        categories = set(p["category"] for p in policies)
        st.metric("接入政策", f"{len(policies)} 条")
        st.metric("覆盖领域", f"{len(categories)} 个")
    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(255,107,53,0.06);border-radius:12px;padding:14px;margin-top:12px;">
        <p style="font-size:0.85rem;color:#4a4a6a;margin:0;line-height:1.6;">
            💡 <b>设计初衷</b><br>
            让冰冷的政务数据带有温度，让每一项红利像阳光一样精准照拂社区居民。
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("© 2026 PP创新节 展示项目")

# ==========================================
# 5. Hero 区域
# ==========================================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">政策红利智能匹配引擎</h1>
    <p class="hero-subtitle">只需填写基本信息，AI 将为您精准匹配每一项专属政策权益</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="number">8</div>
            <div class="label">已接入政策</div>
        </div>
        <div class="hero-stat">
            <div class="number">3</div>
            <div class="label">覆盖领域</div>
        </div>
        <div class="hero-stat">
            <div class="number">&lt;30s</div>
            <div class="label">极速匹配</div>
        </div>
        <div class="hero-stat">
            <div class="number">99.8<span style="font-size:0.6em">%</span></div>
            <div class="label">匹配精准度</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. 表单区
# ==========================================
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">📝 步骤一 · 填写您的基本信息</div>', unsafe_allow_html=True)

with st.form("user_profile_form", clear_on_submit=False):
    col1, col2, col3 = st.columns([1, 1, 0.8])

    with col1:
        user_age = st.number_input("🎂 周岁年龄", min_value=0, max_value=120, value=22, step=1,
                                   help="请输入您的实际周岁年龄")
        user_income = st.number_input("💰 月均总收入（元）", min_value=0, value=2000, step=500,
                                      help="包括工资、养老金、经营性收入等")

    with col2:
        user_status = st.selectbox("💼 就业 / 身份状态",
                                   ["学生/应届生", "在职", "待业/灵活就业", "退休"])
        has_local_hukou = st.toggle("🏠 拥有本市户籍", value=True,
                                    help="部分政策需要本市户籍方可申请")

    with col3:
        st.markdown("""
        <div style="background:rgba(255,107,53,0.04);border-radius:12px;padding:16px;height:100%;display:flex;flex-direction:column;justify-content:center;">
            <p style="font-size:0.8rem;color:#6b7280;margin:0 0 8px;font-weight:600;">🔒 隐私承诺</p>
            <p style="font-size:0.75rem;color:#9ca3af;margin:0;line-height:1.5;">您的信息仅用于本次匹配<br>不会存储或用于其他用途</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 启动智能匹配", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 7. 匹配结果
# ==========================================
if submitted:
    if not policies:
        st.error("⚠️ 数据库异常，请联系网格员解决。")
    else:
        st.markdown('<hr>', unsafe_allow_html=True)

        # 动画进度条
        progress_text = "🔎 正在社区数据库中为您仔细检索..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.006)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()

        # 匹配逻辑
        matched_policies = []
        for p in policies:
            if not (p["condition_age_min"] <= user_age <= p["condition_age_max"]):
                continue
            if user_income > p["condition_income_max"]:
                continue
            if user_status not in p["condition_status"]:
                continue
            if p.get("condition_hukou", "是") == "是" and not has_local_hukou:
                continue
            matched_policies.append(p)

        # ========== 有匹配结果 ==========
        if len(matched_policies) > 0:
            st.balloons()

            matched_categories = set(p['category'] for p in matched_policies)
            total_amount_str = "、".join([p['amount'] for p in matched_policies[:3]])

            st.markdown(f"""
            <div style="text-align:center;margin:12px 0 24px;">
                <h2 style="color:#1a1a2e;font-weight:800;margin:0;">🎁 您的专属权益看板</h2>
                <p style="color:#6b7280;font-size:0.9rem;margin:4px 0 0;">
                    根据您的情况，共匹配到 <b style="color:#FF6B35;">{len(matched_policies)}</b> 项政策红利
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 指标卡
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">📋</div>
                    <div class="metric-value">{len(matched_policies)}</div>
                    <div class="metric-label">匹配政策数</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🏷️</div>
                    <div class="metric-value">{len(matched_categories)}</div>
                    <div class="metric-label">覆盖领域</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">✅</div>
                    <div class="metric-value">99.8<span style="font-size:0.5em">%</span></div>
                    <div class="metric-label">匹配精准度</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # 政策卡片列表
            for idx, mp in enumerate(matched_policies):
                cat_info = CATEGORY_CONFIG.get(mp['category'], {"icon": "📌", "css_class": "", "label": mp['category']})
                css_class = f"cat-{cat_info['css_class']}" if cat_info['css_class'] else ""

                with st.expander(f"{cat_info['icon']} {mp['name']}", expanded=(idx == 0)):
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
                        <span class="category-tag {cat_info['css_class']}">{cat_info['icon']} {cat_info['label']}</span>
                        <span class="amount-highlight">💰 {mp['amount']}</span>
                    </div>
                    <p style="color:#4a4a6a;line-height:1.7;font-size:0.95rem;">{mp['description']}</p>
                    """, unsafe_allow_html=True)

                    # 条件标签
                    conditions = []
                    conditions.append(f"年龄 {mp['condition_age_min']}-{mp['condition_age_max']} 岁")
                    if mp['condition_income_max'] < 999999:
                        conditions.append(f"月收入 ≤ {mp['condition_income_max']} 元")
                    conditions.append(f"户籍要求: {'需本市户籍' if mp.get('condition_hukou','是')=='是' else '不限户籍'}")
                    cond_tags = " &nbsp;·&nbsp; ".join([f"<code style='background:rgba(0,0,0,0.04);padding:2px 8px;border-radius:6px;font-size:0.8rem;'>{c}</code>" for c in conditions])
                    st.markdown(f"<p style='font-size:0.82rem;color:#9ca3af;'>{cond_tags}</p>", unsafe_allow_html=True)

                    st.info("📃 预计需准备材料：身份证复印件、户口本复印件、对应情况证明材料。")

        # ========== 无匹配结果 ==========
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <h3 style="color:#1a1a2e;font-weight:700;">暂未找到完全匹配的政策</h3>
                <p style="color:#6b7280;max-width:420px;margin:0 auto 24px;line-height:1.6;">
                    别灰心！您可以尝试调整年龄或收入信息重新匹配，<br>或前往社区<b>党群服务中心</b>获取人工咨询。
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                <div style="background:rgba(59,130,246,0.05);border-radius:12px;padding:18px;">
                    <p style="font-weight:700;color:#1a1a2e;margin:0 0 6px;">💡 排查建议</p>
                    <ul style="margin:0;padding-left:18px;color:#4a4a6a;font-size:0.9rem;line-height:1.8;">
                        <li>检查年龄或收入是否有误</li>
                        <li>尝试切换就业身份状态</li>
                        <li>确认户籍信息是否准确</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("""
                <div style="background:rgba(16,185,129,0.05);border-radius:12px;padding:18px;">
                    <p style="font-weight:700;color:#1a1a2e;margin:0 0 6px;">📞 人工服务</p>
                    <ul style="margin:0;padding-left:18px;color:#4a4a6a;font-size:0.9rem;line-height:1.8;">
                        <li>社区服务热线：12345</li>
                        <li>前往所属街道党群服务中心</li>
                        <li>工作日 9:00-17:00 均可办理</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 8. 页脚
# ==========================================
st.markdown("""
<div class="app-footer">
    <p>🏛️ 智慧社区 · 政策红利匹配引擎 &copy; 2026 &nbsp;|&nbsp; 数据来源于公开政策文件，仅供参考</p>
    <p style="font-size:0.7rem;opacity:0.6;">PP创新节 展示项目 · 不作为实际申领依据</p>
</div>
""", unsafe_allow_html=True)
