# Streamlit là một thư viện Python để tạo ứng dụng web đơn giản
# Sử dụng 'st' làm alias để dễ dàng truy cập các chức năng của Streamlit
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Thiết lập trang
st.set_page_config(
    page_title="Quản Lý Công Việc Cá Nhân",
    page_icon="✅",
    layout="wide"
)

# Hàm để lưu dữ liệu công việc
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(st.session_state.tasks, f)

# Hàm để tải dữ liệu công việc
def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            return json.load(f)
    return []

# Khởi tạo session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

def main():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>✅ Quản Lý Công Việc Cá Nhân</h1>", unsafe_allow_html=True)

    # Form thêm công việc mới
    st.markdown('<div class="section-header">📌 Thêm Công Việc Mới</div>', unsafe_allow_html=True)
    with st.form("new_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("📋 Tên công việc:")
            priority = st.selectbox("🎯 Độ ưu tiên:", ["Cao", "Trung bình", "Thấp"])
        with col2:
            due_date = st.date_input("📅 Hạn hoàn thành:")
            task_description = st.text_area("📝 Mô tả:")
        submitted = st.form_submit_button("➕ Thêm công việc")
        
        if submitted and task_name:
            new_task = {
                "tên": task_name,
                "mô tả": task_description,
                "hạn": str(due_date),
                "ưu tiên": priority,
                "trạng thái": "Chưa hoàn thành",
                "ngày tạo": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success("✅ Đã thêm công việc mới!")

    # Hiển thị danh sách công việc
    st.markdown('<div class="section-header">📋 Danh Sách Công Việc</div>', unsafe_allow_html=True)
    tasks = st.session_state.tasks
    
    if tasks:
        col1, col2 = st.columns([2,1])
        with col1:
            status_filter = st.selectbox("🔍 Lọc theo trạng thái:", ["Tất cả", "Chưa hoàn thành", "Đã hoàn thành"])
        with col2:
            priority_filter = st.selectbox("🎯 Lọc theo độ ưu tiên:", ["Tất cả", "Cao", "Trung bình", "Thấp"])

        df = pd.DataFrame(tasks)
        if status_filter != "Tất cả":
            df = df[df["trạng thái"] == status_filter]
        if priority_filter != "Tất cả":
            df = df[df["ưu tiên"] == priority_filter]

        for idx, task in df.iterrows():
            priority_class = {
                "Cao": "priority-high",
                "Trung bình": "priority-medium",
                "Thấp": "priority-low"
            }[task['ưu tiên']]
            
            status_class = "status-completed" if task['trạng thái'] == "Đã hoàn thành" else "status-pending"
            
            with st.expander(f"🔸 {task['tên']}"):
                st.markdown(f"""
                <div class="task-card">
                    <p><span class="{priority_class}">{'🔴' if task['ưu tiên'] == 'Cao' else '🟡' if task['ưu tiên'] == 'Trung bình' else '🟢'} {task['ưu tiên']}</span></p>
                    <p>📝 <b>Mô tả:</b> {task['mô tả']}</p>
                    <p>📅 <b>Hạn:</b> {task['hạn']}</p>
                    <p><span class="{status_class}">{task['trạng thái']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Thêm phần chỉnh sửa công việc
                if st.button("✏️ Chỉnh sửa", key=f"edit_{idx}"):
                    st.session_state[f'editing_{idx}'] = True

                # Hiển thị form chỉnh sửa khi nút được nhấn
                if st.session_state.get(f'editing_{idx}', False):
                    with st.form(key=f"edit_form_{idx}"):
                        st.subheader("📝 Chỉnh sửa công việc")
                        new_name = st.text_input("Tên công việc:", value=task['tên'])
                        new_description = st.text_area("Mô tả:", value=task['mô tả'])
                        new_due_date = st.date_input("Hạn hoàn thành:", value=datetime.strptime(task['hạn'], "%Y-%m-%d").date())
                        new_priority = st.selectbox("Độ ưu tiên:", ["Cao", "Trung bình", "Thấp"], index=["Cao", "Trung bình", "Thấp"].index(task['ưu tiên']))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Lưu thay đổi"):
                                st.session_state.tasks[idx].update({
                                    "tên": new_name,
                                    "mô tả": new_description,
                                    "hạn": str(new_due_date),
                                    "ưu tiên": new_priority
                                })
                                save_tasks()
                                del st.session_state[f'editing_{idx}']
                                st.success("✅ Đã cập nhật công việc!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("❌ Hủy"):
                                del st.session_state[f'editing_{idx}']
                                st.rerun()

                # Các nút thao tác khác
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✔️ " + ("Đánh dấu hoàn thành" if task['trạng thái'] == "Chưa hoàn thành" else "Đánh dấu chưa hoàn thành"), key=f"btn_{idx}"):
                        st.session_state.tasks[idx]['trạng thái'] = "Đã hoàn thành" if task['trạng thái'] == "Chưa hoàn thành" else "Chưa hoàn thành"
                        save_tasks()
                        st.rerun()
                with col2:
                    if st.button("🗑️ Xóa công việc này", key=f"del_{idx}"):
                        st.session_state.tasks.pop(idx)
                        save_tasks()
                        st.rerun()
    else:
        st.info("📌 Chưa có công việc nào được thêm.")

if __name__ == "__main__":
    main()
