import { useState, useCallback, useMemo } from "react";

const GITHUB_BASE = "https://raw.githubusercontent.com/HLH2000/Food_Game/main/";
const MUSCLE_BASE = GITHUB_BASE + "muscle_lowerlimbs/";
const NERVE_BASE  = GITHUB_BASE + "nerve_lowerlimbs/";

function muscleImg(n)  { return `${MUSCLE_BASE}muscle_lowerlimbs_${n}.jpg`; }
function nerveImg(n)   { return `${NERVE_BASE}nerve_lowerlimbs_${n}.jpg`; }

const NERVES = [
  { id: "sup_glut",  zh: "上臀神經",  en: "Sup. Gluteal n.",        color: "#0F6E56", light: "#E1F5EE", imgPair: [1,2]  },
  { id: "inf_glut",  zh: "下臀神經",  en: "Inf. Gluteal n.",        color: "#185FA5", light: "#E6F1FB", imgPair: [3,4]  },
  { id: "femoral",   zh: "股神經",    en: "Femoral n.",             color: "#534AB7", light: "#EEEDFE", imgPair: [5,6]  },
  { id: "obturator", zh: "閉孔神經",  en: "Obturator n.",           color: "#993C1D", light: "#FAECE7", imgPair: [7,8]  },
  { id: "sciatic",   zh: "坐骨神經",  en: "Sciatic n.",             color: "#993556", light: "#FBEAF0", imgPair: [9,10] },
  { id: "com_fib",   zh: "總腓神經",  en: "Common fibular n.",      color: "#3B6D11", light: "#EAF3DE", imgPair: [11,12]},
  { id: "sup_fib",   zh: "淺腓神經",  en: "Superficial fibular n.", color: "#854F0B", light: "#FAEEDA", imgPair: [13,14]},
  { id: "deep_fib",  zh: "深腓神經",  en: "Deep fibular n.",        color: "#A32D2D", light: "#FCEBEB", imgPair: [15,16]},
  { id: "tibial",    zh: "脛神經",    en: "Tibial n.",              color: "#185FA5", light: "#E6F1FB", imgPair: [17,18]},
  { id: "med_plan",  zh: "內蹠神經",  en: "Medial plantar n.",      color: "#534AB7", light: "#EEEDFE", imgPair: [19,20]},
  { id: "lat_plan",  zh: "外蹠神經",  en: "Lateral plantar n.",     color: "#0F6E56", light: "#E1F5EE", imgPair: [21,22]},
];

const NERVE_MAP = Object.fromEntries(NERVES.map(n => [n.id, n]));

// muscle index → [text_img_odd, diagram_img_even]
const MUSCLES = [
  { id: "glut_med",     zh: "臀中肌",           en: "Gluteus medius m.",                    imgs: [1,2],    nerves: ["sup_glut"] },
  { id: "glut_min",     zh: "臀小肌",           en: "Gluteus minimus m.",                   imgs: [3,4],    nerves: ["sup_glut"] },
  { id: "tfl",          zh: "擴筋膜張肌",        en: "Tensor fasciae latae m.",              imgs: [5,6],    nerves: ["sup_glut"] },
  { id: "glut_max",     zh: "臀大肌",           en: "Gluteus maximus m.",                   imgs: [7,8],    nerves: ["inf_glut"] },
  { id: "quad_fem",     zh: "股四頭肌",          en: "Quadriceps femoris m.",                imgs: [9,10],   nerves: ["femoral"] },
  { id: "rect_fem",     zh: "股直肌",           en: "Rectus femoris m.",                    imgs: [11,12],  nerves: ["femoral"] },
  { id: "vas_lat",      zh: "股外側肌",          en: "Vastus lateralis m.",                  imgs: [13,14],  nerves: ["femoral"] },
  { id: "vas_med",      zh: "股內側肌",          en: "Vastus medialis m.",                   imgs: [15,16],  nerves: ["femoral"] },
  { id: "vas_int",      zh: "股中間肌",          en: "Vastus intermedius m.",                imgs: [17,18],  nerves: ["femoral"] },
  { id: "sartorius",    zh: "縫匠肌",           en: "Sartorius m.",                         imgs: [19,20],  nerves: ["femoral"] },
  { id: "pectineus",    zh: "恥骨肌",           en: "Pectineus m.",                         imgs: [21,22],  nerves: ["femoral","obturator"], dual: true },
  { id: "gracilis",     zh: "股薄肌",           en: "Gracilis m.",                          imgs: [23,24],  nerves: ["obturator"] },
  { id: "add_mag",      zh: "內收大肌",          en: "Adductor magnus m.",                   imgs: [25,26],  nerves: ["obturator","sciatic"], dual: true },
  { id: "add_lon",      zh: "內收長肌",          en: "Adductor longus m.",                   imgs: [27,28],  nerves: ["obturator"] },
  { id: "add_bre",      zh: "內收短肌",          en: "Adductor brevis m.",                   imgs: [29,30],  nerves: ["obturator"] },
  { id: "bic_lon",      zh: "股二頭肌長頭",       en: "Biceps femoris m. (long head)",        imgs: [31,32],  nerves: ["tibial"], dual: true },
  { id: "bic_sho",      zh: "股二頭肌短頭",       en: "Biceps femoris m. (short head)",       imgs: [33,34],  nerves: ["com_fib"], dual: true },
  { id: "semiten",      zh: "半腱肌",           en: "Semitendinosus m.",                    imgs: [35,36],  nerves: ["sciatic","tibial"] },
  { id: "semimem",      zh: "半膜肌",           en: "Semimembranosus m.",                   imgs: [37,38],  nerves: ["sciatic","tibial"] },
  { id: "fib_lon",      zh: "腓長肌",           en: "Fibularis longus m.",                  imgs: [39,40],  nerves: ["sup_fib"] },
  { id: "fib_bre",      zh: "腓短肌",           en: "Fibularis brevis m.",                  imgs: [41,42],  nerves: ["sup_fib"] },
  { id: "tib_ant",      zh: "脛前肌",           en: "Tibialis anterior m.",                 imgs: [43,44],  nerves: ["deep_fib"] },
  { id: "ext_dig_lon",  zh: "伸趾長肌",          en: "Extensor digitorum longus m.",         imgs: [45,46],  nerves: ["deep_fib"] },
  { id: "ext_hal_lon",  zh: "伸姆長肌",          en: "Extensor hallucis longus m.",          imgs: [47,48],  nerves: ["deep_fib"] },
  { id: "fib_ter",      zh: "第三腓骨肌",         en: "Fibularis tertius m.",                 imgs: [49,50],  nerves: ["deep_fib"] },
  { id: "ext_dig_bre",  zh: "伸趾短肌",          en: "Extensor digitorum brevis m.",         imgs: [51,52],  nerves: ["deep_fib"] },
  { id: "ext_hal_bre",  zh: "伸姆短肌",          en: "Extensor hallucis brevis m.",          imgs: [53,54],  nerves: ["deep_fib"] },
  { id: "gastro",       zh: "腓腸肌",           en: "Gastrocnemius m.",                     imgs: [55,56],  nerves: ["tibial"] },
  { id: "soleus",       zh: "比目魚肌",          en: "Soleus m.",                            imgs: [57,58],  nerves: ["tibial"] },
  { id: "plantaris",    zh: "蹠肌",             en: "Plantaris m.",                         imgs: [59,60],  nerves: ["tibial"] },
  { id: "tib_pos",      zh: "脛後肌",           en: "Tibialis posterior m.",                imgs: [61,62],  nerves: ["tibial"] },
  { id: "fle_hal_lon",  zh: "屈姆長肌",          en: "Flexor hallucis longus m.",            imgs: [63,64],  nerves: ["tibial"] },
  { id: "fle_dig_lon",  zh: "屈趾長肌",          en: "Flexor digitorum longus m.",           imgs: [65,66],  nerves: ["tibial"] },
  { id: "poplit",       zh: "膕肌",             en: "Popliteus m.",                         imgs: [67,68],  nerves: ["tibial"] },
  { id: "fle_dig_bre",  zh: "屈趾短肌",          en: "Flexor digitorum brevis m.",           imgs: [69,70],  nerves: ["med_plan"] },
  { id: "abd_hal",      zh: "外展姆肌",          en: "Abductor hallucis m.",                 imgs: [71,72],  nerves: ["med_plan"] },
  { id: "quad_pla",     zh: "掌方肌",           en: "Quadratus plantae m.",                 imgs: [73,74],  nerves: ["lat_plan"] },
  { id: "fle_hal_bre",  zh: "屈姆短肌",          en: "Flexor hallucis brevis m.",            imgs: [75,76],  nerves: ["med_plan"] },
  { id: "lumb1",        zh: "內側第1蚓狀肌",      en: "Medial 1st lumbrical m.",              imgs: [77,78],  nerves: ["med_plan"] },
  { id: "abd_dmi",      zh: "外展小趾肌",         en: "Abductor digiti minimi m.",            imgs: [79,80],  nerves: ["lat_plan"] },
  { id: "fle_dmi_bre",  zh: "屈小趾短肌",         en: "Flexor digiti minimi brevis m.",       imgs: [81,82],  nerves: ["lat_plan"] },
  { id: "lumb23",       zh: "外側1-3蚓狀肌",      en: "Lat. 1-3 lumbrical m.",               imgs: [83,84],  nerves: ["lat_plan"] },
  { id: "add_hal",      zh: "內收姆肌",          en: "Adductor hallucis m.",                 imgs: [85,86],  nerves: ["lat_plan"] },
  { id: "plan_int",     zh: "掌骨中間肌",         en: "Plantar interosseous m.",              imgs: [87,88],  nerves: ["lat_plan"] },
  { id: "dors_int",     zh: "背骨中間肌",         en: "Dorsal interosseous m.",               imgs: [89,90],  nerves: ["lat_plan"] },
];

const MUSCLE_MAP = Object.fromEntries(MUSCLES.map(m => [m.id, m]));

const BASE_PTS = 50;

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function initState() {
  return {
    deck: shuffle(MUSCLES.map(m => m.id)),
    placed: Object.fromEntries(NERVES.map(n => [n.id, []])),
    result: {},
    scored: new Set(),
    selected: new Set(),
    score: 0,
    submitCount: 0,
    locked: false,
    message: null,
    returnWrong: false,
    imgMode: "text", // "text" | "diagram"
    filterNerve: "all",
  };
}

const TOTAL = MUSCLES.reduce((s, m) => s + m.nerves.length, 0);

export default function App() {
  const [st, setSt] = useState(initState);

  const pts = useMemo(() => Math.max(1, Math.round(BASE_PTS / Math.pow(2, st.submitCount))), [st.submitCount]);

  const remainingCards = useMemo(() => {
    return st.deck.filter(id => {
      const m = MUSCLE_MAP[id];
      const placedCount = NERVES.filter(n => (st.placed[n.id] || []).includes(id)).length;
      return placedCount < m.nerves.length;
    });
  }, [st.deck, st.placed]);

  const filteredDeck = useMemo(() => {
    if (st.filterNerve === "all") return remainingCards;
    return remainingCards.filter(id => MUSCLE_MAP[id].nerves.includes(st.filterNerve));
  }, [remainingCards, st.filterNerve]);

  const wrongPairs = useMemo(() => {
    const pairs = [];
    for (const n of NERVES) {
      for (const mid of (st.placed[n.id] || [])) {
        if (st.result[`${mid}|${n.id}`] === "wrong") pairs.push([mid, n.id]);
      }
    }
    return pairs;
  }, [st.placed, st.result]);

  const scoredCount = st.scored.size;
  const progress = Math.round(scoredCount / TOTAL * 100);

  const toggleSelect = useCallback((id) => {
    if (st.locked) return;
    setSt(prev => {
      const sel = new Set(prev.selected);
      sel.has(id) ? sel.delete(id) : sel.add(id);
      return { ...prev, selected: sel };
    });
  }, [st.locked]);

  const placeCards = useCallback((nerveId) => {
    setSt(prev => {
      if (!prev.selected.size) return { ...prev, message: { type: "warn", text: "請先點選手牌卡片！" } };
      const placed = { ...prev.placed };
      const result = { ...prev.result };
      let count = 0;
      for (const mid of prev.selected) {
        const m = MUSCLE_MAP[mid];
        if (!m) continue;
        if ((placed[nerveId] || []).includes(mid)) continue;
        if (!m.dual) {
          // remove from other nerves if not scored there
          for (const nid of NERVES.map(n => n.id)) {
            if (nid !== nerveId && placed[nid]?.includes(mid)) {
              const key = `${mid}|${nid}`;
              if (prev.scored.has(key)) continue;
              placed[nid] = placed[nid].filter(x => x !== mid);
              delete result[key];
            }
          }
        }
        placed[nerveId] = [...(placed[nerveId] || []), mid];
        delete result[`${mid}|${nerveId}`];
        count++;
      }
      if (!count) return { ...prev, message: { type: "warn", text: "所選卡片已在此神經區或已鎖定" } };
      return { ...prev, placed, result, selected: new Set(), message: { type: "ok", text: `✓ 放入 ${count} 張至【${NERVE_MAP[nerveId].zh}】` } };
    });
  }, []);

  const removeCard = useCallback((mid, nerveId) => {
    setSt(prev => {
      const key = `${mid}|${nerveId}`;
      if (prev.scored.has(key) || prev.locked) return prev;
      const placed = { ...prev.placed, [nerveId]: prev.placed[nerveId].filter(x => x !== mid) };
      const result = { ...prev.result };
      delete result[key];
      return { ...prev, placed, result };
    });
  }, []);

  const submit = useCallback(() => {
    setSt(prev => {
      if (prev.locked) return prev;
      const rem = prev.deck.filter(id => {
        const m = MUSCLE_MAP[id];
        const pc = NERVES.filter(n => (prev.placed[n.id] || []).includes(id)).length;
        return pc < m.nerves.length;
      });
      if (rem.length) return { ...prev, message: { type: "warn", text: `還有 ${rem.length} 張在手牌，請全部放入後再提交！` } };
      const result = { ...prev.result };
      const scored = new Set(prev.scored);
      const thisPts = Math.max(1, Math.round(BASE_PTS / Math.pow(2, prev.submitCount)));
      let newCorrect = 0, wrong = 0, gain = 0;
      for (const n of NERVES) {
        for (const mid of (prev.placed[n.id] || [])) {
          const key = `${mid}|${n.id}`;
          const m = MUSCLE_MAP[mid];
          if (m.nerves.includes(n.id)) {
            result[key] = "correct";
            if (!scored.has(key)) { scored.add(key); gain += thisPts; newCorrect++; }
          } else {
            result[key] = "wrong"; wrong++;
          }
        }
      }
      const newScore = prev.score + gain;
      const submitCount = prev.submitCount + 1;
      const allDone = wrong === 0 && scored.size >= TOTAL;
      return {
        ...prev, result, scored, score: newScore, submitCount,
        locked: allDone,
        returnWrong: wrong > 0,
        message: allDone
          ? { type: "win", text: `🏆 完美通關！本次得 ${gain} 分，總分 ${newScore} 分！` }
          : { type: wrong === 0 ? "ok" : "warn", text: `批改：✓ 答對 ${newCorrect}　✗ 答錯 ${wrong}　+${gain} 分` },
      };
    });
  }, []);

  const returnWrong = useCallback(() => {
    setSt(prev => {
      const placed = { ...prev.placed };
      const result = { ...prev.result };
      let count = 0;
      for (const [mid, nid] of wrongPairs) {
        const key = `${mid}|${nid}`;
        if (!prev.scored.has(key)) {
          placed[nid] = placed[nid].filter(x => x !== mid);
          delete result[key]; count++;
        }
      }
      return { ...prev, placed, result, returnWrong: false, message: { type: "info", text: `↩ 退回 ${count} 張錯誤卡牌，請重新放置` } };
    });
  }, [wrongPairs]);

  const restart = useCallback(() => setSt(initState()), []);

  const msgStyle = st.message ? ({
    ok: { bg: "#e6f9f0", border: "#15803D", color: "#14532D" },
    win: { bg: "#fef9c3", border: "#854d0e", color: "#713f12" },
    warn: { bg: "#fef3c7", border: "#d97706", color: "#78350f" },
    info: { bg: "#e0f2fe", border: "#0284c7", color: "#0c4a6e" },
  })[st.message.type] : null;

  return (
    <div style={{ fontFamily: "var(--font-sans,'Noto Sans TC',sans-serif)", padding: "12px 10px 24px", maxWidth: 1100, margin: "0 auto" }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0F6E56 0%, #185FA5 60%, #534AB7 100%)", borderRadius: 16, padding: "14px 20px", marginBottom: 12, display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
        <div style={{ color: "#fff", fontWeight: 700, fontSize: 18 }}>🦵 下肢神經肌肉分類</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {[
            ["⭐ 總分", st.score],
            ["🔢 提交", `${st.submitCount} 次`],
            ["💎 每題", `${pts} 分`],
            ["🎴 手牌", `${remainingCards.length} 張`],
          ].map(([label, val]) => (
            <span key={label} style={{ background: "rgba(0,0,0,0.3)", borderRadius: 50, padding: "4px 12px", color: "#fff", fontSize: 12, fontWeight: 600 }}>
              {label} <strong>{val}</strong>
            </span>
          ))}
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ background: "#e5e7eb", borderRadius: 50, height: 8, marginBottom: 4, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${progress}%`, background: "#15803D", borderRadius: 50, transition: "width 0.5s" }} />
      </div>
      <div style={{ fontSize: 11, color: "var(--color-text-secondary)", textAlign: "right", marginBottom: 10 }}>
        進度 {progress}%（{scoredCount}/{TOTAL} 已鎖定）
      </div>

      {/* Message */}
      {st.message && (
        <div style={{ background: msgStyle.bg, border: `1.5px solid ${msgStyle.border}`, borderRadius: 10, padding: "9px 14px", marginBottom: 8, fontSize: 13, color: msgStyle.color, fontWeight: 500 }}>
          {st.message.text}
        </div>
      )}

      {/* Return wrong banner */}
      {st.returnWrong && wrongPairs.length > 0 && (
        <div style={{ background: "#7f1d1d", borderRadius: 12, padding: "10px 16px", marginBottom: 10, display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ flex: 1, color: "#fef2f2", fontSize: 13 }}>
            ❌ 發現 {wrongPairs.length} 張錯誤卡牌，可一鍵退回手牌
            <span style={{ color: "#fde68a", fontSize: 11, marginLeft: 8 }}>（每次批改後僅能使用一次）</span>
          </div>
          <button onClick={returnWrong} style={{ background: "#B91C1C", color: "#fff", border: "none", borderRadius: 8, padding: "6px 14px", fontSize: 12, fontWeight: 700, cursor: "pointer" }}>
            ↩ 一鍵退回 {wrongPairs.length} 張
          </button>
        </div>
      )}

      {/* Main layout */}
      <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 16 }}>

        {/* LEFT: Hand cards */}
        <div>
          <div style={{ fontWeight: 700, fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 8, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span>🎴 手牌區（{remainingCards.length} 張）</span>
            <button onClick={() => setSt(p => ({ ...p, imgMode: p.imgMode === "text" ? "diagram" : "text" }))}
              style={{ fontSize: 11, padding: "3px 8px", borderRadius: 6, border: "1px solid #ccc", background: "var(--color-background-secondary)", cursor: "pointer", color: "var(--color-text-secondary)" }}>
              {st.imgMode === "text" ? "切換解剖圖" : "切換說明圖"}
            </button>
          </div>

          {/* Filter by nerve */}
          <select value={st.filterNerve} onChange={e => setSt(p => ({ ...p, filterNerve: e.target.value }))}
            style={{ width: "100%", marginBottom: 8, fontSize: 12, padding: "4px 8px", borderRadius: 6, border: "1px solid var(--color-border-tertiary)", background: "var(--color-background-primary)", color: "var(--color-text-primary)" }}>
            <option value="all">全部肌肉</option>
            {NERVES.map(n => <option key={n.id} value={n.id}>{n.zh} / {n.en}</option>)}
          </select>

          {remainingCards.length === 0 ? (
            <div style={{ background: "#14532D", color: "#fff", borderRadius: 10, padding: "12px 16px", textAlign: "center", fontSize: 13, fontWeight: 600 }}>
              🎉 手牌已清空！請提交答案
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 6, maxHeight: 520, overflowY: "auto", paddingRight: 2 }}>
              {filteredDeck.map(mid => {
                const m = MUSCLE_MAP[mid];
                const sel = st.selected.has(mid);
                const imgIdx = st.imgMode === "text" ? m.imgs[0] : m.imgs[1];
                return (
                  <div key={mid} onClick={() => toggleSelect(mid)} style={{
                    borderRadius: 8, overflow: "hidden", border: `2.5px solid ${sel ? "#B91C1C" : m.dual ? "#534AB7" : "#d1d5db"}`,
                    cursor: st.locked ? "default" : "pointer", position: "relative",
                    boxShadow: sel ? "0 0 0 2px rgba(185,28,28,0.2)" : "none",
                    opacity: st.locked ? 0.5 : 1, background: "#fff",
                  }}>
                    {sel && <div style={{ position: "absolute", top: -6, right: -6, zIndex: 5, background: "#B91C1C", color: "#fff", borderRadius: "50%", width: 20, height: 20, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 700, border: "2px solid #fff" }}>✓</div>}
                    {m.dual && <div style={{ position: "absolute", top: 3, left: 3, zIndex: 5, background: "#534AB7", color: "#fff", borderRadius: 4, padding: "1px 4px", fontSize: 9, fontWeight: 700 }}>雙重</div>}
                    <div style={{ width: "100%", paddingTop: "100%", position: "relative", overflow: "hidden" }}>
                      <img src={muscleImg(imgIdx)} alt={m.zh} loading="lazy" style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", objectFit: "cover" }} />
                    </div>
                    <div style={{ background: "#f9fafb", borderTop: "1.5px solid #e5e7eb", padding: "3px 2px", textAlign: "center" }}>
                      <div style={{ fontSize: 9, fontWeight: 700, color: "#111827", lineHeight: 1.2 }}>{m.zh}</div>
                      <div style={{ fontSize: 8, color: "#6b7280", lineHeight: 1.2 }}>{m.en.split("(")[0].trim()}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          <div style={{ marginTop: 10, fontSize: 10, color: "var(--color-text-secondary)", background: "var(--color-background-secondary)", borderRadius: 8, padding: "6px 10px", lineHeight: 1.6 }}>
            <strong style={{ color: "#534AB7" }}>紫框</strong> = 雙重神經支配（需放入多個神經區）<br />
            點選卡片後 → 點右側「放入」按鈕
          </div>
        </div>

        {/* RIGHT: Nerve zones */}
        <div>
          <div style={{ fontWeight: 700, fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 8 }}>🧠 神經分類區</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
            {NERVES.map(nerve => {
              const placed = st.placed[nerve.id] || [];
              return (
                <div key={nerve.id} style={{ border: `2px solid ${nerve.color}`, borderRadius: 12, overflow: "hidden", background: "var(--color-background-primary)" }}>
                  {/* Nerve header */}
                  <div style={{ background: nerve.color, padding: "7px 12px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <div>
                      <div style={{ color: "#fff", fontWeight: 700, fontSize: 12 }}>{nerve.zh}</div>
                      <div style={{ color: "rgba(255,255,255,0.8)", fontSize: 10 }}>{nerve.en}</div>
                    </div>
                    <span style={{ background: "rgba(0,0,0,0.3)", color: "#fff", borderRadius: 50, padding: "2px 8px", fontSize: 10, fontWeight: 700 }}>{placed.length}</span>
                  </div>
                  {/* Place button */}
                  <div style={{ padding: "6px 8px 4px" }}>
                    <button onClick={() => placeCards(nerve.id)} disabled={st.locked || st.selected.size === 0}
                      style={{ width: "100%", padding: "5px", borderRadius: 6, border: `1.5px solid ${nerve.color}`, background: "transparent", color: nerve.color, fontWeight: 700, fontSize: 11, cursor: "pointer", opacity: (st.locked || st.selected.size === 0) ? 0.4 : 1 }}>
                      📥 放入此神經
                    </button>
                  </div>
                  {/* Cards in zone */}
                  <div style={{ padding: "0 8px 8px", minHeight: 40 }}>
                    {placed.length === 0
                      ? <div style={{ textAlign: "center", color: "#9ca3af", fontSize: 10, padding: "6px 0" }}>尚無肌肉</div>
                      : (
                        <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                          {placed.map(mid => {
                            const m = MUSCLE_MAP[mid];
                            const key = `${mid}|${nerve.id}`;
                            const res = st.result[key];
                            const isLocked = st.scored.has(key);
                            const borderColor = isLocked || res === "correct" ? "#15803D" : res === "wrong" ? "#B91C1C" : "#9ca3af";
                            const canRemove = !isLocked && !st.locked && res !== "correct" && res !== "wrong";
                            return (
                              <div key={mid + nerve.id} style={{ position: "relative", width: 52 }}>
                                <div style={{ border: `2px solid ${borderColor}`, borderRadius: 6, overflow: "hidden", background: "#fff" }}>
                                  {(isLocked || res === "correct") && <div style={{ position: "absolute", top: -5, right: -5, zIndex: 3, background: "#15803D", color: "#fff", borderRadius: "50%", width: 14, height: 14, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 8, border: "1.5px solid #fff" }}>✓</div>}
                                  {res === "wrong" && !isLocked && <div style={{ position: "absolute", top: -5, right: -5, zIndex: 3, background: "#B91C1C", color: "#fff", borderRadius: "50%", width: 14, height: 14, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 8, border: "1.5px solid #fff" }}>✗</div>}
                                  <div style={{ width: "100%", paddingTop: "100%", position: "relative" }}>
                                    <img src={muscleImg(st.imgMode === "text" ? m.imgs[0] : m.imgs[1])} alt={m.zh} loading="lazy"
                                      style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", objectFit: "cover" }} />
                                  </div>
                                  <div style={{ background: isLocked || res === "correct" ? "#14532D" : res === "wrong" ? "#7f1d1d" : "#f9fafb", padding: "2px", textAlign: "center", borderTop: "1px solid #e5e7eb" }}>
                                    <div style={{ fontSize: 7.5, fontWeight: 700, color: (isLocked || res === "correct") ? "#86efac" : res === "wrong" ? "#fca5a5" : "#374151", lineHeight: 1.2 }}>{m.zh}</div>
                                  </div>
                                </div>
                                {canRemove && (
                                  <button onClick={() => removeCard(mid, nerve.id)}
                                    style={{ marginTop: 2, width: "100%", padding: "1px 0", fontSize: 9, border: "1px solid #d1d5db", borderRadius: 4, background: "var(--color-background-secondary)", cursor: "pointer", color: "var(--color-text-secondary)" }}>
                                    退回
                                  </button>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom action bar */}
      <div style={{ marginTop: 14, borderTop: "1px solid var(--color-border-tertiary)", paddingTop: 12, display: "flex", gap: 10 }}>
        <button onClick={submit} disabled={st.locked}
          style={{ flex: 3, padding: "10px", borderRadius: 10, border: "none", background: st.locked ? "#9ca3af" : "#15803D", color: "#fff", fontWeight: 700, fontSize: 14, cursor: st.locked ? "default" : "pointer" }}>
          ✅ 提交答案
        </button>
        <button onClick={restart}
          style={{ flex: 1, padding: "10px", borderRadius: 10, border: "1.5px solid #d1d5db", background: "var(--color-background-secondary)", color: "var(--color-text-primary)", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>
          🔄 重新開始
        </button>
      </div>
      <div style={{ marginTop: 8, fontSize: 11, color: "var(--color-text-secondary)", textAlign: "center" }}>
        45 塊肌肉 × 多神經支配 → 共 {TOTAL} 道題 ｜ 雙重神經支配肌肉需分別放入對應的兩條神經
      </div>
    </div>
  );
}
