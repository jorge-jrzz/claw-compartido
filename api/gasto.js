// Vercel Serverless Function — registra gastos Apple Pay
const REPO = "jorge-jrzz/claw-compartido";
const FILE_PATH = "data/gastos-yorch.json";
const BOT_TOKEN = "8053108844:AAHoYXITiiS9mLWgIeNIf5ANfjNaJaCEjDM";
const CHAT_ID = "1341397907";

async function notifyTelegram(gasto) {
  const emojis = { Comida: "🍔", Café: "☕", Transport: "🚗", Super: "🛒", Otros: "💳" };
  const emoji = emojis[gasto.categoria] || "💳";
  const msg = `${emoji} *${gasto.comercio}*\n💵 $${gasto.monto.toFixed(2)} MXN — ${gasto.categoria}${gasto.nota ? '\n📝 ' + gasto.nota : ''}`;
  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: CHAT_ID, text: msg, parse_mode: "Markdown" })
  });
}

function parseMonto(val) {
  if (val == null) return null;
  const clean = String(val).replace(/[^0-9.]/g, "");
  const n = parseFloat(clean);
  return isNaN(n) ? null : n;
}

async function getFile(token) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`, {
    headers: { Authorization: `token ${token}`, Accept: "application/vnd.github.v3+json" }
  });
  const d = await r.json();
  if (!d.content) throw new Error("GitHub content missing: " + JSON.stringify(d).slice(0, 200));
  const decoded = Buffer.from(d.content.replace(/\n/g, ""), "base64").toString("utf-8");
  return { content: JSON.parse(decoded), sha: d.sha };
}

async function pushFile(token, content, sha, msg) {
  const encoded = Buffer.from(JSON.stringify(content, null, 2), "utf-8").toString("base64");
  const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`, {
    method: "PUT",
    headers: { Authorization: `token ${token}`, "Content-Type": "application/json", Accept: "application/vnd.github.v3+json" },
    body: JSON.stringify({ message: msg, content: encoded, sha })
  });
  return r.status;
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const token = process.env.GITHUB_TOKEN;
  if (!token) return res.status(500).json({ error: "GITHUB_TOKEN not configured" });

  const body = req.body || {};

  // Debug: log what we received
  const received = { comercio: body.comercio, monto: body.monto, card: body.card, categoria: body.categoria };

  const comercio = body.comercio ? String(body.comercio).trim() : null;
  const monto = parseMonto(body.monto);

  if (!comercio || monto === null) {
    return res.status(400).json({ error: "Faltan campos válidos", received });
  }

  const gasto = {
    comercio,
    monto,
    categoria: body.categoria || "Otros",
    nota: body.card ? `Tarjeta: ${body.card}` : (body.nota || "")
  };

  try {
    const { content, sha } = await getFile(token);
    content.gastos = content.gastos || [];
    const nuevo = { id: content.gastos.length + 1, fecha: new Date().toISOString(), ...gasto, fuente: "apple_pay" };
    content.gastos.push(nuevo);
    const status = await pushFile(token, content, sha, `💳 ${gasto.comercio} $${gasto.monto}`);
    await notifyTelegram(nuevo);
    return res.status(200).json({ ok: true, gasto: nuevo, github: status });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
};
