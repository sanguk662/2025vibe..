import streamlit as st
from datetime import datetime
import uuid

# 타이틀
st.set_page_config(page_title="할 일 체크리스트 앱")
st.title("✅ 할 일 체크리스트 앱")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 추가 UI
with st.form(key="todo_form", clear_on_submit=True):
    cols = st.columns([0.7, 0.3])
    text = cols[0].text_input("할 일을 입력하세요 ✍️", label_visibility="collapsed")
    date = cols[1].date_input("기한", datetime.today())
    submitted = st.form_submit_button("➕ 추가하기")
    if submitted and text:
        st.session_state.todos.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "date": date.strftime("%Y-%m-%d"),
            "done": False
        })

# 필터 탭
tab1, tab2, tab3 = st.tabs(["📌 오늘 할 일", "📅 예정된 할 일", "✅ 완료된 할 일"])

# 할 일 표시 함수
def show_tasks(title, filter_fn):
    st.subheader(title)
    found = False
    updated_todos = []
    delete_task_id = None

    for item in st.session_state.todos:
        if "id" in item and filter_fn(item):
            found = True
            task_id = item["id"]
            safe_title = title.replace(" ", "_").replace("✅", "done").replace("📅", "future").replace("📌", "today")
            unique_key = f"{task_id}_{safe_title}"

            cols = st.columns([0.08, 0.75, 0.1])
            done = cols[0].checkbox("✅", value=item["done"], key=f"done_{unique_key}")

            if done:
                cols[1].markdown(f"~~{item['text']}~~ (📅 {item['date']})")
            else:
                cols[1].markdown(f"{item['text']} (📅 {item['date']})")

            if cols[2].button("🗑️", key=f"del_{unique_key}"):
                delete_task_id = task_id

            updated_todos.append({**item, "done": done})
        else:
            updated_todos.append(item)

    if delete_task_id:
        st.session_state.todos = [t for t in updated_todos if t.get("id") != delete_task_id]
        st.experimental_rerun()
    else:
        st.session_state.todos = updated_todos

    if not found:
        st.info("할 일이 없습니다!")
