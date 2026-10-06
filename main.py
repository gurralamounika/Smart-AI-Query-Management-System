import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------

conn = sqlite3.connect("queries.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    status TEXT,
    time TEXT
)
""")

conn.commit()


# ---------------- AI RESPONSE ----------------

def get_answer(question):

    q = question.lower()

    if "python" in q:
        return "Python is a popular programming language used for AI, web development, automation and data science."

    elif "ai" in q or "artificial intelligence" in q:
        return "Artificial Intelligence allows computers to perform tasks that normally require human intelligence."

    elif "database" in q:
        return "A database is used to store, organize and manage application data."

    elif "streamlit" in q:
        return "Streamlit is a Python framework used to quickly build interactive web applications and dashboards."

    elif "password" in q:
        return "You can reset your password using the Forgot Password option."

    else:
        return "I received your query: " + question


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Smart AI Query Management System",
    page_icon="🤖",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #f8fbff, #eef4ff);
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

h1 {
    font-size: 46px !important;
    font-weight: 800 !important;
    text-align: center;
}

.hero-text {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 25px;
}

.section-title {
    font-size: 30px;
    font-weight: 700;
    margin-top: 25px;
}

.stTextInput input {
    border-radius: 12px;
    padding: 14px;
    font-size: 17px;
}

.stButton button {
    border-radius: 12px;
    padding: 10px 25px;
    font-weight: 600;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    """
    <div style="text-align:center;">
        <h1>🤖 Smart AI Query Management System</h1>
        <p>Your intelligent assistant for faster answers and smarter queries.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- AI IMAGE ----------------

st.image(
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1400&q=80",
    use_container_width=True
)


# ---------------- QUERY SECTION ----------------
st.markdown(
    '<div class="section-title">💬 Ask Your Question</div>',
    unsafe_allow_html=True
)
question = st.text_input(
    "Enter your query",
    placeholder="Example: What is Python?"
)


if st.button("🚀 Submit Query"):

    if question.strip() == "":
        st.warning("Please enter a question first.")

    else:

        answer = get_answer(question)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO queries
            (question, answer, status, time)
            VALUES (?, ?, ?, ?)
            """,
            (
                question,
                answer,
                "Completed",
                current_time
            )
        )

        conn.commit()

        st.success("Query processed successfully!")

        st.markdown(
            f"""
            <div class="card">
                <h3>🤖 AI Response</h3>
                <p>{answer}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------- QUICK QUESTIONS ----------------

st.markdown(
    '<div class="section-title">✨ Quick Questions</div>',
    unsafe_allow_html=True
)

st.caption("Try one of these popular queries to get started:")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🐍 Python\n\nLearn about Python programming.")

with col2:
    st.info("🤖 Artificial Intelligence\n\nExplore AI concepts.")

with col3:
    st.info("🗄️ Database\n\nUnderstand database basics.")


# ---------------- QUERY HISTORY ----------------

st.markdown(
    '<div class="section-title">📋 Query History</div>',
    unsafe_allow_html=True
)

cursor.execute(
    """
    SELECT id, question, answer, status, time
    FROM queries
    ORDER BY id DESC
    """
)

rows = cursor.fetchall()

if rows:

    for row in rows:

        query_id, q, a, status, time = row

        with st.expander(f"Query #{query_id} — {q}"):

            st.write("**Question:**")
            st.write(q)

            st.write("**AI Response:**")
            st.write(a)

            st.write("**Status:**", status)
            st.write("**Time:**", time)

else:

    st.info("No queries submitted yet.")


# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Smart AI Query Management System • Built with Python, Streamlit and SQLite"
)