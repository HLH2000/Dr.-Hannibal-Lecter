import streamlit as st
import random
import json

# ══════════════════════════════════════════════
# 頁面設定
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="上肢神經肌肉分類遊戲 💪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────── 圖片路徑（請依實際存放路徑修改） ───────────────
BASE_DIR    = "上肢/"
MUSCLE_DIR  = BASE_DIR + "Muscle/"
NERVE_DIR   = BASE_DIR + "Nerve/"

def muscle_img(n: int) -> str:
    return f"{MUSCLE_DIR}muscle_upperlim_{n:03d}.jpg"

def nerve_img(n: int) -> str:
    return f"{NERVE_DIR}nerve_upperlim_{n:03d}.jpg"

# ─────────────── 神經資料 ───────────────
NERVES = [
    {"id": "dor_scap",  "zh": "背肩胛神經", "en": "Dorsal scapular n.",      "color": "#0F6E56", "light": "#E1F5EE"},
    {"id": "long_thor", "zh": "長胸神經",   "en": "Long thoracic n.",        "color": "#185FA5", "light": "#E6F1FB"},
    {"id": "suprascap", "zh": "肩胛上神經", "en": "Suprascapular n.",        "color": "#534AB7", "light": "#EEEDFE"},
    {"id": "subscap",   "zh": "肩胛下神經", "en": "Subscapular n.",          "color": "#993C1D", "light": "#FAECE7"},
    {"id": "thoracodor","zh": "胸背神經",   "en": "Thoracodorsal n.",        "color": "#7C3AED", "light": "#EDE9FE"},
    {"id": "lat_pect",  "zh": "外胸神經",   "en": "Lateral pectoral n.",     "color": "#3B6D11", "light": "#EAF3DE"},
    {"id": "med_pect",  "zh": "內胸神經",   "en": "Medial pectoral n.",      "color": "#854F0B", "light": "#FAEEDA"},
    {"id": "axillary",  "zh": "腋神經",     "en": "Axillary n.",             "color": "#A32D2D", "light": "#FCEBEB"},
    {"id": "musculocut","zh": "肌皮神經",   "en": "Musculocutaneous n.",     "color": "#0C6478", "light": "#CFFAFE"},
    {"id": "radial",    "zh": "橈神經",     "en": "Radial n.",               "color": "#6D28D9", "light": "#EDE9FE"},
    {"id": "median",    "zh": "正中神經",   "en": "Median n.",               "color": "#065F46", "light": "#D1FAE5"},
    {"id": "ulnar",     "zh": "尺神經",     "en": "Ulnar n.",                "color": "#B45309", "light": "#FEF3C7"},
]
NERVE_MAP  = {n["id"]: n for n in NERVES}
NERVE_KEYS = [n["id"] for n in NERVES]
NERVE_KEY_TO_NERVE = {n["id"]: n for n in NERVES}

# ─────────────── 肌肉資料 ───────────────
# imgs: [說明圖編號, 解剖圖編號]（此處兩者皆暫用同一張圖卡編號，如有獨立說明圖請自行替換第二個數字）
MUSCLES = [
    {"id": "pect_maj",   "zh": "大胸肌",         "en": "Pectoralis major m.",                          "imgs": [48, 48], "nerves": ["lat_pect", "med_pect"], "dual": True},
    {"id": "pect_min",   "zh": "小胸肌",         "en": "Pectoralis minor m.",                          "imgs": [47, 47], "nerves": ["med_pect"],             "dual": False},
    {"id": "lev_scap",   "zh": "提肩胛肌",       "en": "Levator scapulae m.",                          "imgs": [9,  9],  "nerves": ["dor_scap"],             "dual": False},
    {"id": "rhom_min",   "zh": "小菱型肌",       "en": "Rhomboid minor m.",                            "imgs": [7,  7],  "nerves": ["dor_scap"],             "dual": False},
    {"id": "rhom_maj",   "zh": "大菱型肌",       "en": "Rhomboid major m.",                            "imgs": [37, 37], "nerves": ["dor_scap"],             "dual": False},
    {"id": "serr_ant",   "zh": "前鋸肌",         "en": "Serratus anterior m.",                         "imgs": [6,  6],  "nerves": ["long_thor"],            "dual": False},
    {"id": "supraspin",  "zh": "棘上肌",         "en": "Supraspinatus m.",                             "imgs": [39, 39], "nerves": ["suprascap"],            "dual": False},
    {"id": "infraspin",  "zh": "棘下肌",         "en": "Infraspinatus m.",                             "imgs": [40, 40], "nerves": ["suprascap"],            "dual": False},
    {"id": "subscapul",  "zh": "肩胛下肌",       "en": "Subscapularis m.",                             "imgs": [8,  8],  "nerves": ["subscap"],              "dual": False},
    {"id": "teres_maj",  "zh": "大圓肌",         "en": "Teres major m.",                               "imgs": [41, 41], "nerves": ["subscap"],              "dual": False},
    {"id": "lat_dorsi",  "zh": "擴背肌",         "en": "Latissimus dorsi m.",                          "imgs": [38, 38], "nerves": ["thoracodor"],           "dual": False},
    {"id": "deltoid",    "zh": "三角肌",         "en": "Deltoid m.",                                   "imgs": [43, 43], "nerves": ["axillary"],             "dual": False},
    {"id": "teres_min",  "zh": "小圓肌",         "en": "Teres minor m.",                               "imgs": [42, 42], "nerves": ["axillary"],             "dual": False},
    {"id": "coracobr",   "zh": "喙肱肌",         "en": "Coracobrachialis m.",                          "imgs": [11, 11], "nerves": ["musculocut"],           "dual": False},
    {"id": "biceps_br",  "zh": "肱二頭肌",       "en": "Biceps brachii m.",                            "imgs": [10, 10], "nerves": ["musculocut"],           "dual": False},
    {"id": "brachialis", "zh": "肱肌",           "en": "Brachialis m.",                                "imgs": [32, 32], "nerves": ["musculocut", "radial"], "dual": True},
    {"id": "triceps_br", "zh": "肱三頭肌",       "en": "Triceps brachii m.",                           "imgs": [44, 44], "nerves": ["radial"],               "dual": False},
    {"id": "anconeus",   "zh": "肘肌",           "en": "Anconeus m.",                                  "imgs": [17, 17], "nerves": ["radial"],               "dual": False},
    {"id": "brachiorad", "zh": "肱橈肌",         "en": "Brachioradialis m.",                           "imgs": [20, 20], "nerves": ["radial"],               "dual": False},
    {"id": "ecr_long",   "zh": "橈側伸腕長肌",   "en": "Extensor carpi radialis longus m.",            "imgs": [33, 33], "nerves": ["radial"],               "dual": False},
    {"id": "ecr_brev",   "zh": "橈側伸腕短肌",   "en": "Extensor carpi radialis brevis m.",            "imgs": [34, 34], "nerves": ["radial"],               "dual": False},
    {"id": "supinator",  "zh": "旋後肌",         "en": "Supinator m.",                                 "imgs": [35, 35], "nerves": ["radial"],               "dual": False},
    {"id": "ext_dig",    "zh": "伸指肌",         "en": "Extensor digitorum m.",                        "imgs": [46, 46], "nerves": ["radial"],               "dual": False},
    {"id": "edm",        "zh": "伸小指肌",       "en": "Extensor digiti minimi m.",                    "imgs": [19, 19], "nerves": ["radial"],               "dual": False},
    {"id": "ecu",        "zh": "尺側伸腕肌",     "en": "Extensor carpi ulnaris m.",                    "imgs": [45, 45], "nerves": ["radial"],               "dual": False},
    {"id": "apl",        "zh": "外展姆長肌",     "en": "Abductor pollicis longus m.",                  "imgs": [2,  2],  "nerves": ["radial"],               "dual": False},
    {"id": "epb",        "zh": "伸姆短肌",       "en": "Extensor pollicis brevis m.",                  "imgs": [13, 13], "nerves": ["radial"],               "dual": False},
    {"id": "epl",        "zh": "伸姆長肌",       "en": "Extensor pollicis longus m.",                  "imgs": [12, 12], "nerves": ["radial"],               "dual": False},
    {"id": "ext_ind",    "zh": "伸食指肌",       "en": "Extensor indicis m.",                          "imgs": [1,  1],  "nerves": ["radial"],               "dual": False},
    {"id": "pron_teres", "zh": "旋前圓肌",       "en": "Pronator teres m.",                            "imgs": [22, 22], "nerves": ["median"],               "dual": False},
    {"id": "fcr",        "zh": "橈側屈腕肌",     "en": "Flexor carpi radialis m.",                     "imgs": [36, 36], "nerves": ["median"],               "dual": False},
    {"id": "palm_long",  "zh": "掌長肌",         "en": "Palmaris longus m.",                           "imgs": [24, 24], "nerves": ["median"],               "dual": False},
    {"id": "fds",        "zh": "屈指淺肌",       "en": "Flexor digitorum superficialis m.",            "imgs": [5,  5],  "nerves": ["median"],               "dual": False},
    {"id": "fdp_lat",    "zh": "屈指深肌（外側部）", "en": "Flexor digitorum profundus (Lateral part)", "imgs": [25, 25], "nerves": ["median"],               "dual": False},
    {"id": "fdp_med",    "zh": "屈指深肌（內側部）", "en": "Flexor digitorum profundus (Medial part)",  "imgs": [16, 16], "nerves": ["ulnar"],                "dual": False},
    {"id": "fpl",        "zh": "屈姆長肌",       "en": "Flexor pollicis longus m.",                    "imgs": [15, 15], "nerves": ["median"],               "dual": False},
    {"id": "pron_quad",  "zh": "旋前方肌",       "en": "Pronator quadratus m.",                        "imgs": [23, 23], "nerves": ["median"],               "dual": False},
    {"id": "apb",        "zh": "外展姆短肌",     "en": "Abductor pollicis brevis m.",                  "imgs": [31, 31], "nerves": ["median"],               "dual": False},
    {"id": "fpb",        "zh": "屈姆短肌",       "en": "Flexor pollicis brevis m.",                    "imgs": [30, 30], "nerves": ["median", "ulnar"],      "dual": True},
    {"id": "opp_poll",   "zh": "姆對指肌",       "en": "Opponens pollicis m.",                         "imgs": [29, 29], "nerves": ["median"],               "dual": False},
    {"id": "lumb_lat",   "zh": "蚓狀肌（外側兩條）", "en": "Lumbricals (Lateral two)",                  "imgs": [21, 21], "nerves": ["median"],               "dual": False},
    {"id": "lumb_med",   "zh": "蚓狀肌（內側兩條）", "en": "Lumbricals (Medial two)",                   "imgs": [27, 27], "nerves": ["ulnar"],                "dual": False},
    {"id": "add_poll",   "zh": "內收姆肌",       "en": "Adductor pollicis m.",                         "imgs": [14, 14], "nerves": ["ulnar"],                "dual": False},
    {"id": "fcu",        "zh": "尺側屈腕肌",     "en": "Flexor carpi ulnaris m.",                      "imgs": [4,  4],  "nerves": ["ulnar"],                "dual": False},
    {"id": "adm",        "zh": "外展小指肌",     "en": "Abductor digiti minimi m.",                    "imgs": [18, 18], "nerves": ["ulnar"],                "dual": False},
    {"id": "fdmb",       "zh": "屈小指肌",       "en": "Flexor digiti minimi brevis m.",               "imgs": [28, 28], "nerves": ["ulnar"],                "dual": False},
    {"id": "opp_dm",     "zh": "小指對指肌",     "en": "Opponens digiti minimi m.",                    "imgs": [26, 26], "nerves": ["ulnar"],                "dual": False},
    {"id": "inteross",   "zh": "背骨間肌／掌骨間肌", "en": "Dorsal interossei / Palmar interossei",     "imgs": [3,  3],  "nerves": ["ulnar"],                "dual": False},
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
.pcard-img { width: 100%; aspect-ratio: 1; object-fit: contain; display: block; background: #fff; }
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
  <div class="game-title">💪 上肢神經肌肉分類遊戲</div>
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

    # ── JS iframe：動態隨圖片適應高度 ──
    hand_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Noto Sans TC',sans-serif;}}
body{{
  background:transparent;
  padding:10px 8px 28px 8px;
  overflow-x:auto;
  overflow-y:hidden;
}}
.hint{{color:#475569;font-size:0.7rem;font-weight:600;margin-bottom:6px;padding-left:4px;}}
.row{{
  display:flex;flex-wrap:nowrap;gap:10px;
  padding:8px 8px 16px 8px;
  width:max-content;
  align-items:flex-start;
}}
.card{{
  flex-shrink:0;width:148px;border-radius:10px;overflow:visible;
  border:2.5px solid #94a3b8;background:white;cursor:pointer;position:relative;
  box-shadow:0 4px 12px rgba(0,0,0,0.12);
  transition:transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
  user-select:none;
}}
.card.sel{{
  border-color:#B91C1C !important;
  box-shadow:0 0 0 3px rgba(185,28,28,0.18),0 8px 18px rgba(185,28,28,0.25);
  transform: translateY(-3px);
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
.lbl{{background:white;border-top:2px solid #e5e7eb;padding:5px 4px;text-align:center;border-radius:0 0 8px 8px;}}
.lbl .zh{{font-size:13px;font-weight:700;color:#1e293b;line-height:1.25;}}
.lbl .en{{font-size:10px;color:#64748b;line-height:1.2;margin-top:1px;}}
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
                f'<div><span style="font-size:0.88rem;">{nerve["zh"]}</span>'
                f'<div class="nerve-en">{nerve["en"]}</div></div>'
                f'<span class="nerve-cnt">{cnt} 張</span>'
                f'</div><div class="nerve-body">',
                unsafe_allow_html=True,
            )

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
    f'{len(MUSCLES)} 塊肌肉 ✕ 多神經支配 → 共 {TOTAL_NEEDED} 道題｜'
    f'雙重神經支配肌肉（🔵紫框）需分別放入兩個神經區</div>',
    unsafe_allow_html=True,
)
