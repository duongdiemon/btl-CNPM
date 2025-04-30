import streamlit as st
from datetime import datetime
from models.task import Task

def tasks_page():
    st.title("📝 Quản lý công việc")
    
    # Form thêm công việc mới
    with st.expander("➕ Thêm công việc mới", expanded=True):
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("Tiêu đề")
            description = st.text_area("Mô tả")
            due_date = st.date_input("Hạn hoàn thành")
            priority = st.selectbox(
                "Độ ưu tiên",
                ["Cao", "Trung bình", "Thấp"]
            )
            
            if st.form_submit_button("Thêm"):
                if title and description:
                    new_task = Task(
                        title=title,
                        description=description,
                        due_date=due_date,
                        priority=priority
                    )
                    st.session_state.current_user.tasks.append(new_task.to_dict())
                    st.success("✅ Đã thêm công việc mới!")
                    st.rerun()
                else:
                    st.error("Vui lòng điền đầy đủ thông tin!")
    
    # Hiển thị danh sách công việc
    st.subheader("📋 Danh sách công việc")
    
    # Bộ lọc
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.selectbox(
            "Lọc theo trạng thái",
            ["Tất cả", "Chưa hoàn thành", "Đã hoàn thành"]
        )
    with col2:
        filter_priority = st.selectbox(
            "Lọc theo độ ưu tiên",
            ["Tất cả", "Cao", "Trung bình", "Thấp"]
        )
    
    # Hiển thị công việc
    tasks = st.session_state.current_user.tasks
    if not tasks:
        st.info("📝 Chưa có công việc nào!")
    else:
        for i, task_data in enumerate(tasks):
            task = Task.from_dict(task_data)
            
            # Áp dụng bộ lọc
            if filter_status != "Tất cả" and task.status != filter_status:
                continue
            if filter_priority != "Tất cả" and task.priority != filter_priority:
                continue
            
            with st.expander(f"{'✅' if task.status == 'Đã hoàn thành' else '📌'} {task.title}"):
                st.write(f"📄 Mô tả: {task.description}")
                st.write(f"⏰ Hạn hoàn thành: {task.due_date.strftime('%d/%m/%Y') if task.due_date else 'Không có'}")
                st.write(f"🎯 Độ ưu tiên: {task.priority}")
                st.write(f"📅 Ngày tạo: {task.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                
                # Form chỉnh sửa công việc
                with st.form(key=f"edit_task_form_{i}"):
                    edited_title = st.text_input("Tiêu đề", value=task.title)
                    edited_description = st.text_area("Mô tả", value=task.description)
                    edited_due_date = st.date_input(
                        "Hạn hoàn thành",
                        value=task.due_date if task.due_date else datetime.now()
                    )
                    edited_priority = st.selectbox(
                        "Độ ưu tiên",
                        ["Cao", "Trung bình", "Thấp"],
                        index=["Cao", "Trung bình", "Thấp"].index(task.priority)
                    )
                    edited_status = st.selectbox(
                        "Trạng thái",
                        ["Chưa hoàn thành", "Đã hoàn thành"],
                        index=1 if task.status == "Đã hoàn thành" else 0
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Lưu thay đổi"):
                            task.title = edited_title
                            task.description = edited_description
                            task.due_date = edited_due_date
                            task.priority = edited_priority
                            task.status = edited_status
                            if edited_status == "Đã hoàn thành" and task.status != "Đã hoàn thành":
                                task.completed_at = datetime.now()
                            st.session_state.current_user.tasks[i] = task.to_dict()
                            st.success("✅ Đã lưu thay đổi!")
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("🗑️ Xóa"):
                            st.session_state.current_user.tasks.pop(i)
                            st.success("✅ Đã xóa công việc!")
                            st.rerun() 