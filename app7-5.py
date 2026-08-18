"""
AIRPORTB3DA — English Airport (Duolingo Dark Mode)
Proyecto para feria de inglés — 100% Python, 100% gratis.

Tema: vocabulario, gramática y frases del inglés que se usa en un aeropuerto real
(check-in, seguridad, inmigración, puerta de embarque, a bordo, reclamo de equipaje),
con interfaz multi-idioma (español, portugués, chino, ruso) para que cualquier
estudiante entienda lo que está diciendo mientras practica inglés.
"""

import difflib
import random
import re
from io import BytesIO

import speech_recognition as sr
import streamlit as st
from gtts import gTTS

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# ----------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA #
# ----------------------------------------------------------------------
st.set_page_config(page_title="AIRPORTB3DA — English Airport", page_icon="", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.85); }
        70% { opacity: 1; transform: scale(1.04); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-6px); }
        40% { transform: translateX(6px); }
        60% { transform: translateX(-4px); }
        80% { transform: translateX(4px); }
    }
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: 200px 0; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 6px rgba(88,204,2,0.25); }
        50% { box-shadow: 0 0 18px rgba(88,204,2,0.55); }
    }

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
        color: #f1f5f9 !important;
    }
    .stApp {
        background: linear-gradient(160deg, #16232a 0%, #0f181d 100%) !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        animation: fadeInUp 0.35s ease;
    }
    p, label, span, div { color: #e2e8f0; }
    [data-testid="stCaptionContainer"] p, .stCaption { color: #8394a0 !important; font-weight: 700 !important; }

    .block-container { animation: fadeInUp 0.3s ease; }
    .fade-card { animation: fadeInUp 0.4s ease; }
    .pop-card { animation: popIn 0.35s ease; }

    div.stButton > button {
        background-color: #58cc02 !important;
        color: #ffffff !important;
        border: none !important;
        border-bottom: 4px solid #46a302 !important;
        border-radius: 16px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        padding: 10px 24px !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.15s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background-color: #61e002 !important;
        color: #ffffff !important;
        transform: translateY(-2px) scale(1.015);
        box-shadow: 0 6px 14px rgba(88,204,2,0.25);
    }
    div.stButton > button:active { transform: translateY(2px) scale(0.98) !important; border-bottom: 1px solid #46a302 !important; }
    div.stButton > button:disabled {
        background-color: #37464f !important;
        border-bottom: 4px solid #2a343b !important;
        color: #8394a0 !important;
        opacity: 1 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stColumn"] div.stButton > button { width: 100%; }

    section[data-testid="stSidebar"] { background-color: #182730 !important; border-right: 2px solid #2e383e !important; }

    div[data-baseweb="select"] > div, input, textarea {
        background-color: #202f36 !important;
        border-radius: 12px !important;
        border: 2px solid #37464f !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-baseweb="select"] * { color: #ffffff !important; }
    div[data-baseweb="popover"] div { background-color: #202f36 !important; color: #ffffff !important; }
    div[data-baseweb="select"] > div:hover, input:focus, textarea:focus {
        border-color: #1cb0f6 !important;
        box-shadow: 0 0 0 3px rgba(28,176,246,0.2) !important;
    }

    div[role="radiogroup"] { gap: 10px; }
    div[role="radiogroup"] label {
        background: #202f36 !important;
        border: 2px solid #37464f !important;
        border-radius: 16px !important;
        padding: 10px 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 0 #182329 !important;
        transition: all 0.15s ease !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #1cb0f6 !important;
        background: #193848 !important;
        transform: translateX(3px);
    }
    div[role="radiogroup"] label p { color: #ffffff !important; }

    div[data-testid="stExpander"] {
        background-color: #202f36 !important;
        border: 2px solid #37464f !important;
        border-radius: 16px !important;
        transition: border-color 0.15s ease !important;
    }
    div[data-testid="stExpander"]:hover { border-color: #1cb0f6 !important; }
    div.stAlert { border-radius: 16px !important; border: none !important; font-weight: 700 !important; animation: popIn 0.3s ease; }
    div.stProgress > div > div > div > div {
        background: linear-gradient(90deg, #58cc02, #8fe030) !important;
        border-radius: 10px;
        transition: width 0.5s ease-in-out !important;
    }

    .score-card {
        background-color: #202f36; border: 2px solid #37464f; border-radius: 16px; padding: 12px;
        text-align: center; box-shadow: 0 4px 0 #182329; margin-bottom: 20px;
        animation: fadeInUp 0.3s ease;
    }
    .score-title { color: #8394a0; font-size: 12px; font-weight: 800; text-transform: uppercase; }
    .score-value { color: #ffc800; font-size: 24px; font-weight: 900; }
    .lives-row { text-align: center; font-size: 22px; margin-bottom: 12px; }
    .lives-row span.heart-lost { display: inline-block; animation: shake 0.4s ease; }
    .streak-badge {
        display: inline-block; background: linear-gradient(90deg,#ff9600,#ffc800); color: #182329 !important;
        font-weight: 900; padding: 4px 14px; border-radius: 20px; font-size: 13px; margin-bottom: 10px;
        animation: popIn 0.4s ease, glow 1.8s ease-in-out infinite;
    }
    .translation-box {
        background: #182730; border: 2px dashed #37464f; border-radius: 12px;
        padding: 10px 14px; margin-top: 8px; color: #84d8ff; font-weight: 700;
        animation: fadeInUp 0.35s ease;
    }
    .xp-bar-wrap {
        background: #0f181d; border-radius: 20px; height: 14px; overflow: hidden;
        border: 2px solid #37464f; margin-bottom: 16px;
    }
    .xp-bar-fill {
        height: 100%; background: linear-gradient(90deg, #1cb0f6, #58cc02);
        border-radius: 20px; transition: width 0.5s ease-in-out;
    }
    hr { border-color: #2e383e !important; margin: 20px 0 !important; }

    .b3da-watermark {
    position: fixed;
    top: 10px;
    right: 14px;
    z-index: 9999;
    font-family: 'Nunito', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: #8394a0 !important;
    opacity: 0.75;
    text-decoration: none !important;
    transition: opacity 0.15s ease;
}

.b3da-watermark:hover {
    opacity: 0.95;
    color: #1cb0f6 !important;
} </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<a class="b3da-watermark" href="https://www.instagram.com/alxxr.mrqz/" target="_blank">@alxxr.mrqz</a>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style="font-size: 38px; color: #58cc02 !important; margin-bottom: 0px;">AIRPORTB3DA</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# HELPER DE TRADUCCIÓN #
# ----------------------------------------------------------------------
def L(en, es, pt, zh, ru):
    return {"en": en, "es": es, "pt": pt, "zh": zh, "ru": ru}


LANG_OPTIONS = {
    "Español": "es",
    "Português": "pt",
    "中文 (Chino)": "zh",
    "Русский (Ruso)": "ru",
}
GTTS_CODE = {"en": "en", "es": "es", "pt": "pt", "zh": "zh-CN", "ru": "ru"}


def speak(text: str, lang: str = "en"):
    """Genera y reproduce un audio a partir de texto, usando gTTS."""
    tts = gTTS(text=text, lang=lang)
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    st.audio(buf, format="audio/mp3")


# ----------------------------------------------------------------------
# CATEGORÍAS #
# ----------------------------------------------------------------------
CATEGORIES = [
    "Check-in",
    "Seguridad",
    "Inmigración y aduana",
    "Puerta de embarque",
    "A bordo",
    "Reclamo de equipaje",
]

# Etiquetas traducidas de cada categoría (la clave interna sigue siendo el español,
# usado en todos los diccionarios de contenido; solo cambia lo que se muestra)
CATEGORY_LABELS = {
    "Check-in": {"en": "Check-in", "es": "Check-in", "pt": "Check-in", "zh": "值机", "ru": "Регистрация"},
    "Seguridad": {"en": "Security", "es": "Seguridad", "pt": "Segurança", "zh": "安检", "ru": "Безопасность"},
    "Inmigración y aduana": {"en": "Immigration and customs", "es": "Inmigración y aduana", "pt": "Imigração e alfândega",
                              "zh": "移民和海关", "ru": "Иммиграция и таможня"},
    "Puerta de embarque": {"en": "Boarding gate", "es": "Puerta de embarque", "pt": "Portão de embarque",
                            "zh": "登机口", "ru": "Выход на посадку"},
    "A bordo": {"en": "On board", "es": "A bordo", "pt": "A bordo", "zh": "机上", "ru": "На борту"},
    "Reclamo de equipaje": {"en": "Baggage claim", "es": "Reclamo de equipaje", "pt": "Retirada de bagagem",
                             "zh": "行李领取", "ru": "Выдача багажа"},
    "Todas": {"en": "All", "es": "Todas", "pt": "Todas", "zh": "全部", "ru": "Все"},
}

# Claves internas de los módulos (neutras) → etiqueta traducida mostrada en el menú
MENU_LABELS = {
    "quiz": {"en": "Quiz", "es": "Quiz", "pt": "Quiz", "zh": "测验", "ru": "Тест"},
    "vocab": {"en": "Vocabulary", "es": "Vocabulario", "pt": "Vocabulário", "zh": "词汇", "ru": "Словарь"},
    "grammar": {"en": "Grammar checker", "es": "Corrector de gramática", "pt": "Corretor de gramática",
                "zh": "语法纠错", "ru": "Проверка грамматики"},
    "pron": {"en": "Pronunciation", "es": "Pronunciación", "pt": "Pronúncia", "zh": "发音", "ru": "Произношение"},
    "conv": {"en": "Conversation", "es": "Conversación", "pt": "Conversação", "zh": "对话", "ru": "Разговор"},
}

# ----------------------------------------------------------------------
# TEXTOS DE INTERFAZ — toda la página se traduce, no solo el contenido
# ----------------------------------------------------------------------
UI_TEXT = {
    "subtitle": {"en": "Learn a new language for the airport — English Fair Edition!",
                 "es": "Aprende un nuevo idioma para el aeropuerto — ¡Edición Feria de Inglés!",
                 "pt": "Aprenda um novo idioma para o aeroporto — Edição Feira de Inglês!",
                 "zh": "学习机场用语 —— 英语展览特别版!",
                 "ru": "Учи новый язык для аэропорта — выпуск для конкурса английского!"},
    "sidebar_score_title": {"en": "SCORE / XP", "es": "PUNTAJE / XP", "pt": "PONTUAÇÃO / XP", "zh": "得分 / XP", "ru": "ОЧКИ / XP"},
    "sidebar_modules_label": {"en": "LEARNING MODULES", "es": "MÓDULOS DE APRENDIZAJE", "pt": "MÓDULOS DE APRENDIZAGEM",
                               "zh": "学习模块", "ru": "МОДУЛИ ОБУЧЕНИЯ"},
    "sidebar_target_title": {"en": "LEARNING", "es": "APRENDIENDO", "pt": "APRENDENDO", "zh": "正在学习", "ru": "ИЗУЧАЮ"},
    "change_lang_button": {"en": "🌐 Change my language", "es": "🌐 Cambiar mi idioma", "pt": "🌐 Mudar meu idioma", "zh": "🌐 更改我的语言",
                            "ru": "🌐 Сменить мой язык"},
    "change_target_button": {"en": "🎯 Change language to learn", "es": "🎯 Cambiar idioma a aprender",
                              "pt": "🎯 Mudar idioma a aprender", "zh": "🎯 更改要学习的语言",
                              "ru": "🎯 Сменить изучаемый язык"},
    "quiz_header": {"en": "🧠 Quiz", "es": "🧠 Quiz de inglés", "pt": "🧠 Quiz de inglês", "zh": "🧠 英语测验",
                     "ru": "🧠 Тест по английскому"},
    "area_label": {"en": "Choose the airport area:", "es": "Elige el área del aeropuerto:", "pt": "Escolha a área do aeroporto:",
                   "zh": "选择机场区域:", "ru": "Выберите зону аэропорта:"},
    "quiz_no_lives": {"en": "💔 You ran out of lives! The quiz will restart.",
                       "es": "💔 ¡Te quedaste sin vidas! El quiz se reinicia.",
                       "pt": "💔 Você ficou sem vidas! O quiz será reiniciado.",
                       "zh": "💔 你的生命值用完了!测验将重新开始。",
                       "ru": "💔 У вас закончились жизни! Тест начнётся заново."},
    "quiz_retry": {"en": "🔄 Retry quiz", "es": "🔄 Reintentar quiz", "pt": "🔄 Tentar novamente", "zh": "🔄 重新开始测验",
                    "ru": "🔄 Попробовать снова"},
    "quiz_streak": {"en": "🔥 Streak of", "es": "🔥 Racha de", "pt": "🔥 Sequência de", "zh": "🔥 连续答对", "ru": "🔥 Серия из"},
    "quiz_select_answer": {"en": "Select the correct answer:", "es": "Selecciona la respuesta correcta:", "pt": "Selecione a resposta correta:",
                            "zh": "选择正确答案:", "ru": "Выберите правильный ответ:"},
    "quiz_back": {"en": "⬅ Back", "es": "⬅ Atrás", "pt": "⬅ Voltar", "zh": "⬅ 返回", "ru": "⬅ Назад"},
    "quiz_check": {"en": "Check", "es": "Comprobar", "pt": "Verificar", "zh": "检查", "ru": "Проверить"},
    "quiz_pick_first": {"en": "Pick an option first.", "es": "Elige una opción primero.", "pt": "Escolha uma opção primeiro.",
                         "zh": "请先选择一个选项。", "ru": "Сначала выберите вариант."},
    "quiz_next": {"en": "Next ▶", "es": "Siguiente ▶", "pt": "Próxima ▶", "zh": "下一题 ▶", "ru": "Далее ▶"},
    "quiz_correct": {"en": "🎉 Correct!", "es": "🎉 ¡Correcto!", "pt": "🎉 Correto!", "zh": "🎉 正确!", "ru": "🎉 Правильно!"},
    "quiz_incorrect": {"en": "💡 Correct answer:", "es": "💡 Respuesta correcta:", "pt": "💡 Resposta correta:",
                        "zh": "💡 正确答案:", "ru": "💡 Правильный ответ:"},
    "vocab_header": {"en": "📖 Interactive vocabulary", "es": "📖 Vocabulario interactivo", "pt": "📖 Vocabulário interativo",
                      "zh": "📖 互动词汇", "ru": "📖 Интерактивный словарь"},
    "listen_target": {"en": "🔊 Listen", "es": "🔊 Escuchar", "pt": "🔊 Ouvir", "zh": "🔊 收听", "ru": "🔊 Слушать"},
    "listen_native": {"en": "🔊 In my language", "es": "🔊 En mi idioma", "pt": "🔊 No meu idioma", "zh": "🔊 用我的语言",
                       "ru": "🔊 На моём языке"},
    "grammar_header": {"en": "🩹 Grammar checker", "es": "🩹 Corrector de gramática", "pt": "🩹 Corretor de gramática",
                        "zh": "🩹 语法纠错器", "ru": "🩹 Проверка грамматики"},
    "grammar_intro": {"en": "Write a sentence in the language you're learning and the system will automatically detect common mistakes.",
                       "es": "Escribe una frase en el idioma que aprendes y el sistema detectará automáticamente errores comunes.",
                       "pt": "Escreva uma frase no idioma que você aprende e o sistema detectará automaticamente erros comuns.",
                       "zh": "用你正在学习的语言写一句话,系统会自动检测常见错误。",
                       "ru": "Напишите фразу на изучаемом языке, и система автоматически найдёт частые ошибки."},
    "grammar_textarea_label": {"en": "Your sentence:", "es": "Tu frase:", "pt": "Sua frase:",
                                "zh": "你的句子:", "ru": "Ваша фраза:"},
    "grammar_placeholder": {"en": "Type a sentence here...", "es": "Escribe una frase aquí...",
                             "pt": "Escreva uma frase aqui...", "zh": "在此输入一句话……",
                             "ru": "Введите фразу здесь..."},
    "grammar_check_button": {"en": "Check sentence", "es": "Revisar frase", "pt": "Revisar frase", "zh": "检查句子", "ru": "Проверить фразу"},
    "grammar_empty_warning": {"en": "Write a sentence first.", "es": "Escribe una frase primero.", "pt": "Escreva uma frase primeiro.",
                               "zh": "请先输入一个句子。", "ru": "Сначала введите фразу."},
    "grammar_suggestion_label": {"en": "Corrected suggestion:", "es": "Sugerencia corregida:", "pt": "Sugestão corrigida:",
                                  "zh": "修改建议:", "ru": "Исправленный вариант:"},
    "grammar_no_errors": {"en": "Perfect! No common errors were detected in the rule base.",
                           "es": "¡Perfecto! No se detectaron errores comunes en la base de reglas.",
                           "pt": "Perfeito! Nenhum erro comum foi detectado na base de regras.",
                           "zh": "太棒了!规则库中未检测到常见错误。",
                           "ru": "Отлично! В базе правил не найдено распространённых ошибок."},
    "grammar_example_label": {"en": "Correct example:", "es": "Ejemplo correcto:", "pt": "Exemplo correto:", "zh": "正确示例:",
                               "ru": "Правильный пример:"},
    "grammar_search_label": {"en": "🔎 Search a rule (optional):", "es": "🔎 Buscar una regla (opcional):", "pt": "🔎 Buscar uma regra (opcional):",
                              "zh": "🔎 搜索规则(可选):", "ru": "🔎 Найти правило (необязательно):"},
    "grammar_search_placeholder": {"en": "E.g.: modals, articles, comparatives...",
                                    "es": "Ej: modales, artículos, comparativos...",
                                    "pt": "Ex: modais, artigos, comparativos...",
                                    "zh": "例如:情态动词、冠词、比较级……",
                                    "ru": "Напр.: модальные глаголы, артикли, сравнения..."},
    "grammar_rules_expander": {"en": "See the {n} grammar rules included",
                                "es": "Ver las {n} reglas gramaticales incluidas",
                                "pt": "Ver as {n} regras gramaticais incluídas",
                                "zh": "查看包含的 {n} 条语法规则", "ru": "Показать {n} включённых правил"},
    "grammar_no_rules_found": {"en": "No rules were found for that term.",
                                "es": "No se encontraron reglas con ese término.",
                                "pt": "Nenhuma regra encontrada com esse termo.",
                                "zh": "未找到与该词相关的规则。", "ru": "Правил по этому запросу не найдено."},
    "pron_header": {"en": "🎙️ Pronunciation practice", "es": "🎙️ Práctica de pronunciación", "pt": "🎙️ Prática de pronúncia",
                     "zh": "🎙️ 发音练习", "ru": "🎙️ Практика произношения"},
    "pron_reverse_checkbox": {"en": "🔄 Reverse mode: show my language first and guess the target language",
                               "es": "🔄 Modo inverso: mostrar mi idioma primero y adivinar el idioma que aprendo",
                               "pt": "🔄 Modo inverso: mostrar meu idioma primeiro e adivinhar o idioma que aprendo",
                               "zh": "🔄 反向模式:先显示我的语言,再猜目标语言",
                               "ru": "🔄 Обратный режим: сначала мой язык, потом угадать изучаемый язык"},
    "pron_reverse_prompt": {"en": "How do you say this in the language you're learning?",
                             "es": "¿Cómo se dice esto en el idioma que aprendes?", "pt": "Como se diz isso no idioma que você aprende?",
                             "zh": "这个用你正在学习的语言怎么说?", "ru": "Как это сказать на изучаемом языке?"},
    "pron_reveal_button": {"en": "👁️ Reveal the sentence", "es": "👁️ Revelar la frase", "pt": "👁️ Revelar a frase",
                            "zh": "👁️ 显示句子", "ru": "👁️ Показать фразу"},
    "pron_repeat_prompt": {"en": "Repeat the following sentence:", "es": "Repite la siguiente frase:", "pt": "Repita a seguinte frase:",
                            "zh": "重复以下句子:", "ru": "Повторите следующую фразу:"},
    "pron_change_button": {"en": "🔁 Change sentence", "es": "🔁 Cambiar frase", "pt": "🔁 Trocar frase", "zh": "🔁 换一句",
                            "ru": "🔁 Сменить фразу"},
    "pron_listen_target_button": {"en": "▶️ Listen in the target language", "es": "▶️ Escuchar en el idioma que aprendo",
                                   "pt": "▶️ Ouvir no idioma que aprendo", "zh": "▶️ 听目标语言", "ru": "▶️ Слушать на изучаемом языке"},
    "pron_listen_native_button": {"en": "▶️ Listen in my language", "es": "▶️ Escuchar en mi idioma", "pt": "▶️ Ouvir no meu idioma",
                                   "zh": "▶️ 听我的语言", "ru": "▶️ Слушать на моём языке"},
    "pron_record_prompt": {"en": "Now record your voice saying the sentence in the target language:",
                            "es": "Ahora graba tu voz diciendo la frase en el idioma que aprendes:",
                            "pt": "Agora grave sua voz dizendo a frase no idioma que você aprende:",
                            "zh": "现在请录制你用目标语言说这句话的声音:",
                            "ru": "Теперь запишите фразу на изучаемом языке своим голосом:"},
    "pron_record_label": {"en": "Record voice", "es": "Grabar voz", "pt": "Gravar voz", "zh": "录音", "ru": "Записать голос"},
    "pron_system_heard": {"en": "The system understood:", "es": "El sistema entendió:", "pt": "O sistema entendeu:", "zh": "系统识别为:",
                           "ru": "Система распознала:"},
    "pron_accuracy_label": {"en": "Accuracy:", "es": "Precisión:", "pt": "Precisão:", "zh": "准确率:", "ru": "Точность:"},
    "pron_excellent": {"en": "Excellent pronunciation! 🎉", "es": "¡Excelente pronunciación! 🎉", "pt": "Excelente pronúncia! 🎉",
                        "zh": "发音非常棒!🎉", "ru": "Отличное произношение! 🎉"},
    "pron_good": {"en": "Well done! But you can still improve a bit more.",
                  "es": "¡Bien hecho! Pero puedes mejorar un poco más.",
                  "pt": "Muito bem! Mas você ainda pode melhorar um pouco.",
                  "zh": "做得不错!但还可以再提高一点。", "ru": "Хорошо! Но можно ещё немного лучше."},
    "pron_keep_practicing": {"en": "Keep practicing that sentence.", "es": "Sigue practicando esa frase.", "pt": "Continue praticando essa frase.",
                              "zh": "继续练习这句话吧。", "ru": "Продолжайте тренировать эту фразу."},
    "pron_unknown_value": {"en": "The audio could not be understood. Speak clearly and close to the microphone.",
                            "es": "No se pudo entender el audio. Habla claro y cerca del micrófono.",
                            "pt": "Não foi possível entender o áudio. Fale claramente e perto do microfone.",
                            "zh": "无法识别音频。请靠近麦克风清晰地说话。",
                            "ru": "Не удалось распознать аудио. Говорите чётко и ближе к микрофону."},
    "pron_request_error": {"en": "No connection to the recognition service. Check your internet.",
                            "es": "Sin conexión al servicio de reconocimiento. Revisa tu internet.",
                            "pt": "Sem conexão com o serviço de reconhecimento. Verifique sua internet.",
                            "zh": "无法连接识别服务。请检查你的网络连接。",
                            "ru": "Нет соединения со службой распознавания. Проверьте интернет."},
    "conv_header": {"en": "💬 Conversation simulation", "es": "💬 Simulación de conversación", "pt": "💬 Simulação de conversa",
                     "zh": "💬 对话模拟", "ru": "💬 Симуляция разговора"},
    "conv_scenario_label": {"en": "Scenario:", "es": "Escenario:", "pt": "Cenário:", "zh": "场景:", "ru": "Сценарий:"},
    "conv_staff_label": {"en": "Airport staff", "es": "Personal del aeropuerto", "pt": "Funcionário do aeroporto",
                          "zh": "机场工作人员", "ru": "Сотрудник аэропорта"},
    "conv_listen_button": {"en": "🔊 Listen", "es": "🔊 Escuchar", "pt": "🔊 Ouvir", "zh": "🔊 收听", "ru": "🔊 Слушать"},
    "conv_choose_response": {"en": "Choose your response:", "es": "Elige tu respuesta:", "pt": "Escolha sua resposta:",
                              "zh": "选择你的回答:", "ru": "Выберите свой ответ:"},
    "conv_you_label": {"en": "you", "es": "tú", "pt": "você", "zh": "你", "ru": "ты"},
    "conv_completed": {"en": "🎉 You've successfully completed this conversation scenario!",
                        "es": "🎉 ¡Has completado con éxito este escenario de conversación!",
                        "pt": "🎉 Você concluiu esse cenário de conversa com sucesso!",
                        "zh": "🎉 你已成功完成这个对话场景!",
                        "ru": "🎉 Вы успешно завершили этот сценарий разговора!"},
    "conv_restart_button": {"en": "Restart this scenario", "es": "Reiniciar este escenario", "pt": "Reiniciar este cenário",
                             "zh": "重新开始此场景", "ru": "Начать сценарий заново"},
}


def ui(key: str) -> str:
    """Devuelve el texto de interfaz en el idioma nativo elegido."""
    return UI_TEXT[key].get(NATIVE, UI_TEXT[key]["en"])


def cat_label(cat: str) -> str:
    """Devuelve la etiqueta traducida de una categoría del aeropuerto."""
    return CATEGORY_LABELS[cat].get(NATIVE, CATEGORY_LABELS[cat]["en"])

# ----------------------------------------------------------------------
# IDIOMAS DISPONIBLES — tanto para "mi idioma" (nativo) como para
# el idioma que la persona quiere APRENDER (objetivo/target)
# ----------------------------------------------------------------------
ALL_LANGS = {
    "English": "en",
    "Español": "es",
    "Português": "pt",
    "中文 (Chino)": "zh",
    "Русский (Ruso)": "ru",
}
REC_LANG_CODE = {"en": "en-US", "es": "es-ES", "pt": "pt-BR", "zh": "zh-CN", "ru": "ru-RU"}
TRANSLATE_LANG_CODE = {"en": "en", "es": "es", "pt": "pt", "zh": "zh-CN", "ru": "ru"}

# Textos mínimos de ConversTranslate — se muestran en el idioma de quien habla en su turno
CT_TEXT = {
    "en": {"title": "🌐 ConversTranslate", "record": "Record your voice", "recognized": "You said:",
           "translated": "Translation:", "next": "Next turn", "restart": "Restart conversation",
           "back": "⬅ Change mode", "not_understood": "Couldn't understand the audio, try again.",
           "conn_error": "No connection to the recognition service."},
    "es": {"title": "🌐 ConversTranslate", "record": "Grabar tu voz", "recognized": "Dijiste:",
           "translated": "Traducción:", "next": "Siguiente turno", "restart": "Reiniciar conversación",
           "back": "⬅ Cambiar de modo", "not_understood": "No se entendió el audio, intenta de nuevo.",
           "conn_error": "Sin conexión al servicio de reconocimiento."},
    "pt": {"title": "🌐 ConversTranslate", "record": "Grave sua voz", "recognized": "Você disse:",
           "translated": "Tradução:", "next": "Próximo turno", "restart": "Reiniciar conversa",
           "back": "⬅ Mudar de modo", "not_understood": "Não entendemos o áudio, tente novamente.",
           "conn_error": "Sem conexão com o serviço de reconhecimento."},
    "zh": {"title": "🌐 ConversTranslate", "record": "录音", "recognized": "你说的是:",
           "translated": "翻译:", "next": "下一轮", "restart": "重新开始对话",
           "back": "⬅ 更改模式", "not_understood": "无法识别音频,请重试。",
           "conn_error": "无法连接识别服务。"},
    "ru": {"title": "🌐 ConversTranslate", "record": "Записать голос", "recognized": "Вы сказали:",
           "translated": "Перевод:", "next": "Следующий ход", "restart": "Начать заново",
           "back": "⬅ Сменить режим", "not_understood": "Не удалось распознать аудио, попробуйте снова.",
           "conn_error": "Нет соединения со службой распознавания."},
}

# ----------------------------------------------------------------------
# ESTADO PERSISTENTE DE LA SESIÓN
# ----------------------------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "conv_nodes" not in st.session_state:
    st.session_state.conv_nodes = {cat: "start" for cat in CATEGORIES}
if "native_lang" not in st.session_state:
    st.session_state.native_lang = None
if "target_lang" not in st.session_state:
    st.session_state.target_lang = None
if "app_mode" not in st.session_state:
    st.session_state.app_mode = None
if "conv_lang_a" not in st.session_state:
    st.session_state.conv_lang_a = None
if "conv_lang_b" not in st.session_state:
    st.session_state.conv_lang_b = None
if "conv_turn" not in st.session_state:
    st.session_state.conv_turn = "a"

# ----------------------------------------------------------------------
# PANTALLA 0 — MODO: ConversTranslate (traducción hablada en vivo entre
# dos personas) o Aprendizaje (el resto de la app, con quiz/vocabulario/etc.)
# ----------------------------------------------------------------------
if st.session_state.app_mode is None:
    st.markdown(
        """
        <div style="text-align:center; margin-top:10px; margin-bottom:20px;">
            <h2 style="color:#58cc02 !important;">¿Qué quieres hacer?</h2>
            <p style="color:#8394a0; font-weight:700;">What do you want to do? · O que você quer fazer?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌐 ConversTranslate", use_container_width=True):
            st.session_state.app_mode = "convers"
            st.rerun()
    with c2:
        if st.button("📚 Aprendizaje", use_container_width=True):
            st.session_state.app_mode = "learn"
            st.rerun()
    st.stop()

# ----------------------------------------------------------------------
# MODO CONVERSTRANSLATE — dos personas, dos idiomas, conversación traducida
# por turnos: graba tu voz → se reconoce → se traduce → se escucha traducida.
# ----------------------------------------------------------------------
if st.session_state.app_mode == "convers":
    if st.button("⬅ Cambiar de modo", key="ct_back"):
        st.session_state.app_mode = None
        st.rerun()

    if not TRANSLATOR_AVAILABLE:
        st.error("Falta instalar la librería 'deep-translator' (pip install deep-translator) para usar este modo.")
        st.stop()

    st.header("🌐 ConversTranslate")

    if st.session_state.conv_lang_a is None or st.session_state.conv_lang_b is None:
        st.caption("Dos personas, dos idiomas, una conversación traducida en tiempo real.")
        col1, col2 = st.columns(2)
        with col1:
            label_a = st.selectbox("Persona A habla:", list(ALL_LANGS.keys()), key="pick_a")
        with col2:
            label_b = st.selectbox("Persona B habla:", list(ALL_LANGS.keys()), key="pick_b")
        if st.button("Comenzar conversación", use_container_width=True):
            st.session_state.conv_lang_a = ALL_LANGS[label_a]
            st.session_state.conv_lang_b = ALL_LANGS[label_b]
            st.session_state.conv_turn = "a"
            st.rerun()
        st.stop()

    lang_a, lang_b = st.session_state.conv_lang_a, st.session_state.conv_lang_b
    turn = st.session_state.conv_turn
    speaker_lang = lang_a if turn == "a" else lang_b
    listener_lang = lang_b if turn == "a" else lang_a
    speaker_person = "A" if turn == "a" else "B"
    t = CT_TEXT.get(speaker_lang, CT_TEXT["en"])
    speaker_label = next(lbl for lbl, code in ALL_LANGS.items() if code == speaker_lang)

    st.subheader(f"🎙️ Persona {speaker_person} — {speaker_label}")
    audio = st.audio_input(t["record"], key=f"ct_audio_{turn}")

    if audio is not None:
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source)
            said = recognizer.recognize_google(audio_data, language=REC_LANG_CODE[speaker_lang])
            st.write(f"{t['recognized']} **{said}**")
            translated = GoogleTranslator(source=TRANSLATE_LANG_CODE[speaker_lang],
                                           target=TRANSLATE_LANG_CODE[listener_lang]).translate(said)
            st.write(f"{t['translated']} **{translated}**")
            speak(translated, GTTS_CODE[listener_lang])
        except sr.UnknownValueError:
            st.error(t["not_understood"])
        except sr.RequestError:
            st.error(t["conn_error"])
        except Exception as e:
            st.error(f"⚠️ {e}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["next"], use_container_width=True, key="ct_next"):
            st.session_state.conv_turn = "b" if turn == "a" else "a"
            st.rerun()
    with col2:
        if st.button(t["restart"], use_container_width=True, key="ct_restart"):
            st.session_state.conv_lang_a = None
            st.session_state.conv_lang_b = None
            st.session_state.conv_turn = "a"
            st.rerun()
    st.stop()

# ----------------------------------------------------------------------
# PANTALLA 1 — IDIOMA NATIVO (el idioma en el que se muestra la página)
# ----------------------------------------------------------------------
if st.session_state.native_lang is None:
    st.markdown(
        """
        <div style="text-align:center; margin-top:10px; margin-bottom:20px;">
            <h2 style="color:#58cc02 !important;">¡Bienvenido! 👋 · Welcome! · Bem-vindo! · 欢迎! · Добро пожаловать!</h2>
            <p style="color:#8394a0; font-weight:700;">
                Elige tu idioma nativo. Toda la página se mostrará en ese idioma.<br>
                Choose your native language. The whole page will switch to it.<br>
                Escolha seu idioma nativo. Toda a página vai mudar para ele.<br>
                请选择您的母语,整个页面将切换为该语言。<br>
                Выберите родной язык — вся страница переключится на него.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (label, code) in enumerate(ALL_LANGS.items()):
        with cols[i % 2]:
            if st.button(label, key=f"native_{code}", use_container_width=True):
                st.session_state.native_lang = code
                st.rerun()
    st.stop()

NATIVE = st.session_state.native_lang

# ----------------------------------------------------------------------
# PANTALLA 2 — IDIOMA A APRENDER (el idioma objetivo del contenido)
# ----------------------------------------------------------------------
if st.session_state.target_lang is None:
    TARGET_SCREEN_TEXT = {
        "en": ("What language do you want to learn?", "All the vocabulary, phrases and conversations will use this language."),
        "es": ("¿Qué idioma quieres aprender?", "Todo el vocabulario, las frases y las conversaciones usarán este idioma."),
        "pt": ("Que idioma você quer aprender?", "Todo o vocabulário, frases e conversas usarão esse idioma."),
        "zh": ("你想学习哪种语言?", "所有词汇、短语和对话都将使用该语言。"),
        "ru": ("Какой язык вы хотите выучить?", "Весь словарь, фразы и разговоры будут на этом языке."),
    }
    title_txt, sub_txt = TARGET_SCREEN_TEXT.get(NATIVE, TARGET_SCREEN_TEXT["en"])
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:10px; margin-bottom:20px;">
            <h2 style="color:#1cb0f6 !important;">{title_txt}</h2>
            <p style="color:#8394a0; font-weight:700;">{sub_txt}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    options = {label: code for label, code in ALL_LANGS.items() if code != NATIVE}
    cols = st.columns(2)
    for i, (label, code) in enumerate(options.items()):
        with cols[i % 2]:
            if st.button(label, key=f"target_{code}", use_container_width=True):
                st.session_state.target_lang = code
                st.rerun()
    st.stop()

TARGET = st.session_state.target_lang

st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px; margin-top: -10px;">
        <p style="color: #8394a0; font-weight: 700; font-size: 16px;">{ui("subtitle")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# BANCO DE PREGUNTAS #
# ----------------------------------------------------------------------
QUIZ_BANK = {
    "en": [
        {"cat": "Check-in", "q": "You ___ check in online before arriving at the airport.",
         "options": ["should", "should to", "must to", "shoulds"], "answer": "should",
         "tip": L("Modal verbs (should, can, must...) are never followed by 'to'.",
                  "Los verbos modales (should, can, must...) nunca van seguidos de 'to'.",
                  "Os verbos modais (should, can, must...) nunca são seguidos de 'to'.",
                  "情态动词(should、can、must 等)后面绝不加 'to'。",
                  "Модальные глаголы (should, can, must...) никогда не сопровождаются 'to'.")},
        {"cat": "Check-in", "q": "I ___ my suitcase already; it's 25 kilos.",
         "options": ["weighed", "weight", "weighted", "have weight"], "answer": "weighed",
         "tip": L("The past tense of 'weigh' is 'weighed'.",
                  "El pasado del verbo 'weigh' (pesar) es 'weighed'.",
                  "O passado do verbo 'weigh' (pesar) é 'weighed'.",
                  "动词 'weigh'(称重)的过去式是 'weighed'。",
                  "Прошедшее время глагола 'weigh' (взвешивать) — 'weighed'.")},
        {"cat": "Check-in", "q": "Would you like a window or an aisle ___?",
         "options": ["sit", "seat", "sat", "seed"], "answer": "seat",
         "tip": L("'Seat' is the noun (chair); 'sit' is the verb 'to sit'.",
                  "'Seat' es el asiento; 'sit' es el verbo 'sentarse'.",
                  "'Seat' é o assento; 'sit' é o verbo 'sentar'.",
                  "'Seat' 是名词“座位”;'sit' 是动词“坐下”。",
                  "'Seat' — существительное «место»; 'sit' — глагол «сидеть».")},
        {"cat": "Check-in", "q": "There ___ two check-in counters open right now.",
         "options": ["is", "are", "be", "was"], "answer": "are",
         "tip": L("'Counters' is plural, so the verb must be 'are'.",
                  "'Counters' es plural, así que el verbo debe ser 'are'.",
                  "'Counters' é plural, então o verbo deve ser 'are'.",
                  "'Counters' 是复数,所以动词要用 'are'。",
                  "'Counters' — множественное число, поэтому глагол должен быть 'are'.")},
        {"cat": "Check-in", "q": "Excuse me, ___ I check in here for flight 205?",
         "options": ["Can", "Do", "Am", "Have"], "answer": "Can",
         "tip": L("To ask for permission or whether something is possible, use 'Can'.",
                  "Para pedir permiso o preguntar si algo es posible se usa 'Can'.",
                  "Para pedir permissão ou perguntar se algo é possível usa-se 'Can'.",
                  "请求许可或询问是否可能时用 'Can'。",
                  "Чтобы попросить разрешения или спросить о возможности, используют 'Can'.")},
        {"cat": "Seguridad", "q": "Please ___ your laptop from your bag before the X-ray scan.",
         "options": ["remove", "removed", "removing", "removes"], "answer": "remove",
         "tip": L("Instructions (imperative) use the verb in its base form.",
                  "Las instrucciones (imperativo) usan el verbo en su forma base.",
                  "Instruções (imperativo) usam o verbo na forma base.",
                  "指令(祈使句)用动词原形。",
                  "Инструкции (повелительное наклонение) используют базовую форму глагола.")},
        {"cat": "Seguridad", "q": "You ___ carry liquids over 100ml in your hand luggage.",
         "options": ["can't", "can", "must", "could"], "answer": "can't",
         "tip": L("This is a prohibition, so the negative form 'can't' is used.",
                  "Es una prohibición, por eso se usa la forma negativa 'can't'.",
                  "É uma proibição, por isso usa-se a forma negativa 'can't'.",
                  "这是禁止,所以用否定形式 'can't'。",
                  "Это запрет, поэтому используется отрицательная форма 'can't'.")},
        {"cat": "Seguridad", "q": "All passengers ___ walk through the metal detector.",
         "options": ["has to", "have to", "having to", "had"], "answer": "have to",
         "tip": L("'Passengers' is plural, so 'have to' is used, not 'has to'.",
                  "'Passengers' es plural, así que se usa 'have to', no 'has to'.",
                  "'Passengers' é plural, então usa-se 'have to', não 'has to'.",
                  "'Passengers' 是复数,用 'have to',不用 'has to'。",
                  "'Passengers' — множественное число, поэтому 'have to', а не 'has to'.")},
        {"cat": "Seguridad", "q": "___ you have any electronic devices in your bag?",
         "options": ["Do", "Does", "Are", "Is"], "answer": "Do",
         "tip": L("With 'you' in the simple present, questions are formed with 'Do'.",
                  "Con 'you' en presente simple, la pregunta se forma con 'Do'.",
                  "Com 'you' no presente simples, a pergunta se forma com 'Do'.",
                  "'you' 的一般现在时疑问句用 'Do'。",
                  "С 'you' в настоящем простом времени вопрос образуется с 'Do'.")},
        {"cat": "Seguridad", "q": "Yesterday I forgot to ___ my belt off, so the alarm went off.",
         "options": ["take", "took", "taking", "taken"], "answer": "take",
         "tip": L("After 'forgot to' the verb goes in the infinitive (base form).",
                  "Después de 'forgot to' el verbo va en infinitivo (forma base).",
                  "Depois de 'forgot to' o verbo vai no infinitivo (forma base).",
                  "'forgot to' 后面用动词原形(不定式)。",
                  "После 'forgot to' глагол ставится в инфинитиве (базовой форме).")},
        {"cat": "Inmigración y aduana", "q": "Do you have anything to ___ at customs?",
         "options": ["declare", "declaration", "declaring", "declared"], "answer": "declare",
         "tip": L("After 'to' the verb goes in its base form: 'to declare'.",
                  "Después de 'to' el verbo va en su forma base: 'to declare'.",
                  "Depois de 'to' o verbo vai na forma base: 'to declare'.",
                  "'to' 后面用动词原形:'to declare'。",
                  "После 'to' глагол ставится в базовой форме: 'to declare'.")},
        {"cat": "Inmigración y aduana", "q": "What is the purpose ___ your visit?",
         "options": ["of", "for", "at", "in"], "answer": "of",
         "tip": L("The correct expression is 'the purpose of'.",
                  "La expresión correcta es 'the purpose of'.",
                  "A expressão correta é 'the purpose of'.",
                  "正确的表达是 'the purpose of'。",
                  "Правильное выражение — 'the purpose of'.")},
        {"cat": "Inmigración y aduana", "q": "How long ___ you planning to stay?",
         "options": ["are", "is", "do", "does"], "answer": "are",
         "tip": L("With 'you', use 'are' in the present continuous.",
                  "Con 'you' se usa 'are' en presente continuo.",
                  "Com 'you' usa-se 'are' no presente contínuo.",
                  "'you' 的现在进行时用 'are'。",
                  "С 'you' в настоящем продолженном времени используется 'are'.")},
        {"cat": "Inmigración y aduana", "q": "Visitors from some countries ___ a visa.",
         "options": ["need", "needs", "needing", "needed"], "answer": "need",
         "tip": L("'Visitors' is plural, so the verb doesn't take -s.",
                  "'Visitors' es plural, así que el verbo no lleva -s.",
                  "'Visitors' é plural, então o verbo não leva -s.",
                  "'Visitors' 是复数,动词不加 -s。",
                  "'Visitors' — множественное число, глагол не принимает -s.")},
        {"cat": "Inmigración y aduana", "q": "The officer asked me ___ my passport.",
         "options": ["to show", "show", "showing", "showed"], "answer": "to show",
         "tip": L("Pattern 'ask someone to do something': the infinitive with 'to' is used.",
                  "Patrón 'ask someone to do something': se usa el infinitivo con 'to'.",
                  "Padrão 'ask someone to do something': usa-se o infinitivo com 'to'.",
                  "结构 'ask someone to do something':用带 'to' 的不定式。",
                  "Модель 'ask someone to do something': используется инфинитив с 'to'.")},
        {"cat": "Puerta de embarque", "q": "Flight 205 ___ now boarding at gate 12.",
         "options": ["is", "are", "be", "was"], "answer": "is",
         "tip": L("'Flight 205' is singular, so the verb is 'is'.",
                  "'Flight 205' es singular, así que el verbo es 'is'.",
                  "'Flight 205' é singular, então o verbo é 'is'.",
                  "'Flight 205' 是单数,动词用 'is'。",
                  "'Flight 205' — единственное число, поэтому глагол 'is'.")},
        {"cat": "Puerta de embarque", "q": "This is the final call ___ passengers traveling to Madrid.",
         "options": ["for", "to", "at", "of"], "answer": "for",
         "tip": L("The correct expression is 'final call for'.",
                  "La expresión correcta es 'final call for'.",
                  "A expressão correta é 'final call for'.",
                  "正确的表达是 'final call for'。",
                  "Правильное выражение — 'final call for'.")},
        {"cat": "Puerta de embarque", "q": "Your flight ___ delayed by one hour.",
         "options": ["has been", "have been", "is been", "was being"], "answer": "has been",
         "tip": L("'Flight' is singular → passive present perfect: 'has been delayed'.",
                  "'Flight' es singular → presente perfecto pasivo: 'has been delayed'.",
                  "'Flight' é singular → presente perfeito passivo: 'has been delayed'.",
                  "'Flight' 是单数 → 被动现在完成时:'has been delayed'。",
                  "'Flight' — единственное число → пассивный перфект: 'has been delayed'.")},
        {"cat": "Puerta de embarque", "q": "If you don't hurry, you ___ miss your flight.",
         "options": ["will", "would", "are", "were"], "answer": "will",
         "tip": L("First conditional: If + present, ... + will + verb.",
                  "Primer condicional: If + presente, ... + will + verbo.",
                  "Primeiro condicional: If + presente, ... + will + verbo.",
                  "第一条件句:If + 现在时, ... + will + 动词。",
                  "Первое условное: If + настоящее время, ... + will + глагол.")},
        {"cat": "Puerta de embarque", "q": "Passengers with small children ___ board first.",
         "options": ["can", "cans", "could to", "canning"], "answer": "can",
         "tip": L("'Can' never changes form and is never followed by 'to'.",
                  "'Can' no cambia de forma y nunca lleva 'to' después.",
                  "'Can' nunca muda de forma e nunca leva 'to' depois.",
                  "'Can' 不会变形,后面也绝不加 'to'。",
                  "'Can' не меняет форму и никогда не сопровождается 'to'.")},
        {"cat": "A bordo", "q": "Please ___ your seatbelt during takeoff.",
         "options": ["fasten", "fastens", "fastening", "fastened"], "answer": "fasten",
         "tip": L("Instruction (imperative): the verb goes in its base form.",
                  "Instrucción (imperativo): el verbo va en su forma base.",
                  "Instrução (imperativo): o verbo vai na forma base.",
                  "指令(祈使句):动词用原形。",
                  "Инструкция (повелительное наклонение): глагол в базовой форме.")},
        {"cat": "A bordo", "q": "The flight attendant ___ drinks after takeoff.",
         "options": ["serve", "serves", "serving", "served"], "answer": "serves",
         "tip": L("Third-person singular subject → the verb takes -s.",
                  "Sujeto en tercera persona singular → el verbo lleva -s.",
                  "Sujeito na terceira pessoa do singular → o verbo leva -s.",
                  "主语是第三人称单数 → 动词加 -s。",
                  "Подлежащее в третьем лице единственного числа → глагол принимает -s.")},
        {"cat": "A bordo", "q": "We ___ experiencing some turbulence right now.",
         "options": ["are", "is", "be", "was"], "answer": "are",
         "tip": L("With 'we' in the present continuous, use 'are'.",
                  "Con 'we' en presente continuo se usa 'are'.",
                  "Com 'we' no presente contínuo usa-se 'are'.",
                  "'we' 的现在进行时用 'are'。",
                  "С 'we' в настоящем продолженном используется 'are'.")},
        {"cat": "A bordo", "q": "Passengers ___ use their phones in airplane mode.",
         "options": ["can", "cans", "could to", "must to"], "answer": "can",
         "tip": L("Modals never take 's' or are followed by 'to'.",
                  "Los modales nunca llevan 's' ni van seguidos de 'to'.",
                  "Os modais nunca levam 's' nem são seguidos de 'to'.",
                  "情态动词绝不加 's',也不接 'to'。",
                  "Модальные глаголы никогда не принимают 's' и не сопровождаются 'to'.")},
        {"cat": "A bordo", "q": "Please put your bag ___ the seat in front of you.",
         "options": ["under", "in", "on", "at"], "answer": "under",
         "tip": L("The correct preposition for 'underneath' is 'under'.",
                  "La preposición correcta para 'debajo de' es 'under'.",
                  "A preposição correta para 'debaixo de' é 'under'.",
                  "“在……下面”的正确介词是 'under'。",
                  "Правильный предлог для «под» — 'under'.")},
        {"cat": "Reclamo de equipaje", "q": "Your suitcase will arrive on ___ number 4.",
         "options": ["carousel", "carrousel", "carusel", "carosel"], "answer": "carousel",
         "tip": L("The correct English spelling is 'carousel'.",
                  "La ortografía correcta en inglés es 'carousel'.",
                  "A ortografia correta em inglês é 'carousel'.",
                  "英语的正确拼写是 'carousel'。",
                  "Правильное написание по-английски — 'carousel'.")},
        {"cat": "Reclamo de equipaje", "q": "I need to report ___ luggage.",
         "options": ["lost", "lose", "losing", "loses"], "answer": "lost",
         "tip": L("'Lost' works here as an adjective (past participle).",
                  "'Lost' funciona aquí como adjetivo (participio pasado).",
                  "'Lost' funciona aqui como adjetivo (particípio passado).",
                  "这里 'lost' 用作形容词(过去分词)。",
                  "'Lost' здесь выступает как прилагательное (причастие прошедшего времени).")},
        {"cat": "Reclamo de equipaje", "q": "Where ___ I collect my baggage?",
         "options": ["can", "do", "is", "are"], "answer": "can",
         "tip": L("To ask where it's possible to do something, use 'can'.",
                  "Para preguntar dónde es posible hacer algo se usa 'can'.",
                  "Para perguntar onde é possível fazer algo usa-se 'can'.",
                  "询问哪里可以做某事时用 'can'。",
                  "Чтобы спросить, где можно что-то сделать, используют 'can'.")},
        {"cat": "Reclamo de equipaje", "q": "Keep your claim tag until you ___ your bag.",
         "options": ["receive", "received", "receiving", "receives"], "answer": "receive",
         "tip": L("With 'you' the verb goes in the base form: 'receive', not 'receives'.",
                  "Con 'you' el verbo va en forma base: 'receive', no 'receives'.",
                  "Com 'you' o verbo vai na forma base: 'receive', não 'receives'.",
                  "'you' 后面用动词原形:'receive',不用 'receives'。",
                  "С 'you' глагол в базовой форме: 'receive', а не 'receives'.")},
        {"cat": "Reclamo de equipaje", "q": "There ___ several bags still on the carousel.",
         "options": ["are", "is", "be", "was"], "answer": "are",
         "tip": L("'Several bags' is plural, so the verb is 'are'.",
                  "'Several bags' es plural, así que el verbo es 'are'.",
                  "'Several bags' é plural, então o verbo é 'are'.",
                  "'Several bags' 是复数,动词用 'are'。",
                  "'Several bags' — множественное число, поэтому глагол 'are'.")},
    ],
    "es": [
        {"cat": "Check-in", "q": "¿Prefiere un asiento de ventana o de ___?",
         "options": ["pasillo", "pasillos", "pasilla", "pasear"], "answer": "pasillo",
         "tip": L("'Pasillo' is the noun for 'aisle'.", "'Pasillo' es el sustantivo para 'aisle' en inglés (el corredor).",
                  "'Pasillo' é o substantivo para corredor.", "'Pasillo' 是名词“过道”。", "'Pasillo' — существительное «проход».")},
        {"cat": "Check-in", "q": "Yo ___ mi maleta esta mañana.",
         "options": ["facturé", "factura", "facturo", "facturaba"], "answer": "facturé",
         "tip": L("Use the preterite (facturé) for a finished past action.", "Se usa el pretérito (facturé) para una acción terminada en el pasado.",
                  "Usa-se o pretérito (facturé) para uma ação passada terminada.", "过去已完成的动作用简单过去时(facturé)。",
                  "Для завершённого действия в прошлом используется претерит (facturé).")},
        {"cat": "Seguridad", "q": "Debe quitarse los zapatos ___ pasar por el detector.",
         "options": ["antes de", "antes", "después", "desde"], "answer": "antes de",
         "tip": L("'Antes de' + infinitive means 'before doing something'.", "'Antes de' + infinitivo significa 'before doing something'.",
                  "'Antes de' + infinitivo significa 'antes de fazer algo'.", "'Antes de' + 不定式表示“做某事之前”。",
                  "'Antes de' + инфинитив означает «перед тем как сделать что-то».")},
        {"cat": "Seguridad", "q": "Los líquidos ___ ir en un envase pequeño.",
         "options": ["deben", "debe", "deber", "debo"], "answer": "deben",
         "tip": L("'Líquidos' is plural, so the verb is 'deben'.", "'Líquidos' es plural, así que el verbo es 'deben'.",
                  "'Líquidos' é plural, então o verbo é 'deben'.", "'Líquidos' 是复数,动词用 'deben'。",
                  "'Líquidos' — множественное число, поэтому глагол 'deben'.")},
        {"cat": "Inmigración y aduana", "q": "¿Cuál es el ___ de su visita?",
         "options": ["motivo", "movido", "mundo", "modo"], "answer": "motivo",
         "tip": L("'Motivo' means 'purpose/reason'.", "'Motivo' significa 'purpose/reason' en inglés.",
                  "'Motivo' significa 'propósito/razão'.", "'Motivo' 的意思是“目的/原因”。", "'Motivo' означает «цель/причина».")},
        {"cat": "Inmigración y aduana", "q": "Yo ___ turista, no vengo a trabajar.",
         "options": ["soy", "estoy", "es", "está"], "answer": "soy",
         "tip": L("Use 'ser' (soy) for identity/occupation, not 'estar'.", "Se usa 'ser' (soy) para identidad/ocupación, no 'estar'.",
                  "Usa-se 'ser' (soy) para identidade/ocupação, não 'estar'.", "表示身份/职业用 'ser'(soy),不用 'estar'。",
                  "Для идентичности/рода занятий используется 'ser' (soy), а не 'estar'.")},
        {"cat": "Puerta de embarque", "q": "El vuelo ___ retrasado una hora.",
         "options": ["está", "es", "son", "están"], "answer": "está",
         "tip": L("Use 'estar' (está) for a temporary state like a delay.", "Se usa 'estar' (está) para un estado temporal como un retraso.",
                  "Usa-se 'estar' (está) para um estado temporário como um atraso.", "表示临时状态(如延误)用 'estar'(está)。",
                  "Для временного состояния, как задержка, используется 'estar' (está).")},
        {"cat": "Puerta de embarque", "q": "Su puerta de embarque ___ la número doce.",
         "options": ["es", "está", "son", "fue"], "answer": "es",
         "tip": L("Use 'ser' (es) to identify which gate it is.", "Se usa 'ser' (es) para identificar cuál es la puerta.",
                  "Usa-se 'ser' (es) para identificar qual é o portão.", "表示是哪个登机口用 'ser'(es)。",
                  "Для указания, какой это выход, используется 'ser' (es).")},
        {"cat": "A bordo", "q": "Por favor, ___ su cinturón de seguridad.",
         "options": ["abróchese", "abrochando", "abrochar", "abrocha"], "answer": "abróchese",
         "tip": L("Formal commands use the 'usted' imperative form.", "Los mandatos formales usan la forma imperativa de 'usted'.",
                  "Comandos formais usam a forma imperativa de 'usted'.", "正式命令用“您”的祈使式。",
                  "Формальные команды используют повелительную форму «usted».")},
        {"cat": "A bordo", "q": "Estamos experimentando ___ turbulencia.",
         "options": ["algo de", "algunos", "mucho de", "unos"], "answer": "algo de",
         "tip": L("'Algo de' means 'a bit of' before an uncountable noun.", "'Algo de' significa 'a bit of' antes de un sustantivo incontable.",
                  "'Algo de' significa 'um pouco de' antes de um substantivo incontável.", "'Algo de' 用在不可数名词前,意为“一点”。",
                  "'Algo de' означает «немного» перед неисчисляемым существительным.")},
        {"cat": "Reclamo de equipaje", "q": "Su maleta llegará en la ___ número cuatro.",
         "options": ["banda", "banco", "bando", "baño"], "answer": "banda",
         "tip": L("'Banda' is the word for the baggage carousel.", "'Banda' es la palabra para la banda transportadora.",
                  "'Banda' é a palavra para a esteira de bagagem.", "'Banda' 指行李传送带。", "'Banda' — слово для багажной ленты.")},
        {"cat": "Reclamo de equipaje", "q": "Necesito reportar una maleta ___.",
         "options": ["perdida", "perdido", "perdidos", "perdidas"], "answer": "perdida",
         "tip": L("Adjectives agree in gender/number: 'maleta' is feminine singular.", "Los adjetivos concuerdan en género/número: 'maleta' es femenino singular.",
                  "Os adjetivos concordam em gênero/número: 'maleta' é feminino singular.", "形容词需与名词性数一致:'maleta' 是阴性单数。",
                  "Прилагательные согласуются в роде/числе: 'maleta' — женский род, единственное число.")},
    ],
    "pt": [
        {"cat": "Check-in", "q": "Você prefere um assento na janela ou no ___?",
         "options": ["corredor", "corredores", "corrida", "correndo"], "answer": "corredor",
         "tip": L("'Corredor' means 'aisle'.", "'Corredor' significa 'aisle' en inglés.", "'Corredor' significa 'aisle' (corredor do avião).",
                  "'Corredor' 的意思是“过道”。", "'Corredor' означает «проход».")},
        {"cat": "Check-in", "q": "Eu ___ minha mala esta manhã.",
         "options": ["despachei", "despacho", "despachava", "despachando"], "answer": "despachei",
         "tip": L("Use the simple past (despachei) for a completed action.", "Se usa el pretérito (despachei) para una acción completada.",
                  "Usa-se o pretérito perfeito (despachei) para uma ação concluída.", "已完成的动作用简单过去式(despachei)。",
                  "Для завершённого действия используется прошедшее время (despachei).")},
        {"cat": "Seguridad", "q": "Você deve tirar os sapatos ___ passar pelo detector.",
         "options": ["antes de", "antes", "depois", "desde"], "answer": "antes de",
         "tip": L("'Antes de' + infinitive means 'before doing something'.", "'Antes de' + infinitivo significa 'before doing something'.",
                  "'Antes de' + infinitivo significa 'antes de fazer algo'.", "'Antes de' + 不定式表示“做某事之前”。",
                  "'Antes de' + инфинитив означает «перед тем как сделать что-то».")},
        {"cat": "Seguridad", "q": "Os líquidos ___ estar em um recipiente pequeno.",
         "options": ["devem", "deve", "dever", "devo"], "answer": "devem",
         "tip": L("'Líquidos' is plural, so the verb is 'devem'.", "'Líquidos' es plural, así que el verbo es 'devem'.",
                  "'Líquidos' é plural, então o verbo é 'devem'.", "'Líquidos' 是复数,动词用 'devem'。",
                  "'Líquidos' — множественное число, поэтому глагол 'devem'.")},
        {"cat": "Inmigración y aduana", "q": "Qual é o ___ da sua visita?",
         "options": ["motivo", "movido", "mundo", "modo"], "answer": "motivo",
         "tip": L("'Motivo' means 'purpose/reason'.", "'Motivo' significa 'purpose/reason'.", "'Motivo' significa 'propósito/razão'.",
                  "'Motivo' 的意思是“目的/原因”。", "'Motivo' означает «цель/причина».")},
        {"cat": "Inmigración y aduana", "q": "Eu ___ turista, não venho trabalhar.",
         "options": ["sou", "estou", "é", "está"], "answer": "sou",
         "tip": L("Use 'ser' (sou) for identity/occupation, not 'estar'.", "Se usa 'ser' (sou) para identidad/ocupación, no 'estar'.",
                  "Usa-se 'ser' (sou) para identidade/ocupação, não 'estar'.", "表示身份/职业用 'ser'(sou),不用 'estar'。",
                  "Для идентичности/занятия используется 'ser' (sou), а не 'estar'.")},
        {"cat": "Puerta de embarque", "q": "O voo ___ atrasado uma hora.",
         "options": ["está", "é", "são", "estão"], "answer": "está",
         "tip": L("Use 'estar' (está) for a temporary state like a delay.", "Se usa 'estar' (está) para un estado temporal como un retraso.",
                  "Usa-se 'estar' (está) para um estado temporário, como um atraso.", "表示临时状态(如延误)用 'estar'(está)。",
                  "Для временного состояния, как задержка, используется 'estar' (está).")},
        {"cat": "Puerta de embarque", "q": "Seu portão de embarque ___ o número doze.",
         "options": ["é", "está", "são", "foi"], "answer": "é",
         "tip": L("Use 'ser' (é) to identify which gate it is.", "Se usa 'ser' (es) para identificar cuál es la puerta.",
                  "Usa-se 'ser' (é) para identificar qual é o portão.", "表示是哪个登机口用 'ser'(é)。",
                  "Для указания, какой это выход, используется 'ser' (é).")},
        {"cat": "A bordo", "q": "Por favor, ___ o cinto de segurança.",
         "options": ["afivele", "afivelando", "afivelar", "afivela"], "answer": "afivele",
         "tip": L("Formal commands use the imperative form.", "Los mandatos formales usan la forma imperativa.",
                  "Comandos formais usam a forma imperativa.", "正式命令用祈使式。", "Формальные команды используют повелительную форму.")},
        {"cat": "A bordo", "q": "Estamos passando por ___ turbulência.",
         "options": ["um pouco de", "alguns", "muito de", "uns"], "answer": "um pouco de",
         "tip": L("'Um pouco de' means 'a bit of' before an uncountable noun.", "'Un poco de' significa 'a bit of' antes de sustantivo incontable.",
                  "'Um pouco de' significa 'a bit of' antes de substantivo incontável.", "'Um pouco de' 用在不可数名词前,意为“一点”。",
                  "'Um pouco de' означает «немного» перед неисчисляемым существительным.")},
        {"cat": "Reclamo de equipaje", "q": "Sua mala vai chegar na ___ número quatro.",
         "options": ["esteira", "banco", "banda", "banho"], "answer": "esteira",
         "tip": L("'Esteira' is the word for the baggage carousel.", "'Esteira' es la palabra para la banda transportadora en portugués.",
                  "'Esteira' é a palavra para a esteira de bagagem.", "'Esteira' 指行李传送带。", "'Esteira' — слово для багажной ленты.")},
        {"cat": "Reclamo de equipaje", "q": "Preciso reportar uma mala ___.",
         "options": ["perdida", "perdido", "perdidos", "perdidas"], "answer": "perdida",
         "tip": L("Adjectives agree in gender/number: 'mala' is feminine singular.", "Los adjetivos concuerdan en género/número: 'mala' es femenino singular.",
                  "Os adjetivos concordam em gênero/número: 'mala' é feminino singular.", "形容词需与名词性数一致:'mala' 是阴性单数。",
                  "Прилагательные согласуются в роде/числе: 'mala' — женский род, единственное число.")},
    ],
    "zh": [
        {"cat": "Check-in", "q": "您想要靠窗还是靠___的座位?",
         "options": ["走道", "走路", "跑道", "通道"], "answer": "走道",
         "tip": L("'走道' means 'aisle'.", "'走道' significa 'aisle' (pasillo).", "'走道' significa 'aisle' (corredor).",
                  "'走道' 的意思是“过道”。", "'走道' означает «проход».")},
        {"cat": "Check-in", "q": "我今天早上___了我的行李。",
         "options": ["托运", "托运了", "在托运", "要托运"], "answer": "托运了",
         "tip": L("Add '了' after the verb to show a completed action.", "Se añade '了' después del verbo para mostrar una acción completada.",
                  "Adiciona-se '了' depois do verbo para mostrar uma ação concluída.", "动词后加“了”表示动作已完成。",
                  "После глагола добавляется «了» для завершённого действия.")},
        {"cat": "Seguridad", "q": "过安检前请___鞋子。",
         "options": ["脱掉", "脱掉了", "脱着", "脱去着"], "answer": "脱掉",
         "tip": L("'脱掉' means to take something off completely.", "'脱掉' significa quitarse algo por completo.", "'脱掉' significa tirar algo completamente.",
                  "'脱掉' 表示把某物完全脱下。", "'脱掉' означает полностью снять что-то.")},
        {"cat": "Seguridad", "q": "液体必须装在___的容器里。",
         "options": ["小", "小的", "是小", "很小是"], "answer": "小的",
         "tip": L("Adjective + '的' + noun is the basic modifier pattern.", "Adjetivo + '的' + sustantivo es el patrón básico.",
                  "Adjetivo + '的' + substantivo é o padrão básico.", "“形容词+的+名词”是基本的修饰结构。",
                  "«Прилагательное + 的 + существительное» — базовая модель.")},
        {"cat": "Inmigración y aduana", "q": "您此行___是什么?",
         "options": ["目的", "目标", "目录", "目光"], "answer": "目的",
         "tip": L("'目的' means 'purpose'.", "'目的' significa 'purpose' (propósito).", "'目的' significa 'purpose' (propósito).",
                  "'目的' 的意思是“目的”。", "'目的' означает «цель».")},
        {"cat": "Inmigración y aduana", "q": "我___游客,不是来工作的。",
         "options": ["是", "在", "很", "有"], "answer": "是",
         "tip": L("'是' links identity/category: subject + 是 + noun.", "'是' conecta identidad/categoría: sujeto + 是 + sustantivo.",
                  "'是' liga identidade/categoria: sujeito + 是 + substantivo.", "'是' 用于连接身份/类别:主语+是+名词。",
                  "'是' связывает подлежащее с существительным для указания категории.")},
        {"cat": "Puerta de embarque", "q": "航班___延误了一个小时。",
         "options": ["已经", "正在", "快要", "曾经"], "answer": "已经",
         "tip": L("'已经' (already) is used with a completed change of state.", "'已经' (ya) se usa con un cambio de estado ya completado.",
                  "'já' (已经) usa-se com uma mudança de estado já concluída.", "'已经' 用于已经发生的状态变化。",
                  "'已经' (уже) используется для завершённого изменения состояния.")},
        {"cat": "Puerta de embarque", "q": "您的登机口___十二号。",
         "options": ["是", "在", "有", "很"], "answer": "是",
         "tip": L("'是' identifies which gate it is.", "'是' identifica cuál es la puerta.", "'é' (是) identifica qual é o portão.",
                  "'是' 用来说明是哪个登机口。", "'是' указывает, какой это выход.")},
        {"cat": "A bordo", "q": "请___好安全带。",
         "options": ["系", "开", "关", "拿"], "answer": "系",
         "tip": L("'系' means to fasten/tie (a seatbelt).", "'系' significa abrocharse (el cinturón).", "'系' significa apertar/amarrar (o cinto).",
                  "'系' 表示“系上”(安全带)。", "'系' означает пристегнуть/завязать (ремень).")},
        {"cat": "A bordo", "q": "我们正在经历一些___。",
         "options": ["颠簸", "颠倒", "颠峰", "颠簸的"], "answer": "颠簸",
         "tip": L("'颠簸' means 'turbulence'.", "'颠簸' significa 'turbulence' (turbulencia).", "'颠簸' significa 'turbulence' (turbulência).",
                  "'颠簸' 的意思是“颠簸/湍流”。", "'颠簸' означает «турбулентность».")},
        {"cat": "Reclamo de equipaje", "q": "您的行李将从___号转盘取回。",
         "options": ["四", "四个", "四位", "四条"], "answer": "四",
         "tip": L("Numbers before '号' (number) don't need a measure word.", "Los números antes de '号' (número) no necesitan clasificador.",
                  "Números antes de '号' (número) não precisam de classificador.", "数字在“号”前不需要量词。",
                  "Числа перед «号» (номер) не требуют счётного слова.")},
        {"cat": "Reclamo de equipaje", "q": "我需要报告一___丢失的行李。",
         "options": ["件", "个", "只", "条"], "answer": "件",
         "tip": L("'件' is the measure word for pieces of luggage.", "'件' es el clasificador para piezas de equipaje.",
                  "'件' é o classificador para peças de bagagem.", "'件' 是行李件数的量词。", "'件' — счётное слово для предметов багажа.")},
    ],
    "ru": [
        {"cat": "Check-in", "q": "Вы предпочитаете место у окна или у ___?",
         "options": ["прохода", "проход", "проходе", "проходом"], "answer": "прохода",
         "tip": L("'У' requires the genitive case: 'у прохода'.", "'У' requiere el caso genitivo: 'у прохода'.",
                  "'У' requer o caso genitivo: 'у прохода'.", "'У' 后面要用第二格(属格):'у прохода'。",
                  "После 'у' используется родительный падеж: 'у прохода'.")},
        {"cat": "Check-in", "q": "Я уже ___ свой чемодан.",
         "options": ["сдал", "сдаю", "сдавать", "сдам"], "answer": "сдал",
         "tip": L("The perfective past 'сдал' shows a completed action.", "El pasado perfectivo 'сдал' muestra una acción completada.",
                  "O passado perfectivo 'сдал' mostra uma ação concluída.", "完成体过去式 'сдал' 表示动作已完成。",
                  "Совершенный вид прошедшего времени 'сдал' показывает завершённое действие.")},
        {"cat": "Seguridad", "q": "Снимите обувь ___ проходом через сканер.",
         "options": ["перед", "до", "после", "между"], "answer": "перед",
         "tip": L("'Перед' + instrumental means 'before' an event.", "'Перед' + instrumental significa 'before' (antes de).",
                  "'Перед' + instrumental significa 'antes de'.", "'Перед'+第五格(工具格)表示“在……之前”。",
                  "'Перед' + творительный падеж означает «до».")},
        {"cat": "Seguridad", "q": "Жидкости должны быть в маленьк___ контейнере.",
         "options": ["ом", "ая", "ое", "ий"], "answer": "ом",
         "tip": L("Adjective agrees with the noun's case: prepositional masculine 'маленьком'.", "El adjetivo concuerda con el caso del sustantivo: prepositivo masculino.",
                  "O adjetivo concorda com o caso do substantivo: preposicional masculino.", "形容词要与名词的格一致:阳性前置格。",
                  "Прилагательное согласуется с падежом существительного: предложный, мужской род.")},
        {"cat": "Inmigración y aduana", "q": "Какова ___ вашего визита?",
         "options": ["цель", "целая", "целями", "целям"], "answer": "цель",
         "tip": L("'Цель' means 'purpose' (feminine noun, nominative).", "'Цель' significa 'purpose' (sustantivo femenino, nominativo).",
                  "'Цель' significa 'purpose' (substantivo feminino, nominativo).", "'Цель' 的意思是“目的”(阴性名词,主格)。",
                  "'Цель' означает «цель» (существительное женского рода, именительный падеж).")},
        {"cat": "Inmigración y aduana", "q": "Я ___ турист, я не приехал работать.",
         "options": ["—", "есть", "был", "буду"], "answer": "—",
         "tip": L("In the present tense, Russian usually omits the verb 'to be'.", "En presente, el ruso normalmente omite el verbo 'ser/estar'.",
                  "No presente, o russo geralmente omite o verbo 'ser/estar'.", "俄语现在时通常省略系动词“是”。",
                  "В настоящем времени в русском языке глагол «быть» обычно опускается.")},
        {"cat": "Puerta de embarque", "q": "Наш рейс ___ на один час.",
         "options": ["задержан", "задержать", "задержка", "задерживал"], "answer": "задержан",
         "tip": L("'Задержан' is the short passive participle for a delayed flight.", "'Задержан' es el participio pasivo corto para un vuelo retrasado.",
                  "'Задержан' é o particípio passivo curto para um voo atrasado.", "'Задержан' 是短尾被动分词,表示航班延误。",
                  "'Задержан' — краткое страдательное причастие, обозначающее задержку рейса.")},
        {"cat": "Puerta de embarque", "q": "Ваш выход ___ номер двенадцать.",
         "options": ["—", "есть", "была", "будет"], "answer": "—",
         "tip": L("Again, the present-tense 'to be' is omitted here.", "De nuevo, se omite el verbo 'ser' en presente.",
                  "Novamente, o verbo 'ser' no presente é omitido.", "现在时同样省略系动词。", "Здесь также опускается настоящее время глагола «быть».")},
        {"cat": "A bordo", "q": "Пожалуйста, ___ ремень безопасности.",
         "options": ["пристегните", "пристегнуть", "пристёгивать", "пристегнул"], "answer": "пристегните",
         "tip": L("Formal imperative: 'пристегните' (you-plural/polite).", "Imperativo formal: 'пристегните' (usted/plural).",
                  "Imperativo formal: 'пристегните' (você/plural).", "正式祈使式:'пристегните'(您/复数)。",
                  "Формальное повелительное наклонение: 'пристегните' (вы).")},
        {"cat": "A bordo", "q": "Мы попали в небольшую ___.",
         "options": ["турбулентность", "турбулентности", "турбулентностью", "турбулентностей"], "answer": "турбулентность",
         "tip": L("Direct object in accusative — for this noun it looks like the nominative.", "Objeto directo en acusativo — para este sustantivo es igual al nominativo.",
                  "Objeto direto no acusativo — para este substantivo é igual ao nominativo.", "宾语用第四格(宾格)——此名词与主格同形。",
                  "Прямое дополнение в винительном падеже — для этого слова совпадает с именительным.")},
        {"cat": "Reclamo de equipaje", "q": "Ваш багаж прибудет на ___ номер четыре.",
         "options": ["ленту", "лента", "ленты", "лентой"], "answer": "ленту",
         "tip": L("'На' + accusative case: 'на ленту'.", "'На' + caso acusativo: 'на ленту'.", "'На' + caso acusativo: 'на ленту'.",
                  "'На'+第四格(宾格):'на ленту'。", "'На' + винительный падеж: 'на ленту'.")},
        {"cat": "Reclamo de equipaje", "q": "Мне нужно сообщить о ___ чемодане.",
         "options": ["потерянном", "потерянный", "потерянного", "потерянным"], "answer": "потерянном",
         "tip": L("'О' + prepositional case: 'о потерянном чемодане'.", "'О' + caso prepositivo: 'о потерянном чемодане'.",
                  "'О' + caso preposicional: 'о потерянном чемодане'.", "'О'+第六格(前置格):'о потерянном чемодане'。",
                  "'О' + предложный падеж: 'о потерянном чемодане'.")},
    ],
}

# ----------------------------------------------------------------------
# VOCABULARIO DEL AEROPUERTO — término en 5 idiomas + ejemplo de referencia en inglés
# ----------------------------------------------------------------------
AIRPORT_VOCAB = {
    "Check-in": [
        (L("boarding pass", "pase de abordar", "cartão de embarque", "登机牌", "посадочный талон"),
         "Please have your boarding pass ready."),
        (L("passport", "pasaporte", "passaporte", "护照", "паспорт"),
         "Can I see your passport, please?"),
        (L("check-in counter", "mostrador de check-in", "balcão de check-in", "值机柜台", "стойка регистрации"),
         "The check-in counter closes forty minutes before departure."),
        (L("baggage allowance", "límite de equipaje", "franquia de bagagem", "行李限额", "норма провоза багажа"),
         "Your baggage allowance is twenty three kilograms."),
        (L("overweight", "con sobrepeso", "com excesso de peso", "超重", "с перевесом"),
         "I'm sorry, your suitcase is overweight."),
        (L("carry-on bag", "equipaje de mano", "bagagem de mão", "随身行李", "ручная кладь"),
         "You can bring one carry-on bag."),
        (L("aisle seat / window seat", "asiento de pasillo / de ventana", "assento no corredor / na janela",
           "靠走道座位 / 靠窗座位", "место у прохода / у окна"),
         "I would like a window seat, please."),
    ],
    "Seguridad": [
        (L("security checkpoint", "control de seguridad", "controle de segurança", "安检口", "пункт досмотра"),
         "Please proceed to the security checkpoint."),
        (L("metal detector", "detector de metales", "detector de metais", "金属探测器", "металлодетектор"),
         "Please walk through the metal detector."),
        (L("X-ray machine", "máquina de rayos X", "máquina de raio-X", "X光机", "рентгеновский аппарат"),
         "Put your bag on the X-ray machine belt."),
        (L("liquids", "líquidos", "líquidos", "液体", "жидкости"),
         "Liquids must be in containers of one hundred milliliters or less."),
        (L("pat-down", "revisión manual", "revista manual", "人工搜身检查", "досмотр вручную"),
         "You may be asked for a pat-down."),
        (L("boarding area", "sala de embarque", "área de embarque", "登机区", "зона посадки"),
         "Please wait in the boarding area."),
    ],
    "Inmigración y aduana": [
        (L("immigration officer", "oficial de inmigración", "agente de imigração", "移民官",
           "сотрудник иммиграционной службы"),
         "Show your passport to the immigration officer."),
        (L("customs", "aduana", "alfândega", "海关", "таможня"),
         "Do you have anything to declare at customs?"),
        (L("declare", "declarar", "declarar", "申报", "декларировать"),
         "You must declare amounts over ten thousand dollars."),
        (L("visa", "visa", "visto", "签证", "виза"),
         "Do you need a visa to enter this country?"),
        (L("purpose of visit", "motivo del viaje", "motivo da viagem", "访问目的", "цель визита"),
         "What is the purpose of your visit?"),
        (L("residence permit", "permiso de residencia", "autorização de residência", "居留许可",
           "вид на жительство"),
         "Please show your residence permit."),
    ],
    "Puerta de embarque": [
        (L("boarding gate", "puerta de embarque", "portão de embarque", "登机口", "выход на посадку"),
         "Your boarding gate is number twelve."),
        (L("final call", "última llamada", "última chamada", "最后广播", "последнее объявление"),
         "This is the final call for flight four oh two."),
        (L("delayed", "retrasado", "atrasado", "延误", "задержан"),
         "Your flight has been delayed by one hour."),
        (L("on time", "a tiempo", "no horário", "准时", "вовремя"),
         "The flight is on time."),
        (L("now boarding", "ahora embarcando", "embarcando agora", "正在登机", "идёт посадка"),
         "Flight two oh five is now boarding."),
        (L("priority boarding", "embarque prioritario", "embarque prioritário", "优先登机",
           "приоритетная посадка"),
         "Priority boarding is for first class passengers."),
    ],
    "A bordo": [
        (L("tray table", "mesa plegable", "mesinha", "小桌板", "откидной столик"),
         "Please return your tray table to its upright position."),
        (L("seatbelt", "cinturón de seguridad", "cinto de segurança", "安全带", "ремень безопасности"),
         "Please fasten your seatbelt."),
        (L("flight attendant", "auxiliar de vuelo", "comissário(a) de bordo", "空乘人员", "бортпроводник"),
         "Ask the flight attendant for some water."),
        (L("turbulence", "turbulencia", "turbulência", "颠簸", "турбулентность"),
         "We are experiencing some turbulence."),
        (L("emergency exit", "salida de emergencia", "saída de emergência", "紧急出口", "аварийный выход"),
         "The emergency exit is located at the rear of the plane."),
        (L("overhead compartment", "compartimento superior", "compartimento superior", "头顶行李舱",
           "верхняя багажная полка"),
         "Put your bag in the overhead compartment."),
    ],
    "Reclamo de equipaje": [
        (L("baggage claim", "reclamo de equipaje", "retirada de bagagem", "行李领取处", "зона выдачи багажа"),
         "Go to baggage claim to collect your suitcase."),
        (L("carousel", "banda transportadora", "esteira de bagagem", "行李转盘", "багажная лента"),
         "Your bag will arrive on carousel number four."),
        (L("lost luggage", "equipaje perdido", "bagagem extraviada", "行李丢失", "потерянный багаж"),
         "I need to report lost luggage."),
        (L("claim tag", "etiqueta de reclamo", "etiqueta de bagagem", "行李领取牌", "багажная бирка"),
         "Keep your claim tag until you receive your bag."),
    ],
}

# ----------------------------------------------------------------------
# MOTOR DE REGLAS GRAMATICALES PROPIO (sin API externa, 100% offline)
# Un banco de reglas distinto por cada idioma que se puede aprender.
# El "tip" (explicación) se muestra en el idioma nativo de la persona;
# el "example" está en el idioma objetivo (el que se está aprendiendo),
# porque demuestra el uso correcto de ESE idioma.
# ----------------------------------------------------------------------
GRAMMAR_RULES = {
    "en": [
        {"pattern": r"\bhe don't\b", "fix": "he doesn't",
         "tip": L("With he/she/it, use 'doesn't', not 'don't'.", "Con he/she/it se usa 'doesn't', no 'don't'.",
                  "Com he/she/it usa-se 'doesn't', não 'don't'.", "he/she/it 后面用 'doesn't',不用 'don't'。",
                  "С he/she/it используется 'doesn't', а не 'don't'."),
         "example": "He doesn't like coffee."},
        {"pattern": r"\bshe don't\b", "fix": "she doesn't",
         "tip": L("With he/she/it, use 'doesn't', not 'don't'.", "Con he/she/it se usa 'doesn't', no 'don't'.",
                  "Com he/she/it usa-se 'doesn't', não 'don't'.", "he/she/it 后面用 'doesn't',不用 'don't'。",
                  "С he/she/it используется 'doesn't', а не 'don't'."),
         "example": "She doesn't speak French."},
        {"pattern": r"\bit don't\b", "fix": "it doesn't",
         "tip": L("With he/she/it, use 'doesn't', not 'don't'.", "Con he/she/it se usa 'doesn't', no 'don't'.",
                  "Com he/she/it usa-se 'doesn't', não 'don't'.", "he/she/it 后面用 'doesn't',不用 'don't'。",
                  "С he/she/it используется 'doesn't', а не 'don't'."),
         "example": "It doesn't matter."},
        {"pattern": r"\bshe have\b", "fix": "she has",
         "tip": L("With he/she/it, use 'has', not 'have'.", "Con he/she/it se usa 'has', no 'have'.",
                  "Com he/she/it usa-se 'has', não 'have'.", "he/she/it 后面用 'has',不用 'have'。",
                  "С he/she/it используется 'has', а не 'have'."),
         "example": "She has two brothers."},
        {"pattern": r"\bhe have\b", "fix": "he has",
         "tip": L("With he/she/it, use 'has', not 'have'.", "Con he/she/it se usa 'has', no 'have'.",
                  "Com he/she/it usa-se 'has', não 'have'.", "he/she/it 后面用 'has',不用 'have'。",
                  "С he/she/it используется 'has', а не 'have'."),
         "example": "He has a new phone."},
        {"pattern": r"\bi are\b", "fix": "I am",
         "tip": L("With 'I', use 'am', not 'are'.", "Con 'I' se usa 'am', no 'are'.",
                  "Com 'I' usa-se 'am', não 'are'.", "'I' 后面用 'am',不用 'are'。",
                  "С 'I' используется 'am', а не 'are'."),
         "example": "I am ready to go."},
        {"pattern": r"\bi has\b", "fix": "I have",
         "tip": L("With 'I', use 'have', not 'has'.", "Con 'I' se usa 'have', no 'has'.",
                  "Com 'I' usa-se 'have', não 'has'.", "'I' 后面用 'have',不用 'has'。",
                  "С 'I' используется 'have', а не 'has'."),
         "example": "I have two suitcases."},
        {"pattern": r"\bthe news are\b", "fix": "the news is",
         "tip": L("'News' is uncountable and singular in English.", "'News' es incontable y singular en inglés.",
                  "'News' é incontável e singular em inglês.", "'News' 在英语中是不可数且单数的名词。",
                  "'News' — неисчисляемое и единственное число в английском."),
         "example": "The news is very good today."},
        {"pattern": r"\bpolice is\b", "fix": "police are",
         "tip": L("'Police' is treated as plural in English, even though it's singular in Spanish/other languages.",
                  "'Police' se trata como plural en inglés, aunque en español sea singular.",
                  "'Police' é tratado como plural em inglês, embora em português seja singular.",
                  "'Police' 在英语中被当作复数,尽管在其他语言中是单数。",
                  "'Police' в английском считается множественным числом, хотя в других языках — единственным."),
         "example": "The police are investigating the case."},
        {"pattern": r"\bi am go\b", "fix": "I am going",
         "tip": L("The present continuous needs the verb in -ing: 'am/is/are + verb-ing'.",
                  "El presente continuo necesita el verbo en -ing: 'am/is/are + verbo-ing'.",
                  "O presente contínuo precisa do verbo em -ing: 'am/is/are + verbo-ing'.",
                  "现在进行时需要动词以 -ing 结尾:'am/is/are + 动词-ing'。",
                  "Настоящее продолженное время требует глагола с -ing: 'am/is/are + глагол-ing'."),
         "example": "I am going to the airport."},
        {"pattern": r"\bi will going\b", "fix": "I will go",
         "tip": L("After 'will', the verb goes in its base form, not -ing.",
                  "Después de 'will' el verbo va en su forma base, no en -ing.",
                  "Depois de 'will' o verbo vai na forma base, não em -ing.",
                  "'will' 后面的动词用原形,不用 -ing 形式。",
                  "После 'will' глагол ставится в базовой форме, а не с -ing."),
         "example": "I will go to the gate now."},
        {"pattern": r"\bcould to\b", "fix": "could",
         "tip": L("Modal verbs (can, could, should, must) are never followed by 'to'.",
                  "Los modales (can, could, should, must) nunca van seguidos de 'to'.",
                  "Os verbos modais (can, could, should, must) nunca são seguidos de 'to'.",
                  "情态动词(can、could、should、must)后面绝不加 'to'。",
                  "Модальные глаголы (can, could, should, must) никогда не сопровождаются 'to'."),
         "example": "I could help you with your bags."},
        {"pattern": r"\bmust to\b", "fix": "must",
         "tip": L("Modal verbs (can, could, should, must) are never followed by 'to'.",
                  "Los modales (can, could, should, must) nunca van seguidos de 'to'.",
                  "Os verbos modais (can, could, should, must) nunca são seguidos de 'to'.",
                  "情态动词(can、could、should、must)后面绝不加 'to'。",
                  "Модальные глаголы (can, could, should, must) никогда не сопровождаются 'to'."),
         "example": "You must show your passport."},
        {"pattern": r"\bcan to\b", "fix": "can",
         "tip": L("Modal verbs (can, could, should, must) are never followed by 'to'.",
                  "Los modales (can, could, should, must) nunca van seguidos de 'to'.",
                  "Os verbos modais (can, could, should, must) nunca são seguidos de 'to'.",
                  "情态动词(can、could、should、must)后面绝不加 'to'。",
                  "Модальные глаголы (can, could, should, must) никогда не сопровождаются 'to'."),
         "example": "You can check in online."},
        {"pattern": r"\bshould to\b", "fix": "should",
         "tip": L("Modal verbs (can, could, should, must) are never followed by 'to'.",
                  "Los modales (can, could, should, must) nunca van seguidos de 'to'.",
                  "Os verbos modais (can, could, should, must) nunca são seguidos de 'to'.",
                  "情态动词(can、could、should、must)后面绝不加 'to'。",
                  "Модальные глаголы (can, could, should, must) никогда не сопровождаются 'to'."),
         "example": "You should arrive two hours early."},
        {"pattern": r"\bdidn't went\b", "fix": "didn't go",
         "tip": L("After 'didn't', the verb goes in the infinitive (go), not in the past tense.",
                  "Después de 'didn't' el verbo va en infinitivo (go), no en pasado.",
                  "Depois de 'didn't' o verbo vai no infinitivo (go), não no passado.",
                  "'didn't' 后面用动词原形(go),不用过去式。",
                  "После 'didn't' глагол ставится в инфинитиве (go), а не в прошедшем времени."),
         "example": "I didn't go to the gate on time."},
        {"pattern": r"\byesterday i go\b", "fix": "yesterday I went",
         "tip": L("With past-time markers like 'yesterday', the verb must be in the past tense.",
                  "Con marcadores de pasado como 'yesterday', el verbo debe ir en pasado.",
                  "Com marcadores de passado como 'yesterday', o verbo deve ir no passado.",
                  "有 'yesterday' 这样的过去时间状语时,动词必须用过去式。",
                  "С маркерами прошедшего времени, как 'yesterday', глагол должен быть в прошедшем времени."),
         "example": "Yesterday I went to the airport early."},
        {"pattern": r"\bi born in\b", "fix": "I was born in",
         "tip": L("In English you say 'I was born in...' — the verb 'be' is required.",
                  "En inglés se dice 'I was born in...', el verbo 'be' es obligatorio.",
                  "Em inglês diz-se 'I was born in...', o verbo 'be' é obrigatório.",
                  "英语中要说 'I was born in...',动词 'be' 是必须的。",
                  "По-английски говорят 'I was born in...', глагол 'be' обязателен."),
         "example": "I was born in San Salvador."},
        {"pattern": r"\bmore better\b", "fix": "better",
         "tip": L("'Better' is already comparative; it's not combined with 'more'.",
                  "'Better' ya es comparativo; no se combina con 'more'.",
                  "'Better' já é comparativo; não se combina com 'more'.",
                  "'Better' 本身已经是比较级,不能再加 'more'。",
                  "'Better' уже является сравнительной степенью, не сочетается с 'more'."),
         "example": "This flight is better than the last one."},
        {"pattern": r"\bmost best\b", "fix": "best",
         "tip": L("'Best' is already superlative; it's not combined with 'most'.",
                  "'Best' ya es superlativo; no se combina con 'most'.",
                  "'Best' já é superlativo; não se combina com 'most'.",
                  "'Best' 本身已经是最高级,不能再加 'most'。",
                  "'Best' уже является превосходной степенью, не сочетается с 'most'."),
         "example": "This is the best airline I know."},
        {"pattern": r"\bmore easier\b", "fix": "easier",
         "tip": L("'Easier' is already comparative; it's not combined with 'more'.",
                  "'Easier' ya es comparativo; no se combina con 'more'.",
                  "'Easier' já é comparativo; não se combina com 'more'.",
                  "'Easier' 本身已经是比较级,不能再加 'more'。",
                  "'Easier' уже является сравнительной степенью, не сочетается с 'more'."),
         "example": "Online check-in is easier than the counter."},
        {"pattern": r"\bmore taller\b", "fix": "taller",
         "tip": L("'Taller' is already comparative; it's not combined with 'more'.",
                  "'Taller' ya es comparativo; no se combina con 'more'.",
                  "'Taller' já é comparativo; não se combina com 'more'.",
                  "'Taller' 本身已经是比较级,不能再加 'more'。",
                  "'Taller' уже является сравнительной степенью, не сочетается с 'more'."),
         "example": "He is taller than his brother."},
        {"pattern": r"\bmost tallest\b", "fix": "tallest",
         "tip": L("'Tallest' is already superlative; it's not combined with 'most'.",
                  "'Tallest' ya es superlativo; no se combina con 'most'.",
                  "'Tallest' já é superlativo; não se combina com 'most'.",
                  "'Tallest' 本身已经是最高级,不能再加 'most'。",
                  "'Tallest' уже является превосходной степенью, не сочетается с 'most'."),
         "example": "That's the tallest building at the airport."},
        {"pattern": r"\bless worse\b", "fix": "worse",
         "tip": L("'Worse' is already comparative; it's not combined with 'less'.",
                  "'Worse' ya es comparativo; no se combina con 'less'.",
                  "'Worse' já é comparativo; não se combina com 'less'.",
                  "'Worse' 本身已经是比较级,不能再加 'less'。",
                  "'Worse' уже является сравнительной степенью, не сочетается с 'less'."),
         "example": "The traffic today is worse than yesterday."},
        {"pattern": r"\ba (?=[aeiouAEIOU])(\w+)", "fix": r"an \1",
         "tip": L("Before a vowel sound, use 'an', not 'a'.", "Antes de un sonido vocálico se usa 'an', no 'a'.",
                  "Antes de um som vocálico usa-se 'an', não 'a'.", "元音发音前用 'an',不用 'a'。",
                  "Перед гласным звуком используется 'an', а не 'a'."),
         "example": "I need an umbrella."},
        {"pattern": r"\bmuch people\b", "fix": "many people",
         "tip": L("'People' is countable, so use 'many', not 'much'.", "'People' es contable → se usa 'many', no 'much'.",
                  "'People' é contável → usa-se 'many', não 'much'.", "'People' 是可数名词,用 'many',不用 'much'。",
                  "'People' — исчисляемое, поэтому 'many', а не 'much'."),
         "example": "There are many people at the gate."},
        {"pattern": r"\bpeoples\b", "fix": "people",
         "tip": L("'People' is already plural, it doesn't take an 's'.", "'People' ya es plural, no lleva 's'.",
                  "'People' já é plural, não leva 's'.", "'People' 已经是复数形式,不加 's'。",
                  "'People' уже множественное число, 's' не добавляется."),
         "example": "Many people travel in summer."},
        {"pattern": r"\binformations\b", "fix": "information",
         "tip": L("'Information' is uncountable; it has no plural form.", "'Information' es incontable, no tiene forma plural.",
                  "'Information' é incontável, não tem forma plural.", "'Information' 是不可数名词,没有复数形式。",
                  "'Information' неисчисляемое, множественного числа не имеет."),
         "example": "I need more information about my flight."},
        {"pattern": r"\badvices\b", "fix": "advice",
         "tip": L("'Advice' is uncountable; it has no plural form.", "'Advice' es incontable, no tiene forma plural.",
                  "'Advice' é incontável, não tem forma plural.", "'Advice' 是不可数名词,没有复数形式。",
                  "'Advice' неисчисляемое, множественного числа не имеет."),
         "example": "Can you give me some advice?"},
        {"pattern": r"\bluggages\b", "fix": "luggage",
         "tip": L("'Luggage' is uncountable; it has no plural form (very useful to know at the airport).",
                  "'Luggage' es incontable, no tiene forma plural (muy útil en el aeropuerto).",
                  "'Luggage' é incontável, não tem forma plural (muito útil no aeroporto).",
                  "'Luggage' 是不可数名词,没有复数形式(在机场很常用)。",
                  "'Luggage' неисчисляемое, без множественного числа (полезно знать в аэропорту)."),
         "example": "Where is the luggage?"},
        {"pattern": r"\bfurnitures\b", "fix": "furniture",
         "tip": L("'Furniture' is uncountable; it has no plural form.", "'Furniture' es incontable, no tiene forma plural.",
                  "'Furniture' é incontável, não tem forma plural.", "'Furniture' 是不可数名词,没有复数形式。",
                  "'Furniture' неисчисляемое, множественного числа не имеет."),
         "example": "The lounge has comfortable furniture."},
        {"pattern": r"\bequipments\b", "fix": "equipment",
         "tip": L("'Equipment' is uncountable; it has no plural form.", "'Equipment' es incontable, no tiene forma plural.",
                  "'Equipment' é incontável, não tem forma plural.", "'Equipment' 是不可数名词,没有复数形式。",
                  "'Equipment' неисчисляемое, множественного числа не имеет."),
         "example": "The crew checked all the equipment."},
        {"pattern": r"\bknowledges\b", "fix": "knowledge",
         "tip": L("'Knowledge' is uncountable; it has no plural form.", "'Knowledge' es incontable, no tiene forma plural.",
                  "'Knowledge' é incontável, não tem forma plural.", "'Knowledge' 是不可数名词,没有复数形式。",
                  "'Knowledge' неисчисляемое, множественного числа не имеет."),
         "example": "She has good knowledge of English."},
        {"pattern": r"\bmarried with\b", "fix": "married to",
         "tip": L("In English you say 'married to', not 'married with'.", "En inglés se dice 'married to', no 'married with'.",
                  "Em inglês diz-se 'married to', não 'married with'.", "英语中要说 'married to',不说 'married with'。",
                  "По-английски говорят 'married to', а не 'married with'."),
         "example": "He is married to a flight attendant."},
        {"pattern": r"\bdepend of\b", "fix": "depend on",
         "tip": L("In English you say 'depend on', not 'depend of'.", "En inglés se dice 'depend on', no 'depend of'.",
                  "Em inglês diz-se 'depend on', não 'depend of'.", "英语中要说 'depend on',不说 'depend of'。",
                  "По-английски говорят 'depend on', а не 'depend of'."),
         "example": "It depends on the weather."},
        {"pattern": r"\bis depend on\b", "fix": "depends on",
         "tip": L("You simply say 'depends on', without 'is' before it.", "Se dice simplemente 'depends on', sin el verbo 'is' antes.",
                  "Diz-se simplesmente 'depends on', sem o verbo 'is' antes.", "直接说 'depends on' 即可,前面不加 'is'。",
                  "Просто говорят 'depends on', без 'is' перед этим."),
         "example": "The gate depends on the terminal."},
        {"pattern": r"\blisten music\b", "fix": "listen to music",
         "tip": L("You say 'listen to music', with the preposition 'to'.", "Se dice 'listen to music', con la preposición 'to'.",
                  "Diz-se 'listen to music', com a preposição 'to'.", "要说 'listen to music',带介词 'to'。",
                  "Говорят 'listen to music', с предлогом 'to'."),
         "example": "I like to listen to music on the plane."},
        {"pattern": r"\bwait (him|her|me|them|us)\b", "fix": r"wait for \1",
         "tip": L("You say 'wait for someone', with the preposition 'for'.", "Se dice 'wait for someone', con la preposición 'for'.",
                  "Diz-se 'wait for someone', com a preposição 'for'.", "要说 'wait for someone',带介词 'for'。",
                  "Говорят 'wait for someone', с предлогом 'for'."),
         "example": "Please wait for me at the gate."},
        {"pattern": r"\bexplain (me|him|her|them|us)\b", "fix": r"explain to \1",
         "tip": L("You say 'explain to someone', with the preposition 'to'.", "Se dice 'explain to someone', con la preposición 'to'.",
                  "Diz-se 'explain to someone', com a preposição 'to'.", "要说 'explain to someone',带介词 'to'。",
                  "Говорят 'explain to someone', с предлогом 'to'."),
         "example": "Can you explain to me how this works?"},
        {"pattern": r"\bassist to\b", "fix": "attend",
         "tip": L("'Assist' means 'to help'; to 'attend an event' you use 'attend'.",
                  "'Assist' significa 'ayudar'; para 'asistir a un evento' se usa 'attend'.",
                  "'Assist' significa 'ajudar'; para 'assistir a um evento' usa-se 'attend'.",
                  "'Assist' 的意思是“帮助”;“参加某活动”要用 'attend'。",
                  "'Assist' означает «помогать»; для «посетить мероприятие» используется 'attend'."),
         "example": "I will attend the meeting tomorrow."},
        {"pattern": r"\bin the night\b", "fix": "at night",
         "tip": L("In English you say 'at night', not 'in the night'.", "En inglés se dice 'at night', no 'in the night'.",
                  "Em inglês diz-se 'at night', não 'in the night'.", "英语中要说 'at night',不说 'in the night'。",
                  "По-английски говорят 'at night', а не 'in the night'."),
         "example": "The flight leaves at night."},
        {"pattern": r"\bin this moment\b", "fix": "at this moment",
         "tip": L("In English you say 'at this moment', not 'in this moment'.", "En inglés se dice 'at this moment', no 'in this moment'.",
                  "Em inglês diz-se 'at this moment', não 'in this moment'.", "英语中要说 'at this moment',不说 'in this moment'。",
                  "По-английски говорят 'at this moment', а не 'in this moment'."),
         "example": "I'm boarding at this moment."},
        {"pattern": r"\bcongratulations for\b", "fix": "congratulations on",
         "tip": L("In English you say 'congratulations on', not 'congratulations for'.",
                  "En inglés se dice 'congratulations on', no 'congratulations for'.",
                  "Em inglês diz-se 'congratulations on', não 'congratulations for'.",
                  "英语中要说 'congratulations on',不说 'congratulations for'。",
                  "По-английски говорят 'congratulations on', а не 'congratulations for'."),
         "example": "Congratulations on your new job!"},
        {"pattern": r"\benjoy to (\w+)", "fix": r"enjoy \1ing",
         "tip": L("After 'enjoy' you use the gerund (-ing), not 'to'.", "Después de 'enjoy' se usa el gerundio (-ing), no 'to'.",
                  "Depois de 'enjoy' usa-se o gerúndio (-ing), não 'to'.", "'enjoy' 后面用动名词(-ing),不用 'to'。",
                  "После 'enjoy' используется герундий (-ing), а не 'to'."),
         "example": "I enjoy traveling by plane."},
        {"pattern": r"\bavoid to (\w+)", "fix": r"avoid \1ing",
         "tip": L("After 'avoid' you use the gerund (-ing), not 'to'.", "Después de 'avoid' se usa el gerundio (-ing), no 'to'.",
                  "Depois de 'avoid' usa-se o gerúndio (-ing), não 'to'.", "'avoid' 后面用动名词(-ing),不用 'to'。",
                  "После 'avoid' используется герундий (-ing), а не 'to'."),
         "example": "Try to avoid arriving late."},
        {"pattern": r"\bfinish to (\w+)", "fix": r"finish \1ing",
         "tip": L("After 'finish' you use the gerund (-ing), not 'to'.", "Después de 'finish' se usa el gerundio (-ing), no 'to'.",
                  "Depois de 'finish' usa-se o gerúndio (-ing), não 'to'.", "'finish' 后面用动名词(-ing),不用 'to'。",
                  "После 'finish' используется герундий (-ing), а не 'to'."),
         "example": "Did you finish packing?"},
        {"pattern": r"\bsuggest to (\w+)", "fix": r"suggest \1ing",
         "tip": L("After 'suggest' you use the gerund (-ing), not 'to'.", "Después de 'suggest' se usa el gerundio (-ing), no 'to'.",
                  "Depois de 'suggest' usa-se o gerúndio (-ing), não 'to'.", "'suggest' 后面用动名词(-ing),不用 'to'。",
                  "После 'suggest' используется герундий (-ing), а не 'to'."),
         "example": "I suggest checking in early."},
        {"pattern": r"\bclose the light\b", "fix": "turn off the light",
         "tip": L("In English you don't 'close' a light; you say 'turn off the light'.",
                  "En inglés no se 'cierra' la luz; se dice 'turn off the light'.",
                  "Em inglês não se 'fecha' a luz; diz-se 'turn off the light'.",
                  "英语中不说“关闭”灯,要说 'turn off the light'。",
                  "По-английски свет не «закрывают», говорят 'turn off the light'."),
         "example": "Please turn off the light before takeoff."},
        {"pattern": r"\bopen the light\b", "fix": "turn on the light",
         "tip": L("In English you don't 'open' a light; you say 'turn on the light'.",
                  "En inglés no se 'abre' la luz; se dice 'turn on the light'.",
                  "Em inglês não se 'abre' a luz; diz-se 'turn on the light'.",
                  "英语中不说“打开”灯,要说 'turn on the light'。",
                  "По-английски свет не «открывают», говорят 'turn on the light'."),
         "example": "The flight attendant turned on the light."},
        {"pattern": r"\bput attention\b", "fix": "pay attention",
         "tip": L("You say 'pay attention', not 'put attention'.", "Se dice 'pay attention', no 'put attention'.",
                  "Diz-se 'pay attention', não 'put attention'.", "要说 'pay attention',不说 'put attention'。",
                  "Говорят 'pay attention', а не 'put attention'."),
         "example": "Please pay attention to the safety demonstration."},
        {"pattern": r"\bmake a party\b", "fix": "have a party",
         "tip": L("In English you say 'have a party', not 'make a party'.", "En inglés se dice 'have a party', no 'make a party'.",
                  "Em inglês diz-se 'have a party', não 'make a party'.", "英语中要说 'have a party',不说 'make a party'。",
                  "По-английски говорят 'have a party', а не 'make a party'."),
         "example": "We had a party after landing safely."},
        {"pattern": r"\bmake a question\b", "fix": "ask a question",
         "tip": L("You say 'ask a question', not 'make a question'.", "Se dice 'ask a question', no 'make a question'.",
                  "Diz-se 'ask a question', não 'make a question'.", "要说 'ask a question',不说 'make a question'。",
                  "Говорят 'ask a question', а не 'make a question'."),
         "example": "Can I ask a question about my ticket?"},
        {"pattern": r"\bmake a photo\b", "fix": "take a photo",
         "tip": L("In English you say 'take a photo', not 'make a photo'.", "En inglés se dice 'take a photo', no 'make a photo'.",
                  "Em inglês diz-se 'take a photo', não 'make a photo'.", "英语中要说 'take a photo',不说 'make a photo'。",
                  "По-английски говорят 'take a photo', а не 'make a photo'."),
         "example": "I want to take a photo of the airplane."},
        {"pattern": r"\bdo a mistake\b", "fix": "make a mistake",
         "tip": L("You say 'make a mistake', not 'do a mistake'.", "Se dice 'make a mistake', no 'do a mistake'.",
                  "Diz-se 'make a mistake', não 'do a mistake'.", "要说 'make a mistake',不说 'do a mistake'。",
                  "Говорят 'make a mistake', а не 'do a mistake'."),
         "example": "I made a mistake with my booking."},
        {"pattern": r"\bshe said me\b", "fix": "she told me",
         "tip": L("With a person as the direct object, use 'tell', not 'say'.",
                  "Con un objeto directo de persona se usa 'tell', no 'say'.",
                  "Com um objeto direto de pessoa usa-se 'tell', não 'say'.",
                  "宾语是人时用 'tell',不用 'say'。", "С прямым дополнением-человеком используется 'tell', а не 'say'."),
         "example": "She told me the gate had changed."},
        {"pattern": r"\bhe said me\b", "fix": "he told me",
         "tip": L("With a person as the direct object, use 'tell', not 'say'.",
                  "Con un objeto directo de persona se usa 'tell', no 'say'.",
                  "Com um objeto direto de pessoa usa-se 'tell', não 'say'.",
                  "宾语是人时用 'tell',不用 'say'。", "С прямым дополнением-человеком используется 'tell', а не 'say'."),
         "example": "He told me to hurry up."},
        {"pattern": r"\bdiscuss about\b", "fix": "discuss",
         "tip": L("'Discuss' already includes the meaning of 'about'; it's not used together with it.",
                  "'Discuss' ya incluye el significado de 'about'; no se usa junto.",
                  "'Discuss' já inclui o significado de 'about'; não se usa junto.",
                  "'Discuss' 本身已经包含 'about' 的意思,不要一起用。", "'Discuss' уже включает значение 'about', вместе не используются."),
         "example": "Let's discuss the itinerary."},
        {"pattern": r"\breturn back\b", "fix": "return",
         "tip": L("'Return' already means 'to go back'; 'back' is redundant.",
                  "'Return' ya significa 'volver'; 'back' es redundante.",
                  "'Return' já significa 'voltar'; 'back' é redundante.",
                  "'Return' 本身已经有“回来”的意思,'back' 是多余的。", "'Return' уже означает «вернуться», 'back' избыточно."),
         "example": "We will return next Monday."},
        {"pattern": r"\brepeat again\b", "fix": "repeat",
         "tip": L("'Repeat' already means 'to do again'; 'again' is redundant.",
                  "'Repeat' ya significa 'volver a hacer'; 'again' es redundante.",
                  "'Repeat' já significa 'fazer de novo'; 'again' é redundante.",
                  "'Repeat' 本身已经有“再做一次”的意思,'again' 是多余的。", "'Repeat' уже означает «сделать снова», 'again' избыточно."),
         "example": "Could you repeat the announcement?"},
        {"pattern": r"\bdon't have nothing\b", "fix": "don't have anything",
         "tip": L("English doesn't use double negatives; you say 'don't... anything'.",
                  "En inglés no se usan dobles negaciones; se dice 'don't... anything'.",
                  "Em inglês não se usam duplas negações; diz-se 'don't... anything'.",
                  "英语中不使用双重否定,要说 'don't... anything'。", "В английском не используются двойные отрицания, говорят 'don't... anything'."),
         "example": "I don't have anything to declare."},
        {"pattern": r"\bdon't know nobody\b", "fix": "don't know anybody",
         "tip": L("English doesn't use double negatives; you say 'don't... anybody'.",
                  "En inglés no se usan dobles negaciones; se dice 'don't... anybody'.",
                  "Em inglês não se usam duplas negações; diz-se 'don't... anybody'.",
                  "英语中不使用双重否定,要说 'don't... anybody'。", "В английском не используются двойные отрицания, говорят 'don't... anybody'."),
         "example": "I don't know anybody on this flight."},
        {"pattern": r"\bsince (\d+) years\b", "fix": r"for \1 years",
         "tip": L("'Since' is used with a point in time; 'for' with a duration.",
                  "'Since' se usa con un punto en el tiempo; 'for' con una duración.",
                  "'Since' usa-se com um ponto no tempo; 'for' com uma duração.",
                  "'Since' 用于时间点;'for' 用于时长。", "'Since' используется с моментом времени, 'for' — с продолжительностью."),
         "example": "I have lived here for five years."},
        {"pattern": r"\bi have (\d+) years\b", "fix": r"I am \1 years old",
         "tip": L("In English you say 'I am X years old', not 'I have X years'.",
                  "En inglés se dice 'I am X years old', no 'I have X years'.",
                  "Em inglês diz-se 'I am X years old', não 'I have X years'.",
                  "英语中要说 'I am X years old',不说 'I have X years'。", "По-английски говорят 'I am X years old', а не 'I have X years'."),
         "example": "I am 20 years old."},
        {"pattern": r"\bi have (\d+) years old\b", "fix": r"I am \1 years old",
         "tip": L("In English you say 'I am X years old', not 'I have X years old'.",
                  "En inglés se dice 'I am X years old', no 'I have X years old'.",
                  "Em inglês diz-se 'I am X years old', não 'I have X years old'.",
                  "英语中要说 'I am X years old',不说 'I have X years old'。", "По-английски говорят 'I am X years old', а не 'I have X years old'."),
         "example": "My brother is 15 years old."},
        {"pattern": r"\bhow many time\b", "fix": "how much time",
         "tip": L("'Time' is uncountable in this sense, so use 'how much', not 'how many'.",
                  "'Time' es incontable en este sentido → se usa 'how much', no 'how many'.",
                  "'Time' é incontável nesse sentido → usa-se 'how much', não 'how many'.",
                  "此处 'time' 是不可数名词,用 'how much',不用 'how many'。", "'Time' в этом смысле неисчисляемое, поэтому 'how much', а не 'how many'."),
         "example": "How much time do we have before boarding?"},
        {"pattern": r"\bwant that you\b", "fix": "want you to",
         "tip": L("The correct pattern is 'want someone to do something'.",
                  "El patrón correcto es 'want someone to do something'.",
                  "O padrão correto é 'want someone to do something'.",
                  "正确的结构是 'want someone to do something'。", "Правильная модель — 'want someone to do something'."),
         "example": "I want you to check the gate number."},
        {"pattern": r"\bi am agree\b", "fix": "I agree",
         "tip": L("'Agree' is a verb, it's not used with 'am'.", "'Agree' es un verbo, no se usa con 'am'.",
                  "'Agree' é um verbo, não se usa com 'am'.", "'Agree' 是动词,不与 'am' 连用。",
                  "'Agree' — глагол, не используется с 'am'."),
         "example": "I agree with the new schedule."},
        {"pattern": r"\bi am boring\b", "fix": "I am bored",
         "tip": L("'Boring' describes something that bores others; if you feel bored, use 'bored'.",
                  "'Boring' describe algo que aburre a otros; si tú te sientes aburrido, usa 'bored'.",
                  "'Boring' descreve algo que entedia outros; se você está entediado, use 'bored'.",
                  "'Boring' 描述让别人感到无聊的事物;如果自己感到无聊,要用 'bored'。",
                  "'Boring' описывает то, что скучно другим; если скучно вам самому, используйте 'bored'."),
         "example": "I am bored during the layover."},
        {"pattern": r"\byour welcome\b", "fix": "you're welcome",
         "tip": L("'You're' (you are) has an apostrophe; 'your' is possessive.",
                  "'You're' (you are) lleva apóstrofe; 'your' es posesivo.",
                  "'You're' (you are) leva apóstrofo; 'your' é possessivo.",
                  "'You're'(you are)带撇号;'your' 是所有格。", "'You're' (you are) пишется с апострофом; 'your' — притяжательное."),
         "example": "You're welcome, have a safe trip!"},
        {"pattern": r"\byour going\b", "fix": "you're going",
         "tip": L("'You're' (you are) has an apostrophe; 'your' is possessive.",
                  "'You're' (you are) lleva apóstrofe; 'your' es posesivo.",
                  "'You're' (you are) leva apóstrofo; 'your' é possessivo.",
                  "'You're'(you are)带撇号;'your' 是所有格。", "'You're' (you are) пишется с апострофом; 'your' — притяжательное."),
         "example": "You're going to gate 12."},
        {"pattern": r"\bits a\b", "fix": "it's a",
         "tip": L("'It's' (it is) has an apostrophe; 'its' is possessive.",
                  "'It's' (it is) lleva apóstrofe; 'its' es posesivo.",
                  "'It's' (it is) leva apóstrofo; 'its' é possessivo.",
                  "'It's'(it is)带撇号;'its' 是所有格。", "'It's' (it is) пишется с апострофом; 'its' — притяжательное."),
         "example": "It's a long flight."},
        {"pattern": r"\bits the\b", "fix": "it's the",
         "tip": L("'It's' (it is) has an apostrophe; 'its' is possessive.",
                  "'It's' (it is) lleva apóstrofe; 'its' es posesivo.",
                  "'It's' (it is) leva apóstrofo; 'its' é possessivo.",
                  "'It's'(it is)带撇号;'its' 是所有格。", "'It's' (it is) пишется с апострофом; 'its' — притяжательное."),
         "example": "It's the last call for boarding."},
    ],
    "es": [
        {"pattern": r"\bsoy cansado\b", "fix": "estoy cansado",
         "tip": L("Use 'estar' for temporary states like tiredness, not 'ser'.",
                  "Se usa 'estar' para estados temporales como el cansancio, no 'ser'.",
                  "Usa-se 'estar' para estados temporários como cansaço, não 'ser'.",
                  "表示疲惫等临时状态用 'estar',不用 'ser'。", "Для временных состояний, как усталость, используется 'estar', а не 'ser'."),
         "example": "Estoy cansado después del vuelo."},
        {"pattern": r"\bsoy en\b", "fix": "estoy en",
         "tip": L("Location is expressed with 'estar', not 'ser'.", "La ubicación se expresa con 'estar', no con 'ser'.",
                  "A localização se expressa com 'estar', não com 'ser'.", "表示位置用 'estar',不用 'ser'。",
                  "Местоположение выражается глаголом 'estar', а не 'ser'."),
         "example": "Estoy en el aeropuerto."},
        {"pattern": r"\bel maleta\b", "fix": "la maleta",
         "tip": L("'Maleta' is a feminine noun, so it takes 'la'.", "'Maleta' es un sustantivo femenino, así que lleva 'la'.",
                  "'Maleta' é um substantivo feminino, então leva 'la'.", "'Maleta' 是阴性名词,用 'la'。",
                  "'Maleta' — существительное женского рода, поэтому 'la'."),
         "example": "La maleta es negra."},
        {"pattern": r"\bmucho gracias\b", "fix": "muchas gracias",
         "tip": L("'Gracias' is plural feminine, so it needs 'muchas', not 'mucho'.",
                  "'Gracias' es plural femenino, necesita 'muchas', no 'mucho'.",
                  "'Gracias' é plural feminino, precisa de 'muchas', não 'mucho'.",
                  "'Gracias' 是阴性复数,要用 'muchas',不用 'mucho'。", "'Gracias' — женского рода множественного числа, нужно 'muchas', а не 'mucho'."),
         "example": "Muchas gracias por su ayuda."},
        {"pattern": r"\byo tiene\b", "fix": "yo tengo",
         "tip": L("With 'yo' the verb 'tener' conjugates as 'tengo'.", "Con 'yo' el verbo 'tener' se conjuga como 'tengo'.",
                  "Com 'yo' o verbo 'tener' se conjuga como 'tengo'.", "'yo' 后面动词 'tener' 变位为 'tengo'。",
                  "С 'yo' глагол 'tener' спрягается как 'tengo'."),
         "example": "Yo tengo dos maletas."},
        {"pattern": r"\bmas mejor\b", "fix": "mejor",
         "tip": L("'Mejor' is already comparative; it's not combined with 'más'.",
                  "'Mejor' ya es comparativo; no se combina con 'más'.",
                  "'Mejor' já é comparativo; não se combina com 'mais'.",
                  "'Mejor' 本身已是比较级,不能再加 'más'。", "'Mejor' уже является сравнительной степенью, не сочетается с 'más'."),
         "example": "Este vuelo es mejor que el anterior."},
        {"pattern": r"\bhaber personas\b", "fix": "hay personas",
         "tip": L("The impersonal form of 'haber' in the present is 'hay', not 'haber'.",
                  "La forma impersonal de 'haber' en presente es 'hay', no 'haber'.",
                  "A forma impessoal de 'haber' no presente é 'hay', não 'haber'.",
                  "'haber' 现在时的无人称形式是 'hay',不是 'haber'。", "Безличная форма 'haber' в настоящем времени — 'hay', а не 'haber'."),
         "example": "Hay muchas personas en la puerta."},
        {"pattern": r"\ba el\b", "fix": "al",
         "tip": L("'A' + 'el' contracts to 'al'.", "'A' + 'el' se contrae en 'al'.",
                  "'A' + 'el' se contrai em 'al'.", "'a'+'el' 缩合为 'al'。", "'A' + 'el' стягивается в 'al'."),
         "example": "Voy al aeropuerto."},
        {"pattern": r"\bde el\b", "fix": "del",
         "tip": L("'De' + 'el' contracts to 'del'.", "'De' + 'el' se contrae en 'del'.",
                  "'De' + 'el' se contrai em 'del'.", "'de'+'el' 缩合为 'del'。", "'De' + 'el' стягивается в 'del'."),
         "example": "Vengo del aeropuerto."},
        {"pattern": r"\bpasaporte roja\b", "fix": "pasaporte rojo",
         "tip": L("'Pasaporte' is masculine, so the adjective must be masculine too.",
                  "'Pasaporte' es masculino, así que el adjetivo también debe ser masculino.",
                  "'Passaporte' é masculino, então o adjetivo também deve ser masculino.",
                  "'Pasaporte' 是阳性名词,形容词也要用阳性。", "'Pasaporte' — мужского рода, поэтому прилагательное тоже должно быть мужского рода."),
         "example": "Mi pasaporte es rojo."},
        {"pattern": r"\bnecesito de\b", "fix": "necesito",
         "tip": L("'Necesitar' doesn't take the preposition 'de' before a noun.",
                  "'Necesitar' no lleva la preposición 'de' antes de un sustantivo.",
                  "'Necesitar' não leva a preposição 'de' antes de um substantivo.",
                  "'necesitar' 后面名词前不加介词 'de'。", "'Necesitar' не требует предлога 'de' перед существительным."),
         "example": "Necesito un vaso de agua."},
        {"pattern": r"\bdebo de\b", "fix": "debo",
         "tip": L("'Deber' + infinitive (obligation) doesn't need 'de'; 'deber de' implies probability.",
                  "'Deber' + infinitivo (obligación) no necesita 'de'; 'deber de' implica probabilidad.",
                  "'Dever' + infinitivo (obrigação) não precisa de 'de'; 'dever de' implica probabilidade.",
                  "'deber'+不定式(义务)不需要 'de';'deber de' 表示推测。", "'Deber' + инфинитив (обязанность) не требует 'de'; 'deber de' выражает вероятность."),
         "example": "Debo mostrar mi pasaporte."},
        {"pattern": r"\bvoy viajar\b", "fix": "voy a viajar",
         "tip": L("'Ir' + 'a' + infinitive expresses near future; don't drop the 'a'.",
                  "'Ir' + 'a' + infinitivo expresa futuro próximo; no se omite la 'a'.",
                  "'Ir' + 'a' + infinitivo expressa futuro próximo; não se omite o 'a'.",
                  "'ir'+'a'+不定式表示将来;不能省略 'a'。", "'Ir' + 'a' + инфинитив выражает ближайшее будущее; 'a' нельзя опускать."),
         "example": "Voy a viajar mañana."},
        {"pattern": r"\byo gusto\b", "fix": "me gusta",
         "tip": L("'Gustar' works like 'to please': use 'me gusta', not 'yo gusto'.",
                  "'Gustar' funciona como 'to please': se usa 'me gusta', no 'yo gusto'.",
                  "'Gostar/gustar' funciona como 'to please': usa-se 'me gusta', não 'yo gusto'.",
                  "'gustar' 的用法类似“使高兴”:用 'me gusta',不用 'yo gusto'。", "'Gustar' работает как «нравиться»: используется 'me gusta', а не 'yo gusto'."),
         "example": "Me gusta viajar en avión."},
        {"pattern": r"\bun pregunta\b", "fix": "una pregunta",
         "tip": L("'Pregunta' is feminine, so it takes 'una', not 'un'.", "'Pregunta' es femenino, así que lleva 'una', no 'un'.",
                  "'Pergunta' é feminino, então leva 'uma', não 'um'.", "'Pregunta' 是阴性名词,用 'una',不用 'un'。",
                  "'Pregunta' — женского рода, поэтому 'una', а не 'un'."),
         "example": "Tengo una pregunta sobre mi vuelo."},
    ],
    "pt": [
        {"pattern": r"\beu sou cansado\b", "fix": "eu estou cansado",
         "tip": L("Use 'estar' for temporary states like tiredness, not 'ser'.",
                  "Se usa 'estar' para estados temporales como el cansancio, no 'ser'.",
                  "Usa-se 'estar' para estados temporários como cansaço, não 'ser'.",
                  "表示疲惫等临时状态用 'estar',不用 'ser'。", "Для временных состояний, как усталость, используется 'estar', а не 'ser'."),
         "example": "Estou cansado depois do voo."},
        {"pattern": r"\beu sou no\b", "fix": "eu estou no",
         "tip": L("Location is expressed with 'estar', not 'ser'.", "La ubicación se expresa con 'estar', no con 'ser'.",
                  "A localização se expressa com 'estar', não com 'ser'.", "表示位置用 'estar',不用 'ser'。",
                  "Местоположение выражается глаголом 'estar', а не 'ser'."),
         "example": "Estou no aeroporto."},
        {"pattern": r"\bo mala\b", "fix": "a mala",
         "tip": L("'Mala' is a feminine noun, so it takes 'a'.", "'Mala' es femenino, así que lleva 'a'.",
                  "'Mala' é feminino, então leva 'a'.", "'Mala' 是阴性名词,用 'a'。", "'Mala' — женского рода, поэтому 'a'."),
         "example": "A mala é preta."},
        {"pattern": r"\beu tem\b", "fix": "eu tenho",
         "tip": L("With 'eu' the verb 'ter' conjugates as 'tenho'.", "Con 'yo' el verbo 'tener' (ter) se conjuga como 'tenho'.",
                  "Com 'eu' o verbo 'ter' se conjuga como 'tenho'.", "'eu' 后面动词 'ter' 变位为 'tenho'。",
                  "С 'eu' глагол 'ter' спрягается как 'tenho'."),
         "example": "Eu tenho duas malas."},
        {"pattern": r"\bmais melhor\b", "fix": "melhor",
         "tip": L("'Melhor' is already comparative; it's not combined with 'mais'.",
                  "'Melhor' ya es comparativo; no se combina con 'más'.",
                  "'Melhor' já é comparativo; não se combina com 'mais'.",
                  "'Melhor' 本身已是比较级,不能再加 'mais'。", "'Melhor' уже является сравнительной степенью, не сочетается с 'mais'."),
         "example": "Este voo é melhor que o anterior."},
        {"pattern": r"\ba o\b", "fix": "ao",
         "tip": L("'A' + 'o' contracts to 'ao'.", "'A' + 'el' (o) se contrae en 'ao'.",
                  "'A' + 'o' se contrai em 'ao'.", "'a'+'o' 缩合为 'ao'。", "'A' + 'o' стягивается в 'ao'."),
         "example": "Vou ao aeroporto."},
        {"pattern": r"\bde o\b", "fix": "do",
         "tip": L("'De' + 'o' contracts to 'do'.", "'De' + 'el' (o) se contrae en 'do'.",
                  "'De' + 'o' se contrai em 'do'.", "'de'+'o' 缩合为 'do'。", "'De' + 'o' стягивается в 'do'."),
         "example": "Venho do aeroporto."},
        {"pattern": r"\bpassaporte vermelha\b", "fix": "passaporte vermelho",
         "tip": L("'Passaporte' is masculine, so the adjective must be masculine too.",
                  "'Pasaporte' es masculino, el adjetivo también debe serlo.",
                  "'Passaporte' é masculino, então o adjetivo também deve ser.",
                  "'Passaporte' 是阳性名词,形容词也要用阳性。", "'Passaporte' — мужского рода, прилагательное тоже должно быть мужского рода."),
         "example": "Meu passaporte é vermelho."},
        {"pattern": r"\bum pergunta\b", "fix": "uma pergunta",
         "tip": L("'Pergunta' is feminine, so it takes 'uma', not 'um'.", "'Pregunta' es femenino, lleva 'una', no 'un'.",
                  "'Pergunta' é feminino, leva 'uma', não 'um'.", "'Pergunta' 是阴性名词,用 'uma',不用 'um'。",
                  "'Pergunta' — женского рода, поэтому 'uma', а не 'um'."),
         "example": "Tenho uma pergunta sobre meu voo."},
        {"pattern": r"\bdevo de\b", "fix": "devo",
         "tip": L("'Dever' + infinitive doesn't need 'de' for obligation.", "'Deber' + infinitivo no necesita 'de' para obligación.",
                  "'Dever' + infinitivo não precisa de 'de' para obrigação.", "'dever'+不定式(义务)不需要 'de'。",
                  "'Dever' + инфинитив не требует 'de' для обязанности."),
         "example": "Devo mostrar meu passaporte."},
        {"pattern": r"\bgosto viajar\b", "fix": "gosto de viajar",
         "tip": L("'Gostar' requires the preposition 'de' before a verb.",
                  "'Gustar' (gostar) requiere la preposición 'de' antes de un verbo.",
                  "'Gostar' exige a preposição 'de' antes de um verbo.",
                  "'gostar' 后面接动词时需要介词 'de'。", "'Gostar' требует предлога 'de' перед глаголом."),
         "example": "Gosto de viajar de avião."},
        {"pattern": r"\bmuito turbulência\b", "fix": "muita turbulência",
         "tip": L("'Turbulência' is feminine, so use 'muita', not 'muito'.",
                  "'Turbulencia' es femenino, se usa 'muita', no 'muito'.",
                  "'Turbulência' é feminino, usa-se 'muita', não 'muito'.",
                  "'Turbulência' 是阴性名词,用 'muita',不用 'muito'。", "'Турбулентность' (Turbulência) — женского рода, используется 'muita', а не 'muito'."),
         "example": "Estamos com muita turbulência."},
        {"pattern": r"\bpara mim fazer\b", "fix": "para eu fazer",
         "tip": L("Before an infinitive as subject, use 'eu', not 'mim'.",
                  "Antes de infinitivo como sujeto, se usa 'yo', no 'mí'.",
                  "Antes de um infinitivo como sujeito, usa-se 'eu', não 'mim'.",
                  "不定式作主语前用 'eu',不用 'mim'。", "Перед инфинитивом в роли подлежащего используется 'eu', а не 'mim'."),
         "example": "É importante para eu chegar cedo."},
        {"pattern": r"\bduas mala\b", "fix": "duas malas",
         "tip": L("Plural nouns need a plural adjective/number agreement too.",
                  "Los sustantivos plurales necesitan concordancia también en número.",
                  "Substantivos plurais precisam de concordância também no número.",
                  "复数名词也需要数的一致。", "Множественные существительные тоже требуют согласования в числе."),
         "example": "Tenho duas malas."},
        {"pattern": r"\bviajar com aviao\b", "fix": "viajar de avião",
         "tip": L("Use 'de' for the means of transport, not 'com'.", "Se usa 'de' para el medio de transporte, no 'con'.",
                  "Usa-se 'de' para o meio de transporte, não 'com'.", "交通方式用 'de',不用 'com'。",
                  "Для способа передвижения используется 'de', а не 'com'."),
         "example": "Vou viajar de avião."},
    ],
    "zh": [
        {"pattern": "我是忙", "fix": "我很忙",
         "tip": L("Adjectives used as predicates use '很', not '是'.", "Los adjetivos como predicado usan '很', no '是'.",
                  "Adjetivos como predicado usam '很', não '是'.", "形容词作谓语时用“很”,不用“是”。",
                  "Прилагательные в роли сказуемого используют «很», а не «是»."),
         "example": "我很忙。"},
        {"pattern": "我是累", "fix": "我很累",
         "tip": L("Adjectives used as predicates use '很', not '是'.", "Los adjetivos como predicado usan '很', no '是'.",
                  "Adjetivos como predicado usam '很', não '是'.", "形容词作谓语时用“很”,不用“是”。",
                  "Прилагательные в роли сказуемого используют «很», а не «是»."),
         "example": "我很累。"},
        {"pattern": "两行李", "fix": "两件行李",
         "tip": L("Numbers need a measure word before the noun: '件' for luggage.",
                  "Los números necesitan un clasificador antes del sustantivo: '件' para equipaje.",
                  "Números precisam de um classificador antes do substantivo: '件' para bagagem.",
                  "数字后面名词前要加量词:行李用“件”。", "После числительного перед существительным нужно счётное слово: «件» для багажа."),
         "example": "我有两件行李。"},
        {"pattern": "三护照", "fix": "三本护照",
         "tip": L("'本' is the measure word for booklet-like items such as passports.",
                  "'本' es el clasificador para objetos como libretas, como el pasaporte.",
                  "'本' é o classificador para itens como livretos, como o passaporte.",
                  "'本' 是用于护照等册子类物品的量词。", "'本' — счётное слово для книжек, например паспортов."),
         "example": "我有一本护照。"},
        {"pattern": "我去过飞机场昨天", "fix": "我昨天去过飞机场",
         "tip": L("Time words usually come before the verb, not at the end of the sentence.",
                  "Las palabras de tiempo suelen ir antes del verbo, no al final.",
                  "As palavras de tempo geralmente vêm antes do verbo, não no final.",
                  "时间词通常放在动词前面,而不是句末。", "Слова времени обычно ставятся перед глаголом, а не в конце предложения."),
         "example": "我昨天去过飞机场。"},
        {"pattern": "在机场我", "fix": "我在机场",
         "tip": L("The subject usually comes first, before the location phrase.",
                  "El sujeto suele ir primero, antes de la frase de lugar.",
                  "O sujeito geralmente vem primeiro, antes da frase de lugar.",
                  "主语通常放在最前面,地点状语在其后。", "Подлежащее обычно ставится первым, перед обстоятельством места."),
         "example": "我在机场等你。"},
        {"pattern": "我很喜欢是", "fix": "我很喜欢",
         "tip": L("Don't add '是' after a verb like '喜欢'; it's not needed.",
                  "No se añade '是' después de un verbo como '喜欢'; no es necesario.",
                  "Não se adiciona '是' depois de um verbo como '喜欢'; não é necessário.",
                  "像“喜欢”这样的动词后面不需要加“是”。", "После глагола вроде «喜欢» не нужно добавлять «是»."),
         "example": "我很喜欢坐飞机。"},
        {"pattern": "没有了行李", "fix": "没有行李了",
         "tip": L("The particle '了' usually comes at the end of the clause, not right after '没有'.",
                  "La partícula '了' suele ir al final de la cláusula, no justo después de '没有'.",
                  "A partícula '了' geralmente vai no final da oração, não logo depois de '没有'.",
                  "助词“了”通常放在分句末尾,而不是紧跟在“没有”后面。", "Частица «了» обычно ставится в конце фразы, а не сразу после «没有»."),
         "example": "我没有行李了。"},
        {"pattern": "登机口十二", "fix": "十二号登机口",
         "tip": L("The gate number goes before the noun, with '号'.", "El número de puerta va antes del sustantivo, con '号'.",
                  "O número do portão vai antes do substantivo, com '号'.", "登机口号码放在名词前面,加“号”。",
                  "Номер выхода ставится перед существительным, с «号»."),
         "example": "请前往十二号登机口。"},
        {"pattern": "行李我的丢了", "fix": "我的行李丢了",
         "tip": L("Possessive + noun ('我的行李') comes before the verb.",
                  "Posesivo + sustantivo ('mi equipaje') va antes del verbo.",
                  "Possessivo + substantivo ('minha bagagem') vem antes do verbo.",
                  "所有格+名词(“我的行李”)放在动词前面。", "Притяжательное + существительное («мой багаж») ставится перед глаголом."),
         "example": "我的行李丢了。"},
        {"pattern": "我要个签证", "fix": "我要一个签证",
         "tip": L("Don't drop the number '一' before the measure word '个'.",
                  "No se omite el número '一' antes del clasificador '个'.",
                  "Não se omite o número '一' antes do classificador '个'.",
                  "量词“个”前不能省略数字“一”。", "Числительное «一» перед счётным словом «个» нельзя опускать."),
         "example": "我要一个签证。"},
        {"pattern": "很多液体是", "fix": "有很多液体",
         "tip": L("To express existence, use '有', not '是'.", "Para expresar existencia se usa '有', no '是'.",
                  "Para expressar existência usa-se '有', não '是'.", "表示存在用“有”,不用“是”。",
                  "Для выражения наличия используется «有», а не «是»."),
         "example": "包里有很多液体。"},
        {"pattern": "登机牌和护照准备", "fix": "准备好登机牌和护照",
         "tip": L("The verb usually comes before its object in this kind of instruction.",
                  "El verbo suele ir antes del objeto en este tipo de instrucción.",
                  "O verbo geralmente vem antes do objeto nesse tipo de instrução.",
                  "在这类指令中,动词通常放在宾语前面。", "В таких инструкциях глагол обычно ставится перед дополнением."),
         "example": "请准备好登机牌和护照。"},
        {"pattern": "我不知道不", "fix": "我不知道",
         "tip": L("Chinese doesn't use double negation like some other languages.",
                  "El chino no usa doble negación como otros idiomas.",
                  "O chinês não usa dupla negação como outros idiomas.",
                  "汉语不像有些语言那样使用双重否定。", "В китайском языке, в отличие от некоторых других языков, не используется двойное отрицание."),
         "example": "我不知道登机口在哪里。"},
        {"pattern": "谢谢你为", "fix": "谢谢你",
         "tip": L("'谢谢你' alone is enough to say 'thank you'; no extra preposition needed.",
                  "'谢谢你' solo ya significa 'thank you'; no se necesita preposición extra.",
                  "'谢谢你' sozinho já significa 'thank you'; não precisa de preposição extra.",
                  "“谢谢你”本身就足够表达感谢,不需要多余的介词。", "«谢谢你» само по себе означает «спасибо»; лишний предлог не нужен."),
         "example": "谢谢你的帮助。"},
    ],
    "ru": [
        {"pattern": r"\bя есть турист\b", "fix": "я турист",
         "tip": L("The present tense of 'to be' is normally omitted in Russian.",
                  "El verbo 'ser/estar' en presente normalmente se omite en ruso.",
                  "O verbo 'ser/estar' no presente normalmente é omitido em russo.",
                  "俄语现在时通常省略系动词“是”。", "Глагол «быть» в настоящем времени в русском обычно опускается."),
         "example": "Я турист."},
        {"pattern": r"\bя имею\b", "fix": "у меня есть",
         "tip": L("Possession is usually expressed with 'у меня есть', not 'я имею'.",
                  "La posesión se expresa normalmente con 'у меня есть', no 'я имею'.",
                  "A posse é normalmente expressa com 'у меня есть', não 'я имею'.",
                  "所有关系通常用“у меня есть”表达,而不是“я имею”。", "Обладание обычно выражается фразой «у меня есть», а не «я имею»."),
         "example": "У меня есть два чемодана."},
        {"pattern": r"\bя в аэропорту иду\b", "fix": "я иду в аэропорт",
         "tip": L("Movement toward a place uses accusative case, not prepositional.",
                  "El movimiento hacia un lugar usa el caso acusativo, no el prepositivo.",
                  "O movimento em direção a um lugar usa o caso acusativo, não o preposicional.",
                  "表示朝某地移动用第四格(宾格),而不是第六格(前置格)。", "Движение к месту требует винительного падежа, а не предложного."),
         "example": "Я иду в аэропорт."},
        {"pattern": r"\bбольшой турбулентность\b", "fix": "большая турбулентность",
         "tip": L("'Турбулентность' is feminine, so the adjective must agree: 'большая'.",
                  "'Turbulencia' es femenino, el adjetivo debe concordar: 'большая'.",
                  "'Turbulência' é feminino, o adjetivo deve concordar: 'большая'.",
                  "'Турбулентность' 是阴性名词,形容词要一致:'большая'。", "'Турбулентность' — женского рода, прилагательное должно согласовываться: 'большая'."),
         "example": "Это была большая турбулентность."},
        {"pattern": r"\bя хочу идти\b", "fix": "я хочу пойти",
         "tip": L("After 'хочу' (want), the perfective infinitive 'пойти' is more natural for a single trip.",
                  "Después de 'хочу' (querer), el infinitivo perfectivo 'пойти' es más natural para un viaje único.",
                  "Depois de 'хочу' (querer), o infinitivo perfectivo 'пойти' é mais natural para uma única viagem.",
                  "'хочу'(想要)后面接完成体不定式“пойти”更自然,表示一次性动作。", "После 'хочу' (хотеть) для одноразового похода естественнее совершенный вид 'пойти'."),
         "example": "Я хочу пойти к выходу на посадку."},
        {"pattern": r"\bмой паспорт красная\b", "fix": "мой паспорт красный",
         "tip": L("'Паспорт' is masculine, so the adjective must be masculine too: 'красный'.",
                  "'Pasaporte' es masculino, el adjetivo también debe serlo: 'красный'.",
                  "'Passaporte' é masculino, o adjetivo também deve ser: 'красный'.",
                  "'Паспорт' 是阳性名词,形容词也要用阳性:'красный'。", "'Паспорт' — мужского рода, прилагательное тоже должно быть мужского рода: 'красный'."),
         "example": "Мой паспорт красный."},
        {"pattern": r"\bя жду он\b", "fix": "я жду его",
         "tip": L("'Ждать' takes a direct object in the accusative/genitive case, not nominative.",
                  "'Esperar' lleva un objeto directo en caso acusativo/genitivo, no nominativo.",
                  "'Esperar' leva um objeto direto no caso acusativo/genitivo, não nominativo.",
                  "“等”后面的宾语要用第四格/第二格,不用主格。", "'Ждать' требует прямого дополнения в винительном/родительном падеже, а не в именительном."),
         "example": "Я жду его у выхода."},
        {"pattern": r"\bдва билет\b", "fix": "два билета",
         "tip": L("After 'два/три/четыре', the noun takes the genitive singular ending.",
                  "Después de 'два/три/четыре', el sustantivo lleva la terminación genitiva singular.",
                  "Depois de 'два/три/четыре', o substantivo leva a terminação genitiva singular.",
                  "“два/три/четыре”后面的名词要用单数第二格词尾。", "После «два/три/четыре» существительное принимает окончание родительного падежа единственного числа."),
         "example": "У меня два билета."},
        {"pattern": r"\bбез виза\b", "fix": "без визы",
         "tip": L("'Без' (without) always requires the genitive case.", "'Без' (sin) siempre requiere el caso genitivo.",
                  "'Без' (sem) sempre requer o caso genitivo.", "'без'(没有)后面总是要用第二格(属格)。",
                  "'Без' (без) всегда требует родительного падежа."),
         "example": "Нельзя въехать без визы."},
        {"pattern": r"\bя не понимаю ничего не\b", "fix": "я ничего не понимаю",
         "tip": L("Russian uses double negation correctly — but word order still matters: 'ничего не' comes before the verb.",
                  "El ruso usa doble negación correctamente, pero el orden importa: 'ничего не' va antes del verbo.",
                  "O russo usa dupla negação corretamente, mas a ordem importa: 'ничего не' vem antes do verbo.",
                  "俄语正确使用双重否定,但语序仍然重要:“ничего не”放在动词前面。", "В русском двойное отрицание корректно, но порядок слов важен: «ничего не» ставится перед глаголом."),
         "example": "Я ничего не понимаю."},
        {"pattern": r"\bспасибо за помощь вы\b", "fix": "спасибо вам за помощь",
         "tip": L("Thanking someone uses the dative case: 'спасибо вам'.", "Agradecer a alguien usa el caso dativo: 'спасибо вам'.",
                  "Agradecer a alguém usa o caso dativo: 'спасибо вам'.", "感谢某人要用第三格(与格):“спасибо вам”。",
                  "Благодарность кому-либо требует дательного падежа: «спасибо вам»."),
         "example": "Спасибо вам за помощь."},
        {"pattern": r"\bя иду к аэропорт\b", "fix": "я иду к аэропорту",
         "tip": L("'К' (toward) always requires the dative case.", "'К' (hacia) siempre requiere el caso dativo.",
                  "'К' (em direção a) sempre requer o caso dativo.", "'к'(朝向)后面总是要用第三格(与格)。",
                  "'К' (к) всегда требует дательного падежа."),
         "example": "Я иду к выходу на посадку."},
        {"pattern": r"\bсамолёт летит быстро очень\b", "fix": "самолёт летит очень быстро",
         "tip": L("The intensifier 'очень' (very) goes before the adjective/adverb it modifies.",
                  "El intensificador 'очень' (muy) va antes del adjetivo/adverbio que modifica.",
                  "O intensificador 'очень' (muito) vai antes do adjetivo/advérbio que modifica.",
                  "程度副词“очень”(非常)放在它修饰的形容词/副词之前。", "Усилитель «очень» ставится перед прилагательным/наречием, которое он определяет."),
         "example": "Самолёт летит очень быстро."},
        {"pattern": r"\bя хочу вода\b", "fix": "я хочу воду",
         "tip": L("A direct object after 'хочу' takes the accusative case.", "Un objeto directo después de 'хочу' lleva el caso acusativo.",
                  "Um objeto direto depois de 'хочу' leva o caso acusativo.", "'хочу'(想要)后面的直接宾语要用第四格(宾格)。",
                  "Прямое дополнение после 'хочу' требует винительного падежа."),
         "example": "Я хочу воду, пожалуйста."},
        {"pattern": r"\bдве чемодана\b", "fix": "два чемодана",
         "tip": L("'Чемодан' is masculine, so it takes 'два', not 'две'.", "'Maleta/chemodan' es masculino, lleva 'два', no 'две'.",
                  "'Chemodan' é masculino, leva 'два', não 'две'.", "'Чемодан' 是阳性名词,用 'два',不用 'две'。",
                  "'Чемодан' — мужского рода, поэтому 'два', а не 'две'."),
         "example": "У меня два чемодана."},
    ],
}

# ----------------------------------------------------------------------
# ANUNCIOS DE AEROPUERTO PARA PRONUNCIACIÓN — con traducción a 5 idiomas
# ----------------------------------------------------------------------
AIRPORT_ANNOUNCEMENTS = {
    "Check-in": [
        L("Please have your boarding pass and passport ready.",
          "Ten listo tu pase de abordar y tu pasaporte, por favor.",
          "Tenha seu cartão de embarque e passaporte prontos, por favor.",
          "请准备好您的登机牌和护照。",
          "Пожалуйста, приготовьте посадочный талон и паспорт."),
        L("Is this your only bag?",
          "¿Es esta tu única maleta?", "Esta é a sua única mala?", "这是您唯一的行李吗?",
          "Это ваш единственный багаж?"),
        L("Would you like a window or an aisle seat?",
          "¿Prefieres un asiento de ventana o de pasillo?",
          "Você prefere um assento na janela ou no corredor?",
          "您想要靠窗还是靠走廊的座位?",
          "Вы бы хотели место у окна или у прохода?"),
    ],
    "Seguridad": [
        L("Please remove your laptop from your bag.",
          "Por favor, saca tu laptop de la bolsa.",
          "Por favor, retire seu laptop da bolsa.",
          "请把笔记本电脑从包里拿出来。",
          "Пожалуйста, достаньте ноутбук из сумки."),
        L("Empty your pockets before walking through the scanner.",
          "Vacía tus bolsillos antes de pasar por el escáner.",
          "Esvazie os bolsos antes de passar pelo scanner.",
          "过安检前请清空口袋。",
          "Опустошите карманы перед проходом через сканер."),
        L("Liquids must be in containers of one hundred milliliters or less.",
          "Los líquidos deben ir en envases de cien mililitros o menos.",
          "Os líquidos devem estar em recipientes de cem mililitros ou menos.",
          "液体必须装在一百毫升或以下的容器中。",
          "Жидкости должны быть в контейнерах объёмом сто миллилитров или меньше."),
    ],
    "Inmigración y aduana": [
        L("What is the purpose of your visit?",
          "¿Cuál es el motivo de tu visita?", "Qual é o motivo da sua visita?", "您此行的目的是什么?",
          "Какова цель вашего визита?"),
        L("Do you have anything to declare?",
          "¿Tienes algo que declarar?", "Você tem algo a declarar?", "您有什么需要申报的吗?",
          "У вас есть что декларировать?"),
        L("How long are you planning to stay?",
          "¿Cuánto tiempo planeas quedarte?", "Quanto tempo você planeja ficar?", "您计划停留多久?",
          "Сколько времени вы планируете остаться?"),
    ],
    "Puerta de embarque": [
        L("This is the final boarding call for flight four oh two.",
          "Esta es la última llamada de embarque para el vuelo cuatro cero dos.",
          "Esta é a última chamada de embarque para o voo quatrocentos e dois.",
          "这是402号航班的最后登机广播。",
          "Это последнее объявление на посадку рейса четыреста два."),
        L("Flight two oh five is now boarding at gate twelve.",
          "El vuelo dos cero cinco está embarcando ahora en la puerta doce.",
          "O voo duzentos e cinco está embarcando agora no portão doze.",
          "205号航班现在在12号登机口开始登机。",
          "Рейс двести пять сейчас начинает посадку у выхода двенадцать."),
        L("Your flight has been delayed by one hour.",
          "Tu vuelo se ha retrasado una hora.", "Seu voo foi atrasado em uma hora.", "您的航班延误了一个小时。",
          "Ваш рейс задержан на один час."),
    ],
    "A bordo": [
        L("Please fasten your seatbelt and return your tray table to its upright position.",
          "Por favor, abróchate el cinturón y coloca la mesa plegable en posición vertical.",
          "Por favor, afivele o cinto e coloque a mesinha na posição vertical.",
          "请系好安全带,并将小桌板收起。",
          "Пожалуйста, пристегните ремень безопасности и верните столик в вертикальное положение."),
        L("We are experiencing some turbulence.",
          "Estamos experimentando algo de turbulencia.", "Estamos passando por um pouco de turbulência.",
          "我们正在经历一些颠簸。", "Мы попали в небольшую турбулентность."),
        L("The captain has turned on the seatbelt sign.",
          "El capitán ha encendido la señal del cinturón de seguridad.",
          "O comandante acendeu o aviso de cinto de segurança.",
          "机长已经打开了安全带指示灯。",
          "Командир корабля включил табло пристегнуть ремни."),
    ],
    "Reclamo de equipaje": [
        L("Your bag will arrive on carousel number four.",
          "Tu maleta llegará en la banda número cuatro.", "Sua mala vai chegar na esteira número quatro.",
          "您的行李将从4号行李转盘取回。", "Ваш багаж прибудет на ленту номер четыре."),
        L("I need to report a lost suitcase.",
          "Necesito reportar una maleta perdida.", "Preciso reportar uma mala perdida.",
          "我需要报告一件丢失的行李。", "Мне нужно сообщить о потерянном чемодане."),
        L("Please keep your claim tag until you receive your bag.",
          "Por favor, conserva tu etiqueta de reclamo hasta recibir tu maleta.",
          "Por favor, guarde sua etiqueta de reclamação até receber sua mala.",
          "请保留您的行李领取牌,直到收到行李为止。",
          "Пожалуйста, сохраняйте багажную бирку до получения багажа."),
    ],
}

# ----------------------------------------------------------------------
# ÁRBOLES DE CONVERSACIÓN — 6 escenarios, cada línea traducida a 5 idiomas
# ----------------------------------------------------------------------
AIRPORT_CONVERSATIONS = {
    "Check-in": {
        "start": {"bot": L("Good morning! Can I have your passport and booking reference, please?",
                            "¡Buenos días! ¿Me puede dar su pasaporte y su código de reserva, por favor?",
                            "Bom dia! Pode me dar seu passaporte e o código de reserva, por favor?",
                            "早上好!请出示您的护照和预订编号,可以吗?",
                            "Доброе утро! Могу я увидеть ваш паспорт и номер бронирования, пожалуйста?"),
                  "options": [{"label": L("Here you go", "Aquí tiene.", "Aqui está.", "给您。", "Вот, пожалуйста."),
                               "next": "bags"}]},
        "bags": {"bot": L("Thank you. How many bags are you checking in today?",
                           "Gracias. ¿Cuántas maletas va a facturar hoy?",
                           "Obrigado. Quantas malas você vai despachar hoje?",
                           "谢谢。您今天要托运几件行李?",
                           "Спасибо. Сколько чемоданов вы сдаёте сегодня?"),
                 "options": [
                     {"label": L("Just one", "Solo una.", "Só uma.", "只有一件。", "Только один."), "next": "seat"},
                     {"label": L("Two bags", "Dos maletas.", "Duas malas.", "两件行李。", "Два чемодана."),
                      "next": "seat"},
                 ]},
        "seat": {"bot": L("Would you like a window or an aisle seat?",
                           "¿Prefiere un asiento de ventana o de pasillo?",
                           "Você prefere um assento na janela ou no corredor?",
                           "您想要靠窗还是靠走道的座位?",
                           "Вы бы хотели место у окна или у прохода?"),
                 "options": [
                     {"label": L("Window, please", "Ventana, por favor.", "Janela, por favor.", "靠窗,谢谢。",
                                  "У окна, пожалуйста."), "next": "done"},
                     {"label": L("Aisle, please", "Pasillo, por favor.", "Corredor, por favor.", "靠走道,谢谢。",
                                  "У прохода, пожалуйста."), "next": "done"},
                 ]},
        "done": {"bot": L("Here is your boarding pass. Your gate is B12, boarding starts at 10:30. Have a nice flight!",
                           "Aquí tiene su pase de abordar. Su puerta es la B12, el embarque empieza a las 10:30. ¡Buen vuelo!",
                           "Aqui está seu cartão de embarque. Seu portão é o B12, o embarque começa às 10h30. Bom voo!",
                           "这是您的登机牌。您的登机口是B12,登机时间是10:30。祝您旅途愉快!",
                           "Вот ваш посадочный талон. Ваш выход B12, посадка начинается в 10:30. Хорошего полёта!")},
    },
    "Seguridad": {
        "start": {"bot": L("Please place your laptop and liquids in a separate tray.",
                            "Por favor, coloque su laptop y sus líquidos en una bandeja aparte.",
                            "Por favor, coloque seu laptop e seus líquidos em uma bandeja separada.",
                            "请把笔记本电脑和液体放在单独的托盘里。",
                            "Пожалуйста, положите ноутбук и жидкости в отдельный лоток."),
                  "options": [{"label": L("Okay, one moment", "Está bien, un momento.", "Certo, um momento.",
                                            "好的,请稍等。", "Хорошо, минутку."), "next": "walk"}]},
        "walk": {"bot": L("Now please walk through the metal detector.",
                           "Ahora, por favor, pase por el detector de metales.",
                           "Agora, por favor, passe pelo detector de metais.",
                           "现在请通过金属探测器。",
                           "Теперь, пожалуйста, пройдите через металлодетектор."),
                 "options": [{"label": L("Sure", "Claro.", "Claro.", "好的。", "Конечно."), "next": "beep"}]},
        "beep": {"bot": L("The alarm went off. Do you have any metal items in your pockets?",
                           "Sonó la alarma. ¿Tiene algún objeto metálico en los bolsillos?",
                           "O alarme disparou. Você tem algum item de metal nos bolsos?",
                           "警报响了。您口袋里有金属物品吗?",
                           "Сработала сигнализация. У вас есть металлические предметы в карманах?"),
                 "options": [
                     {"label": L("Just my keys, sorry", "Solo mis llaves, disculpe.", "Só minhas chaves, desculpe.",
                                  "只有我的钥匙,抱歉。", "Только ключи, извините."), "next": "clear"},
                     {"label": L("No, nothing", "No, nada.", "Não, nada.", "没有,什么都没有。", "Нет, ничего."),
                      "next": "clear"},
                 ]},
        "clear": {"bot": L("Please try again... All clear! You may collect your belongings.",
                            "Intente de nuevo, por favor... ¡Todo despejado! Puede recoger sus pertenencias.",
                            "Tente novamente, por favor... Tudo certo! Você pode pegar seus pertences.",
                            "请再试一次……一切正常!您可以拿走您的物品了。",
                            "Пожалуйста, попробуйте ещё раз... Всё чисто! Вы можете забрать свои вещи.")},
    },
    "Inmigración y aduana": {
        "start": {"bot": L("Good afternoon. Passport, please. What is the purpose of your visit?",
                            "Buenas tardes. Su pasaporte, por favor. ¿Cuál es el motivo de su visita?",
                            "Boa tarde. Passaporte, por favor. Qual é o motivo da sua visita?",
                            "下午好。请出示护照。您此行的目的是什么?",
                            "Добрый день. Паспорт, пожалуйста. Какова цель вашего визита?"),
                  "options": [
                      {"label": L("Tourism", "Turismo.", "Turismo.", "旅游。", "Туризм."), "next": "duration"},
                      {"label": L("Business", "Negocios.", "Negócios.", "商务。", "Бизнес."), "next": "duration"},
                  ]},
        "duration": {"bot": L("How long are you planning to stay?",
                               "¿Cuánto tiempo planea quedarse?", "Quanto tempo você planeja ficar?",
                               "您计划停留多久?", "Сколько времени вы планируете остаться?"),
                     "options": [
                         {"label": L("One week", "Una semana.", "Uma semana.", "一个星期。", "Одну неделю."),
                          "next": "address"},
                         {"label": L("Two weeks", "Dos semanas.", "Duas semanas.", "两个星期。", "Две недели."),
                          "next": "address"},
                     ]},
        "address": {"bot": L("Where will you be staying?",
                              "¿Dónde se va a hospedar?", "Onde você vai ficar hospedado?", "您将住在哪里?",
                              "Где вы будете останавливаться?"),
                    "options": [
                        {"label": L("A hotel downtown", "En un hotel del centro.", "Em um hotel no centro.",
                                     "市中心的一家酒店。", "В отеле в центре города."), "next": "stamp"},
                        {"label": L("With family", "Con mi familia.", "Com a família.", "和家人住在一起。",
                                     "У родственников."), "next": "stamp"},
                    ]},
        "stamp": {"bot": L("Everything looks fine. Welcome, and enjoy your trip!",
                            "Todo está en orden. ¡Bienvenido y que disfrute su viaje!",
                            "Está tudo certo. Seja bem-vindo e aproveite sua viagem!",
                            "一切正常。欢迎您,祝您旅途愉快!",
                            "Всё в порядке. Добро пожаловать, приятной поездки!")},
    },
    "Puerta de embarque": {
        "start": {"bot": L("Boarding pass and ID, please.",
                            "Su pase de abordar y una identificación, por favor.",
                            "Cartão de embarque e identidade, por favor.",
                            "请出示登机牌和身份证件。",
                            "Посадочный талон и удостоверение личности, пожалуйста."),
                  "options": [{"label": L("Here you are", "Aquí tiene.", "Aqui está.", "给您。", "Пожалуйста."),
                               "next": "group"}]},
        "group": {"bot": L("You're in boarding group 2. Please have a seat until your group is called.",
                            "Usted está en el grupo de embarque 2. Por favor, tome asiento hasta que llamen a su grupo.",
                            "Você está no grupo de embarque 2. Sente-se até que seu grupo seja chamado.",
                            "您属于第2登机组。请就座,等待广播叫到您的组。",
                            "Вы в группе посадки номер 2. Пожалуйста, присядьте, пока не объявят вашу группу."),
                  "options": [{"label": L("Thank you", "Gracias.", "Obrigado.", "谢谢。", "Спасибо."), "next": "call"}]},
        "call": {"bot": L("Now boarding group 2 for flight 205 to Madrid.",
                           "Ahora está embarcando el grupo 2 del vuelo 205 con destino a Madrid.",
                           "Agora embarcando o grupo 2 do voo 205 para Madri.",
                           "现在开始205航班飞往马德里的第2组登机。",
                           "Сейчас идёт посадка группы 2 на рейс 205 до Мадрида."),
                 "options": [{"label": L("That's me!", "¡Ese soy yo!", "Sou eu!", "是我!", "Это я!"),
                              "next": "board"}]},
        "board": {"bot": L("Enjoy your flight!",
                            "¡Que tenga un buen vuelo!", "Tenha um bom voo!", "祝您旅途愉快!",
                            "Приятного полёта!")},
    },
    "A bordo": {
        "start": {"bot": L("Hi there! Would you like something to drink?",
                            "¡Hola! ¿Le gustaría algo de beber?", "Olá! Gostaria de beber algo?",
                            "您好!您想喝点什么吗?", "Здравствуйте! Хотите что-нибудь выпить?"),
                  "options": [
                      {"label": L("Water, please", "Agua, por favor.", "Água, por favor.", "水,谢谢。",
                                   "Воды, пожалуйста."), "next": "snack"},
                      {"label": L("Orange juice, please", "Jugo de naranja, por favor.",
                                   "Suco de laranja, por favor.", "橙汁,谢谢。", "Апельсиновый сок, пожалуйста."),
                       "next": "snack"},
                  ]},
        "snack": {"bot": L("Would you also like a snack?",
                            "¿También le gustaría un refrigerio?", "Você também gostaria de um lanche?",
                            "您还想要点小吃吗?", "Хотите также лёгкую закуску?"),
                  "options": [
                      {"label": L("Yes, please", "Sí, por favor.", "Sim, por favor.", "好的,谢谢。",
                                   "Да, пожалуйста."), "next": "end"},
                      {"label": L("No, thank you", "No, gracias.", "Não, obrigado.", "不用了,谢谢。",
                                   "Нет, спасибо."), "next": "end"},
                  ]},
        "end": {"bot": L("Here you go. Let me know if you need anything else. Enjoy your flight!",
                          "Aquí tiene. Avíseme si necesita algo más. ¡Buen vuelo!",
                          "Aqui está. Me avise se precisar de mais alguma coisa. Bom voo!",
                          "给您。如果还需要什么请告诉我。祝您旅途愉快!",
                          "Пожалуйста. Дайте знать, если понадобится что-то ещё. Приятного полёта!")},
    },
    "Reclamo de equipaje": {
        "start": {"bot": L("Hello, how can I help you?",
                            "Hola, ¿en qué puedo ayudarle?", "Olá, como posso ajudá-lo?", "您好,我能帮您什么?",
                            "Здравствуйте, чем могу помочь?"),
                  "options": [{"label": L("I can't find my suitcase", "No encuentro mi maleta.",
                                            "Não consigo encontrar minha mala.", "我找不到我的行李了。",
                                            "Я не могу найти свой чемодан."), "next": "details"}]},
        "details": {"bot": L("I'm sorry to hear that. What does your suitcase look like?",
                              "Lamento escuchar eso. ¿Cómo es su maleta?", "Sinto muito por isso. Como é a sua mala?",
                              "很抱歉听到这个。您的行李是什么样子的?", "Мне очень жаль. Как выглядит ваш чемодан?"),
                    "options": [{"label": L("It's a black bag with a red tag",
                                              "Es una maleta negra con una etiqueta roja.",
                                              "É uma mala preta com uma etiqueta vermelha.",
                                              "是一个黑色的箱子,上面有一个红色的标签。",
                                              "Это чёрный чемодан с красной биркой."), "next": "form"}]},
        "form": {"bot": L("Thank you. Please fill out this lost luggage form, and we'll contact you within 24 hours.",
                           "Gracias. Por favor, llene este formulario de equipaje perdido y nos pondremos en contacto en 24 horas.",
                           "Obrigado. Por favor, preencha este formulário de bagagem extraviada e entraremos em contato em 24 horas.",
                           "谢谢。请填写这份行李丢失表格,我们会在24小时内联系您。",
                           "Спасибо. Пожалуйста, заполните эту форму о потерянном багаже, мы свяжемся с вами в течение 24 часов."),
                 "options": [{"label": L("Okay, thank you", "Está bien, gracias.", "Certo, obrigado.", "好的,谢谢。",
                                           "Хорошо, спасибо."), "next": "end"}]},
        "end": {"bot": L("You're welcome. Sorry for the inconvenience!",
                          "De nada. ¡Disculpe las molestias!", "De nada. Desculpe pelo transtorno!",
                          "不客气。给您带来不便,非常抱歉!", "Пожалуйста. Извините за неудобства!")},
    },
}

# ----------------------------------------------------------------------
# MENÚ LATERAL MODO OSCURO
# ----------------------------------------------------------------------
lives_display = "❤️ " * st.session_state.lives + "🖤 " * (3 - st.session_state.lives)
target_label = next((label for label, code in ALL_LANGS.items() if code == TARGET), TARGET)
st.sidebar.markdown(
    f"""
    <div class="score-card">
        <div class="score-title">{ui("sidebar_score_title")}</div>
        <div class="score-value">⭐ {st.session_state.score} / {st.session_state.answered}</div>
        <div style="margin-top:6px; font-size:18px;">{lives_display}</div>
    </div>
    <div style="text-align:center; margin-top:-10px; margin-bottom:16px; color:#8394a0; font-size:12px; font-weight:800; text-transform:uppercase;">
        {ui("sidebar_target_title")}: <span style="color:#1cb0f6;">{target_label}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

menu = st.sidebar.radio(
    ui("sidebar_modules_label"),
    ["quiz", "vocab", "grammar", "pron", "conv"],
    format_func=lambda k: MENU_LABELS[k][NATIVE] if NATIVE in MENU_LABELS[k] else MENU_LABELS[k]["en"],
)

col_lang1, col_lang2 = st.sidebar.columns(2)
with col_lang1:
    if st.button(ui("change_lang_button")):
        st.session_state.native_lang = None
        st.rerun()
with col_lang2:
    if st.button(ui("change_target_button")):
        st.session_state.target_lang = None
        st.rerun()
if st.sidebar.button("🔀 ConversTranslate / Aprendizaje"):
    st.session_state.app_mode = None
    st.rerun()

# ----------------------------------------------------------------------
# MÓDULO 1 — QUIZ #
# ----------------------------------------------------------------------

if menu == "quiz":
    st.header(f'{ui("quiz_header")} — {target_label}')

    quiz_bank_target = QUIZ_BANK[TARGET]
    options_cat = ["Todas"] + CATEGORIES
    selected_cat = st.selectbox(ui("area_label"), options_cat, key="quiz_cat",
                                 format_func=lambda c: cat_label(c))
    pool = quiz_bank_target if selected_cat == "Todas" else [q for q in quiz_bank_target if q["cat"] == selected_cat]

    if ("quiz_sequence" not in st.session_state
            or st.session_state.get("quiz_cat_prev") != selected_cat
            or st.session_state.get("quiz_target_prev") != TARGET):
        st.session_state.quiz_sequence = [random.choice(pool)]
        st.session_state.quiz_index = 0
        st.session_state.quiz_answered = {}
        st.session_state.quiz_cat_prev = selected_cat
        st.session_state.quiz_target_prev = TARGET
        st.session_state.lives = 3
        st.session_state.streak = 0

    if st.session_state.lives <= 0:
        st.markdown('<div class="pop-card">', unsafe_allow_html=True)
        st.error(ui("quiz_no_lives"))
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(ui("quiz_retry")):
            st.session_state.quiz_sequence = [random.choice(pool)]
            st.session_state.quiz_index = 0
            st.session_state.quiz_answered = {}
            st.session_state.lives = 3
            st.session_state.streak = 0
            st.session_state.score = 0
            st.session_state.answered = 0
            st.rerun()
    else:
        idx = st.session_state.quiz_index
        q = st.session_state.quiz_sequence[idx]
        already_answered = idx in st.session_state.quiz_answered

        # Racha con insignia animada (solo se muestra si hay racha activa)
        if st.session_state.streak >= 2:
            st.markdown(
                f'<div style="text-align:center;"><span class="streak-badge">{ui("quiz_streak")} {st.session_state.streak}</span></div>',
                unsafe_allow_html=True,
            )

        hearts_class = "lives-row"
        heart_html = ""
        for i in range(3):
            if i < st.session_state.lives:
                heart_html += "❤️ "
            else:
                heart_html += '<span class="heart-lost">🖤</span> '
        st.markdown(f'<div class="{hearts_class}">{heart_html}</div>', unsafe_allow_html=True)

        # Barra XP: progreso de preguntas contestadas dentro de la categoría elegida
        answered_in_pool = min(len(st.session_state.quiz_answered), len(pool))
        xp_pct = int((answered_in_pool / len(pool)) * 100) if pool else 0
        st.markdown(
            f'<div class="xp-bar-wrap"><div class="xp-bar-fill" style="width:{xp_pct}%;"></div></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="fade-card" style="background: #202f36; border: 2px solid #37464f; border-radius: 16px; padding: 20px; box-shadow: 0 4px 0 #182329; margin-bottom: 20px;">
                <span style="background: #193848; color: #1cb0f6; font-weight: 800; padding: 4px 12px; border-radius: 12px; font-size: 12px; text-transform: uppercase;">
                    📍 {cat_label(q['cat'])}
                </span>
                <h3 style="margin-top: 15px; margin-bottom: 0px; color: #ffffff !important;">{q['q']}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        prev_choice = st.session_state.quiz_answered[idx]["choice"] if already_answered else None
        choice = st.radio(
            ui("quiz_select_answer"),
            q["options"],
            index=q["options"].index(prev_choice) if prev_choice in q["options"] else None,
            disabled=already_answered,
            key=f"quiz_choice_{idx}",
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(ui("quiz_back"), disabled=(idx == 0), key=f"back_{idx}"):
                st.session_state.quiz_index -= 1
                st.rerun()
        with col2:
            if not already_answered:
                if st.button(ui("quiz_check"), key=f"check_{idx}"):
                    if choice is None:
                        st.info(ui("quiz_pick_first"))
                    else:
                        correct = choice == q["answer"]
                        st.session_state.quiz_answered[idx] = {"choice": choice, "correct": correct}
                        st.session_state.answered += 1
                        if correct:
                            st.session_state.score += 1
                            st.session_state.streak += 1
                            if st.session_state.streak in (5, 10, 15, 20):
                                st.balloons()
                        else:
                            st.session_state.lives -= 1
                            st.session_state.streak = 0
                        st.rerun()
        with col3:
            if st.button(ui("quiz_next"), disabled=not already_answered, key=f"next_{idx}"):
                if idx + 1 < len(st.session_state.quiz_sequence):
                    st.session_state.quiz_index += 1
                else:
                    st.session_state.quiz_sequence.append(random.choice(pool))
                    st.session_state.quiz_index += 1
                st.rerun()

        if already_answered:
            result = st.session_state.quiz_answered[idx]
            if result["correct"]:
                st.markdown('<div class="pop-card">', unsafe_allow_html=True)
                q_tip = q["tip"].get(NATIVE, q["tip"]["en"])
                st.success(f"{ui('quiz_correct')} {q_tip}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="pop-card">', unsafe_allow_html=True)
                q_tip = q["tip"].get(NATIVE, q["tip"]["en"])
                st.error(f"{ui('quiz_incorrect')} '{q['answer']}'. {q_tip}")
                st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# MÓDULO 2 — VOCABULARIO #
# ----------------------------------------------------------------------
elif menu == "vocab":
    st.header(ui("vocab_header"))
    cat = st.selectbox(ui("area_label"), CATEGORIES, key="vocab_cat", format_func=lambda c: cat_label(c))

    for term, example_en in AIRPORT_VOCAB[cat]:
        target_text = term[TARGET]
        st.markdown(
            f"""
            <div class="fade-card" style="background: #202f36; border: 2px solid #37464f; border-radius: 16px; padding: 16px; margin-bottom: 12px; box-shadow: 0 3px 0 #182329;">
                <div style="font-size: 18px; font-weight: 800; color: #1cb0f6;">{target_text}</div>
                <div style="font-size: 14px; font-weight: 700; color: #8394a0; margin-bottom: 6px;">{term[NATIVE]}</div>
                {f'<div style="font-size: 14px; font-style: italic; color: #e2e8f0;">"{example_en}"</div>' if TARGET == "en" else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button(ui("listen_target"), key=f"listen_target_{cat}_{term['en']}"):
                speak(example_en if TARGET == "en" else target_text, GTTS_CODE[TARGET])
        with c2:
            if st.button(ui("listen_native"), key=f"listen_native_{cat}_{term['en']}"):
                speak(term[NATIVE], GTTS_CODE[NATIVE])

# ----------------------------------------------------------------------
# MÓDULO 3 — CORRECTOR DE GRAMÁTICA #
# ----------------------------------------------------------------------
elif menu == "grammar":
    grammar_rules_target = GRAMMAR_RULES[TARGET]
    st.header(f'{ui("grammar_header")} — {target_label}')
    st.write(ui("grammar_intro"))

    text = st.text_area(ui("grammar_textarea_label"), height=100, placeholder=ui("grammar_placeholder"))

    if st.button(ui("grammar_check_button")):
        if not text.strip():
            st.info(ui("grammar_empty_warning"))
        else:
            corrected = text
            found_any = False
            for rule in grammar_rules_target:
                if re.search(rule["pattern"], corrected, re.IGNORECASE):
                    found_any = True
                    corrected = re.sub(rule["pattern"], rule["fix"], corrected, flags=re.IGNORECASE)
                    tip_text = rule["tip"].get(NATIVE, rule["tip"]["en"])
                    st.warning(f"⚠️ {tip_text}  \n*{ui('grammar_example_label')} \"{rule['example']}\"*")
            if found_any:
                st.write(ui("grammar_suggestion_label"))
                st.success(corrected)
                st.balloons()
            else:
                st.info(ui("grammar_no_errors"))

    search = st.text_input(ui("grammar_search_label"), placeholder=ui("grammar_search_placeholder"))
    with st.expander(ui("grammar_rules_expander").format(n=len(grammar_rules_target))):
        shown = 0
        for rule in grammar_rules_target:
            tip_text = rule["tip"].get(NATIVE, rule["tip"]["en"])
            if search and search.lower() not in tip_text.lower() and search.lower() not in rule["example"].lower():
                continue
            shown += 1
            st.markdown(
                f"""
                <div class="fade-card" style="background:#182730; border:1px solid #37464f; border-radius:10px; padding:8px 12px; margin-bottom:6px;">
                    <span style="color:#e2e8f0;">- {tip_text}</span><br>
                    <span style="color:#1cb0f6; font-style:italic; font-size:13px;">"{rule['example']}"</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if shown == 0:
            st.write(ui("grammar_no_rules_found"))

# ----------------------------------------------------------------------
# MÓDULO 4 — PRONUNCIACIÓN #
# ----------------------------------------------------------------------
elif menu == "pron":
    st.header(ui("pron_header"))

    cat = st.selectbox(ui("area_label"), CATEGORIES, key="pron_cat", format_func=lambda c: cat_label(c))
    reverse_mode = st.checkbox(ui("pron_reverse_checkbox"))

    if "target_sentence" not in st.session_state or st.session_state.get("pron_cat_prev") != cat or st.session_state.get("pron_target_prev") != TARGET:
        st.session_state.target_sentence = random.choice(AIRPORT_ANNOUNCEMENTS[cat])
        st.session_state.pron_cat_prev = cat
        st.session_state.pron_target_prev = TARGET
        st.session_state.reveal = False

    sentence = st.session_state.target_sentence

    if reverse_mode:
        st.markdown(
            f"""
            <div class="fade-card" style="background: #193848; border: 2px solid #2b7090; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="color: #84d8ff; font-size: 13px; font-weight: 800; text-transform: uppercase;">{ui("pron_reverse_prompt")}</div>
                <div style="color: #ffffff; font-size: 22px; font-weight: 800; margin-top: 5px;">"{sentence[NATIVE]}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(ui("pron_reveal_button")):
            st.session_state.reveal = True
        if st.session_state.get("reveal"):
            st.markdown(f'<div class="translation-box">🎯 {sentence[TARGET]}</div> <br> ', unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div class="fade-card" style="background: #193848; border: 2px solid #2b7090; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <div style="color: #84d8ff; font-size: 13px; font-weight: 800; text-transform: uppercase;">{ui("pron_repeat_prompt")}</div>
                <div style="color: #ffffff; font-size: 22px; font-weight: 800; margin-top: 5px;">"{sentence[TARGET]}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="translation-box">💬 {sentence[NATIVE]}</div> <br>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(ui("pron_change_button")):
            st.session_state.target_sentence = random.choice(AIRPORT_ANNOUNCEMENTS[cat])
            st.session_state.reveal = False
            st.rerun()
    with col2:
        if st.button(ui("pron_listen_target_button")):
            speak(sentence[TARGET], GTTS_CODE[TARGET])
    with col3:
        if st.button(ui("pron_listen_native_button")):
            speak(sentence[NATIVE], GTTS_CODE[NATIVE])

    st.write(ui("pron_record_prompt"))
    audio_value = st.audio_input(ui("pron_record_label"))

    if audio_value is not None:
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio_value) as source:
                audio_data = recognizer.record(source)
            said = recognizer.recognize_google(audio_data, language=REC_LANG_CODE[TARGET])
            st.write(f"{ui('pron_system_heard')} **{said}**")

            ratio = difflib.SequenceMatcher(None, said.lower(), sentence[TARGET].lower()).ratio()
            score_pct = round(ratio * 100)
            st.progress(score_pct / 100)
            st.write(f"{ui('pron_accuracy_label')} **{score_pct}%**")

            if score_pct > 85:
                st.success(ui("pron_excellent"))
            elif score_pct > 60:
                st.warning(ui("pron_good"))
            else:
                st.error(ui("pron_keep_practicing"))
        except sr.UnknownValueError:
            st.error(ui("pron_unknown_value"))
        except sr.RequestError:
            st.error(ui("pron_request_error"))

# ----------------------------------------------------------------------
# MÓDULO 5 — CONVERSACIÓN #
# ----------------------------------------------------------------------
elif menu == "conv":
    st.header(ui("conv_header"))

    scenario = st.selectbox(ui("conv_scenario_label"), CATEGORIES, key="conv_scenario", format_func=lambda c: cat_label(c))
    tree = AIRPORT_CONVERSATIONS[scenario]
    current_node_key = st.session_state.conv_nodes[scenario]
    node = tree[current_node_key]
    bot_text = node["bot"]
    you_label = ui("conv_you_label")

    st.markdown(
        f"""
        <div class="fade-card" style="background: #202f36; border: 2px solid #37464f; border-radius: 16px; padding: 20px; box-shadow: 0 4px 0 #182329; margin-bottom: 10px;">
            <div style="color: #8394a0; font-size: 12px; font-weight: 800; text-transform: uppercase;">{ui("conv_staff_label")}</div>
            <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-top: 5px;"> "{bot_text[TARGET]}"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="translation-box">{you_label}: {bot_text[NATIVE]}</div> <br>', unsafe_allow_html=True)
    if st.button(ui("conv_listen_button"), key=f"conv_listen_{scenario}_{current_node_key}"):
        speak(bot_text[TARGET], GTTS_CODE[TARGET])

    st.write("")

    if "options" in node:
        st.write(ui("conv_choose_response"))
        for opt in node["options"]:
            label = opt["label"]
            if st.button(f"{you_label}: {label[TARGET]}  —  {label[NATIVE]}",
                         key=f"{scenario}_{current_node_key}_{label['en']}"):
                st.session_state.conv_nodes[scenario] = opt["next"]
                st.rerun()
    else:
        st.info(ui("conv_completed"))
        if st.button(ui("conv_restart_button")):
            st.session_state.conv_nodes[scenario] = "start"
            st.rerun()