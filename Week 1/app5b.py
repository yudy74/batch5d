import streamlit as st

ROLES = ["Programmer", "UI/UX Designer", "Data Scientist"]

QUESTIONS = [
    {
        "pertanyaan": "Saat nongkrong, lu lebih suka...",
        "pilihan": [
            "Duduk sambil ngerjain side project (iya, bawa laptop😎)",
            "Nge-review desain cafe: 'Ini kok norak bgt desainnya😐'",
            "Ngobrolin tren crypto, data Tiktok"
        ]
    },
    {
        "pertanyaan": "Kalo disuruh ikut lomba, lu paling semangat kalau...",
        "pilihan": [
            "Hackathon bikin web/aplikasi",
            "Bikin desain buat aplikasi",
            "Suruh ngolah data buanyak banget biar rapih"
        ]
    },
    {
        "pertanyaan": "Waktu kerja kelompok, lu biasanya...",
        "pilihan": [
            "Paling gercep ngambil coding-an pokoknya biar cepet kelar",
            "Maunya yang gambar gambar mulu",
            "Selalu nanya, 'INI DATA DAPET DARIMANA'"
        ]
    }
]

def score_quiz(answers):
    scores = {role: 0 for role in ROLES}
    for idx, ans in enumerate(answers):
        if ans is not None:
            scores[ROLES[QUESTIONS[idx]["pilihan"].index(ans)]] += 1
    return scores

def get_result(scores):
    max_score = max(scores.values())
    top_roles = [role for role, score in scores.items() if score == max_score]
    if len(top_roles) == 1:
        if top_roles[0] == "Programmer":
            return "SELAMAT KAMU OTW TIDUR 1 JAM PER HARI SEBAGAI PROGRAMMER"
        elif top_roles[0] == "UI/UX Designer":
            return "SELAMAT KAMU BISA BEDAIN WARNA #FFFFFF SAMA #FEFEFE. COCOK JADI UIUX DESIGNER"
        else:
            return "SELAMAT KAMU BISA NGELIHAT 1000 LINE EXCEL SEKALIGUS. SEPUH DATSCI"
    else:
        return "SELAMAT KAMU ALL ROLE, COCOK JADI PROGRAMMER, UIUX, SAMA DATSCI"
        # Jika ada beberapa role dengan skor tertinggi, tampilkan pesan umum

# --- Streamlit UI ---
st.title("🧐WHAT IS YOUR PASSION🧐")
st.header("Mini quizzz")

if "p_index" not in st.session_state:
    st.session_state.p_index = 0
if "jawaban_user" not in st.session_state:
    st.session_state.jawaban_user = [None] * len(QUESTIONS)
if "submitted" not in st.session_state:
    st.session_state.submitted = False

index = st.session_state.p_index
q = QUESTIONS[index]

st.subheader(f"Pertanyaan ke-{index+1} dari {len(QUESTIONS)}")
jawaban = st.radio(
    q["pertanyaan"],
    q["pilihan"],
    index=q["pilihan"].index(st.session_state.jawaban_user[index]) if st.session_state.jawaban_user[index] in q["pilihan"] else 0,
    key=f"radio_{index}"
)
st.session_state.jawaban_user[index] = jawaban

col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back", on_click=lambda: st.session_state.update(p_index=max(0, st.session_state.p_index-1)))
with col2:
    if index == len(QUESTIONS) - 1:
        if st.button("Submit"):
            if None in st.session_state.jawaban_user:
                st.warning("Jawab semua pertanyaan dulu ya!")
            else:
                st.session_state.submitted = True
    else:
        st.button("Next", on_click=lambda: st.session_state.update(p_index=min(len(QUESTIONS)-1, st.session_state.p_index+1)))

if st.session_state.submitted:
    scores = score_quiz(st.session_state.jawaban_user)
    result = get_result(scores)
    st.subheader(result)
    if result.startswith("SELAMAT KAMU OTW"):
        st.balloons()
        st.image("https://media.giphy.com/media/YTbZzCkRQCEJa/giphy.gif")
    if result.startswith("SELAMAT KAMU BISA BEDAIN"):
        st.balloons()
        st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTZiaXRtZTcyNXk5cnJ4eGhxeWhlcXdyd3hiNzQ0b2lkMjlxbHN5ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kyLYXonQYYfwYDIeZl/giphy.gif")
    if result.startswith("SELAMAT KAMU BISA NGELIHAT"):
        st.balloons()
        st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTRsNmQ0eGl4NHQydGtpYTNzaWFlcG12NXg4ejVteG5qaGR4cXhiZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/artj92V8o75VPL7AeQ/giphy.gif")
    if result.startswith("SELAMAT KAMU ALL ROLE"):
        st.balloons()
        st.image("https://media1.giphy.com/giphy.gif")
    if st.button("Reset"):
        st.session_state.p_index = 0
        st.session_state.jawaban_user = [None] * len(QUESTIONS)
        st.session_state.submitted = False