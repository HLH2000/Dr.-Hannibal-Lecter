import streamlit as st
import random
import json

# ══════════════════════════════════════════════
# 頁面設定
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="下肢神經肌肉分類遊戲 🦵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────── GitHub 圖片路徑 ───────────────
GITHUB_BASE   = "https://raw.githubusercontent.com/HLH2000/Dr.-Hannibal-Lecter/main/"
MUSCLE_BASE   = GITHUB_BASE + "muscle/"
NERVE_BASE    = GITHUB_BASE + "nerve/"

def muscle_img(n: int) -> str:
    return f"{MUSCLE_BASE}muscle_lowerlimbs_{n}.jpg"

def nerve_img(n: int) -> str:
    return f"{NERVE_BASE}nerve_lowerlimbs_{n}.jpg"

# ─────────────── 神經資料 ───────────────
NERVES = [
    {"id": "sup_glut",  "zh": "上臀神經",   "en": "Sup. Gluteal n.",         "color": "#0F6E56", "light": "#E1F5EE", "img_pair": [1,  2]},
    {"id": "inf_glut",  "zh": "下臀神經",   "en": "Inf. Gluteal n.",         "color": "#185FA5", "light": "#E6F1FB", "img_pair": [3,  4]},
    {"id": "femoral",   "zh": "股神經",     "en": "Femoral n.",              "color": "#534AB7", "light": "#EEEDFE", "img_pair": [5,  6]},
    {"id": "obturator", "zh": "閉孔神經",   "en": "Obturator n.",            "color": "#993C1D", "light": "#FAECE7", "img_pair": [7,  8]},
    {"id": "sciatic",   "zh": "坐骨神經",   "en": "Sciatic n.",              "color": "#7C3AED", "light": "#EDE9FE", "img_pair": [9,  10]},
    {"id": "com_fib",   "zh": "總腓神經",   "en": "Common fibular n.",       "color": "#3B6D11", "light": "#EAF3DE", "img_pair": [11, 12]},
    {"id": "sup_fib",   "zh": "淺腓神經",   "en": "Superficial fibular n.",  "color": "#854F0B", "light": "#FAEEDA", "img_pair": [13, 14]},
    {"id": "deep_fib",  "zh": "深腓神經",   "en": "Deep fibular n.",         "color": "#A32D2D", "light": "#FCEBEB", "img_pair": [15, 16]},
    {"id": "tibial",    "zh": "脛神經",     "en": "Tibial n.",               "color": "#0C6478", "light": "#CFFAFE", "img_pair": [17, 18]},
    {"id": "med_plan",  "zh": "內蹠神經",   "en": "Medial plantar n.",       "color": "#6D28D9", "light": "#EDE9FE", "img_pair": [19, 20]},
    {"id": "lat_plan",  "zh": "外蹠神經",   "en": "Lateral plantar n.",      "color": "#065F46", "light": "#D1FAE5", "img_pair": [21, 22]},
]
NERVE_MAP  = {n["id"]: n for n in NERVES}
NERVE_KEYS = [n["id"] for n in NERVES]
NERVE_KEY_TO_NERVE = {n["id"]: n for n in NERVES}

# ─────────────── 肌肉資料 ───────────────
MUSCLES = [
    {"id": "glut_med",    "zh": "臀中肌",       "en": "Gluteus medius m.",                 "imgs": [1,  2],  "nerves": ["sup_glut"],             "dual": False},
    {"id": "glut_min",    "zh": "臀小肌",       "en": "Gluteus minimus m.",                "imgs": [3,  4],  "nerves": ["sup_glut"],             "dual": False},
    {"id": "tfl",         "zh": "擴筋膜張肌",   "en": "Tensor fasciae latae m.",           "imgs": [5,  6],  "nerves": ["sup_glut"],             "dual": False},
    {"id": "glut_max",    "zh": "臀大肌",       "en": "Gluteus maximus m.",                "imgs": [7,  8],  "nerves": ["inf_glut"],             "dual": False},
    {"id": "quad_fem",    "zh": "股四頭肌",     "en": "Quadriceps femoris m.",             "imgs": [9,  10], "nerves": ["femoral"],              "dual": False},
    {"id": "rect_fem",    "zh": "股直肌",       "en": "Rectus femoris m.",                 "imgs": [11, 12], "nerves": ["femoral"],              "dual": False},
    {"id": "vas_lat",     "zh": "股外側肌",     "en": "Vastus lateralis m.",               "imgs": [13, 14], "nerves": ["femoral"],              "dual": False},
    {"id": "vas_med",     "zh": "股內側肌",     "en": "Vastus medialis m.",                "imgs": [15, 16], "nerves": ["femoral"],              "dual": False},
    {"id": "vas_int",     "zh": "股中間肌",     "en": "Vastus intermedius m.",             "imgs": [17, 18], "nerves": ["femoral"],              "dual": False},
    {"id": "sartorius",   "zh": "縫匠肌",       "en": "Sartorius m.",                      "imgs": [19, 20], "nerves": ["femoral"],              "dual": False},
    {"id": "pectineus",   "zh": "恥骨肌",       "en": "Pectineus m.",                      "imgs": [21, 22], "nerves": ["femoral", "obturator"], "dual": True},
    {"id": "gracilis",    "zh": "股薄肌",       "en": "Gracilis m.",                       "imgs": [23, 24], "nerves": ["obturator"],            "dual": False},
    {"id": "add_mag",     "zh": "內收大肌",     "en": "Adductor magnus m.",                "imgs": [25, 26], "nerves": ["obturator", "sciatic"], "dual": True},
    {"id": "add_lon",     "zh": "內收長肌",     "en": "Adductor longus m.",                "imgs": [27, 28], "nerves": ["obturator"],            "dual": False},
    {"id": "add_bre",     "zh": "內收短肌",     "en": "Adductor brevis m.",                "imgs": [29, 30], "nerves": ["obturator"],            "dual": False},
    {"id": "bic_lon",     "zh": "股二頭肌長頭", "en": "Biceps femoris (long head)",       "imgs": [31, 32], "nerves": ["tibial"],               "dual": True},
    {"id": "bic_sho",     "zh": "股二頭肌短頭", "en": "Biceps femoris (short head)",      "imgs": [33, 34], "nerves": ["com_fib"],              "dual": True},
    {"id": "semiten",     "zh": "半腱肌",       "en": "Semitendinosus m.",                 "imgs": [35, 36], "nerves": ["sciatic", "tibial"],    "dual": True},
    {"id": "semimem",     "zh": "半膜肌",       "en": "Semimembranosus m.",                "imgs": [37, 38], "nerves": ["sciatic", "tibial"],    "dual": True},
    {"id": "fib_lon",     "zh": "腓長肌",       "en": "Fibularis longus m.",               "imgs": [39, 40], "nerves": ["sup_fib"],              "dual": False},
    {"id": "fib_bre",     "zh": "腓短肌",       "en": "Fibularis brevis m.",               "imgs": [41, 42], "nerves": ["sup_fib"],              "dual": False},
    {"id": "tib_ant",     "zh": "脛前肌",       "en": "Tibialis anterior m.",              "imgs": [43, 44], "nerves": ["deep_fib"],             "dual": False},
    {"id": "ext_dig_lon", "zh": "伸趾長肌",     "en": "Extensor digitorum longus m.",      "imgs": [45, 46], "nerves": ["deep_fib"],             "dual": False},
    {"id": "ext_hal_lon", "zh": "伸姆長肌",     "en": "Extensor hallucis longus m.",       "imgs": [47, 48], "nerves": ["deep_fib"],             "dual": False},
    {"id": "fib_ter",     "zh": "第三腓骨肌",   "en": "Fibularis tertius m.",              "imgs": [49, 50], "nerves": ["deep_fib"],             "dual": False},
    {"id": "ext_dig_bre", "zh": "伸趾短肌",     "en": "Extensor digitorum brevis m.",      "imgs": [51, 52], "nerves": ["deep_fib"],             "dual": False},
    {"id": "ext_hal_bre", "zh": "伸姆短肌",     "en": "Extensor hallucis brevis m.",       "imgs": [53, 54], "nerves": ["deep_fib"],             "dual": False},
    {"id": "gastro",      "zh": "腓腸肌",       "en": "Gastrocnemius m.",                  "imgs": [55, 56], "nerves": ["tibial"],               "dual": False},
    {"id": "soleus",      "zh": "比目魚肌",     "en": "Soleus m.",                         "imgs": [57, 58], "nerves": ["tibial"],               "dual": False},
    {"id": "plantaris",   "zh": "蹠肌",         "en": "Plantaris m.",                      "imgs": [59, 60], "nerves": ["tibial"],               "dual": False},
    {"id": "tib_pos",     "zh": "脛後肌",       "en": "Tibialis posterior m.",             "imgs": [61, 62], "nerves": ["tibial"],               "dual": False},
    {"id": "fle_hal_lon", "zh": "屈姆長肌",     "en": "Flexor hallucis longus m.",         "imgs": [63, 64], "nerves": ["tibial"],               "dual": False},
    {"id": "fle_dig_lon", "zh": "屈趾長肌",     "en": "Flexor digitorum longus m.",        "imgs": [65, 66], "nerves": ["tibial"],               "dual": False},
    {"id": "poplit",      "zh": "膕肌",         "en": "Popliteus m.",                      "imgs": [67, 68], "nerves": ["tibial"],               "dual": False},
    {"id": "fle_dig_bre", "zh": "屈趾短肌",     "en": "Flexor digitorum brevis m.",        "imgs": [69, 70], "nerves": ["med_plan"],             "dual": False},
    {"id": "abd_hal",     "zh": "外展姆肌",     "en": "Abductor hallucis m.",              "imgs": [71, 72], "nerves": ["med_plan"],             "dual": False},
    {"id": "quad_pla",    "zh": "掌方肌",       "en": "Quadratus plantae m.",              "imgs": [73, 74], "nerves": ["lat_plan"],             "dual": False},
    {"id": "fle_hal_bre", "zh": "屈姆短肌",     "en": "Flexor hallucis brevis m.",         "imgs": [75, 76], "nerves": ["med_plan"],             "dual": False},
    {"id": "lumb1",       "zh": "內側第1蚓狀肌","en": "Medial 1st lumbrical m.",           "imgs": [77, 78], "nerves": ["med_plan"],             "dual": False},
    {"id": "abd_dmi",     "zh": "外展小趾肌",   "en": "Abductor digiti minimi m.",         "imgs": [79, 80], "nerves": ["lat_plan"],             "dual": False},
    {"id": "fle_dmi_bre", "zh": "屈小趾短肌",   "en": "Flexor digiti minimi brevis m.",    "imgs": [81, 82], "nerves": ["lat_plan"],             "dual": False},
    {"id": "lumb23",      "zh": "外側1-3蚓狀肌","en": "Lat. 1-3 lumbrical m.",             "imgs": [83, 84], "nerves": ["lat_plan"],             "dual": False},
    {"id": "add_hal",     "zh": "內收姆肌",     "en": "Adductor hallucis m.",              "imgs": [85, 86], "nerves": ["lat_plan"],             "dual": False},
    {"id": "plan_int",    "zh": "掌骨中間肌",   "en": "Plantar interosseous m.",           "imgs": [87, 88], "nerves": ["lat_plan"],             "dual": False},
    {"id": "dors_int",    "zh": "背骨中間肌",   "en": "Dorsal interosseous m.",            "imgs": [89, 90], "nerves": ["lat_plan"],             "dual": False},
]
MUSCLE_MAP = {m["id"]: m for m in MUSCLES}
TOTAL_NEEDED = sum(len(m["nerves"]) for m in MUSCLES)
SEP = "|||"
BASE_SCORE = 50


# ══════════════════════════════════════════════
# query_params 讀寫輔助（JS 寫 selected，Python 讀）
# ══════════════════════════════════════════════
def read_selected() -> set:
    raw = st.query_params.get("sel", "")
    if not raw:
        return set()
    return set(raw.split(SEP))

def read_img_mode() -> str:
    return st.query_params.get("img_mode", "text")

# ══════════════════════════════════════════════
# 初始化
# ══════════════════════════════════════════════
def init_game():
    deck = [m["id"] for m in MUSCLES]
    random.shuffle(deck)
    st.session_state.update({
        "game_init":    True,
        "score":        0,
        "submit_count": 0,
        "locked":       False,
        "scored_keys":  set(),
        "result":       {},
        "placed":       {n["id"]: [] for n in NERVES},
        "message":      "",
        "message_type": "info",
        "return_wrong": False,
        "deck":         deck,
    })
    st.query_params.clear()

if "game_init" not in st.session_state:
    init_game()

selected = read_selected()
img_mode = read_img_mode()


# ──────────────────────────────────────────────
# 核心邏輯 (使用 On_click Callbacks)
# ──────────────────────────────────────────────

def place_cards(nerve_id: str):
    """將選中的手牌放入目標神經區"""
    placed  = st.session_state.placed
    scored  = st.session_state.scored_keys
    result  = st.session_state.result
    
    sel_raw = st.query_params.get("sel", "")
    current_selected = set(sel_raw.split(SEP)) if sel_raw else set()

    if not current_selected:
        st.session_state.message = "⚠️ 請先點選手牌卡片！"
        st.session_state.message_type = "warning"
        return

    count = 0
    for mid in list(current_selected):
        m = MUSCLE_MAP.get(mid)
        if not m:
            continue
        if mid in placed[nerve_id]:
            continue
        
        # 非雙重神經支配：先從其他分類移除（未批改的）
        if not m["dual"]:
            for other_nid in NERVE_KEYS:
                if other_nid != nerve_id and mid in placed[other_nid]:
                    key = f"{mid}|{other_nid}"
                    if key in scored:
                        continue
                    placed[other_nid].remove(mid)
                    result.pop(key, None)
                    
        placed[nerve_id].append(mid)
        result.pop(f"{mid}|{nerve_id}", None)
        count += 1
        
    # 清空選擇參數
    st.query_params.pop("sel", None)

    if count:
        nname = NERVE_KEY_TO_NERVE[nerve_id]["zh"]
        st.session_state.message = f"✅ 成功放入 {count} 張至【{nname}】"
        st.session_state.message_type = "success"
    else:
        st.session_state.message = "⚠️ 所選卡片已在此神經區或已鎖定"
        st.session_state.message_type = "warning"

def toggle_img_mode():
    """切換手牌顯示圖片模式"""
    current = st.query_params.get("img_mode", "text")
    st.query_params["img_mode"] = "diagram" if current == "text" else "text"

def get_remaining() -> list:
    placed = st.session_state.placed
    out = []
    for mid in st.session_state.deck:
        m = MUSCLE_MAP[mid]
        placed_cnt = sum(1 for nid in NERVE_KEYS if mid in placed[nid])
        if placed_cnt < len(m["nerves"]):
            out.append(mid)
    return out

def get_pts() -> int:
    return max(1, round(BASE_SCORE / (2 ** st.session_state.submit_count)))

def get_wrong_pairs() -> list:
    result = st.session_state.result
    return [
        (mid, nid)
        for nid in NERVE_KEYS
        for mid in st.session_state.placed[nid]
        if result.get(f"{mid}|{nid}") == "wrong"
    ]

def remove_card(mid: str, nid: str):
    if st.session_state.locked:
        return
    key = f"{mid}|{nid}"
    if key in st.session_state.scored_keys:
        return
    st.session_state.placed[nid].remove(mid)
    st.session_state.result.pop(key, None)

def submit_answers():
    if st.session_state.locked:
        return
    rem = get_remaining()
    if rem:
        st.session_state.message = f"⚠️ 還有 {len(rem)} 張在手牌，請全部放入後再提交！"
        st.session_state.message_type = "warning"
        return
    placed  = st.session_state.placed
    scored  = st.session_state.scored_keys
    result  = st.session_state.result
    pts     = get_pts()
    new_correct = wrong = new_pts = 0
    for nid in NERVE_KEYS:
        for mid in placed[nid]:
            key = f"{mid}|{nid}"
            m   = MUSCLE_MAP[mid]
            if nid in m["nerves"]:
                result[key] = "correct"
                if key not in scored:
                    scored.add(key)
                    new_pts += pts
                    new_correct += 1
            else:
                result[key] = "wrong"
                wrong += 1
    st.session_state.submit_count += 1
    st.session_state.score += new_pts
    if wrong == 0 and len(scored) >= TOTAL_NEEDED:
        st.session_state.locked = True
        st.session_state.message = f"🏆 完美通關！本次得 {new_pts} 分，總分 {st.session_state.score} 分！"
        st.session_state.message_type = "success"
        st.session_state.return_wrong = False
    else:
        wp = get_wrong_pairs()
        wnames = "、".join(MUSCLE_MAP[m]["zh"] for m, _ in wp[:5]) + ("…" if len(wp) > 5 else "")
        st.session_state.message = (
            f"批改完成：✅ 答對 {new_correct} 題 ❌ 答錯 {wrong} 題 ＋{new_pts} 分"
            + (f"\n錯誤：{wnames}" if wp else "")
        )
        st.session_state.message_type = "info" if wrong == 0 else "warning"
        st.session_state.return_wrong = wrong > 0

def do_return_wrong():
    pairs = get_wrong_pairs()
    result = st.session_state.result
    scored = st.session_state.scored_keys
    count = 0
    for mid, nid in pairs:
        key = f"{mid}|{nid}"
        if key not in scored:
            st.session_state.placed[nid].remove(mid)
            result.pop(key, None)
            count += 1
    st.session_state.return_wrong = False
    st.session_state.message = f"↩ 已退回 {count} 張錯誤卡牌至手牌，請重新放置後再提交！"
    st.session_state.message_type = "info"

def restart_game():
    st.session_state.clear()
    st.query_params.clear()


# ══════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;900&display=swap');
* { font-family: 'Noto Sans TC', sans-serif !important; }
[data-testid="stAppViewContainer"] {
    background: #F0F4FF;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(15,110,86,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(83,74,183,0.08) 0%, transparent 50%);
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; }

/* Header */
.game-header {
    background: linear-gradient(120deg, #0F6E56 0%, #185FA5 50%, #534AB7 100%);
    border-radius: 18px; padding: 14px 22px; margin-bottom: 10px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 6px 28px rgba(0,0,0,0.22); flex-wrap: wrap; gap: 10px;
}
.game-title { font-size: 1.5rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px; }
.stat-row { display: flex; gap: 7px; flex-wrap: wrap; }
.stat-pill {
    background: rgba(0,0,0,0.32); border: 1.5px solid rgba(255,255,255,0.25);
    border-radius: 50px; padding: 4px 12px; color: #FFFFFF;
    font-weight: 700; font-size: 0.78rem; white-space: nowrap;
}
.stat-pill b { font-size: 0.88rem; }

/* Progress */
.prog-wrap { background: #CBD5E1; border-radius: 50px; height: 10px; overflow: hidden; margin: 6px 0 2px; }
.prog-fill { height: 100%; border-radius: 50px; background: #15803D; transition: width 0.5s ease; }
.prog-label { font-size: 0.75rem; color: #475569; font-weight: 600; text-align: right; margin-bottom: 8px; }

/* Hand section label */
.section-title {
    font-size: 0.95rem; font-weight: 800; color: #1e293b;
    padding: 6px 0 8px; border-bottom: 2px solid #e2e8f0; margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
}
.badge-count {
    background: #e2e8f0; color: #475569; border-radius: 50px;
    padding: 2px 10px; font-size: 0.72rem; font-weight: 700;
}

/* Nerve zone */
.nerve-zone {
    border-radius: 12px; overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.09); margin-bottom: 10px;
}
.nerve-hdr {
    padding: 8px 14px; font-weight: 800; color: #FFFFFF;
    display: flex; align-items: center; justify-content: space-between;
}
.nerve-hdr .nerve-en { font-size: 0.72rem; font-weight: 600; opacity: 0.85; }
.nerve-hdr .nerve-cnt {
    background: rgba(0,0,0,0.28); border-radius: 50px;
    padding: 2px 9px; font-size: 0.72rem; font-weight: 700;
}
.nerve-body { background: #F8FAFC; padding: 8px; }
.nerve-empty { color: #94a3b8; font-size: 0.73rem; text-align: center; padding: 4px 0; }

/* Placed cards */
.pcard-wrap { position: relative; width: 100%; }
.pcard {
    border-radius: 8px; overflow: hidden; border: 2.5px solid #94a3b8;
    background: white; cursor: default;
}
.pcard.pc { border-color: #15803D; }
.pcard.pw { border-color: #B91C1C; }
.pcard-img { width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }
.pcard-lbl {
    text-align: center; padding: 3px 2px;
    border-top: 1.5px solid #e5e7eb;
    font-size: 9px; font-weight: 700; color: #1e293b;
    line-height: 1.3; background: white;
}
.pcard-lbl.lc { background: #14532D; color: #86efac; }
.pcard-lbl.lw { background: #7f1d1d; color: #fca5a5; }
.pcard-ov {
    position: absolute; top: -6px; right: -6px; z-index: 10;
    width: 18px; height: 18px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 9px; font-weight: 900; border: 2px solid white;
}
.pcard-ov.c { background: #15803D; color: #fff; }
.pcard-ov.w { background: #B91C1C; color: #fff; }
.dual-badge {
    position: absolute; top: 3px; left: 3px; z-index: 10;
    background: #6D28D9; color: #fff; border-radius: 4px;
    padding: 1px 4px; font-size: 8px; font-weight: 800;
}

/* Return wrong banner */
.return-banner {
    background: #7f1d1d; border: 2px solid #991b1b; border-radius: 14px;
    padding: 10px 16px; display: flex; align-items: center; gap: 12px;
    margin: 4px 0 10px;
}
.stButton > button {
    border-radius: 8px !important; font-weight: 800 !important;
    font-size: 0.8rem !important;
    transition: transform 0.12s, box-shadow 0.12s !important;
}
.stButton > button:hover:not([disabled]) {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important;
}
.stButton > button[disabled] { opacity: 0.42 !important; }
iframe { border: none !important; }
hr { border-color: #e2e8f0 !important; margin: 8px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 狀態計算
# ══════════════════════════════════════════════
rem_cards   = get_remaining()
wrong_pairs = get_wrong_pairs()
scored_cnt  = len(st.session_state.scored_keys)
prog_pct    = round(scored_cnt / TOTAL_NEEDED * 100)


# ══════════════════════════════════════════════
# Header
# ══════════════════════════════════════════════
st.markdown(f"""
<div class="game-header">
  <div class="game-title">🦵 下肢神經肌肉分類遊戲</div>
  <div class="stat-row">
    <div class="stat-pill">⭐ 總分 <b>{st.session_state.score}</b></div>
    <div class="stat-pill">🔢 提交 <b>{st.session_state.submit_count}</b> 次</div>
    <div class="stat-pill">💎 每題 <b>{get_pts()}</b> 分</div>
    <div class="stat-pill">🎴 手牌 <b>{len(rem_cards)}</b> 張</div>
  </div>
</div>
<div class="prog-wrap"><div class="prog-fill" style="width:{prog_pct}%"></div></div>
<div class="prog-label">完成進度 {prog_pct}%（{scored_cnt}/{TOTAL_NEEDED} 題已鎖定）</div>
""", unsafe_allow_html=True)

# Message bar
if st.session_state.message:
    _s = {
        "success": ("#14532D", "#ffffff", "#4ade80"),
        "warning": ("#1F2937", "#F9FAFB", "#F59E0B"),
        "info":    ("#1F2937", "#F9FAFB", "#60A5FA"),
    }
    bg, tc, ac = _s.get(st.session_state.message_type, _s["info"])
    msg_html = st.session_state.message.replace("\n", "<br>")
    st.markdown(f"""
    <div style="background:{bg};border-left:4px solid {ac};border-radius:10px;
        padding:10px 16px;margin:4px 0;font-size:0.86rem;color:{tc};font-weight:500;line-height:1.7;">
      {msg_html}
    </div>""", unsafe_allow_html=True)

if st.session_state.locked:
    st.balloons()

# Return wrong banner
if st.session_state.return_wrong and wrong_pairs:
    n_w = len(wrong_pairs)
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"""
        <div class="return-banner">
          <div style="font-size:1.6rem;">↩️</div>
          <div style="flex:1;color:#fef2f2;font-size:0.82rem;">
            <b>❌ 發現 {n_w} 張錯誤卡牌</b><br>
            可一鍵退回手牌後重新放置。
            <span style="color:#fde68a;font-size:0.7rem;">（每次批改後僅能使用一次）</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(f"↩ 退回 {n_w} 張", key="ret_wrong",
                  on_click=do_return_wrong, use_container_width=True, type="primary")

st.divider()


# ══════════════════════════════════════════════
# 手牌區（上方，橫向 JS iframe）
# ══════════════════════════════════════════════
img_mode_label = "切換解剖圖" if img_mode == "text" else "切換說明圖"
hcol1, hcol2 = st.columns([6, 1])
with hcol1:
    st.markdown(
        f'<div class="section-title">🎴 手牌區 <span class="badge-count">剩 {len(rem_cards)} 張</span>'
        f'<span style="color:#64748b;font-size:0.72rem;font-weight:600;"> 點選卡片（可多選）→ 點下方神經區「📥 放入」</span>'
        f'<span style="color:#7C3AED;font-size:0.72rem;font-weight:700;"> 🔵 紫框 = 雙重神經支配</span></div>',
        unsafe_allow_html=True,
    )
with hcol2:
    st.button(img_mode_label, key="toggle_img_btn", on_click=toggle_img_mode)

if not rem_cards:
    st.markdown(
        '<div style="background:#14532D;color:#fff;border-radius:10px;padding:12px 18px;'
        'text-align:center;font-weight:700;font-size:0.9rem;">🎉 手牌已清空！請點「提交答案」</div>',
        unsafe_allow_html=True,
    )
else:
    cards_data = []
    for mid in rem_cards:
        m = MUSCLE_MAP[mid]
        img_idx = m["imgs"][0] if img_mode == "text" else m["imgs"][1]
        cards_data.append({
            "id":       mid,
            "zh":       m["zh"],
            "en":       m["en"].split("(")[0].strip(),
            "url":      muscle_img(img_idx),
            "dual":     m["dual"],
            "selected": mid in selected,
        })

    cards_json  = json.dumps(cards_data, ensure_ascii=False)
    locked_json = json.dumps(st.session_state.locked)
    sep_json    = json.dumps(SEP)

    # ── JS iframe：橫向捲動手牌 (放大的卡片尺寸與保留安全間距) ──
    hand_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Noto Sans TC',sans-serif;}}
body{{background:transparent;padding:6px 4px 24px 4px;overflow-x:auto;overflow-y:hidden;}}
.hint{{color:#475569;font-size:0.7rem;font-weight:600;margin-bottom:6px;padding-left:4px;}}
.row{{display:flex;flex-wrap:nowrap;gap:12px;padding:4px 4px 10px;width:max-content;}}
.card{{
  flex-shrink:0;width:240px;border-radius:12px;overflow:visible;
  border:3px solid #94a3b8;background:white;cursor:pointer;position:relative;
  box-shadow:0 3px 10px rgba(0,0,0,0.1);
  transition:border-color 0.12s,box-shadow 0.12s;user-select:none;
}}
.card.sel{{
  border-color:#B91C1C !important;
  box-shadow:0 0 0 4px rgba(185,28,28,0.18),0 6px 18px rgba(185,28,28,0.15);
}}
.card.dual{{ border-color:#6D28D9; }}
.card.dual.sel{{ border-color:#B91C1C !important; }}
.card.locked-card{{opacity:0.5;cursor:default;}}
.img-box{{width:100%;padding-top:100%;position:relative;overflow:hidden;border-radius:9px 9px 0 0;}}
.img-box img{{position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;display:block;pointer-events:none;}}
.lbl{{background:white;border-top:2px solid #e5e7eb;padding:8px 6px;text-align:center;border-radius:0 0 9px 9px;}}
.lbl .zh{{font-size:18px;font-weight:700;color:#1e293b;line-height:1.3;}}
.lbl .en{{font-size:13px;color:#64748b;line-height:1.3;margin-top:2px;}}
.badge-sel{{
  position:absolute;top:-10px;right:-10px;z-index:20;
  background:#B91C1C;color:#fff;border-radius:50%;
  width:32px;height:32px;display:flex;align-items:center;justify-content:center;
  font-size:16px;font-weight:900;border:3px solid white;
  box-shadow:0 3px 8px rgba(0,0,0,0.25);
}}
.badge-dual{{
  position:absolute;top:6px;left:6px;z-index:20;
  background:#6D28D9;color:#fff;border-radius:6px;
  padding:3px 8px;font-size:12px;font-weight:800;
}}
</style></head><body>
<div class="row" id="row"></div>
<script>
const CARDS  = {cards_json};
const LOCKED = {locked_json};
const SEP    = {sep_json};
let selected = new Set(CARDS.filter(c=>c.selected).map(c=>c.id));

function render(){{
  const row = document.getElementById('row');
  row.innerHTML = '';
  CARDS.forEach(c=>{{
    const isSel = selected.has(c.id);
    const div = document.createElement('div');
    div.className = 'card' + (isSel?' sel':'') + (c.dual?' dual':'') + (LOCKED?' locked-card':'');
    div.innerHTML =
      (isSel ? '<div class="badge-sel">✓</div>' : '') +
      (c.dual ? '<div class="badge-dual">雙重</div>' : '') +
      `<div class="img-box"><img src="${{c.url}}" loading="lazy"></div>` +
      `<div class="lbl"><div class="zh">${{c.zh}}</div><div class="en">${{c.en}}</div></div>`;
    if(!LOCKED){{
      div.addEventListener('click',()=>{{
        if(selected.has(c.id)) selected.delete(c.id);
        else selected.add(c.id);
        render();
        syncQP();
      }});
    }}
    row.appendChild(div);
  }});
}}

function syncQP(){{
  try{{
    const url = new URL(window.parent.location.href);
    if(selected.size > 0) url.searchParams.set('sel',[...selected].join(SEP));
    else url.searchParams.delete('sel');
    window.parent.history.pushState(null, '', url.toString());
    window.parent.dispatchEvent(new Event('popstate'));
  }}catch(e){{}}
}}

render();

function resize(){{
  const h = document.documentElement.scrollHeight + 8;
  try{{
    window.parent.document.querySelectorAll('iframe').forEach(f=>{{
      try{{
        if(f.contentWindow===window){{ f.style.height=h+'px'; f.height=h; }}
      }}catch(e){{}}
    }});
  }}catch(e){{}}
}}
setTimeout(resize,150); setTimeout(resize,600); window.addEventListener('load',()=>setTimeout(resize,100));
</script></body></html>"""

    n_rows_est = 1
    iframe_h = 420 # 極大化 iframe 高度，徹底防止被裁掉
    st.iframe(hand_html, height=iframe_h)

st.divider()


# ══════════════════════════════════════════════
# 神經分類區（下方，2 欄）
# ══════════════════════════════════════════════
st.markdown('<div class="section-title">🧠 神經分類區</div>', unsafe_allow_html=True)

result = st.session_state.result
locked = st.session_state.locked
scored = st.session_state.scored_keys

IMG_COLS = 5  # placed cards per row in nerve zone

left_nerves  = NERVES[:6]
right_nerves = NERVES[6:]
col_l, col_r = st.columns(2, gap="medium")

for col_widget, nerve_list in [(col_l, left_nerves), (col_r, right_nerves)]:
    with col_widget:
        for nerve in nerve_list:
            nid    = nerve["id"]
            color  = nerve["color"]
            light  = nerve["light"]
            placed_list = st.session_state.placed[nid]
            cnt = len(placed_list)

            st.markdown(
                f'<div class="nerve-zone" style="border:2px solid {color};">'
                f'<div class="nerve-hdr" style="background:{color};">'
                f'<div><span style="font-size:0.88rem;">{nerve["zh"]}</span>'
                f'<div class="nerve-en">{nerve["en"]}</div></div>'
                f'<span class="nerve-cnt">{cnt} 張</span>'
                f'</div><div class="nerve-body">',
                unsafe_allow_html=True,
            )

            # Place button (直接使用 Callback)
            st.button(
                f"📥 放入【{nerve['zh']}】",
                key=f"put_{nid}",
                on_click=place_cards,
                args=(nid,),
                use_container_width=True,
            )

            if not placed_list:
                st.markdown('<div class="nerve-empty">尚無肌肉卡片</div>', unsafe_allow_html=True)
            else:
                for row_start in range(0, len(placed_list), IMG_COLS):
                    row_muscles = placed_list[row_start:row_start + IMG_COLS]
                    pcols = st.columns(IMG_COLS, gap="small")
                    for ci, mid in enumerate(row_muscles):
                        with pcols[ci]:
                            m      = MUSCLE_MAP[mid]
                            key    = f"{mid}|{nid}"
                            is_lkd = key in scored
                            res    = result.get(key)
                            img_i  = m["imgs"][0] if img_mode == "text" else m["imgs"][1]
                            url    = muscle_img(img_i)

                            if is_lkd or res == "correct":
                                pw, ov_c, ov_t, lc = "pc", "c", "✓", "lc"
                            elif res == "wrong":
                                pw, ov_c, ov_t, lc = "pw", "w", "✗", "lw"
                            else:
                                pw, ov_c, ov_t, lc = "", "", "", ""

                            ov_html = f'<div class="pcard-ov {ov_c}">{ov_t}</div>' if ov_c else ""
                            dual_html = '<div class="dual-badge">雙</div>' if m["dual"] else ""

                            st.markdown(
                                f'<div class="pcard-wrap">'
                                f'<div class="pcard {pw}">{ov_html}{dual_html}'
                                f'<img src="{url}" class="pcard-img" loading="lazy">'
                                f'<div class="pcard-lbl {lc}">{m["zh"]}</div>'
                                f'</div></div>',
                                unsafe_allow_html=True,
                            )

                            can_rm = not is_lkd and not locked and res not in ("correct", "wrong")
                            if can_rm:
                                st.button("↩", key=f"rm_{mid}_{nid}",
                                          on_click=remove_card, args=(mid, nid),
                                          use_container_width=True)

            st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 底部按鈕
# ══════════════════════════════════════════════
st.divider()
b1, b2 = st.columns([3, 1])
with b1:
    st.button("✅ 提交答案", type="primary",
              disabled=st.session_state.locked,
              on_click=submit_answers, use_container_width=True)
with b2:
    st.button("🔄 重新開始", use_container_width=True, on_click=restart_game)

st.markdown(
    f'<div style="text-align:center;color:#94a3b8;font-size:0.72rem;margin-top:6px;">'
    f'45 塊肌肉 ✕ 多神經支配 → 共 {TOTAL_NEEDED} 道題｜'
    f'雙重神經支配肌肉（🔵紫框）需分別放入兩個神經區</div>',
    unsafe_allow_html=True,
)
