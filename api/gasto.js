// Vercel Serverless Function — registra gastos Apple Pay
const REPO = "jorge-jrzz/claw-compartido";
const FILE_PATH = "data/gastos-yorch.json";

function parseText(text) {
  const short = text.match(/apple pay en (.+?),\s*gaste\s*\$?([\d,.]+)/i);
  if (short) return { comercio: short[1].trim(), monto: parseFloat(short[2].replace(",", "")) };
  const comercio = text.match(/comercio[:\s]+(.+)/i)?.[1]?.trim();
  const monto = text.match(/monto[:\s]+\$?([\d,.]+)/i)?.[1]?.replace(",", "");
  const categoria = text.match(/categor[ií]a[:\s]+(.+)/i)?.[1]?.trim();
  if (comercio && monto) return { comercio, monto: parseFloat(monto), categoria };
  return null;
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
  let gasto;

  if (body.text) {
    const parsed = parseText(body.text);
    if (!parsed) return res.status(400).json({ error: "No se pudo parsear: " + body.text });
    gasto = { ...parsed, categoria: body.categoria || "Otros", nota: body.nota || "" };
  } else if (body.comercio && body.monto != null) {
    gasto = { comercio: body.comercio, monto: parseFloat(body.monto), categoria: body.categoria || "Otros", nota: body.nota || "" };
  } else {
    return res.status(400).json({ error: "Faltan campos", received: body });
  }

  try {
    const { content, sha } = await getFile(token);
    content.gastos = content.gastos || [];
    const nuevo = { id: content.gastos.length + 1, fecha: new Date().toISOString(), ...gasto, fuente: "apple_pay" };
    content.gastos.push(nuevo);
    const status = await pushFile(token, content, sha, `💳 ${gasto.comercio} $${gasto.monto}`);
    return res.status(200).json({ ok: true, gasto: nuevo, github: status });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
};
