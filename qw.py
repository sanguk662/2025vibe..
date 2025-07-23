import streamlit as st
import datetime
import uuid

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(page_title="✅ 할 일 체크리스트 앱", layout="centered")
st.title("✅ 할 일 체크리스트 앱")

# -----------------------
# 세션 상태 초기화
# -----------------------
if "todos" not in st.session_state:
    st.session_state.todos = []

# -----------------------
# 날짜 변환 함수
# -----------------------
def parse_date(val):
    return val if isinstance(val, datetime.date) else datetime.datetime.strptime(val, "%Y-%m-%d").date()

# -----------------------
# 할 일 추가 폼
# -----------------------
with st.form("add_task_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        task_text = st.text_input("할 일을 입력하세요 ✍️")
    with col2:
        due_date = st.date_input("기한", datetime.date.today())

    submitted = st.form_submit_button("➕ 추가하기")

    if submitted:
        if task_text.strip():
            st.session_state.todos.append({
                "id": str(uuid.uuid4()),
                "text": task_text.strip(),
                "done": False,
                "date": due_date
            })
            st.success(f"'{task_text}' 할 일이 추가되었습니다!")
        else:
            st.warning("할 일을 입력해 주세요!")

st.markdown("---")

# -----------------------
# 할 일 출력 함수
# -----------------------
def show_tasks(title, filter_fn):
    st.subheader(title)
    found = False
    updated_todos = []

    for item in st.session_state.todos:
        if "id" in item and filter_fn(item):
            found = True
            task_id = item["id"]
            unique_key = f"{task_id}_{title.replace(' ', '_')}"

            cols = st.columns([0.08, 0.75, 0.1])
            done = cols[0].checkbox("✅", value=item["done"], key=f"done_{unique_key}")

            if done:
                cols[1].markdown(f"~~{item['text']}~~ (📅 {item['date']})")
            else:
                cols[1].markdown(f"{item['text']} (📅 {item['date']})")

            if cols[2].button("🗑️", key=f"del_{unique_key}"):
                st.session_state.todos = [
                    t for t in st.session_state.todos if t.get("id") != task_id
                ]
                st.rerun()

            updated_todos.append({**item, "done": done})
        else:
            updated_todos.append(item)

    st.session_state.todos = updated_todos

    if not found:
        st.info("할 일이 없습니다!")

# -----------------------
# 탭 구성 및 필터링 기준
# -----------------------
today = datetime.date.today()
tab1, tab2, tab3 = st.tabs(["📌 오늘 할 일", "📆 예정된 할 일", "✅ 완료된 할 일"])

with tab1:
    show_tasks("📌 오늘 할 일", lambda x: not x["done"] and parse_date(x["date"]) == today)

with tab2:
    show_tasks("📆 예정된 할 일", lambda x: not x["done"] and parse_date(x["date"]) > today)

with tab3:
    show_tasks("✅ 완료된 할 일", lambda x: x["done"])

# -----------------------
# 진행률 표시 + 완료 메시지
# -----------------------
total = len(st.session_state.todos)
done = len([x for x in st.session_state.todos if x["done"]])

if total > 0:
    percent = int((done / total) * 100)
    st.markdown("---")
    st.progress(done / total)
    st.write(f"📊 완료된 일: {done} / {total}개 ({percent}%)")

    # 🎉 완료된 경우 풍선 + 메시지
    if done == total:
        st.success("🎉 할 일을 모두 끝냈어요! 정말 멋져요! 👏")
        st.balloons()
else:
    st.info("할 일을 추가해보세요 😄")
