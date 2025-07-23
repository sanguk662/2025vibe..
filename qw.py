def show_tasks(title, filter_fn):
    st.subheader(title)
    found = False
    updated_todos = []
    delete_task_id = None  # 🔑 삭제 예약용 변수

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

            # ✅ 삭제 예약
            if cols[2].button("🗑️", key=f"del_{unique_key}"):
                delete_task_id = task_id

            updated_todos.append({**item, "done": done})
        else:
            updated_todos.append(item)

    # 실제 삭제는 루프 바깥에서!
    if delete_task_id:
        st.session_state.todos = [t for t in updated_todos if t.get("id") != delete_task_id]
        st.experimental_rerun()
    else:
        st.session_state.todos = updated_todos

    if not found:
        st.info("할 일이 없습니다!")

    if title.startswith("✅"):
        completed_count = sum(1 for t in st.session_state.todos if t["done"])
        if completed_count == len(st.session_state.todos) and len(st.session_state.todos) > 0:
            st.success("모든 할 일을 완료했습니다! 잘하셨어요! 🎉")
            st.balloons()
