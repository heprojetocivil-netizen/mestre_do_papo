import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(page_title="Mestre do Papo IA", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp { background-color:#F8F9FB; font-family:'Inter',sans-serif; }
[data-testid="stSidebar"] { display:none; }
.stTextInput>div>div>input, .stTextArea>div>textarea,
.stSelectbox>div>div>div, .stNumberInput>div>div>input {
    background-color:#FFFFFF !important; color:#1E293B !important;
    border:1px solid #CBD5E1 !important; font-family:'Inter',sans-serif !important;
}
.stButton>button {
    width:100%; border-radius:10px; height:3.2em;
    background:linear-gradient(135deg,#16A34A,#22C55E) !important; color:white !important;
    font-weight:600; border:none; box-shadow:2px 2px 12px rgba(22,163,74,0.2);
    font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
}
.stButton>button:hover { background:linear-gradient(135deg,#22C55E,#16A34A) !important; transform:translateY(-1px); }
.stApp .stButton>button, .stApp .stButton>button p,
.stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }
.stApp h1,.stApp h2,.stApp h3 { color:#0F172A !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }
.stApp label,.stApp p,.stApp div { color:#334155 !important; }
.stTabs [data-baseweb="tab-list"] { background:#E2E8F0; border-radius:12px; padding:4px; gap:4px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; color:#64748B !important; font-weight:600; padding:8px 16px; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#16A34A,#22C55E) !important; color:white !important; }
.card { background:#FFFFFF; padding:20px; border-radius:14px; border:1px solid #E2E8F0; margin-bottom:14px; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
.stApp .card,.stApp .card p,.stApp .card div,.stApp .card span { color:#1E293B !important; }
.card-resultado { background:#FFFFFF; padding:22px; border-radius:14px; border:1px solid #16A34A; margin-bottom:14px; box-shadow:0 2px 8px rgba(22,163,74,0.10); }
.stApp .card-resultado,.stApp .card-resultado p,.stApp .card-resultado div,.stApp .card-resultado span { color:#1E293B !important; }
.card-chat-user { background:#EFF6FF; border-radius:12px; padding:12px 16px; margin:6px 0; border-left:3px solid #3B82F6; }
.card-chat-ia { background:#F0FDF4; border-radius:12px; padding:12px 16px; margin:6px 0; border-left:3px solid #22C55E; }
.stApp .card-chat-user,.stApp .card-chat-ia,.stApp .card-chat-user div,.stApp .card-chat-ia div { color:#1E293B !important; }
.tag { background:#16A34A; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.8em; font-weight:600; display:inline-block; margin:3px; }
.tag-verde { background:#DCFCE7; color:#166534 !important; padding:4px 12px; border-radius:20px; font-size:0.8em; font-weight:600; display:inline-block; margin:3px; border:1px solid #86EFAC; }
.tag-amarelo { background:#FEF9C3; color:#854D0E !important; padding:4px 12px; border-radius:20px; font-size:0.8em; font-weight:600; display:inline-block; margin:3px; border:1px solid #FDE047; }
.tag-vermelho { background:#FEE2E2; color:#991B1B !important; padding:4px 12px; border-radius:20px; font-size:0.8em; font-weight:600; display:inline-block; margin:3px; border:1px solid #FCA5A5; }
.divider { border:none; height:1px; background:linear-gradient(to right,transparent,#22C55E,transparent); margin:18px 0; }
.destaque { color:#16A34A !important; font-weight:700; }
.node-box { background:#F1F5F9; border:1px solid #CBD5E1; border-radius:10px; padding:12px 16px; margin:6px 0; }
.stApp .node-box,.stApp .node-box div { color:#1E293B !important; }
.score-bar { background:#F8FAFC; border-radius:8px; padding:10px 16px; margin:6px 0; border:1px solid #E2E8F0; }
.stApp .score-bar div { color:#1E293B !important; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """Você é o MESTRE DO PAPO IA — um coach de comunicação, storytelling e conversa sedutora.

Sua função é desenvolver a capacidade do usuário de conversar, contar histórias, criar conexões e explorar assuntos com naturalidade.

Você NÃO é apenas um gerador de perguntas. Seu objetivo é ensinar o usuário a transformar:
ASSUNTO → CURIOSIDADE → PERGUNTA → RESPOSTA → COMENTÁRIO → GANCHO → NOVO ASSUNTO → HISTÓRIA → CONEXÃO.

REGRAS:
1. Nunca gere apenas uma lista aleatória de perguntas.
2. Sempre procure criar caminhos de exploração.
3. Aproveite as respostas anteriores do usuário.
4. Evite transformar a conversa em entrevista.
5. Incentive comentários, histórias e opiniões pessoais.
6. Varie profundidade, humor, curiosidade e emoção.
7. Quando apropriado, conecte assuntos aparentemente distantes.
8. Crie perguntas abertas, mas naturais.
9. Evite perguntas artificiais ou excessivamente genéricas.
10. Priorize espontaneidade. Responda sempre em Português do Brasil."""

def chamar_ia(prompt: str, system: str = SYSTEM_PROMPT) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b", max_tokens=2048
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return ""

def chamar_ia_chat(msgs: list) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            messages=msgs,
            model="openai/gpt-oss-120b", max_tokens=1024
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return ""

def carregar_json_sessao(dados):
    import re as _re
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = ('btn_','sel_','ul_','dl_','_sub','nav_',)
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

defaults = {
    "etapa": "Login",
    "usuario": "",
    "api_key": "",
    "pagina": "Gerar Papo",
    # Gerar Papo
    "resultado_papo": "",
    # Papo Infinito
    "arvore_infinita": [],
    "resultado_infinito": "",
    "no_ativo": "",
    # Transformar em História
    "resultado_historia": "",
    # Papo Sedutor
    "resultado_sedutor": "",
    "resultado_sedutor_resp": "",
    # Detector de Reciprocidade
    "resultado_reciprocidade": "",
    # Treino de Conversa
    "chat_treino": [],
    "treino_ativo": False,
    "resultado_analise_treino": "",
    # Meu Universo
    "universo": {
        "experiencias": [], "interesses": [], "historias": []
    },
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ──
if st.session_state.etapa == "Login":
    st.markdown("# 🎙️ Mestre do Papo IA")
    st.markdown(
        "<div class='card' style='text-align:center;'>"
        "<div style='font-size:1.1em;color:#64748B;'>Transforme qualquer assunto em uma conversa fascinante.</div>"
        "<div style='margin-top:8px;color:#64748B;font-size:0.9em;'>Assuntos infinitos. Histórias melhores. Conversas memoráveis.</div>"
        "</div>", unsafe_allow_html=True
    )
    nome  = st.text_input("Seu Nome:", key="nome_login")
    chave = st.text_input("🔑 Chave API da Groq:", type="password", key="chave_login")
    arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
    if arq_j:
        try:
            carregar_json_sessao(json.load(arq_j))
        except: pass
    if st.button("✨ ENTRAR", key="btn_entrar_login"):
        if len(nome.strip()) < 2:
            st.warning("Digite um nome com pelo menos 2 caracteres.")
        elif chave.strip():
            st.session_state.usuario = nome.strip()
            st.session_state.api_key = chave.strip()
            st.session_state.etapa = "App"
            st.rerun()
        else:
            st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":
    usuario = st.session_state.usuario

    # ── HEADER ──
    st.markdown("# 🎙️ Mestre do Papo IA")
    st.markdown(f"<div style='color:#64748B;margin-bottom:8px;'>Olá, <b style='color:#16A34A'>{usuario}</b> — treine sua conversa com IA.</div>", unsafe_allow_html=True)

    # ── SALVAR / CARREGAR ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bs1, _bs2 = st.columns(2)
        with _bs1:
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith("_") and k != "api_key"}
            st.download_button("💾 Baixar dados (.json)",
                data=json.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"mestre_do_papo_{usuario}.json",
                mime="application/json", key="dl_sv_mp")
        with _bs2:
            _fup = st.file_uploader("📂 Carregar:", type=["json"], key="ul_sv_mp", label_visibility="collapsed")
            if _fup:
                try:
                    for _k, _v in json.loads(_fup.read().decode()).items():
                        if _k not in ("api_key","etapa"): st.session_state[_k] = _v
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── NAVEGAÇÃO ──
    _abas = ["🌳 Gerar Papo", "♾️ Papo Infinito", "📖 Transformar em História",
             "❤️ Papo Sedutor", "🚦 Detector de Reciprocidade",
             "🎭 Treino de Conversa", "🧠 Meu Universo"]
    _mapa_pg = {a.split(" ",1)[1]: a for a in _abas}
    _pg_keys = [a.split(" ",1)[1] for a in _abas]

    _sel_pg = st.selectbox("", _abas,
        index=_pg_keys.index(st.session_state.pagina) if st.session_state.pagina in _pg_keys else 0,
        key="nav_mp", label_visibility="collapsed")
    st.session_state.pagina = _sel_pg.split(" ", 1)[1]

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ════════════════════════════════════
    # 🌳 GERAR PAPO
    # ════════════════════════════════════
    if st.session_state.pagina == "Gerar Papo":
        st.header("🌳 Gerar Papo")
        st.markdown("<div style='color:#64748B;margin-bottom:16px;'>Escolha a situação e o estilo — a IA cria um caminho de conversa completo.</div>", unsafe_allow_html=True)

        gp1, gp2 = st.columns(2)
        with gp1:
            situacao = st.selectbox("Situação:", [
                "Conhecendo alguém", "Primeiro encontro", "Amigos", "Festa / balada",
                "Bar", "Trabalho / faculdade", "Networking", "Família",
                "WhatsApp / mensagem", "Conversa casual", "Conversa profunda", "Papo sedutor"
            ], key="sel_gp_situacao")
        with gp2:
            estilo = st.selectbox("Estilo:", [
                "😂 Divertido", "🧠 Inteligente", "❤️ Pessoal / emocional",
                "🔥 Sedutor", "🤔 Filosófico", "😎 Descontraído",
                "📖 Narrativo", "🎭 Provocante"
            ], key="sel_gp_estilo")

        assunto_livre = st.text_input("Assunto ou tema (opcional):",
            key="inp_gp_assunto",
            placeholder="Ex: viagens, trabalho, esportes, infância... ou deixe em branco para a IA escolher")

        contexto_extra = st.text_area("Contexto (o que você já sabe sobre a pessoa):",
            height=80, key="ta_gp_contexto",
            placeholder="Ex: ela trabalha com design, viajou para Portugal recentemente, parece reservada no início...")

        if st.button("🌳 GERAR CONVERSA", key="btn_gerar_papo", use_container_width=True):
            prompt = (
                f"Situação: {situacao} | Estilo: {estilo}\n"
                f"Assunto sugerido: {assunto_livre or 'escolha o melhor'}\n"
                f"Contexto sobre a pessoa: {contexto_extra or 'nenhum'}\n\n"
                "Gere um caminho de conversa completo com:\n"
                "🎯 TEMA — o assunto principal escolhido\n"
                "🗣️ ABERTURA — uma frase de entrada natural, não genérica\n"
                "🔎 EXPLORE — 4 formas de aprofundar (curiosidade, humor, emoção, profundidade) com uma pergunta ou comentário cada\n"
                "🔀 MUDE O CAMINHO — 5 assuntos relacionados para onde a conversa pode migrar naturalmente\n"
                "💡 DICA DO COACH — um conselho prático sobre como conduzir essa conversa\n\n"
                "Seja específico, natural e criativo. Evite perguntas genéricas tipo 'qual sua comida favorita'."
            )
            with st.spinner("🌳 Criando seu caminho de conversa..."):
                st.session_state.resultado_papo = chamar_ia(prompt)

        if st.session_state.resultado_papo:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                f"{st.session_state.resultado_papo}</pre></div>",
                unsafe_allow_html=True
            )

            # Botão "O que posso perguntar agora?"
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🔮 O que posso perguntar agora?")
            _tom_agora = st.radio("Escolha o caminho:", [
                "😂 Fazer rir", "🧠 Aprofundar", "❤️ Criar conexão", "🔥 Criar clima", "📖 Pedir uma história"
            ], horizontal=True, key="rad_gp_tom")

            if st.button("🔮 GERAR PRÓXIMA PERGUNTA", key="btn_gp_prox", use_container_width=True):
                prompt_prox = (
                    f"Com base neste caminho de conversa gerado:\n{st.session_state.resultado_papo}\n\n"
                    f"O usuário quer: {_tom_agora}\n\n"
                    "Gere 3 opções de próxima pergunta ou comentário que fluem naturalmente a partir desse contexto. "
                    "Cada opção deve ser diferente em tom mas conectada ao que foi dito. "
                    "Numere de 1 a 3 e explique brevemente o efeito de cada uma."
                )
                with st.spinner("🔮 Buscando os melhores caminhos..."):
                    st.session_state["resultado_papo_prox"] = chamar_ia(prompt_prox)

            if st.session_state.get("resultado_papo_prox"):
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state['resultado_papo_prox']}</pre></div>",
                    unsafe_allow_html=True
                )

    # ════════════════════════════════════
    # ♾️ PAPO INFINITO
    # ════════════════════════════════════
    elif st.session_state.pagina == "Papo Infinito":
        st.header("♾️ Papo Infinito")
        st.markdown("<div style='color:#64748B;margin-bottom:16px;'>Qualquer palavra vira uma árvore infinita de conversas. Explore os caminhos.</div>", unsafe_allow_html=True)

        _palavra = st.text_input("Digite qualquer palavra, assunto ou situação:",
            key="inp_pi_palavra",
            placeholder="Ex: academia, viagem, trabalho, relacionamento, música...")

        if st.button("♾️ GERAR ÁRVORE DE CONVERSA", key="btn_pi_gerar", use_container_width=True):
            if _palavra.strip():
                prompt_arvore = (
                    f"Palavra/assunto: {_palavra.upper()}\n\n"
                    "Crie uma árvore de conexões naturais de conversa a partir desse assunto.\n"
                    "Formato exato:\n"
                    "ASSUNTO RAIZ → assunto1 → assunto2 → ... → assunto12\n\n"
                    "Depois gere para o assunto raiz:\n"
                    "🗣️ PERGUNTA PRINCIPAL — uma pergunta poderosa e natural sobre esse assunto\n"
                    "📍 5 NÓDULOS PARA EXPLORAR — 5 sub-assuntos com uma pergunta/comentário cada:\n"
                    "  [emoji] NOME DO NÓ: pergunta ou comentário natural\n\n"
                    "Os sub-assuntos devem variar entre: humor, curiosidade, emoção, filosofia, experiência pessoal."
                )
                with st.spinner("♾️ Gerando árvore infinita..."):
                    st.session_state.resultado_infinito = chamar_ia(prompt_arvore)
                    st.session_state.no_ativo = _palavra.strip()

        if st.session_state.resultado_infinito:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                f"{st.session_state.resultado_infinito}</pre></div>",
                unsafe_allow_html=True
            )

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🔀 Explorar um nó específico")
            _no_escolhido = st.text_input("Digite um assunto da árvore para aprofundar:",
                key="inp_pi_no",
                placeholder="Ex: Autoestima, Disciplina, Relacionamentos...")
            _tom_no = st.radio("Transformar em:", [
                "🧠 Aprofundar", "😂 Deixar divertido", "❤️ Tornar pessoal",
                "🔥 Tornar sedutor", "📖 Transformar em história", "🔀 Mudar de assunto"
            ], horizontal=True, key="rad_pi_tom")

            if st.button("🔀 EXPLORAR NÓ", key="btn_pi_no", use_container_width=True):
                if _no_escolhido.strip():
                    prompt_no = (
                        f"Contexto: estamos numa conversa que começou com '{st.session_state.no_ativo}' "
                        f"e chegou em '{_no_escolhido}'.\n"
                        f"Modo: {_tom_no}\n\n"
                        "Gere:\n"
                        "1. Uma pergunta ou comentário poderoso sobre esse nó no tom escolhido\n"
                        "2. 3 possíveis respostas que a pessoa poderia dar\n"
                        "3. Para cada resposta, um gancho natural de continuação\n"
                        "4. 3 novos assuntos para onde a conversa pode migrar a partir daqui\n\n"
                        "Seja criativo, natural e específico."
                    )
                    with st.spinner("🔀 Explorando..."):
                        st.session_state["resultado_no"] = chamar_ia(prompt_no)

            if st.session_state.get("resultado_no"):
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state['resultado_no']}</pre></div>",
                    unsafe_allow_html=True
                )

    # ════════════════════════════════════
    # 📖 TRANSFORMAR EM HISTÓRIA
    # ════════════════════════════════════
    elif st.session_state.pagina == "Transformar em História":
        st.header("📖 Transformar em História")
        st.markdown("<div style='color:#64748B;margin-bottom:16px;'>Coloque qualquer acontecimento — a IA transforma em uma história com estrutura narrativa profissional.</div>", unsafe_allow_html=True)

        acontecimento = st.text_area("O que aconteceu? Descreva sem se preocupar com forma:",
            height=120, key="ta_hist_acontecimento",
            placeholder="Ex: Uma vez perdi um voo porque achei que tinha chegado cedo. Fiquei andando pelo aeroporto achando que tinha tempo e quando fui ver o portão já estava fechado...")

        th1, th2 = st.columns(2)
        with th1:
            tom_hist = st.selectbox("Tom da história:", [
                "😂 Engraçado / autodepreciativo",
                "🎭 Dramático / tenso",
                "🧠 Reflexivo / filosófico",
                "❤️ Emocionante / vulnerável",
                "😎 Casual / descontraído"
            ], key="sel_hist_tom")
        with th2:
            objetivo_hist = st.selectbox("Objetivo ao contar:", [
                "Fazer rir e criar conexão",
                "Mostrar personalidade e valores",
                "Criar curiosidade e intriga",
                "Gerar empatia e abertura",
                "Demonstrar coragem / superação"
            ], key="sel_hist_obj")

        if st.button("📖 TRANSFORMAR EM HISTÓRIA", key="btn_hist_gerar", use_container_width=True):
            if acontecimento.strip():
                prompt_hist = (
                    f"Acontecimento: {acontecimento}\n"
                    f"Tom: {tom_hist} | Objetivo: {objetivo_hist}\n\n"
                    "Transforme isso em uma história com estrutura narrativa completa:\n\n"
                    "① GANCHO — frase de abertura que prende atenção imediatamente\n"
                    "② CONTEXTO — onde, quando, o que estava acontecendo (2-3 frases)\n"
                    "③ CONFLITO — o que deu errado ou criou tensão\n"
                    "④ ESCALADA — como a situação se desenvolveu / piorou\n"
                    "⑤ VIRADA — o momento inesperado\n"
                    "⑥ CLÍMAX — o momento mais intenso ou engraçado\n"
                    "⑦ FINAL — como terminou\n"
                    "⑧ SIGNIFICADO — o que essa história revela sobre você (opcional, para usar se quiser)\n\n"
                    "💡 DICA — como contar essa história para ter mais impacto\n\n"
                    "Use linguagem natural, detalhes concretos e sensoriais. "
                    "A história deve soar como algo real e espontâneo, não ensaiado."
                )
                with st.spinner("📖 Construindo sua história..."):
                    st.session_state.resultado_historia = chamar_ia(prompt_hist)

        if st.session_state.resultado_historia:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                f"{st.session_state.resultado_historia}</pre></div>",
                unsafe_allow_html=True
            )
            # Guardar no Universo
            if st.button("💾 Salvar esta história no Meu Universo", key="btn_hist_salvar_universo"):
                _resumo = acontecimento[:100] + "..."
                if "historias" not in st.session_state.universo:
                    st.session_state.universo["historias"] = []
                st.session_state.universo["historias"].append({
                    "resumo": _resumo,
                    "historia": st.session_state.resultado_historia,
                    "data": datetime.now().strftime("%d/%m/%Y")
                })
                st.success("✅ História salva no Meu Universo!")

    # ════════════════════════════════════
    # ❤️ PAPO SEDUTOR
    # ════════════════════════════════════
    elif st.session_state.pagina == "Papo Sedutor":
        st.header("❤️ Papo Sedutor")
        st.markdown(
            "<div class='card' style='border-color:#6D28D9;'>"
            "Como criar <b>tensão, curiosidade, leveza e conexão</b> sem parecer ensaiado. "
            "Comunicação romântica baseada em presença, escuta, humor e autenticidade."
            "</div>", unsafe_allow_html=True
        )

        _tab_sed1, _tab_sed2 = st.tabs(["🔥 Gerador de Papo Sedutor", "💬 Analisador de Respostas"])

        with _tab_sed1:
            st.markdown("### Situação atual")
            ps1, ps2 = st.columns(2)
            with ps1:
                situacao_sed = st.selectbox("Onde vocês estão?", [
                    "Acabaram de se conhecer", "Primeira conversa por mensagem",
                    "Segundo / terceiro encontro", "Já se conhecem há um tempo",
                    "Depois de um tempo sem falar", "Tentando reconquistar"
                ], key="sel_sed_situacao")
                personalidade_dela = st.selectbox("Perfil dela:", [
                    "Desconhecido ainda", "Extrovertida e animada", "Reservada / tímida",
                    "Intelectual / séria", "Divertida / espontânea", "Misteriosa / difícil de ler",
                    "Independente / segura", "Intensa / emocional"
                ], key="sel_sed_personalidade")
            with ps2:
                estagio = st.selectbox("Estágio da comunicação sedutora:", [
                    "1 — Presença (chamar atenção)",
                    "2 — Curiosidade (fazer ela querer saber mais de mim)",
                    "3 — Conexão (criar algo em comum)",
                    "4 — Brincadeira (humor e provocação leve)",
                    "5 — Tensão romântica (criar clima)"
                ], key="sel_sed_estagio")
                contexto_sed = st.text_area("O que já aconteceu entre vocês?",
                    height=80, key="ta_sed_contexto",
                    placeholder="Ex: conheci ela hoje numa festa, ela falou que gosta de viajar sozinha e ficou curiosa quando contei que morei fora...")

            if st.button("🔥 GERAR PAPO SEDUTOR", key="btn_sed_gerar", use_container_width=True):
                prompt_sed = (
                    f"Situação: {situacao_sed}\n"
                    f"Perfil dela: {personalidade_dela}\n"
                    f"Estágio: {estagio}\n"
                    f"Contexto: {contexto_sed or 'nenhum'}\n\n"
                    "Gere comunicação sedutora para essa situação:\n\n"
                    "🌱 LEVE — uma frase de entrada ou comentário casual que cria curiosidade\n"
                    "🔍 CURIOSIDADE — uma pergunta que revela personalidade sem ser invasiva\n"
                    "🎭 BRINCADEIRA — uma provocação leve ou comentário bem-humorado\n"
                    "💜 PROFUNDIDADE — algo que cria conexão real\n"
                    "🔥 TENSÃO — uma frase que cria clima (use somente se houver abertura)\n\n"
                    "💡 AVISO DO COACH — o que observar e o que evitar nessa situação específica\n\n"
                    "IMPORTANTE: baseie-se em presença, escuta e autenticidade. "
                    "Nunca sugira pressão, insistência após desinteresse ou manipulação."
                )
                with st.spinner("🔥 Criando seu papo sedutor..."):
                    st.session_state.resultado_sedutor = chamar_ia(prompt_sed)

            if st.session_state.resultado_sedutor:
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state.resultado_sedutor}</pre></div>",
                    unsafe_allow_html=True
                )

        with _tab_sed2:
            st.markdown("### Ela respondeu — o que fazer agora?")
            st.markdown("<div style='color:#64748B;font-size:0.9em;margin-bottom:12px;'>Cole o que você disse e o que ela respondeu. A IA gera 3 caminhos de continuação.</div>", unsafe_allow_html=True)

            o_que_vc_disse = st.text_area("O que você disse:", height=70,
                key="ta_sed_vc", placeholder="Ex: Tenho a impressão de que você é mais perigosa do que parece.")
            o_que_ela_disse = st.text_area("O que ela respondeu:", height=70,
                key="ta_sed_ela", placeholder="Ex: Gosto de pessoas espontâneas.")

            if st.button("💬 GERAR 3 CAMINHOS DE RESPOSTA", key="btn_sed_resp", use_container_width=True):
                if o_que_ela_disse.strip():
                    prompt_resp = (
                        f"Você disse: '{o_que_vc_disse}'\n"
                        f"Ela respondeu: '{o_que_ela_disse}'\n\n"
                        "Gere 3 caminhos de continuação diferentes, cada um com um tom específico:\n\n"
                        "😂 HUMOR — uma resposta engraçada ou autodepreciativa que usa o que ela disse\n"
                        "🧠 CURIOSIDADE — uma pergunta ou comentário que aprofunda o que ela revelou\n"
                        "🔥 FLERTE — uma frase que usa a resposta dela para criar tensão ou aproximação\n\n"
                        "Para cada um:\n"
                        "- A frase exata\n"
                        "- Por que funciona\n"
                        "- O que ela provavelmente sente ao receber\n\n"
                        "Não invente sentimentos da pessoa — baseie-se somente no texto dela."
                    )
                    with st.spinner("💬 Analisando a resposta dela..."):
                        st.session_state.resultado_sedutor_resp = chamar_ia(prompt_resp)

            if st.session_state.resultado_sedutor_resp:
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state.resultado_sedutor_resp}</pre></div>",
                    unsafe_allow_html=True
                )

    # ════════════════════════════════════
    # 🚦 DETECTOR DE RECIPROCIDADE
    # ════════════════════════════════════
    elif st.session_state.pagina == "Detector de Reciprocidade":
        st.header("🚦 Detector de Reciprocidade")
        st.markdown(
            "<div class='card'>"
            "A IA analisa <b>somente os sinais presentes no texto</b>, sem afirmar que sabe o que a outra pessoa sente. "
            "Resultado honesto, sem ilusão e sem julgamento."
            "</div>", unsafe_allow_html=True
        )

        dr1, dr2 = st.columns(2)
        with dr1:
            o_que_vc_disse_dr = st.text_area("O que você disse / fez:", height=100,
                key="ta_dr_vc",
                placeholder="Ex: Mandei mensagem perguntando se ela queria sair no fim de semana...")
        with dr2:
            o_que_ela_disse_dr = st.text_area("O que ela respondeu / fez:", height=100,
                key="ta_dr_ela",
                placeholder="Ex: Ela disse 'que ideia boa! mas esse fim de semana não dá, tô ocupada'")

        contexto_dr = st.text_area("Contexto geral (opcional):", height=70,
            key="ta_dr_ctx",
            placeholder="Ex: nos conhecemos há 2 semanas, ela costuma responder rápido mas às vezes some por dias...")

        if st.button("🚦 ANALISAR RECIPROCIDADE", key="btn_dr_analisar", use_container_width=True):
            if o_que_ela_disse_dr.strip():
                prompt_dr = (
                    f"Você fez/disse: '{o_que_vc_disse_dr}'\n"
                    f"Ela fez/disse: '{o_que_ela_disse_dr}'\n"
                    f"Contexto: {contexto_dr or 'nenhum'}\n\n"
                    "Analise os SINAIS PRESENTES NO TEXTO com honestidade. Classifique:\n\n"
                    "🟢 HÁ SINAIS DE CONTINUIDADE, 🟡 AMBÍGUO ou ⚪ INSUFICIENTE\n\n"
                    "Formato da resposta:\n"
                    "CLASSIFICAÇÃO: [escolha uma]\n\n"
                    "SINAIS OBSERVADOS:\n"
                    "✅ [sinal positivo, se houver]\n"
                    "⚠️ [sinal de cautela, se houver]\n"
                    "❓ [o que está faltando para ter mais clareza]\n\n"
                    "INTERPRETAÇÃO HONESTA: (2-3 frases sem afirmar o que ela sente)\n\n"
                    "RECOMENDAÇÃO: o que fazer agora de forma respeitosa\n\n"
                    "NUNCA: afirme que sabe o que a outra pessoa sente. "
                    "Quando houver baixa reciprocidade, sugira respeitar o espaço."
                )
                with st.spinner("🚦 Analisando sinais..."):
                    st.session_state.resultado_reciprocidade = chamar_ia(prompt_dr)

        if st.session_state.resultado_reciprocidade:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                f"{st.session_state.resultado_reciprocidade}</pre></div>",
                unsafe_allow_html=True
            )

    # ════════════════════════════════════
    # 🎭 TREINO DE CONVERSA
    # ════════════════════════════════════
    elif st.session_state.pagina == "Treino de Conversa":
        st.header("🎭 Treino de Conversa")
        st.markdown("<div style='color:#64748B;margin-bottom:16px;'>A IA vira uma pessoa fictícia. Você conversa, treina e recebe análise de desempenho.</div>", unsafe_allow_html=True)

        if not st.session_state.treino_ativo:
            st.markdown("### Configurar a personagem")
            tc1, tc2 = st.columns(2)
            with tc1:
                personalidade_treino = st.selectbox("Personalidade da personagem:", [
                    "😊 Divertida e espontânea",
                    "😊 Tímida e reservada",
                    "🧠 Intelectual e curiosa",
                    "🔥 Extrovertida e animada",
                    "🌙 Misteriosa e difícil de ler",
                    "😜 Brincalhona e provocadora",
                    "📚 Séria e objetiva",
                    "💜 Interessada e aberta",
                    "😐 Indiferente / difícil de engajar"
                ], key="sel_tc_personalidade")
            with tc2:
                situacao_treino = st.selectbox("Situação:", [
                    "Acabaram de se conhecer numa festa",
                    "Conversa por mensagem (conhecidos)",
                    "Primeiro encontro num café",
                    "Colegas de trabalho começando a se aproximar",
                    "Amiga em comum apresentou vocês",
                    "Bate-papo casual sem contexto definido"
                ], key="sel_tc_situacao")
                nome_personagem = st.text_input("Nome da personagem:", value="Sofia", key="inp_tc_nome")

            if st.button("🎭 INICIAR TREINO", key="btn_tc_iniciar", use_container_width=True):
                system_treino = (
                    f"Você é {nome_personagem}, uma personagem fictícia com a seguinte personalidade: {personalidade_treino}.\n"
                    f"Situação: {situacao_treino}.\n\n"
                    "Regras:\n"
                    "- Responda como essa personagem responderia de verdade.\n"
                    "- Seja autêntica ao perfil: não seja nem fácil demais nem impossível.\n"
                    "- Reaja ao que o usuário diz — se ele for interessante, demonstre; se for genérico, seja mais fechada.\n"
                    "- Use linguagem natural, gírias se couber, emojis ocasionalmente.\n"
                    "- Nunca quebre o personagem ou diga que é uma IA.\n"
                    "- Responda em Português do Brasil."
                )
                st.session_state.chat_treino = [{"role": "system", "content": system_treino}]
                st.session_state["treino_config"] = {
                    "personalidade": personalidade_treino,
                    "situacao": situacao_treino,
                    "nome": nome_personagem
                }
                st.session_state.treino_ativo = True
                st.session_state.resultado_analise_treino = ""
                st.rerun()
        else:
            cfg = st.session_state.get("treino_config", {})
            nome_p = cfg.get("nome", "Personagem")
            st.markdown(
                f"<div class='card' style='border-color:#6D28D9;margin-bottom:12px;'>"
                f"<span style='color:#16A34A;font-weight:700;'>🎭 Conversando com {nome_p}</span> · "
                f"<span style='color:#64748B;font-size:0.85em;'>{cfg.get('personalidade','')} · {cfg.get('situacao','')}</span>"
                f"</div>", unsafe_allow_html=True
            )

            # Exibir histórico (excluindo system)
            msgs_visiveis = [m for m in st.session_state.chat_treino if m["role"] != "system"]
            if not msgs_visiveis:
                st.markdown(
                    "<div class='card' style='text-align:center;padding:20px;'>"
                    f"<div style='color:#16A34A;font-size:1em;'>💬 Diga olá para {nome_p}!</div>"
                    "</div>", unsafe_allow_html=True
                )
            for msg in msgs_visiveis:
                if msg["role"] == "user":
                    st.markdown(
                        f"<div class='card-chat-user'>"
                        f"<span style='color:#2563EB;font-size:0.8em;font-weight:600;'>VOCÊ</span><br>"
                        f"<span style='color:#1E293B;'>{msg['content']}</span></div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='card-chat-ia'>"
                        f"<span style='color:#16A34A;font-size:0.8em;font-weight:600;'>{nome_p.upper()}</span><br>"
                        f"<span style='color:#1E293B;'>{msg['content']}</span></div>",
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            _msg_tc = st.text_area("Sua mensagem:", height=80, key="ta_tc_msg",
                placeholder="Escreva como você realmente falaria...")
            tc_b1, tc_b2 = st.columns([3,1])
            with tc_b1:
                _enviar_tc = st.button("📨 ENVIAR", key="btn_tc_enviar", use_container_width=True)
            with tc_b2:
                _encerrar_tc = st.button("📊 ENCERRAR E ANALISAR", key="btn_tc_encerrar", use_container_width=True)

            if _enviar_tc and _msg_tc.strip():
                st.session_state.chat_treino.append({"role": "user", "content": _msg_tc.strip()})
                with st.spinner(f"💬 {nome_p} está digitando..."):
                    resposta = chamar_ia_chat(st.session_state.chat_treino)
                    if resposta:
                        st.session_state.chat_treino.append({"role": "assistant", "content": resposta})
                st.rerun()

            if _encerrar_tc:
                msgs_conv = [m for m in st.session_state.chat_treino if m["role"] != "system"]
                if len(msgs_conv) >= 2:
                    conv_txt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in msgs_conv])
                    prompt_analise = (
                        f"Analise a seguinte conversa de treino. O usuário conversou com a personagem {nome_p} "
                        f"({cfg.get('personalidade','')}).\n\n"
                        f"CONVERSA:\n{conv_txt}\n\n"
                        "Faça uma análise detalhada com notas de 1 a 10:\n\n"
                        "📊 ANÁLISE DE DESEMPENHO:\n"
                        "- Naturalidade: X/10\n"
                        "- Curiosidade demonstrada: X/10\n"
                        "- Humor: X/10\n"
                        "- Escuta ativa: X/10\n"
                        "- Desenvolvimento de assunto: X/10\n"
                        "- Excesso de perguntas: X/10 (10 = perguntou muito, 0 = equilibrado)\n"
                        "- Criação de conexão: X/10\n\n"
                        "✅ PONTOS FORTES: (o que funcionou bem)\n\n"
                        "⚠️ PONTOS A MELHORAR: (o que atrapalhou)\n\n"
                        "💡 CONSELHO PRINCIPAL: (uma coisa específica para aplicar na próxima vez)\n\n"
                        "Seja honesto e específico. Cite trechos da conversa quando necessário."
                    )
                    with st.spinner("📊 Analisando sua performance..."):
                        st.session_state.resultado_analise_treino = chamar_ia(prompt_analise)
                    st.session_state.treino_ativo = False
                    st.rerun()
                else:
                    st.warning("Converse um pouco mais antes de encerrar.")

            if st.session_state.resultado_analise_treino and not st.session_state.treino_ativo:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📊 Sua Análise de Desempenho")
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state.resultado_analise_treino}</pre></div>",
                    unsafe_allow_html=True
                )
                if st.button("🔄 Novo Treino", key="btn_tc_novo", use_container_width=True):
                    st.session_state.chat_treino = []
                    st.session_state.treino_ativo = False
                    st.session_state.resultado_analise_treino = ""
                    st.rerun()

    # ════════════════════════════════════
    # 🧠 MEU UNIVERSO
    # ════════════════════════════════════
    elif st.session_state.pagina == "Meu Universo":
        st.header("🧠 Meu Universo")
        st.markdown(
            "<div class='card'>"
            "Cadastre suas experiências, interesses e histórias. "
            "O app usa esse contexto para personalizar todas as sugestões — "
            "tornando a IA muito melhor do que um gerador genérico."
            "</div>", unsafe_allow_html=True
        )

        _tab_u1, _tab_u2, _tab_u3, _tab_u4 = st.tabs(["🌍 Experiências", "⭐ Interesses", "📖 Histórias", "🔮 Usar no Papo"])

        with _tab_u1:
            st.markdown("### Suas experiências de vida")
            st.markdown("<div style='color:#64748B;font-size:0.9em;margin-bottom:12px;'>Viagens, trabalhos, conquistas, fracassos, situações marcantes...</div>", unsafe_allow_html=True)

            _nova_exp = st.text_input("Adicionar experiência:", key="inp_u_exp",
                placeholder="Ex: Morei em Portugal por 2 anos, abri um negócio que não deu certo, fiz trilha na Chapada...")
            if st.button("➕ Adicionar", key="btn_u_exp_add"):
                if _nova_exp.strip():
                    st.session_state.universo["experiencias"].append(_nova_exp.strip())
                    st.success("✅ Adicionado!")
                    st.rerun()

            if st.session_state.universo["experiencias"]:
                st.markdown("**Suas experiências:**")
                for i, exp in enumerate(st.session_state.universo["experiencias"]):
                    col_e1, col_e2 = st.columns([5,1])
                    with col_e1:
                        st.markdown(f"<div class='node-box'>• {exp}</div>", unsafe_allow_html=True)
                    with col_e2:
                        if st.button("🗑️", key=f"btn_del_exp_{i}"):
                            st.session_state.universo["experiencias"].pop(i)
                            st.rerun()

        with _tab_u2:
            st.markdown("### Seus interesses")
            st.markdown("<div style='color:#64748B;font-size:0.9em;margin-bottom:12px;'>Esportes, música, negócios, tecnologia, filosofia, filmes...</div>", unsafe_allow_html=True)

            _cats_interesse = ["Esportes", "Música", "Tecnologia", "Negócios/empreendedorismo",
                               "Viagens", "Cinema/séries", "Filosofia/livros", "Gastronomia",
                               "Carros/motos", "Arte/design", "Saúde/fitness", "Outro"]
            _int_cat = st.selectbox("Categoria:", _cats_interesse, key="sel_u_int_cat")
            _int_desc = st.text_input("Detalhe:", key="inp_u_int_desc",
                placeholder="Ex: Treino musculação 5x por semana, adoro jazz dos anos 60...")
            if st.button("➕ Adicionar interesse", key="btn_u_int_add"):
                if _int_desc.strip():
                    st.session_state.universo["interesses"].append(f"{_int_cat}: {_int_desc.strip()}")
                    st.success("✅ Adicionado!")
                    st.rerun()

            if st.session_state.universo["interesses"]:
                st.markdown("**Seus interesses:**")
                for i, inter in enumerate(st.session_state.universo["interesses"]):
                    col_i1, col_i2 = st.columns([5,1])
                    with col_i1:
                        st.markdown(f"<div class='node-box'>• {inter}</div>", unsafe_allow_html=True)
                    with col_i2:
                        if st.button("🗑️", key=f"btn_del_int_{i}"):
                            st.session_state.universo["interesses"].pop(i)
                            st.rerun()

        with _tab_u3:
            st.markdown("### Suas histórias pessoais")
            st.markdown("<div style='color:#64748B;font-size:0.9em;margin-bottom:12px;'>Situações engraçadas, marcantes ou curiosas que valem contar.</div>", unsafe_allow_html=True)

            _nova_hist_resumo = st.text_input("Resumo da história:", key="inp_u_hist_res",
                placeholder="Ex: A vez que perdi meu voo achando que tinha chegado cedo...")
            _nova_hist_texto = st.text_area("Texto completo (opcional):", height=80, key="ta_u_hist_texto",
                placeholder="Detalhes da história para a IA usar como referência...")
            if st.button("➕ Salvar história", key="btn_u_hist_add"):
                if _nova_hist_resumo.strip():
                    if "historias" not in st.session_state.universo:
                        st.session_state.universo["historias"] = []
                    st.session_state.universo["historias"].append({
                        "resumo": _nova_hist_resumo.strip(),
                        "historia": _nova_hist_texto.strip(),
                        "data": datetime.now().strftime("%d/%m/%Y")
                    })
                    st.success("✅ História salva!")
                    st.rerun()

            historias = st.session_state.universo.get("historias", [])
            if historias:
                st.markdown("**Suas histórias:**")
                for i, h in enumerate(historias):
                    with st.expander(f"📖 {h['resumo'][:60]}... — {h.get('data','')}"):
                        if h.get("historia"):
                            st.markdown(f"<div style='color:#334155;white-space:pre-wrap;'>{h['historia']}</div>", unsafe_allow_html=True)
                        if st.button("🗑️ Excluir", key=f"btn_del_hist_{i}"):
                            st.session_state.universo["historias"].pop(i)
                            st.rerun()

        with _tab_u4:
            st.markdown("### 🔮 Usar meu Universo numa conversa")
            st.markdown("<div style='color:#64748B;font-size:0.9em;margin-bottom:12px;'>Descreva o assunto que está rolando — a IA busca no seu universo o que você pode usar.</div>", unsafe_allow_html=True)

            _assunto_uso = st.text_area("Sobre o que vocês estão falando?", height=80,
                key="ta_u_uso",
                placeholder="Ex: Ela mencionou que ama viajar para lugares fora do circuito turístico...")

            if st.button("🔮 O QUE POSSO USAR DESSA CONVERSA?", key="btn_u_usar", use_container_width=True):
                if _assunto_uso.strip() and (st.session_state.universo["experiencias"] or st.session_state.universo["interesses"]):
                    exp_txt = "\n".join(f"- {e}" for e in st.session_state.universo["experiencias"])
                    int_txt = "\n".join(f"- {i}" for i in st.session_state.universo["interesses"])
                    hist_resumos = "\n".join(f"- {h['resumo']}" for h in st.session_state.universo.get("historias",[]))

                    prompt_uso = (
                        f"A conversa está sobre: {_assunto_uso}\n\n"
                        f"EXPERIÊNCIAS DO USUÁRIO:\n{exp_txt or 'nenhuma cadastrada'}\n\n"
                        f"INTERESSES DO USUÁRIO:\n{int_txt or 'nenhum cadastrado'}\n\n"
                        f"HISTÓRIAS DO USUÁRIO:\n{hist_resumos or 'nenhuma cadastrada'}\n\n"
                        "Analise e responda:\n"
                        "🎯 CONEXÃO DIRETA: qual experiência/interesse/história se conecta com o assunto atual?\n"
                        "💬 COMO USAR: uma frase natural para trazer esse elemento à conversa\n"
                        "📖 GANCHO DE HISTÓRIA: se tiver uma história relevante, como introduzi-la?\n"
                        "🔀 PONTES INESPERADAS: conexões criativas entre o assunto dela e algo seu\n\n"
                        "Seja específico e natural. Isso é muito melhor do que perguntas genéricas."
                    )
                    with st.spinner("🔮 Buscando conexões no seu universo..."):
                        st.session_state["resultado_universo"] = chamar_ia(prompt_uso)
                elif not _assunto_uso.strip():
                    st.warning("Descreva o assunto da conversa.")
                else:
                    st.info("Cadastre suas experiências e interesses primeiro nas abas acima.")

            if st.session_state.get("resultado_universo"):
                st.markdown(
                    f"<div class='card-resultado'><pre style='white-space:pre-wrap;font-family:Inter,sans-serif;color:#1E293B;'>"
                    f"{st.session_state['resultado_universo']}</pre></div>",
                    unsafe_allow_html=True
                )

# ── RODAPÉ ──
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;font-size:0.75em;color:#475569;'>"
    "© 2026 Mestre do Papo IA · Você não precisa decorar assuntos. Precisa aprender a enxergar caminhos."
    "</div>", unsafe_allow_html=True
)
