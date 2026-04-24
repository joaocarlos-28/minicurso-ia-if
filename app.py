import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Calculadora de Notas – IF",
    page_icon="🎓",
    layout="centered",
)

# ── Constantes ──────────────────────────────────────────────────────────────
MEDIA_APROVACAO    = 6.0   # média mínima para aprovação
MEDIA_RECUPERACAO  = 5.0   # abaixo disso = reprovado direto
QTD_NOTAS          = 4

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Syne', sans-serif !important;
}

.stApp {
    background: #0d0f14;
    color: #e8eaf6;
}

.result-aprovado  { background: rgba(74,222,128,0.08);  border: 1px solid rgba(74,222,128,0.30);  border-radius:16px; padding:28px 32px; text-align:center; }
.result-recupera  { background: rgba(250,204,21,0.08);  border: 1px solid rgba(250,204,21,0.30);  border-radius:16px; padding:28px 32px; text-align:center; }
.result-reprovado { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.30); border-radius:16px; padding:28px 32px; text-align:center; }

.big-num   { font-size:56px; font-weight:800; line-height:1; font-family:'Syne',sans-serif; }
.sit-label { font-size:18px; font-weight:700; margin-top:8px; letter-spacing:.05em; }

.aprovado-cor  { color:#4ade80; }
.recupera-cor  { color:#facc15; }
.reprovado-cor { color:#f87171; }

.tip { background:rgba(91,140,255,0.08); border:1px solid rgba(91,140,255,0.22);
       border-radius:12px; padding:14px 18px;
       font-family:'DM Mono',monospace; font-size:13px; color:#a5b4fc; margin-top:12px; }

.metric-row { display:flex; gap:12px; margin-bottom:16px; }
.metric-box { flex:1; background:#161a23; border:1px solid #232840;
              border-radius:12px; padding:14px 16px; text-align:center; }
.metric-box .m-val { font-size:24px; font-weight:800; color:#5b8cff; }
.metric-box .m-lbl { font-size:11px; color:#6b7280; font-family:'DM Mono',monospace;
                     text-transform:uppercase; letter-spacing:.08em; margin-top:2px; }

hr { border-color: #232840 !important; margin: 24px 0 !important; }
h1 { font-weight:800 !important; letter-spacing:-1px !important; }
</style>
""", unsafe_allow_html=True)


# ── Funções ──────────────────────────────────────────────────────────────────
def validar_nota(valor: str, label: str):
    """Valida e converte string para float (0–10), aceita vírgula ou ponto."""
    texto = valor.strip().replace(",", ".")
    if texto == "":
        return None, f"⚠️ {label}: campo obrigatório."
    if texto.count(".") > 1:
        return None, f"⚠️ {label}: formato inválido — use apenas um separador decimal (ex.: 7,5)."
    try:
        n = float(texto)
        if not (0.0 <= n <= 10.0):
            return None, f"⚠️ {label}: valor deve estar entre 0 e 10."
        return round(n, 2), None
    except ValueError:
        return None, f"⚠️ {label}: digite apenas números (ex.: 7,5 ou 7.5)."


def classificar(media: float):
    if media >= MEDIA_APROVACAO:
        return ("aprovado", "APROVADO ✅", "aprovado-cor", "result-aprovado", "🎉",
                "Parabéns! Você atingiu a média mínima. Continue com esse ritmo!")
    elif media >= MEDIA_RECUPERACAO:
        faltam = MEDIA_APROVACAO - media
        return ("recupera", "RECUPERAÇÃO ⚠️", "recupera-cor", "result-recupera", "📖",
                f"Atenção! Faltam {faltam:.2f} pontos para aprovação. Você ainda consegue!")
    else:
        return ("reprovado", "REPROVADO ❌", "reprovado-cor", "result-reprovado", "💪",
                "Não desanime! Converse com seu professor e busque apoio.")


def fig_barras(notas, nomes):
    cores = ["#4ade80" if n >= MEDIA_APROVACAO else "#facc15" if n >= MEDIA_RECUPERACAO else "#f87171"
             for n in notas]
    fig = go.Figure(go.Bar(
        x=nomes, y=notas,
        marker_color=cores,
        text=[f"{n:.1f}" for n in notas],
        textposition="outside",
        textfont=dict(size=14, color="#e8eaf6", family="DM Mono"),
        width=0.5,
    ))
    fig.add_hline(y=MEDIA_APROVACAO, line_dash="dot", line_color="#5b8cff", line_width=2,
                  annotation_text=f"  Mínimo ({MEDIA_APROVACAO})",
                  annotation_font_color="#5b8cff", annotation_position="top left")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(22,26,35,1)",
        font=dict(family="Syne", color="#e8eaf6"),
        yaxis=dict(range=[0, 11], gridcolor="#232840", tickfont=dict(family="DM Mono")),
        xaxis=dict(gridcolor="#232840"),
        margin=dict(t=30, b=10, l=10, r=10), height=320, showlegend=False,
    )
    return fig


def fig_radar(notas, nomes):
    fig = go.Figure(go.Scatterpolar(
        r=notas + [notas[0]], theta=nomes + [nomes[0]],
        fill="toself", fillcolor="rgba(91,140,255,0.15)",
        line=dict(color="#5b8cff", width=2),
        marker=dict(size=6, color="#5b8cff"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(22,26,35,1)",
            radialaxis=dict(range=[0, 10], gridcolor="#232840",
                            tickfont=dict(color="#6b7280", family="DM Mono"),
                            tickvals=[0, 2, 4, 6, 8, 10]),
            angularaxis=dict(gridcolor="#232840",
                             tickfont=dict(color="#e8eaf6", family="Syne", size=13)),
        ),
        font=dict(color="#e8eaf6"),
        margin=dict(t=30, b=10, l=40, r=40), height=300,
    )
    return fig


def fig_gauge(media):
    cor = "#4ade80" if media >= MEDIA_APROVACAO else "#facc15" if media >= MEDIA_RECUPERACAO else "#f87171"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=media,
        number={"font": {"size": 42, "family": "Syne", "color": cor}},
        gauge={
            "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#6b7280",
                     "tickfont": {"family": "DM Mono", "color": "#6b7280"}},
            "bar":  {"color": cor, "thickness": 0.25},
            "bgcolor": "#161a23", "borderwidth": 0,
            "steps": [
                {"range": [0, MEDIA_RECUPERACAO],               "color": "rgba(248,113,113,0.12)"},
                {"range": [MEDIA_RECUPERACAO, MEDIA_APROVACAO], "color": "rgba(250,204,21,0.12)"},
                {"range": [MEDIA_APROVACAO, 10],                "color": "rgba(74,222,128,0.12)"},
            ],
            "threshold": {"line": {"color": "#5b8cff", "width": 3},
                          "thickness": 0.8, "value": MEDIA_APROVACAO},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8eaf6", family="Syne"),
        margin=dict(t=20, b=0, l=20, r=20), height=220,
    )
    return fig


# ── Histórico ────────────────────────────────────────────────────────────────
if "historico" not in st.session_state:
    st.session_state.historico = []

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown("# 🎓 Calculadora de Notas")
st.caption(f"Instituto Federal · {QTD_NOTAS} notas · Média mínima para aprovação: **{MEDIA_APROVACAO:.1f}**")
st.divider()

# ── Nome ──────────────────────────────────────────────────────────────────────
nome = st.text_input("👤 Nome do aluno", placeholder="Ex.: João Silva (opcional)")

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown("### 📝 Insira as 4 notas")
col1, col2 = st.columns(2)
with col1:
    v1 = st.text_input("Nota 1", placeholder="0 – 10", key="n1")
    v2 = st.text_input("Nota 2", placeholder="0 – 10", key="n2")
with col2:
    v3 = st.text_input("Nota 3", placeholder="0 – 10", key="n3")
    v4 = st.text_input("Nota 4", placeholder="0 – 10", key="n4")

entradas_raw = [v1, v2, v3, v4]
nomes_notas  = ["Nota 1", "Nota 2", "Nota 3", "Nota 4"]

# Preview em tempo real
preview = [validar_nota(v, "")[0] or 0.0 for v in entradas_raw]
if any(v.strip() != "" for v in entradas_raw):
    st.markdown("#### 👁️ Preview em tempo real")
    st.plotly_chart(fig_barras(preview, nomes_notas), use_container_width=True)

st.divider()

# ── Botões ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([3, 1])
calcular = c1.button("🧮 Calcular Média", use_container_width=True, type="primary")
limpar   = c2.button("🗑️ Limpar", use_container_width=True)

if limpar:
    st.session_state.historico = []
    st.rerun()

# ── Cálculo ───────────────────────────────────────────────────────────────────
if calcular:
    labels = nomes_notas
    notas, erros = [], []
    for label, val in zip(labels, entradas_raw):
        n, err = validar_nota(val, label)
        if err:
            erros.append(err)
        else:
            notas.append(n)

    if erros:
        for e in erros:
            st.error(e)
    else:
        media = sum(notas) / QTD_NOTAS
        aluno = nome.strip() or "Aluno"
        _, sit_texto, cor_cls, card_cls, emoji, dica = classificar(media)

        # Card resultado
        st.markdown(f"""
        <div class="{card_cls}">
            <div style="font-size:40px">{emoji}</div>
            <div class="big-num {cor_cls}">{media:.2f}</div>
            <div class="sit-label {cor_cls}">{sit_texto}</div>
            <div style="font-size:13px;color:#9ca3af;font-family:'DM Mono',monospace;margin-top:6px;">
                {aluno} · {QTD_NOTAS} notas · mínimo {MEDIA_APROVACAO}
            </div>
        </div>
        <div class="tip">💡 {dica}</div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Métricas
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="m-val">{max(notas):.1f}</div><div class="m-lbl">Maior nota</div></div>
            <div class="metric-box"><div class="m-val">{min(notas):.1f}</div><div class="m-lbl">Menor nota</div></div>
            <div class="metric-box"><div class="m-val">{sum(notas):.1f}</div><div class="m-lbl">Soma total</div></div>
            <div class="metric-box"><div class="m-val">{media:.2f}</div><div class="m-lbl">Média final</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Gráficos
        st.markdown("#### 📈 Análise Gráfica")
        tab1, tab2, tab3 = st.tabs(["📊 Barras", "🕸️ Radar", "🎯 Velocímetro"])

        with tab1:
            st.plotly_chart(fig_barras(notas, nomes_notas), use_container_width=True)
        with tab2:
            st.plotly_chart(fig_radar(notas, nomes_notas), use_container_width=True)
        with tab3:
            st.plotly_chart(fig_gauge(media), use_container_width=True)
            st.markdown(
                f"<div style='text-align:center;font-family:DM Mono,monospace;"
                f"font-size:12px;color:#6b7280;'>Linha azul = mínimo para aprovação ({MEDIA_APROVACAO})</div>",
                unsafe_allow_html=True)

        # Tabela detalhada
        with st.expander("📋 Detalhes por nota"):
            df = pd.DataFrame({
                "Nota":                  nomes_notas,
                "Valor":                 notas,
                "Situação":              ["✅ Boa" if n >= MEDIA_APROVACAO else
                                          "⚠️ Regular" if n >= MEDIA_RECUPERACAO else
                                          "❌ Baixa" for n in notas],
                "Diferença p/ mínimo":   [round(n - MEDIA_APROVACAO, 2) for n in notas],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Salvar histórico
        st.session_state.historico.append({
            "Aluno":   aluno,
            "Nota 1":  notas[0], "Nota 2": notas[1],
            "Nota 3":  notas[2], "Nota 4": notas[3],
            "Média":   round(media, 2),
            "Situação": sit_texto.split()[0],
        })

# ── Histórico ─────────────────────────────────────────────────────────────────
if st.session_state.historico:
    st.divider()
    st.markdown("### 📜 Histórico da Sessão")
    df_hist = pd.DataFrame(st.session_state.historico)
    st.dataframe(df_hist, use_container_width=True, hide_index=True)

    if len(st.session_state.historico) > 1:
        fig_hist = px.line(df_hist, x="Aluno", y="Média", markers=True,
                           color_discrete_sequence=["#5b8cff"])
        fig_hist.add_hline(y=MEDIA_APROVACAO, line_dash="dot", line_color="#4ade80",
                           annotation_text=f"  Aprovação ({MEDIA_APROVACAO})",
                           annotation_font_color="#4ade80")
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(22,26,35,1)",
            font=dict(family="Syne", color="#e8eaf6"),
            yaxis=dict(range=[0, 11], gridcolor="#232840"),
            xaxis=dict(gridcolor="#232840"),
            margin=dict(t=20, b=10, l=10, r=10), height=280,
        )
        st.plotly_chart(fig_hist, use_container_width=True)
