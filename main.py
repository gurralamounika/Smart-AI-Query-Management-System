import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------

conn = sqlite3.connect("queries.db")
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
# ---------------- USERS DATABASE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
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

    elif "password" in q:
        return "You can reset your password using the Forgot Password option."

    else:
        return "I received your query: " + question


# ---------------- UI ----------------

st.set_page_config(
    page_title="Smart AI Query Management System",
    page_icon="🤖"
)

st.title("🤖 Smart AI Query Management System")

st.write("Ask your question and get an AI-style response.")

question = st.text_input(
    "Enter your query",
    placeholder="Example: What is Python?"
)

if st.button("Submit Query"):

    if question.strip() == "":
        st.warning("Please enter a query.")

    else:

        answer = get_answer(question)

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO queries
            (question, answer, status, time)
            VALUES (?, ?, ?, ?)
            """,
            (
                question,
                answer,
                "Open",
                current_time
            )
        )

        conn.commit()

        st.success("Query submitted successfully!")

        st.subheader("🤖 AI Response")
        st.info(answer)


# ---------------- QUERY HISTORY ----------------

st.divider()

st.header("📋 Query History")

cursor.execute(
    "SELECT * FROM queries ORDER BY id DESC"
)

all_queries = cursor.fetchall()

if len(all_queries) == 0:

    st.write("No queries yet.")

else:

    for item in all_queries:

        st.subheader("Query #" + str(item[0]))

        st.write("**Question:**", item[1])
        st.write("**Answer:**", item[2])
        st.write("**Status:**", item[3])
        st.caption(item[4])

        st.divider()


        # ---------------- ADMIN DASHBOARD ----------------

st.divider()
st.header("👨‍💼 Admin Dashboard")

cursor.execute("SELECT * FROM queries ORDER BY id DESC")
admin_queries = cursor.fetchall()

if len(admin_queries) == 0:
    st.info("No queries available.")
else:
    query_options = {}

    for item in admin_queries:
        query_options[item[0]] = f"Query #{item[0]} - {item[1][:50]}"

    selected_id = st.selectbox(
        "Select a Query",
        options=list(query_options.keys()),
        format_func=lambda x: query_options[x]
    )

    selected_query = next(
        item for item in admin_queries if item[0] == selected_id
    )

    st.write("### Selected Query")
    st.write(selected_query[1])

    st.write("### Current Answer")
    st.info(selected_query[2])

    new_status = st.selectbox(
        "Update Status",
        ["Open", "In Progress", "Resolved"],
        index=["Open", "In Progress", "Resolved"].index(selected_query[3])
    )

    if st.button("Update Query Status"):
        cursor.execute(
            "UPDATE queries SET status = ? WHERE id = ?",
            (new_status, selected_id)
        )

        conn.commit()

        st.success("Query status updated successfully!")
        