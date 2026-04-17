import streamlit as st
from pymongo import MongoClient
from datetime import date

# ------------------ MONGODB ------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["tasks"]

st.set_page_config(page_title="Student Assistant", layout="centered")

st.title("🎓 Smart Student Assistant")

# ------------------ ADD TASK ------------------
st.header("➕ Add New Task")

subject = st.text_input("Subject")
task = st.text_input("Task")
deadline = st.date_input("Deadline", min_value=date.today())

if st.button("Add Task"):
    if subject and task:
        collection.insert_one({
            "subject": subject,
            "task": task,
            "deadline": str(deadline),
            "status": "pending"
        })
        st.success("Task added successfully ✅")
    else:
        st.warning("Please fill all fields ⚠️")

# ------------------ PROGRESS BAR ------------------
tasks = list(collection.find())

total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t.get("status") == "completed"])

if total_tasks > 0:
    progress = completed_tasks / total_tasks
    st.subheader("📊 Your Progress")
    st.progress(progress)
    st.write(f"{completed_tasks} / {total_tasks} tasks completed ✅")
else:
    st.info("No tasks yet. Add some tasks 🚀")

# ------------------ SHOW TASKS ------------------
st.header("📋 Your Tasks")

for t in tasks:
    col1, col2, col3 = st.columns([4, 1, 1])

    # TASK TEXT
    with col1:
        if t.get("status") == "completed":
            st.write(f"✅ ~{t['subject']} - {t['task']}~ (Done)")
        else:
            st.write(f"📌 {t['subject']} - {t['task']} (Due: {t['deadline']})")

    # ✔️ COMPLETE BUTTON
    with col2:
        if t.get("status") != "completed":
            if st.button("✔️", key=f"done_{t['_id']}"):
                collection.update_one(
                    {"_id": t["_id"]},
                    {"$set": {"status": "completed"}}
                )
                st.rerun()

    # ❌ DELETE BUTTON
    with col3:
        if st.button("❌", key=f"delete_{t['_id']}"):
            collection.delete_one({"_id": t["_id"]})
            st.rerun() 