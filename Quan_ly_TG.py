import streamlit as st
import json
import os
from datetime import datetime, timedelta, date
import pandas as pd
import calendar

# Thiết lập trang
st.set_page_config(
    page_title="Quản Lý Thời Gian",
    page_icon="⏰",
    layout="wide"
)

# Hàm để lưu dữ liệu công việc
def save_tasks():
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.tasks, f, ensure_ascii=False)

# Hàm để tải dữ liệu công việc
def load_tasks():
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                # Kiểm tra và sửa dữ liệu không hợp lệ
                valid_tasks = []
                for task in tasks:
                    if isinstance(task, dict) and 'name' in task:
                        if 'status' not in task:
                            task['status'] = "Chưa hoàn thành"
                        if 'time_spent' not in task:
                            task['time_spent'] = 0
                        valid_tasks.append(task)
                return valid_tasks
        except:
            return []
    return []

# Khởi tạo session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.now().date()
if 'daily_notes' not in st.session_state:
    st.session_state.daily_notes = {}

def add_task():
    with st.form("add_task_form"):
        st.markdown("### 📝 Thêm Công Việc Mới")
        task_name = st.text_input("Tên công việc:")
        task_description = st.text_area("Mô tả:")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Ngày bắt đầu:")
            start_time = st.time_input("Giờ bắt đầu:")
        with col2:
            end_date = st.date_input("Ngày kết thúc:")
            end_time = st.time_input("Giờ kết thúc:")
        priority = st.selectbox("Độ ưu tiên:", ["Thấp", "Trung bình", "Cao"])
        submit = st.form_submit_button("Thêm công việc")
        
        if submit:
            if not task_name.strip():
                st.error("Vui lòng nhập tên công việc!")
                return
                
            new_task = {
                "id": len(st.session_state.tasks),
                "name": task_name.strip(),
                "description": task_description.strip(),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "end_time": end_time.strftime("%H:%M"),
                "priority": priority,
                "status": "Chưa hoàn thành",
                "time_spent": 0
            }
            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success("✅ Đã thêm công việc mới!")

def show_calendar():
    st.markdown("### 📅 Lịch Biểu")
    
    # Chọn tháng và năm
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("Chọn tháng:", range(1, 13), format_func=lambda x: calendar.month_name[x])
    with col2:
        current_year = datetime.now().year
        selected_year = st.selectbox("Chọn năm:", range(current_year-1, current_year+2))
    
    # Tạo lịch
    cal = calendar.monthcalendar(selected_year, selected_month)
    
    # Hiển thị lịch
    st.markdown(f"#### {calendar.month_name[selected_month]} {selected_year}")
    
    # Tạo bảng lịch
    days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    st.markdown("| " + " | ".join(days) + " |")
    st.markdown("|" + "|".join(["---" for _ in range(7)]) + "|")
    
    for week in cal:
        week_str = "|"
        for day in week:
            if day == 0:
                week_str += " |"
            else:
                # Kiểm tra công việc trong ngày
                current_date = date(selected_year, selected_month, day)
                tasks_on_day = [task for task in st.session_state.tasks 
                              if datetime.strptime(task['start_date'], "%Y-%m-%d").date() == current_date]
                
                if tasks_on_day:
                    week_str += f" {day} 📌 |"
                else:
                    week_str += f" {day} |"
        st.markdown(week_str)

def daily_planner():
    st.markdown("### 📋 Thời Gian Biểu Hàng Ngày")
    
    # Chọn ngày
    selected_date = st.date_input("Chọn ngày:", value=st.session_state.current_date)
    
    # Hiển thị công việc trong ngày
    tasks_on_day = [task for task in st.session_state.tasks 
                   if datetime.strptime(task['start_date'], "%Y-%m-%d").date() == selected_date]
    
    if tasks_on_day:
        st.markdown("#### Công việc trong ngày:")
        for idx, task in enumerate(tasks_on_day):
            with st.expander(f"📌 {task['name']} ({task['start_time']} - {task['end_time']})"):
                st.write(f"Mô tả: {task['description']}")
                st.write(f"Độ ưu tiên: {task['priority']}")
                st.write(f"Trạng thái: {task['status']}")
                
                # Theo dõi thời gian
                col1, col2 = st.columns(2)
                with col1:
                    time_spent = st.number_input(f"Thời gian đã dành (phút) cho {task['name']}:", 
                                               min_value=0, value=task['time_spent'],
                                               key=f"time_input_{task['id']}_{selected_date}_{idx}")
                with col2:
                    if st.button("Cập nhật thời gian", 
                               key=f"update_time_{task['id']}_{selected_date}_{idx}"):
                        task['time_spent'] = time_spent
                        save_tasks()
                        st.success("✅ Đã cập nhật thời gian!")
    else:
        st.info("Không có công việc nào trong ngày này.")
    
    # Ghi chú hàng ngày
    st.markdown("#### 📝 Ghi chú:")
    if str(selected_date) not in st.session_state.daily_notes:
        st.session_state.daily_notes[str(selected_date)] = ""
    
    daily_note = st.text_area("Ghi chú cho ngày này:", 
                             value=st.session_state.daily_notes[str(selected_date)],
                             key=f"note_{selected_date}")
    
    if st.button("Lưu ghi chú", key=f"save_note_{selected_date}"):
        st.session_state.daily_notes[str(selected_date)] = daily_note
        st.success("✅ Đã lưu ghi chú!")


def view_tasks():
    st.markdown("### 📋 Danh Sách Công Việc")
    
    if not st.session_state.tasks:
        st.info("Chưa có công việc nào. Hãy thêm công việc mới!")
        return
        
    try:
        # Tạo DataFrame từ danh sách công việc
        df = pd.DataFrame(st.session_state.tasks)
        
        # Hiển thị bảng với các cột đã chọn
        display_columns = ['name', 'description', 'start_date', 'start_time', 
                          'end_date', 'end_time', 'priority', 'status', 'time_spent']
        
        # Kiểm tra xem tất cả các cột cần thiết có tồn tại không
        if all(col in df.columns for col in display_columns):
            # Sắp xếp theo độ ưu tiên
            priority_order = {"Cao": 0, "Trung bình": 1, "Thấp": 2}
            df['Priority_Order'] = df['priority'].map(priority_order)
            df = df.sort_values('Priority_Order')
            
            # Hiển thị bảng đã sắp xếp
            st.dataframe(df[display_columns])
        else:
            # Nếu thiếu cột, hiển thị thông báo lỗi
            st.error("Dữ liệu không đúng định dạng. Vui lòng xóa file tasks.json và thử lại.")
            
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {str(e)}")
        st.info("Vui lòng xóa file tasks.json và thử lại.")
    
    # Thêm chức năng đánh dấu hoàn thành
    try:
        incomplete_tasks = [task['name'] for task in st.session_state.tasks 
                          if isinstance(task, dict) and 'name' in task 
                          and task.get('status', 'Chưa hoàn thành') == "Chưa hoàn thành"]
        
        if incomplete_tasks:
            task_to_complete = st.selectbox(
                "Chọn công việc đã hoàn thành:",
                incomplete_tasks
            )
            
            if st.button("Đánh dấu hoàn thành"):
                for task in st.session_state.tasks:
                    if isinstance(task, dict) and task.get('name') == task_to_complete:
                        task['status'] = "Đã hoàn thành"
                        break
                save_tasks()
                st.success("✅ Đã đánh dấu công việc hoàn thành!")
                st.rerun()
    except Exception as e:
        st.error(f"Có lỗi xảy ra khi xử lý trạng thái công việc: {str(e)}")
        st.info("Vui lòng xóa file tasks.json và thử lại.")

def create_sample_data():
    # Chỉ tạo dữ liệu mẫu nếu không có công việc nào
    if not st.session_state.tasks:
        sample_tasks = [
            {
                "id": 0,
                "name": "Họp nhóm dự án",
                "description": "Thảo luận về tiến độ dự án và phân công công việc",
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "start_time": "09:00",
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "end_time": "10:30",
                "priority": "Cao",
                "status": "Chưa hoàn thành",
                "time_spent": 0
            },
            {
                "id": 1,
                "name": "Viết báo cáo",
                "description": "Hoàn thành báo cáo tuần",
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "start_time": "14:00",
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "end_time": "16:00",
                "priority": "Trung bình",
                "status": "Chưa hoàn thành",
                "time_spent": 0
            }
        ]
        st.session_state.tasks.extend(sample_tasks)
        save_tasks()

def main():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>⏰ Quản Lý Thời Gian</h1>", unsafe_allow_html=True)
    
    # Tạo dữ liệu mẫu nếu chưa có
    create_sample_data()
    
    # Tạo tabs cho các chức năng
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Thêm công việc", "📅 Lịch biểu", "📋 Thời gian biểu", "📊 Danh sách"])
    
    with tab1:
        add_task()
    
    with tab2:
        show_calendar()
    
    with tab3:
        daily_planner()
    
    with tab4:
        view_tasks()

if __name__ == "__main__":
    main()