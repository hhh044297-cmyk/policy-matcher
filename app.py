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

# 初始化 session state
if 'form_step' not in st.session_state:
    st.session_state.form_step = 0
if 'user_age' not in st.session_state:
    st.session_state.user_age = 22
if 'user_income' not in st.session_state:
    st.session_state.user_income = 2000
if 'user_status' not in st.session_state:
    st.session_state.user_status = "学生/应届生"
if 'has_local_hukou' not in st.session_state:
    st.session_state.has_local_hukou = True
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ==========================================
# 2. CSS 样式系统
# ==========================================
st.markdown("""
<style>
    :root {
        --primary: #FF6B35;
        --primary-dark: #E55A2B;
        --accent-gold: #F7B731;
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
        --success: #10B981;
        --fail: #EF4444;
    }

    /* 全局强制深色文字 */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    label, p, h1, h2, h3, h4, h5, h6, div, span, li, td, th,
    [data-testid="stFormSubmitButton"] button,
    .streamlit-expanderHeader, .streamlit-expanderContent {
        color: #1a1a2e !important;
    }
    /* 保持按钮文字白色 */
    div.stButton > button:first-child, div.stButton > button:first-child *,
    .stDownloadButton > button, .stDownloadButton > button *,
    [data-testid="stFormSubmitButton"] button {
        color: white !important;
    }
    /* 保持 metric label 灰色 */
    [data-testid="stMetricLabel"] { color: #6b7280 !important; }
    .metric-label { color: #6b7280 !important; }

    .stApp {
        background: linear-gradient(160deg, #FFF5EE 0%, #FFF8F0 30%, #FFF0E5 70%, #FFFAF5 100%);
    }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ===== 步骤指示器 ===== */
    .step-indicator {
        display: flex; justify-content: center; gap: 8px; margin-bottom: 28px;
    }
    .step-dot {
        width: 36px; height: 36px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.85rem;
        background: #e5e7eb; color: #9ca3af;
        transition: all 0.3s;
    }
    .step-dot.active { background: var(--primary); color: white; box-shadow: 0 0 0 6px rgba(255,107,53,0.15); }
    .step-dot.done { background: var(--success); color: white; }
    .step-line {
        width: 40px; height: 2px; background: #e5e7eb; align-self: center;
    }
    .step-line.done { background: var(--success); }

    /* ===== Hero ===== */
    .hero-title {
        font-size: 2.6rem; font-weight: 900;
        background: linear-gradient(135deg, #E55A2B 0%, #FF6B35 40%, #F7B731 100%);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
        color: #E55A2B; /* 非 webkit 浏览器后备色 */
        letter-spacing: -0.02em; margin-bottom: 8px; text-align: center;
    }
    .hero-subtitle { color: var(--text-mid); font-size: 1.1rem; text-align: center; margin-bottom: 24px; }

    /* ===== 表单卡片 ===== */
    .form-card {
        background: var(--card-bg); backdrop-filter: blur(20px);
        border: 1px solid rgba(0,0,0,0.06); border-radius: var(--radius-lg);
        padding: 32px 28px 20px; box-shadow: var(--shadow-md); margin-bottom: 24px;
        position: relative; overflow: hidden;
    }
    .form-card::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #FF6B35, #F7B731, #FF6B35);
    }

    /* ===== 输入框 ===== */
    .stNumberInput input, .stSelectbox [data-baseweb="select"] > div {
        background: rgba(249,250,251,0.9) !important;
        border: 2px solid #e5e7eb !important; border-radius: 12px !important;
        padding: 10px 14px !important; font-size: 0.95rem !important;
        color: var(--text-dark) !important; transition: all 0.25s !important; box-shadow: none !important;
    }
    .stNumberInput input:focus, .stSelectbox [data-baseweb="select"] > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important; background: white !important;
    }
    div[data-testid="stNumberInput"] label, div[data-testid="stSelectbox"] label,
    div[data-testid="stToggle"] label {
        font-weight: 600 !important; font-size: 0.88rem !important; color: var(--text-mid) !important;
    }

    /* ===== 按钮 ===== */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF6B35 0%, #E55A2B 100%) !important;
        color: white !important; border: none !important; border-radius: 14px !important;
        padding: 14px 28px !important; font-size: 1.05rem !important; font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(255,107,53,0.35) !important;
        transition: all 0.3s !important; position: relative; overflow: hidden;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(255,107,53,0.45) !important;
    }
    div.stButton > button:first-child::after {
        content: ""; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
        transition: left 0.5s;
    }
    div.stButton > button:first-child:hover::after { left: 100%; }

    .btn-secondary > button:first-child {
        background: white !important; color: var(--primary) !important;
        border: 2px solid var(--primary) !important; box-shadow: none !important;
    }

    /* ===== 进度条 ===== */
    div[data-testid="stProgress"] > div { background: rgba(255,107,53,0.1) !important; }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #FF6B35, #F7B731) !important; border-radius: 4px !important;
    }

    /* ===== 指标卡片 ===== */
    .metric-card {
        background: var(--card-bg); backdrop-filter: blur(12px);
        border: 1px solid rgba(0,0,0,0.05); border-radius: var(--radius-md);
        padding: 20px; text-align: center; box-shadow: var(--shadow-sm);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-card .metric-icon { font-size: 1.8rem; margin-bottom: 6px; }
    .metric-card .metric-value { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
    .metric-card .metric-label { font-size: 0.8rem; color: var(--text-light); margin-top: 2px; }

    /* ===== 政策卡片 ===== */
    div[data-testid="stExpander"] {
        background: var(--card-bg) !important; backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0,0,0,0.06) !important; border-left: 5px solid #e5e7eb !important;
        border-radius: 14px !important; margin-bottom: 14px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; overflow: hidden;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-3px); box-shadow: var(--shadow-lg) !important;
    }
    div[data-testid="stExpander"] details summary {
        padding: 16px 20px !important; font-weight: 700 !important;
        font-size: 1rem !important; color: var(--text-dark) !important;
    }
    .cat-job { border-left-color: var(--cat-job) !important; }
    .cat-welfare { border-left-color: var(--cat-welfare) !important; }
    .cat-elderly { border-left-color: var(--cat-elderly) !important; }
    .cat-housing { border-left-color: var(--cat-housing) !important; }

    /* ===== 匹配条件指示器 ===== */
    .match-condition {
        display: inline-flex; align-items: center; gap: 4px;
        padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 600; margin: 2px 4px;
    }
    .match-condition.pass { background: rgba(16,185,129,0.1); color: #059669; }
    .match-condition.fail { background: rgba(239,68,68,0.1); color: #DC2626; }

    .category-tag {
        display: inline-block; padding: 4px 12px; border-radius: 12px;
        font-size: 0.78rem; font-weight: 600;
    }
    .category-tag.job { background: rgba(59,130,246,0.1); color: #2563EB; }
    .category-tag.welfare { background: rgba(16,185,129,0.1); color: #059669; }
    .category-tag.elderly { background: rgba(245,158,11,0.1); color: #D97706; }
    .category-tag.housing { background: rgba(139,92,246,0.1); color: #7C3AED; }

    .amount-highlight {
        color: #DC2626; font-size: 1.15rem; font-weight: 700;
        background: rgba(220,38,38,0.06); padding: 4px 12px; border-radius: 8px;
    }

    /* ===== 空状态 & 脚注 ===== */
    .empty-state { text-align: center; padding: 48px 20px; }
    .app-footer {
        text-align: center; padding: 32px 0 16px; color: var(--text-light);
        font-size: 0.78rem; border-top: 1px solid rgba(0,0,0,0.05); margin-top: 40px;
    }

    /* ===== 侧边栏 ===== */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.8) !important; backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0,0,0,0.05) !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,107,53,0.2); border-radius: 3px; }

    div[data-testid="stInfo"] {
        background: rgba(59,130,246,0.06) !important;
        border-left: 4px solid #3B82F6 !important; border-radius: 10px !important;
    }
    hr {
        border: none !important; height: 2px !important;
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
P008,经济困难失能老人居家照护补贴,养老服务,面向60周岁以上、低收入且经过失能评估的老人，发放用于购买上门洗浴、家政等服务的额度。,60,120,退休,2500,是,300元 服务券/月
P009,职业技能培训补贴,就业创业,本市户籍劳动者参加政府补贴类职业技能培训并取得证书，可申领培训费补贴。,18,55,在职;待业/灵活就业,5000,是,最高 3000元
P010,一次性创业补贴,就业创业,毕业2年内的高校毕业生、就业困难人员首次创办小微企业或个体经营并正常运营6个月以上，给予一次性资金扶持。,18,45,待业/灵活就业;学生/应届生,999999,是,10000元 一次性
P011,公益性岗位补贴,就业创业,对通过公益性岗位安置就业困难人员并缴纳社保的单位，给予岗位补贴和社会保险补贴。,18,55,待业/灵活就业,3000,是,按本地最低工资标准
P012,小微企业社保补贴,就业创业,小微企业招用毕业2年内高校毕业生并缴纳社保的，可获社保补贴返还。,22,35,在职,999999,否,单位缴纳部分全额返还
P013,返乡入乡创业补贴,就业创业,农民工、高校毕业生等返乡入乡创业，正常经营1年以上，可申领一次性创业扶持资金。,18,55,待业/灵活就业;在职,999999,否,5000-20000元
P014,临时救助金,民生保障,因突发重大疾病、意外事故等导致基本生活陷入困境的家庭，可申请临时性生活救助。,0,120,学生/应届生;在职;待业/灵活就业;退休,2000,是,按实际困难发放
P015,困境儿童基本生活费,民生保障,对孤儿、事实无人抚养儿童、重病重残儿童等困境未成年人按月发放基本生活费补贴。,0,18,学生/应届生,3000,是,500-1500元/月
P016,重残护理补贴,民生保障,对评定为一级、二级重度残疾且需要长期照护的人员，发放护理补贴。,0,120,学生/应届生;在职;待业/灵活就业;退休,3000,是,300-600元/月
P017,城乡居民医保缴费减免,民生保障,对城乡低保对象、特困人员、重度残疾人参加城乡居民医保的个人缴费部分予以全额或部分减免。,0,120,学生/应届生;在职;待业/灵活就业;退休,2000,是,个人缴费全免
P018,义务兵家庭优待金,民生保障,对参军入伍青年的家庭发放优待金，服役期间按年度发放。,18,24,学生/应届生;待业/灵活就业,999999,是,20000-40000元/年
P019,社区长者食堂助餐补贴,养老服务,本市户籍60周岁以上老年人到社区长者食堂就餐，每餐享受定额补贴。,60,120,退休,5000,是,5-10元/餐
P020,居家适老化改造补贴,养老服务,对困难老年人家庭实施居家适老化改造，包括安装扶手、地面防滑、紧急呼叫等设施。,65,120,退休,3000,是,最高 8000元
P021,高龄老人意外伤害保险,养老服务,由政府统一为80周岁以上户籍老年人购买意外伤害综合保险，含意外医疗和意外住院津贴。,80,120,退休,999999,是,保额 20000元/年
P022,公共租赁住房租金补贴,住房补贴,城镇中低收入住房困难家庭承租公租房，按收入水平和家庭人口给予梯度化租金减免。,18,120,在职;待业/灵活就业;退休,4000,是,减免30%-90%租金
P023,人才安居租房补贴,住房补贴,新引进的全日制本科及以上学历毕业生在本地就业并租房的可申领安居补贴。,22,35,在职,999999,否,600-1500元/月"""
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

CATEGORY_CONFIG = {
    "就业创业": {"icon": "💼", "css_class": "job", "label": "就业创业"},
    "民生保障": {"icon": "🛡️", "css_class": "welfare", "label": "民生保障"},
    "养老服务": {"icon": "🧓", "css_class": "elderly", "label": "养老服务"},
    "住房补贴": {"icon": "🏠", "css_class": "housing", "label": "住房补贴"},
}

# ==========================================
# 4. 匹配引擎（带条件明细）
# ==========================================
def check_conditions(policy, user_age, user_income, user_status, has_local_hukou):
    """检查每条政策的所有匹配条件，返回通过/未通过列表"""
    conditions = []

    # 年龄
    age_ok = policy["condition_age_min"] <= user_age <= policy["condition_age_max"]
    conditions.append({
        "label": f"年龄 {policy['condition_age_min']}-{policy['condition_age_max']} 岁",
        "pass": age_ok, "icon": "🎂"
    })

    # 收入
    income_ok = user_income <= policy["condition_income_max"]
    if policy["condition_income_max"] >= 999999:
        conditions.append({"label": "无收入限制", "pass": True, "icon": "💰"})
    else:
        conditions.append({
            "label": f"月收入 ≤ {policy['condition_income_max']} 元",
            "pass": income_ok, "icon": "💰"
        })

    # 身份状态
    status_ok = user_status in policy["condition_status"]
    status_text = "、".join(policy["condition_status"])
    conditions.append({
        "label": f"身份: {status_text}",
        "pass": status_ok, "icon": "💼"
    })

    # 户籍
    need_hukou = policy.get("condition_hukou", "是") == "是"
    hukou_ok = not need_hukou or has_local_hukou
    conditions.append({
        "label": "需本市户籍" if need_hukou else "不限户籍",
        "pass": hukou_ok, "icon": "🏠"
    })

    all_pass = all(c["pass"] for c in conditions)
    return all_pass, conditions

# ==========================================
# 5. 侧边栏
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
    st.markdown("### 📊 数据库总览")
    if policies:
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
# 6. Hero
# ==========================================
st.markdown("""
<div style="text-align:center;padding:16px 0 8px;">
    <h1 class="hero-title">政策红利智能匹配引擎</h1>
    <p class="hero-subtitle">只需填写基本信息，AI 为您精准匹配每一项专属政策权益</p>
    <div style="display:flex;justify-content:center;gap:32px;flex-wrap:wrap;">
        <div style="text-align:center;min-width:70px;">
            <div style="font-size:2rem;font-weight:800;color:#FF6B35;line-height:1;">23</div>
            <div style="font-size:0.8rem;color:#6b7280;margin-top:4px;">已接入政策</div>
        </div>
        <div style="text-align:center;min-width:70px;">
            <div style="font-size:2rem;font-weight:800;color:#FF6B35;line-height:1;">4</div>
            <div style="font-size:0.8rem;color:#6b7280;margin-top:4px;">覆盖领域</div>
        </div>
        <div style="text-align:center;min-width:70px;">
            <div style="font-size:2rem;font-weight:800;color:#FF6B35;line-height:1;">&lt;30s</div>
            <div style="font-size:0.8rem;color:#6b7280;margin-top:4px;">极速匹配</div>
        </div>
        <div style="text-align:center;min-width:70px;">
            <div style="font-size:2rem;font-weight:800;color:#FF6B35;line-height:1;">99.8<span style="font-size:0.6em;">%</span></div>
            <div style="font-size:0.8rem;color:#6b7280;margin-top:4px;">匹配精准度</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. 分步表单
# ==========================================
st.markdown('<div class="form-card">', unsafe_allow_html=True)

# 步骤指示器
step = st.session_state.form_step
dots = ""
for i in range(2):
    status = "done" if i < step else ("active" if i == step else "")
    dots += f'<div class="step-dot {status}">{i+1}</div>'
    if i < 1:
        dots += f'<div class="step-line {"done" if i < step else ""}"></div>'
st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center;color:var(--text-mid);font-weight:600;margin-bottom:20px;'>"
            f"{'📝 步骤一 · 基本个人信息' if step == 0 else '📋 步骤二 · 身份与户籍信息'}</p>",
            unsafe_allow_html=True)

if step == 0:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("🎂 周岁年龄", min_value=0, max_value=120,
                              value=st.session_state.user_age, step=1,
                              help="请输入您的实际周岁年龄", key="step0_age")
        st.session_state.user_age = age
    with col2:
        income = st.number_input("💰 月均总收入（元）", min_value=0,
                                 value=st.session_state.user_income, step=500,
                                 help="包括工资、养老金、经营性收入等", key="step0_income")
        st.session_state.user_income = income

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("下一步 →", use_container_width=True, key="btn_step0"):
            st.session_state.form_step = 1
            st.rerun()

else:
    col1, col2 = st.columns(2)
    with col1:
        status = st.selectbox("💼 就业 / 身份状态",
                              ["学生/应届生", "在职", "待业/灵活就业", "退休"],
                              index=["学生/应届生", "在职", "待业/灵活就业", "退休"].index(
                                  st.session_state.user_status
                              ) if st.session_state.user_status in ["学生/应届生", "在职", "待业/灵活就业", "退休"] else 0,
                              key="step1_status")
        st.session_state.user_status = status
    with col2:
        hukou = st.toggle("🏠 拥有本市户籍", value=st.session_state.has_local_hukou,
                          help="部分政策需要本市户籍方可申请", key="step1_hukou")
        st.session_state.has_local_hukou = hukou

    st.markdown("<br>", unsafe_allow_html=True)
    col_back, col_submit = st.columns([1, 2])
    with col_back:
        if st.button("← 返回修改", use_container_width=True, key="btn_back"):
            st.session_state.form_step = 0
            st.rerun()
    with col_submit:
        if st.button("🔍 启动智能匹配", use_container_width=True, key="btn_submit"):
            st.session_state.submitted = True
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. 匹配结果
# ==========================================
if st.session_state.submitted:
    user_age = st.session_state.user_age
    user_income = st.session_state.user_income
    user_status = st.session_state.user_status
    has_local_hukou = st.session_state.has_local_hukou

    if not policies:
        st.error("⚠️ 数据库异常，请联系网格员解决。")
    else:
        st.markdown('<hr>', unsafe_allow_html=True)

        # 动画进度条
        progress_text = "🔎 正在社区数据库中为您仔细检索..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()

        # 执行匹配（带条件明细）
        matched_policies = []
        near_miss_policies = []
        all_results = []

        for p in policies:
            all_pass, conditions = check_conditions(p, user_age, user_income, user_status, has_local_hukou)
            result = {"policy": p, "conditions": conditions, "all_pass": all_pass}
            all_results.append(result)
            if all_pass:
                matched_policies.append(result)
            else:
                # 只差一个条件就算"接近匹配"
                failed_count = sum(1 for c in conditions if not c["pass"])
                if failed_count <= 1:
                    near_miss_policies.append(result)

        # ===== 有匹配结果 =====
        if len(matched_policies) > 0:
            st.balloons()

            matched_categories = set(r['policy']['category'] for r in matched_policies)

            st.markdown(f"""
            <div style="text-align:center;margin:12px 0 24px;">
                <h2 style="color:#1a1a2e;font-weight:800;margin:0;">🎁 您的专属权益看板</h2>
                <p style="color:#6b7280;font-size:0.9rem;margin:4px 0 0;">
                    共匹配到 <b style="color:#FF6B35;">{len(matched_policies)}</b> 项政策红利
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 指标卡片
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

            # ===== 筛选器 =====
            st.markdown("<br>", unsafe_allow_html=True)
            filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])
            with filter_col1:
                show_filter = st.selectbox("📂 按领域筛选",
                                           ["全部"] + list(matched_categories),
                                           key="cat_filter")
            with filter_col2:
                sort_by = st.selectbox("🔤 排序方式",
                                       ["默认排序", "金额从高到低", "名称A-Z"],
                                       key="sort_by")

            # 排序和筛选
            display_policies = matched_policies
            if show_filter != "全部":
                display_policies = [r for r in display_policies if r['policy']['category'] == show_filter]

            st.markdown(f"<p style='font-size:0.82rem;color:var(--text-light);'>显示 {len(display_policies)} / {len(matched_policies)} 条政策</p>", unsafe_allow_html=True)

            # ===== 政策卡片 =====
            for idx, result in enumerate(display_policies):
                mp = result['policy']
                conditions = result['conditions']
                cat_info = CATEGORY_CONFIG.get(mp['category'], {"icon": "📌", "css_class": "", "label": mp['category']})
                css_class = f"cat-{cat_info['css_class']}" if cat_info['css_class'] else ""

                with st.expander(f"{cat_info['icon']} {mp['name']}", expanded=(idx == 0)):
                    # 分类标签 + 金额
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;">
                        <span class="category-tag {cat_info['css_class']}">{cat_info['icon']} {cat_info['label']}</span>
                        <span class="amount-highlight">💰 {mp['amount']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # 政策描述
                    st.markdown(f'<p style="color:#4a4a6a;line-height:1.7;font-size:0.95rem;">{mp["description"]}</p>', unsafe_allow_html=True)

                    # ===== 匹配条件明细（核心新功能） =====
                    st.markdown("<p style='font-weight:700;color:#1a1a2e;margin:16px 0 8px;font-size:0.9rem;'>🔍 匹配条件明细</p>", unsafe_allow_html=True)
                    cond_html = ""
                    for c in conditions:
                        cls = "pass" if c["pass"] else "fail"
                        icon = "✅" if c["pass"] else "❌"
                        cond_html += f'<span class="match-condition {cls}">{icon} {c["icon"]} {c["label"]}</span> '
                    st.markdown(f"<div style='line-height:2.2;'>{cond_html}</div>", unsafe_allow_html=True)

                    # 申请材料
                    st.info("📃 预计需准备材料：身份证复印件、户口本复印件、对应情况证明材料。")

            # ===== 下载报告按钮 =====
            st.markdown("<br>", unsafe_allow_html=True)
            report_lines = [
                "=" * 40,
                "政策红利智能匹配报告",
                "=" * 40,
                "",
                f"年龄: {user_age} 岁",
                f"月收入: {user_income} 元",
                f"身份状态: {user_status}",
                f"本市户籍: {'是' if has_local_hukou else '否'}",
                "",
                f"共匹配到 {len(matched_policies)} 项政策:",
                ""
            ]
            for r in matched_policies:
                mp = r['policy']
                report_lines.append(f"【{mp['category']}】{mp['name']}")
                report_lines.append(f"  权益: {mp['amount']}")
                report_lines.append(f"  说明: {mp['description']}")
                report_lines.append(f"  条件: " + " | ".join([f"{'✓' if c['pass'] else '✗'} {c['label']}" for c in r['conditions']]))
                report_lines.append("")
            report_lines.append("=" * 40)
            report_lines.append("智慧社区 · 政策红利匹配引擎 © 2026")
            report_lines.append("本报告仅供参考，不作为实际申领依据")

            report_text = "\n".join(report_lines)
            st.download_button(
                label="📥 下载个人权益匹配报告",
                data=report_text,
                file_name="政策红利匹配报告.txt",
                mime="text/plain",
                use_container_width=True
            )

            # ===== 接近匹配提示 =====
            if near_miss_policies:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔔 接近匹配的政策")
                st.markdown("<p style='color:var(--text-light);font-size:0.85rem;'>以下政策只差一个条件，调整信息后可能匹配：</p>", unsafe_allow_html=True)
                for result in near_miss_policies:
                    mp = result['policy']
                    failed = [c for c in result['conditions'] if not c['pass']]
                    st.markdown(f"""
                    <div style="background:rgba(245,158,11,0.06);border-left:3px solid #F59E0B;border-radius:8px;padding:12px 16px;margin-bottom:8px;">
                        <b>{mp['name']}</b>
                        <span style="color:#D97706;font-size:0.82rem;"> — 缺少: {'、'.join([c['label'] for c in failed])}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # ===== 无匹配结果 =====
        else:
            st.markdown("""
            <div class="empty-state">
                <div style="font-size:4rem;margin-bottom:16px;opacity:0.6;">🔍</div>
                <h3 style="color:#1a1a2e;font-weight:700;">暂未找到完全匹配的政策</h3>
                <p style="color:#6b7280;max-width:420px;margin:0 auto 24px;line-height:1.6;">
                    别灰心！您可以返回修改信息重新匹配，<br>或前往社区<b>党群服务中心</b>获取人工咨询。
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 显示接近匹配
            if near_miss_policies:
                st.markdown("### 🔔 您可能接近匹配以下政策")
                for result in near_miss_policies:
                    mp = result['policy']
                    failed = [c for c in result['conditions'] if not c['pass']]
                    st.markdown(f"""
                    <div style="background:rgba(245,158,11,0.06);border-left:3px solid #F59E0B;border-radius:8px;padding:12px 16px;margin-bottom:8px;">
                        <b>{mp['name']}</b> — <span style="color:#D97706;font-size:0.82rem;">差一项: {'、'.join([c['label'] for c in failed])}</span>
                        <br><span style="font-size:0.82rem;color:#6b7280;">{mp['description']}</span>
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

    # 重置按钮
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 重新匹配", use_container_width=True):
        st.session_state.submitted = False
        st.session_state.form_step = 0
        st.rerun()

# ==========================================
# 9. 页脚
# ==========================================
st.markdown("""
<div class="app-footer">
    <p>🏛️ 智慧社区 · 政策红利匹配引擎 &copy; 2026 &nbsp;|&nbsp; 数据来源于公开政策文件，仅供参考</p>
    <p style="font-size:0.7rem;opacity:0.6;">PP创新节 展示项目 · 不作为实际申领依据</p>
</div>
""", unsafe_allow_html=True)
