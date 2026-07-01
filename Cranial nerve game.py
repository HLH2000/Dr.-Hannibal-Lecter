import streamlit as st
import random
import json
from urllib.parse import quote

# ══════════════════════════════════════════════
# 頁面設定
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="腦神經功能分類遊戲 🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────── GitHub 圖片路徑 ───────────────
GITHUB_BASE = "https://raw.githubusercontent.com/HLH2000/Dr.-Hannibal-Lecter/main/"
NERVE_DIR   = GITHUB_BASE + quote("crainal nerve") + "/nerve/"
TARGET_DIR  = GITHUB_BASE + quote("crainal nerve") + "/target/"

def nerve_img(n: int) -> str:
    return f"{NERVE_DIR}nerve_crainal_{n:03d}.jpg"

def target_img(n: int) -> str:
    return f"{TARGET_DIR}nerve_target_{n:03d}.jpg"

# ─────────────── 腦神經資料（12對腦神經） ───────────────
NERVES = [
    {"id": "cn1",  "zh": "嗅神經",       "en": "Olfactory n. (CN I)",           "img": 10, "color": "#0F6E56", "light": "#E1F5EE"},
    {"id": "cn2",  "zh": "視神經",       "en": "Optic n. (CN II)",              "img": 4,  "color": "#185FA5", "light": "#E6F1FB"},
    {"id": "cn3",  "zh": "動眼神經",     "en": "Oculomotor n. (CN III)",        "img": 9,  "color": "#534AB7", "light": "#EEEDFE"},
    {"id": "cn4",  "zh": "滑車神經",     "en": "Trochlear n. (CN IV)",          "img": 11, "color": "#993C1D", "light": "#FAECE7"},
    {"id": "cn5",  "zh": "三叉神經",     "en": "Trigeminal n. (CN V)",          "img": 12, "color": "#7C3AED", "light": "#EDE9FE"},
    {"id": "cn6",  "zh": "外展神經",     "en": "Abducens n. (CN VI)",           "img": 1,  "color": "#3B6D11", "light": "#EAF3DE"},
    {"id": "cn7",  "zh": "顏面神經",     "en": "Facial n. (CN VII)",            "img": 2,  "color": "#854F0B", "light": "#FAEEDA"},
    {"id": "cn8",  "zh": "前庭耳蝸神經", "en": "Vestibulocochlear n. (CN VIII)","img": 3,  "color": "#A32D2D", "light": "#FCEBEB"},
    {"id": "cn9",  "zh": "舌咽神經",     "en": "Glossopharyngeal n. (CN IX)",   "img": 5,  "color": "#0C6478", "light": "#CFFAFE"},
    {"id": "cn10", "zh": "迷走神經",     "en": "Vagus n. (CN X)",               "img": 6,  "color": "#6D28D9", "light": "#EDE9FE"},
    {"id": "cn11", "zh": "副神經",       "en": "Accessory n. (CN XI)",          "img": 7,  "color": "#065F46", "light": "#D1FAE5"},
    {"id": "cn12", "zh": "舌下神經",     "en": "Hypoglossal n. (CN XII)",       "img": 8,  "color": "#B45309", "light": "#FEF3C7"},
]
NERVE_KEYS = [n["id"] for n in NERVES]
NERVE_KEY_TO_NERVE = {n["id"]: n for n in NERVES}

# ─────────────── 功能／構造資料 ───────────────
TARGETS = [
    # 一、感覺功能
    {"id": "smell",           "zh": "嗅覺",                 "en": "Smell (olfaction)",                    "img": 2,  "nerves": ["cn1"],  "dual": False},
    {"id": "vision",          "zh": "視覺",                 "en": "Vision",                                "img": 19, "nerves": ["cn2"],  "dual": False},
    {"id": "hearing",         "zh": "聽覺",                 "en": "Hearing",                               "img": 11, "nerves": ["cn8"],  "dual": False},
    {"id": "vestibular",      "zh": "頭部方位變化感知（前庭覺）", "en": "Vestibular sense (head position)", "img": 12, "nerves": ["cn8"],  "dual": False},
    {"id": "taste_ant",       "zh": "舌前 2/3 味覺",         "en": "Taste, anterior 2/3 of tongue",         "img": 9,  "nerves": ["cn7"],  "dual": False},
    {"id": "taste_post",      "zh": "舌後 1/3 味覺",         "en": "Taste, posterior 1/3 of tongue",        "img": 14, "nerves": ["cn9"],  "dual": False},
    {"id": "face_sensation",  "zh": "臉部一般感覺",          "en": "General facial sensation",              "img": 36, "nerves": ["cn5"],  "dual": False},
    {"id": "carotid_sinus",   "zh": "頸動脈竇（偵測血壓）",   "en": "Carotid sinus (baroreceptor)",         "img": 16, "nerves": ["cn9"],  "dual": False},

    # 二、運動功能
    {"id": "levator_palp",    "zh": "提上眼瞼肌",           "en": "Levator palpebrae superioris m.",       "img": 25, "nerves": ["cn3"],  "dual": False},
    {"id": "eye_open",        "zh": "睜眼",                 "en": "Eye opening",                           "img": 32, "nerves": ["cn3"],  "dual": False},
    {"id": "sup_rectus",      "zh": "上直肌",               "en": "Superior rectus m.",                    "img": 26, "nerves": ["cn3"],  "dual": False},
    {"id": "inf_rectus",      "zh": "下直肌",               "en": "Inferior rectus m.",                    "img": 27, "nerves": ["cn3"],  "dual": False},
    {"id": "med_rectus",      "zh": "內直肌",               "en": "Medial rectus m.",                      "img": 28, "nerves": ["cn3"],  "dual": False},
    {"id": "inf_oblique",     "zh": "下斜肌",               "en": "Inferior oblique m.",                   "img": 29, "nerves": ["cn3"],  "dual": False},
    {"id": "sup_oblique",     "zh": "上斜肌",               "en": "Superior oblique m.",                   "img": 35, "nerves": ["cn4"],  "dual": False},
    {"id": "lat_rectus",      "zh": "外直肌",               "en": "Lateral rectus m.",                     "img": 3,  "nerves": ["cn6"],  "dual": False},
    {"id": "mastication",     "zh": "咀嚼肌",               "en": "Muscles of mastication",                "img": 1,  "nerves": ["cn5"],  "dual": False},
    {"id": "temporalis",      "zh": "顳肌",                 "en": "Temporalis m.",                         "img": 37, "nerves": ["cn5"],  "dual": False},
    {"id": "masseter",        "zh": "嚼肌",                 "en": "Masseter m.",                           "img": 38, "nerves": ["cn5"],  "dual": False},
    {"id": "med_pterygoid",   "zh": "內翼肌",               "en": "Medial pterygoid m.",                   "img": 39, "nerves": ["cn5"],  "dual": False},
    {"id": "lat_pterygoid",   "zh": "外翼肌",               "en": "Lateral pterygoid m.",                  "img": 40, "nerves": ["cn5"],  "dual": False},
    {"id": "facial_expr",     "zh": "顏面表情肌",           "en": "Muscles of facial expression",          "img": 4,  "nerves": ["cn7"],  "dual": False},
    {"id": "buccinator",      "zh": "頰肌",                 "en": "Buccinator m.",                         "img": 5,  "nerves": ["cn7"],  "dual": False},
    {"id": "orbicularis_oris","zh": "閉嘴（口輪匝肌）",      "en": "Mouth closing (Orbicularis oris)",      "img": 10, "nerves": ["cn7"],  "dual": False},
    {"id": "stylopharyngeus", "zh": "莖咽肌",               "en": "Stylopharyngeus m.",                    "img": 15, "nerves": ["cn9"],  "dual": False},
    {"id": "pharyngeal_constr","zh": "咽縮肌",              "en": "Pharyngeal constrictor mm.",            "img": 17, "nerves": ["cn10"], "dual": False},
    {"id": "laryngeal_mm",    "zh": "喉發聲肌群",           "en": "Laryngeal (phonation) mm.",             "img": 18, "nerves": ["cn10"], "dual": False},
    {"id": "scm",             "zh": "胸鎖乳突肌",           "en": "Sternocleidomastoid m.",                "img": 21, "nerves": ["cn11"], "dual": False},
    {"id": "trapezius",       "zh": "斜方肌",               "en": "Trapezius m.",                          "img": 22, "nerves": ["cn11"], "dual": False},
    {"id": "tongue_extrinsic","zh": "舌外在肌",             "en": "Extrinsic tongue mm.",                  "img": 23, "nerves": ["cn12"], "dual": False},
    {"id": "tongue_intrinsic","zh": "舌內在肌",             "en": "Intrinsic tongue mm.",                  "img": 24, "nerves": ["cn12"], "dual": False},

    # 三、副交感神經功能
    {"id": "pupil_sphincter", "zh": "瞳孔括約肌",           "en": "Sphincter pupillae m.",                 "img": 30, "nerves": ["cn3"],  "dual": False},
    {"id": "pupil_constrict", "zh": "瞳孔縮小",             "en": "Pupil constriction",                    "img": 34, "nerves": ["cn3"],  "dual": False},
    {"id": "ciliary",         "zh": "睫狀肌",               "en": "Ciliary m.",                            "img": 31, "nerves": ["cn3"],  "dual": False},
    {"id": "accommodation",   "zh": "對焦近物",             "en": "Accommodation (near focus)",            "img": 33, "nerves": ["cn3"],  "dual": False},
    {"id": "lacrimal",        "zh": "淚腺",                 "en": "Lacrimal gland",                        "img": 6,  "nerves": ["cn7"],  "dual": False},
    {"id": "submandibular",   "zh": "頷下腺",               "en": "Submandibular gland",                   "img": 7,  "nerves": ["cn7"],  "dual": False},
    {"id": "sublingual",      "zh": "舌下腺",               "en": "Sublingual gland",                      "img": 8,  "nerves": ["cn7"],  "dual": False},
    {"id": "parotid",         "zh": "耳下腺",               "en": "Parotid gland",                         "img": 13, "nerves": ["cn9"],  "dual": False},
    {"id": "para_vagal",      "zh": "副交感神經－大宗",      "en": "Parasympathetic (vagal, major)",        "img": 20, "nerves": ["cn10"], "dual": False},
]
TARGET_MAP = {t["id"]: t for t in TARGETS}
TOTAL_NEEDED = sum(len(t["nerves"]) for t in TARGETS)
SEP = "|||"
BASE_SCORE = 50


# ══════════════════════════════════════════════
# query_params 讀寫輔助
# ══════════════════════════════════════════════
def read_selected() -> set:
    raw = st.query_params.get("sel", "")
    if not raw:
        return set()
    return set(raw.split(SEP))

# ══════════════════════════════════════════════
# 初始化
# ══════════════════════════════════════════════
def init_game():
    deck = [t["id"] for t in TARGETS]
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
    for tid in list(current_selected):
        t = TARGET_MAP.get(tid)
        if not t:
            continue
        if tid in placed[nerve_id]:
            continue

        if not t["dual"]:
            for other_nid in NERVE_KEYS:
                if other_nid != nerve_id and tid in placed[other_nid]:
                    key = f"{tid}|{other_nid}"
                    if key in scored:
                        continue
                    placed[other_nid].remove(tid)
                    result.pop(key, None)

        placed[nerve_id].append(tid)
        result.pop(f"{tid}|{nerve_id}", None)
        count += 1

    st.query_params.pop("sel", None)

    if count:
        nname = NERVE_KEY_TO_NERVE[nerve_id]["en"]
        st.session_state.message = f"✅ 成功放入 {count} 張至【{nname}】"
        st.session_state.message_type = "success"
    else:
        st.session_state.message = "⚠️ 所選卡片已在此神經區或已鎖定"
        st.session_state.message_type = "warning"

def get_remaining() -> list:
    placed = st.session_state.placed
    out = []
    for tid in st.session_state.deck:
        t = TARGET_MAP[tid]
        placed_cnt = sum(1 for nid in NERVE_KEYS if tid in placed[nid])
        if placed_cnt < len(t["nerves"]):
            out.append(tid)
    return out

def get_pts() -> int:
    return max(1, round(BASE_SCORE / (2 ** st.session_state.submit_count)))

def get_wrong_pairs() -> list:
    result = st.session_state.result
    return [
        (tid, nid)
        for nid in NERVE_KEYS
        for tid in st.session_state.placed[nid]
        if result.get(f"{tid}|{nid}") == "wrong"
    ]

def remove_card(tid: str, nid: str):
    if st.session_state.locked:
        return
    key = f"{tid}|{nid}"
    if key in st.session_state.scored_keys:
        return
    st.session_state.placed[nid].remove(tid)
    st.session_state.result.pop(key, None)
    st.query_params.pop("sel", None)

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
        for tid in placed[nid]:
            key = f"{tid}|{nid}"
            t   = TARGET_MAP[tid]
            if nid in t["nerves"]:
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
        wnames = "、".join(TARGET_MAP[t]["en"].split("(")[0].strip() for t, _ in wp[:5]) + ("…" if len(wp) > 5 else "")
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
    for tid, nid in pairs:
        key = f"{tid}|{nid}"
        if key not in scored:
            st.session_state.placed[nid].remove(tid)
            result.pop(key, None)
            count += 1
    st.session_state.return_wrong = False
    st.query_params.pop("sel", None)
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
.nerve-hdr .nerve-zh { font-size: 0.75rem; font-weight: 600; opacity: 0.85; margin-top: 2px; }
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
.pcard-img { width: 100%; aspect-ratio: 1; object-fit: contain; display: block; background: #fff; }
.pcard-lbl {
    text-align: center; padding: 4px 2px;
    border-top: 1.5px solid #e5e7eb;
    color: #1e293b; line-height: 1.2; background: white;
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
    font-size: 0.85rem !important;
    transition: transform 0.12s, box-shadow 0.12s !important;
}
.stButton > button:hover:not([disabled]) {
    transform: translateY(-1.5px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
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
  <div class="game-title">🧠 腦神經功能分類遊戲</div>
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
st.markdown(
    f'<div class="section-title">🎴 手牌區 <span class="badge-count">剩 {len(rem_cards)} 張</span>'
    f'<span style="color:#64748b;font-size:0.75rem;font-weight:600;margin-left:8px;">點選卡片（可多選）→ 點下方神經區「📥 放入」</span>'
    f'<span style="color:#7C3AED;font-size:0.75rem;font-weight:700;margin-left:8px;">🔵 紫框 = 雙重神經支配</span></div>',
    unsafe_allow_html=True,
)

if not rem_cards:
    st.markdown(
        '<div style="background:linear-gradient(90deg, #14532D, #166534);color:#fff;border-radius:10px;padding:16px 18px;'
        'text-align:center;font-weight:700;font-size:0.95rem;box-shadow:0 4px 10px rgba(0,0,0,0.1);">🎉 手牌已清空！請點擊下方「提交答案」</div>',
        unsafe_allow_html=True,
    )
else:
    cards_data = []
    for tid in rem_cards:
        t = TARGET_MAP[tid]
        cards_data.append({
            "id":       tid,
            "zh":       t["zh"],
            "en":       t["en"].split("(")[0].strip(),
            "url":      target_img(t["img"]),
            "dual":     t["dual"],
            "selected": tid in selected,
        })

    cards_json  = json.dumps(cards_data, ensure_ascii=False)
    locked_json = json.dumps(st.session_state.locked)
    sep_json    = json.dumps(SEP)

    # ── JS iframe：動態隨圖片適應高度 ──
    hand_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;800;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Noto Sans TC',sans-serif;}}
body{{
  background:transparent;
  padding:10px 8px 16px 8px;
  overflow-x:auto;
  overflow-y:hidden;
}}
.row{{
  display:flex;flex-wrap:nowrap;gap:12px;
  padding:8px 8px 16px 8px;
  width:max-content;
  align-items:flex-start;
}}
.card{{
  flex-shrink:0;width:148px;border-radius:10px;overflow:visible;
  border:2.5px solid #94a3b8;background:white;cursor:pointer;position:relative;
  box-shadow:0 4px 10px rgba(0,0,0,0.08);
  transition:transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
  user-select:none;
}}
.card:hover {{
  transform: translateY(-2px);
  box-shadow:0 6px 14px rgba(0,0,0,0.12);
}}
.card.sel{{
  border-color:#B91C1C !important;
  box-shadow:0 0 0 3px rgba(185,28,28,0.15),0 8px 18px rgba(185,28,28,0.22);
  transform: translateY(-4px);
}}
.card.dual{{ border-color:#6D28D9; }}
.card.dual.sel{{ border-color:#B91C1C !important; }}
.card.locked-card{{opacity:0.5;cursor:default;}}
.img-box{{
  width:100%;
  border-radius:8px 8px 0 0;
  overflow:hidden;
  background:#fff;
}}
.img-box img{{
  width:100%;
  height:auto;
  max-height:260px;
  object-fit:contain;
  display:block;
  pointer-events:none;
}}
.lbl{{background:white;border-top:2px solid #e5e7eb;padding:6px 4px;text-align:center;border-radius:0 0 8px 8px;}}
.lbl .en{{font-size:14px;font-weight:800;color:#1e293b;line-height:1.15;}}
.lbl .zh{{font-size:11px;font-weight:600;color:#64748b;line-height:1.2;margin-top:3px;}}
.badge-sel{{
  position:absolute;top:-8px;right:-8px;z-index:20;
  background:#B91C1C;color:#fff;border-radius:50%;
  width:24px;height:24px;display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:900;border:2.5px solid white;
  box-shadow:0 2px 6px rgba(0,0,0,0.25);
}}
.badge-dual{{
  position:absolute;top:4px;left:4px;z-index:20;
  background:#6D28D9;color:#fff;border-radius:5px;
  padding:2px 6px;font-size:9px;font-weight:800;
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
      `<div class="lbl"><div class="en">${{c.en}}</div><div class="zh">${{c.zh}}</div></div>`;
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
  }}catch(e){{}}
}}

render();

function resize(){{
  const h = document.documentElement.scrollHeight + 4;
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

    iframe_h = 380
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

half = (len(NERVES) + 1) // 2
left_nerves  = NERVES[:half]
right_nerves = NERVES[half:]
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
                f'<div><span style="font-size:1.05rem; font-weight:900;">{nerve["en"]}</span>'
                f'<div class="nerve-zh">{nerve["zh"]}</div></div>'
                f'<span class="nerve-cnt">{cnt} 張</span>'
                f'</div><div class="nerve-body">',
                unsafe_allow_html=True,
            )

            st.button(
                f"📥 放入【{nerve['en']}】",
                key=f"put_{nid}",
                on_click=place_cards,
                args=(nid,),
                use_container_width=True,
            )

            if not placed_list:
                st.markdown('<div class="nerve-empty">尚無功能／構造卡片</div>', unsafe_allow_html=True)
            else:
                for row_start in range(0, len(placed_list), IMG_COLS):
                    row_targets = placed_list[row_start:row_start + IMG_COLS]
                    pcols = st.columns(IMG_COLS, gap="small")
                    for ci, tid in enumerate(row_targets):
                        with pcols[ci]:
                            t      = TARGET_MAP[tid]
                            key    = f"{tid}|{nid}"
                            is_lkd = key in scored
                            res    = result.get(key)
                            url    = target_img(t["img"])
                            en_short = t["en"].split("(")[0].strip()

                            if is_lkd or res == "correct":
                                pw, ov_c, ov_t, lc = "pc", "c", "✓", "lc"
                            elif res == "wrong":
                                pw, ov_c, ov_t, lc = "pw", "w", "✗", "lw"
                            else:
                                pw, ov_c, ov_t, lc = "", "", "", ""

                            ov_html = f'<div class="pcard-ov {ov_c}">{ov_t}</div>' if ov_c else ""
                            dual_html = '<div class="dual-badge">雙</div>' if t["dual"] else ""

                            st.markdown(
                                f'<div class="pcard-wrap">'
                                f'<div class="pcard {pw}">{ov_html}{dual_html}'
                                f'<img src="{url}" class="pcard-img" loading="lazy">'
                                f'<div class="pcard-lbl {lc}">'
                                f'<div style="font-size:9.5px;font-weight:800;line-height:1.15;word-wrap:break-word;">{en_short}</div>'
                                f'<div style="font-size:8px;font-weight:600;opacity:0.85;margin-top:2px;">{t["zh"]}</div>'
                                f'</div></div></div>',
                                unsafe_allow_html=True,
                            )

                            can_rm = not is_lkd and not locked and res not in ("correct", "wrong")
                            if can_rm:
                                st.button("↩", key=f"rm_{tid}_{nid}",
                                          on_click=remove_card, args=(tid, nid),
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
    f'<div style="text-align:center;color:#94a3b8;font-size:0.75rem;margin-top:6px;font-weight:500;">'
    f'{len(TARGETS)} 項功能／構造 ✕ 對應腦神經 → 共 {TOTAL_NEEDED} 道題｜'
    f'12 對腦神經分類區，涵蓋感覺、運動與副交感神經功能</div>',
    unsafe_allow_html=True,
)
