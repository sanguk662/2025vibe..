import streamlit as st
import datetime
import uuid

st.set_page_config(page_title="할 일 체크리스트 앱", page_icon="✅")
st.title("✅ 할 일 체크리스트 앱")

if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 추가 폼
with st.form(key="add_form", clear_on_submit=True):
    cols = st.columns([0.7, 0.3])
    text = cols[0].text_input("할 일을 입력하세요 ✍️", placeholder="예: 영어 단어 외우기")
    date = cols[1].date_input("기한", value=datetime.date.today())
    submitted = st.form_submit_button("➕ 추가하기")
    if submitted and text:
        st.session_state.todos.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "date": str(date),
            "done": False
        })
        st.experimental_rerun()

# 탭
tabs = st.tabs(["📌 오늘 할 일", "📅 예정된 할 일", "✅ 완료된 할 일"])
today = datetime.date.today()

# 공통 렌더 함수
def show_tasks(title, filter_fn):
    st.subheader(title)
    found = False
    updated_todos = []

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

            # 삭제 버튼
            if cols[2].button("🗑️", key=f"del_{unique_key}"):
                st.session_state.todos = [t for t in st.session_state.todos if t.get("id") != task_id]
                st.experimental_rerun()

            updated_todos.append({**item, "done": done})
        else:
            updated_todos.append(item)

    st.session_state.todos = updated_todos

    if not found:
        st.info("할 일이 없습니다!")

    # 🎈 완료된 항목이 전부일 때 축하 애니메이션
    if title.startswith("✅"):
        completed_count = sum(1 for t in st.session_state.todos if t["done"])
        if completed_count == len(st.session_state.todos) and len(st.session_state.todos) > 0:
            st.success("모든 할 일을 완료했습니다! 잘하셨어요! 🎉")
            st.balloons()

# 각 탭에 할 일 보여주기
with tabs[0]:
    show_tasks("📌 오늘 할 일", lambda x: not x["done"] and x["date"] == str(today))

with tabs[1]:
    show_tasks("📅 예정된 할 일", lambda x: not x["done"] and x["date"] > str(today))

with tabs[2]:
    show_tasks("✅ 완료된 할 일", lambda x: x["done"])

# 끝!
