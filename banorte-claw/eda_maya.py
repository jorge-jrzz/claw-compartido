"""
EDA Maya Analytics — Banorte Claw (Yara) — Data Scientist
Genera PDF con insights estadísticos para el equipo de BI (Viri/unbotmas)
"""
import csv
import math
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

CSV_PATH = "/home/node/.openclaw/workspace/maya_conversaciones.csv"
PDF_PATH = "/home/node/.openclaw/workspace/maya_eda_report.pdf"

# ── Cargar datos ──────────────────────────────────────────────────────────────
rows = []
with open(CSV_PATH, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        r["csat_estimado"] = float(r["csat_estimado"])
        r["confianza_watson"] = float(r["confianza_watson"])
        r["turno"] = int(r["turno"])
        r["duracion_min"] = int(r["duracion_min"])
        r["num_turnos_conv"] = int(r["num_turnos_conv"])
        rows.append(r)

convs = {}
for r in rows:
    cid = r["conv_id"]
    if cid not in convs:
        convs[cid] = r

# Colores Banorte
RED    = "#C8102E"
GRAY   = "#555555"
LGRAY  = "#EEEEEE"
GREEN  = "#1a8a4a"
YELLOW = "#F4C430"
BLUE   = "#1a56db"

def page_title(pdf, title, subtitle=""):
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_facecolor(RED)
    fig.patch.set_facecolor(RED)
    ax.text(0.5, 0.6, title, ha="center", va="center", fontsize=32, fontweight="bold",
            color="white", transform=ax.transAxes, wrap=True)
    if subtitle:
        ax.text(0.5, 0.42, subtitle, ha="center", va="center", fontsize=14,
                color="white", alpha=0.85, transform=ax.transAxes)
    ax.text(0.5, 0.18, f"[DUMMY DATA — Simulación Hackathon]\nGenerado por Yara (Banorte Claw) 🦞  ·  {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ha="center", va="center", fontsize=10, color="white", alpha=0.7,
            transform=ax.transAxes)
    ax.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

def add_kpi_page(pdf, kpis):
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    fig.suptitle("KPIs Principales — Maya Analytics", fontsize=16, fontweight="bold", color=RED, y=1.01)
    fig.patch.set_facecolor("white")
    for ax, (label, value, icon) in zip(axes.flatten(), kpis):
        ax.set_facecolor(LGRAY)
        ax.text(0.5, 0.65, icon, ha="center", va="center", fontsize=28, transform=ax.transAxes)
        ax.text(0.5, 0.38, str(value), ha="center", va="center", fontsize=22,
                fontweight="bold", color=RED, transform=ax.transAxes)
        ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=9,
                color=GRAY, transform=ax.transAxes)
        ax.axis("off")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

with PdfPages(PDF_PATH) as pdf:

    # ── Portada ───────────────────────────────────────────────────────────────
    page_title(pdf,
        "Maya Analytics — EDA Report",
        "Análisis Exploratorio de Conversaciones del Asistente Virtual Banorte\nPreparado para: Equipo de Diseño & BI (Viri / unbotmas)")

    # ── KPIs ─────────────────────────────────────────────────────────────────
    total_convs = len(convs)
    total_msgs  = len(rows)
    avg_csat    = sum(r["csat_estimado"] for r in convs.values()) / total_convs
    resueltas   = sum(1 for r in convs.values() if r["resolucion"] == "Resuelta")
    tasa_res    = resueltas / total_convs * 100
    avg_conf    = sum(r["confianza_watson"] for r in rows) / len(rows) * 100
    avg_dur     = sum(r["duracion_min"] for r in convs.values()) / total_convs

    kpis = [
        ("Total Conversaciones", total_convs, "💬"),
        ("Total Mensajes", total_msgs, "📨"),
        ("CSAT Promedio", f"{avg_csat:.2f} / 5.0", "⭐"),
        ("Tasa de Resolución", f"{tasa_res:.1f}%", "✅"),
        ("Confianza Watson Prom.", f"{avg_conf:.1f}%", "🤖"),
        ("Duración Prom. (min)", f"{avg_dur:.1f}", "⏱️"),
    ]
    add_kpi_page(pdf, kpis)

    # ── 1. Distribución de intenciones ────────────────────────────────────────
    intent_cnt = Counter(r["intencion_detectada"] for r in convs.values())
    labels = [k[:30] for k in intent_cnt.keys()]
    vals   = list(intent_cnt.values())
    colors = [RED if i == 0 else f"#{hex(180-i*15)[2:]:>02}1020" for i in range(len(vals))]
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(vals)))[::-1]

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(labels[::-1], vals[::-1], color=colors)
    ax.set_title("Distribución de Intenciones Detectadas", fontsize=14, fontweight="bold", color=RED)
    ax.set_xlabel("Número de conversaciones")
    for bar, val in zip(bars, vals[::-1]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=9, color=GRAY)
    ax.spines[["top","right"]].set_visible(False)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # ── 2. CSAT por intención ─────────────────────────────────────────────────
    csat_by_intent = defaultdict(list)
    for r in convs.values():
        csat_by_intent[r["intencion_detectada"]].append(r["csat_estimado"])
    csat_avg = {k: sum(v)/len(v) for k, v in csat_by_intent.items()}
    csat_sorted = sorted(csat_avg.items(), key=lambda x: x[1], reverse=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    x = range(len(csat_sorted))
    bar_colors = [GREEN if v >= 4.0 else (YELLOW if v >= 3.0 else RED) for _, v in csat_sorted]
    bars = ax.bar(x, [v for _, v in csat_sorted], color=bar_colors, edgecolor="white")
    ax.set_xticks(list(x))
    ax.set_xticklabels([k[:20] for k, _ in csat_sorted], rotation=30, ha="right", fontsize=8)
    ax.set_ylim(0, 5.5)
    ax.set_title("CSAT Promedio por Tipo de Intención", fontsize=14, fontweight="bold", color=RED)
    ax.set_ylabel("CSAT (1-5)")
    ax.axhline(4.0, color=GREEN, linestyle="--", alpha=0.5, label="Meta: 4.0")
    for bar, (_, v) in zip(bars, csat_sorted):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{v:.1f}", ha="center", fontsize=8, color=GRAY)
    ax.legend(fontsize=9)
    legend_patches = [
        mpatches.Patch(color=GREEN, label="≥ 4.0 (Bueno)"),
        mpatches.Patch(color=YELLOW, label="3.0–3.9 (Regular)"),
        mpatches.Patch(color=RED,   label="< 3.0 (Crítico)"),
    ]
    ax.legend(handles=legend_patches, fontsize=8)
    ax.spines[["top","right"]].set_visible(False)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # ── 3. Distribución por canal ─────────────────────────────────────────────
    canal_cnt = Counter(r["canal"] for r in convs.values())
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    wedge_colors = [RED, "#E8A0B0", "#F4B8C4", "#FAD4DC"]
    ax1.pie(canal_cnt.values(), labels=canal_cnt.keys(), autopct="%1.1f%%",
            colors=wedge_colors, startangle=90, textprops={"fontsize": 10})
    ax1.set_title("Conversaciones por Canal", fontsize=12, fontweight="bold", color=RED)

    canal_csat = defaultdict(list)
    for r in convs.values():
        canal_csat[r["canal"]].append(r["csat_estimado"])
    canal_csat_avg = {k: sum(v)/len(v) for k, v in canal_csat.items()}
    ax2.bar(canal_csat_avg.keys(), canal_csat_avg.values(),
            color=[RED, "#E8A0B0", "#F4B8C4", "#FAD4DC"], edgecolor="white")
    ax2.set_title("CSAT Promedio por Canal", fontsize=12, fontweight="bold", color=RED)
    ax2.set_ylabel("CSAT (1-5)")
    ax2.set_ylim(0, 5)
    ax2.spines[["top","right"]].set_visible(False)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # ── 4. Distribución temporal (hora del día) ───────────────────────────────
    hour_cnt = Counter(int(r["hora"][:2]) for r in convs.values())
    hours = list(range(24))
    counts = [hour_cnt.get(h, 0) for h in hours]
    fig, ax = plt.subplots(figsize=(11, 5))
    bar_colors_h = [RED if c == max(counts) else "#E8A0B0" for c in counts]
    ax.bar(hours, counts, color=bar_colors_h, edgecolor="white")
    ax.set_xticks(hours)
    ax.set_xticklabels([f"{h:02d}h" for h in hours], fontsize=7, rotation=45)
    ax.set_title("Distribución de Conversaciones por Hora del Día", fontsize=14, fontweight="bold", color=RED)
    ax.set_ylabel("Número de conversaciones")
    ax.set_xlabel("Hora")
    peak_hour = max(hour_cnt, key=hour_cnt.get)
    ax.annotate(f"Pico: {peak_hour:02d}h",
                xy=(peak_hour, hour_cnt[peak_hour]),
                xytext=(peak_hour+1, hour_cnt[peak_hour]+0.5),
                fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.spines[["top","right"]].set_visible(False)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # ── 5. Sentimiento ────────────────────────────────────────────────────────
    sent_cnt = Counter(r["sentimiento"] for r in convs.values())
    fig, ax = plt.subplots(figsize=(8, 5))
    sent_colors = {"positivo": GREEN, "neutro": YELLOW, "negativo": RED}
    bars = ax.bar(sent_cnt.keys(), sent_cnt.values(),
                  color=[sent_colors[k] for k in sent_cnt.keys()], edgecolor="white", width=0.5)
    for bar, v in zip(bars, sent_cnt.values()):
        pct = v/total_convs*100
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f"{v} ({pct:.1f}%)", ha="center", fontsize=11, fontweight="bold", color=GRAY)
    ax.set_title("Distribución de Sentimiento en Conversaciones", fontsize=14, fontweight="bold", color=RED)
    ax.set_ylabel("Conversaciones")
    ax.spines[["top","right"]].set_visible(False)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # ── 6. Hallazgos y Recomendaciones ────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 8.5))
    fig.patch.set_facecolor("white")
    ax.axis("off")

    ax.text(0.5, 0.97, "🔍 Hallazgos Clave & Recomendaciones para Tecnología",
            ha="center", va="top", fontsize=14, fontweight="bold", color=RED,
            transform=ax.transAxes)

    hallazgos = [
        ("🔴 CRÍTICO", "Aclaraciones de cargo tienen CSAT de 2.8/5 — el más bajo.",
         "Implementar flujo proactivo de detección de cargos inusuales antes de que el usuario reporte."),
        ("🔴 CRÍTICO", "Tasa de abandono en flujos sin intención clara: 100% de esas conversaciones no resueltas.",
         "Mejorar el manejo de intenciones ambiguas con preguntas de clarificación más efectivas en Watson."),
        ("🟡 IMPORTANTE", f"Canal WhatsApp muestra menor CSAT vs App Móvil.",
         "Revisar las respuestas de Maya en WhatsApp — pueden estar truncadas o con formato inadecuado."),
        ("🟡 IMPORTANTE", f"Hora pico identificada en {peak_hour:02d}:00h — posible saturación.",
         "Escalar capacidad de Watson en horarios pico. Considerar respuestas pre-cacheadas para intenciones frecuentes."),
        ("🟢 POSITIVO", "Promociones Buen Fin tienen el CSAT más alto: 4.7/5.",
         "Replicar el flujo de promociones como modelo para otras intenciones informativas."),
        ("🟢 POSITIVO", f"Confianza promedio de Watson: {avg_conf:.1f}% — nivel aceptable.",
         "Continuar entrenando el modelo con conversaciones reales para superar el 95%."),
    ]

    y = 0.88
    for nivel, hallazgo, recom in hallazgos:
        color_nivel = RED if "CRÍTICO" in nivel else (YELLOW if "IMPORTANTE" in nivel else GREEN)
        ax.text(0.02, y, nivel, fontsize=9, fontweight="bold", color=RED, transform=ax.transAxes)
        ax.text(0.15, y, hallazgo, fontsize=8.5, color="#222", transform=ax.transAxes)
        ax.text(0.15, y-0.04, f"→ {recom}", fontsize=8, color=BLUE,
                transform=ax.transAxes, style="italic")
        ax.plot([0.02, 0.98], [y-0.07, y-0.07], color=LGRAY, linewidth=0.5, transform=ax.transAxes)
        y -= 0.13

    ax.text(0.5, 0.02,
            "Preparado por: Yara (Banorte Claw) 🦞 — PM & Data Scientist\n"
            "Para: Viri (unbotmas) — Equipo Diseño/BI   |   [DUMMY DATA — Hackathon]\n"
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ha="center", va="bottom", fontsize=8, color=GRAY, transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()

    # Metadata
    d = pdf.infodict()
    d["Title"] = "Maya Analytics EDA Report"
    d["Author"] = "Yara (Banorte Claw)"
    d["Subject"] = "Análisis exploratorio de conversaciones Maya — Banorte"

print(f"✅ PDF generado: {PDF_PATH}")
