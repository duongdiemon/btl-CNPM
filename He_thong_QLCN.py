import streamlit as st
import json
from datetime import datetime, timedelta
import os
import hashlib
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar
import re
import shutil
from pathlib import Path

# Thiết lập giao diện
st.set_page_config(
    page_title="Personal Management App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện đăng nhập/đăng ký
st.markdown("""
<style>
    .auth-form {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2.5rem;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .auth-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2.5rem;
        font-size: 1.8rem;
    }
    
    .auth-button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        border: none;
        margin-top: 1.5rem;
        font-size: 1rem;
    }
    
    .auth-link {
        text-align: center;
        margin-top: 1.5rem;
        padding: 0.5rem;
    }
    
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
        font-size: 1rem;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }

    .calendar {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .calendar th {
        background-color: #4CAF50;
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    .calendar td {
        border: 1px solid #ddd;
        padding: 1rem;
        text-align: center;
        height: 100px;
        vertical-align: top;
        transition: background-color 0.3s;
    }
    
    .calendar td:hover {
        background-color: #f5f5f5;
    }
    
    .today {
        background-color: #e8f5e9;
        font-weight: bold;
    }
    
    .task-count {
        color: #2196F3;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        padding: 0.2rem 0.5rem;
        background-color: rgba(33, 150, 243, 0.1);
        border-radius: 4px;
        display: inline-block;
    }

    .stExpander {
        background-color: white;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #ddd;
    }

    .stExpander:hover {
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }

    .stForm {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .stTextArea>div>div>textarea {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .stSelectbox>div>div>select {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .stNumberInput>div>div>input {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .stDateInput>div>div>input {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .stTimeInput>div>div>input {
        border-radius: 8px;
        padding: 0.8rem;
    }

    .welcome-title {
        font-size: 20px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {
        'name': '',
        'phone': '',
        'address': ''
    }
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'budgets' not in st.session_state:
    st.session_state.budgets = {}
if 'loans' not in st.session_state:
    st.session_state.loans = []
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'daily_planner' not in st.session_state:
    st.session_state.daily_planner = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = True
if 'task_time_tracking' not in st.session_state:
    st.session_state.task_time_tracking = {}
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []
if 'show_personal_info' not in st.session_state:
    st.session_state.show_personal_info = True

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"
    if not re.search(r"[A-Z]", password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ hoa"
    if not re.search(r"[a-z]", password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ thường"
    if not re.search(r"\d", password):
        return False, "Mật khẩu phải chứa ít nhất 1 số"
    return True, ""

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}}

def save_users(users_data):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=4)

def save_data():
    data = {
        'tasks': st.session_state.tasks,
        'notes': st.session_state.notes,
        'personal_info': st.session_state.personal_info,
        'transactions': st.session_state.transactions,
        'budgets': st.session_state.budgets,
        'loans': st.session_state.loans,
        'daily_planner': st.session_state.daily_planner,
        'task_time_tracking': st.session_state.task_time_tracking
    }
    user_data_file = f'user_data_{st.session_state.current_user}.json'
    with open(user_data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    user_data_file = f'user_data_{st.session_state.current_user}.json'
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            st.session_state.tasks = data.get('tasks', [])
            st.session_state.notes = data.get('notes', [])
            st.session_state.personal_info = data.get('personal_info', {})
            st.session_state.transactions = data.get('transactions', [])
            st.session_state.budgets = data.get('budgets', {})
            st.session_state.loans = data.get('loans', [])
            st.session_state.daily_planner = data.get('daily_planner', {})
            st.session_state.task_time_tracking = data.get('task_time_tracking', {})

def register_page():
    st.markdown('<div class="auth-form">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">✨ Đăng ký tài khoản mới</h1>', unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=True):
        username = st.text_input("👤 Tên đăng nhập")
        password = st.text_input("🔑 Mật khẩu", type="password")
        confirm_password = st.text_input("🔄 Xác nhận mật khẩu", type="password")
        
        submit = st.form_submit_button("🚀 Đăng ký")
        if submit:
            if not username or not password or not confirm_password:
                st.error("❌ Vui lòng điền đầy đủ thông tin!")
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.error(f"❌ {message}")
                elif password != confirm_password:
                    st.error("❌ Mật khẩu xác nhận không khớp!")
                else:
                    users_data = load_users()
                    if username in users_data["users"]:
                        st.error("❌ Tên đăng nhập đã tồn tại!")
                    else:
                        users_data["users"][username] = {
                            "password": hash_password(password)
                        }
                        save_users(users_data)
                        st.success("✅ Đăng ký thành công! Vui lòng đăng nhập.")
                        st.session_state.show_register = False
                        st.session_state.show_login = True
                        st.rerun()
    
    st.markdown('<div class="auth-link">', unsafe_allow_html=True)
    if st.button("🔙 Đã có tài khoản? Đăng nhập ngay"):
        st.session_state.show_register = False
        st.session_state.show_login = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def login_page():
    st.markdown('<div class="auth-form">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">🌟 Đăng nhập</h1>', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("👤 Tên đăng nhập")
        password = st.text_input("🔑 Mật khẩu", type="password")
        
        submit = st.form_submit_button("🚀 Đăng nhập")
        if submit:
            users_data = load_users()
            
            if username in users_data["users"] and users_data["users"][username]["password"] == hash_password(password):
                st.session_state.is_logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
    
    st.markdown('<div class="auth-link">', unsafe_allow_html=True)
    if st.button("📝 Chưa có tài khoản? Đăng ký ngay"):
        st.session_state.show_register = True
        st.session_state.show_login = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def task_management():
    st.markdown("<h1 style='text-align: center;'>📋 Quản lý công việc</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_task_form", clear_on_submit=True):
            st.subheader("✨ Thêm công việc mới")
            task_name = st.text_input("📝 Tên công việc")
            task_description = st.text_area("📄 Mô tả")
            
            col_a, col_b = st.columns(2)
            with col_a:
                task_deadline = st.date_input("📅 Hạn chót")
                priority = st.selectbox("🎯 Mức độ ưu tiên", ["Thấp", "Trung bình", "Cao"])
            with col_b:
                category = st.selectbox("📁 Danh mục", ["Công việc", "Cá nhân", "Học tập", "Khác"])
                reminder = st.checkbox("⏰ Đặt nhắc nhở")
                if reminder:
                    reminder_time = st.time_input("🕒 Thời gian nhắc nhở")
            
            if st.form_submit_button("➕ Thêm công việc", use_container_width=True):
                if task_name:
                    new_task = {
                        'name': task_name,
                        'description': task_description,
                        'deadline': task_deadline.strftime('%Y-%m-%d'),
                        'priority': priority,
                        'category': category,
                        'status': 'Chưa hoàn thành',
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'reminder': reminder,
                        'reminder_time': reminder_time.strftime('%H:%M') if reminder else None,
                        'progress': 0
                    }
                    st.session_state.tasks.append(new_task)
                    save_data()
                    log_activity("Thêm công việc", f"Thêm công việc mới: {task_name}")
                    st.success("✅ Đã thêm công việc mới!")
    
    with col2:
        st.subheader("🔍 Lọc công việc")
        priority_filter = st.selectbox("Mức độ ưu tiên", ["Tất cả", "Cao", "Trung bình", "Thấp"])
    
    st.markdown("---")
    
    st.subheader("📋 Danh sách công việc")
    filtered_tasks = st.session_state.tasks
    if priority_filter != "Tất cả":
        filtered_tasks = [task for task in st.session_state.tasks if task['priority'] == priority_filter]
    
    for i, task in enumerate(filtered_tasks):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                expander = st.expander(f"📌 {task['name']} - {task['status']} ({task['priority']})")
                with expander:
                    st.write(f"📝 Mô tả: {task['description']}")
                    st.write(f"📅 Hạn chót: {task['deadline']}")
                    st.write(f"📁 Danh mục: {task['category']}")
                    st.write(f"⏰ Ngày tạo: {task['created_at']}")
                    
                    progress = st.slider("📊 Tiến độ", 0, 100, task.get('progress', 0), key=f"progress_{i}")
                    task['progress'] = progress
                    
                    deadline = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
                    if deadline < datetime.now().date() and task['status'] != 'Đã hoàn thành':
                        st.warning("⚠️ Công việc đã quá hạn!")
                    
                    if task.get('reminder') and task.get('reminder_time'):
                        current_time = datetime.now().strftime('%H:%M')
                        if current_time == task['reminder_time']:
                            st.info(f"🔔 Nhắc nhở: {task['name']}")
            
            with col2:
                if st.button("✅ Hoàn thành", key=f"complete_{i}"):
                    task['status'] = 'Đã hoàn thành'
                    task['progress'] = 100
                    save_data()
                    log_activity("Hoàn thành công việc", f"Hoàn thành công việc: {task['name']}")
                    st.rerun()
                
                if st.button("🗑️ Xóa", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    save_data()
                    log_activity("Xóa công việc", f"Xóa công việc: {task['name']}")
                    st.rerun()
            
            with col3:
                if st.button("✏️ Chỉnh sửa", key=f"edit_{i}"):
                    task['status'] = 'Đang chỉnh sửa'
                    save_data()
                    st.rerun()
                
                if st.button("⏱️ Theo dõi", key=f"track_{i}"):
                    if task['name'] not in st.session_state.task_time_tracking:
                        st.session_state.task_time_tracking[task['name']] = {
                            'start_time': datetime.now(),
                            'total_time': 0
                        }
                    else:
                        tracking = st.session_state.task_time_tracking[task['name']]
                        if 'start_time' in tracking:
                            end_time = datetime.now()
                            duration = (end_time - tracking['start_time']).total_seconds() / 60
                            tracking['total_time'] += duration
                            tracking['start_time'] = end_time
                        else:
                            tracking['start_time'] = datetime.now()
                        save_data()
                        st.success(f"⏱️ Đã ghi nhận thời gian: {tracking['total_time']:.1f} phút")

def time_management():
    st.markdown("<h1 style='text-align: center;'>⏰ Quản lý thời gian</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Lịch biểu")
        current_date = datetime.now()
        
        col_a, col_b = st.columns(2)
        with col_a:
            year = st.number_input("Năm", min_value=2000, max_value=2100, value=current_date.year)
        with col_b:
            month = st.number_input("Tháng", min_value=1, max_value=12, value=current_date.month)
        
        cal = calendar.monthcalendar(year, month)
        
        # Tạo lịch với giao diện đẹp
        st.markdown("""
        <style>
        .calendar {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .calendar th {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .calendar td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
            height: 80px;
            vertical-align: top;
        }
        .calendar td:hover {
            background-color: #f5f5f5;
        }
        .today {
            background-color: #e8f5e9;
            font-weight: bold;
        }
        .task-count {
            color: #2196F3;
            font-size: 12px;
            margin-top: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Tạo HTML cho lịch
        calendar_html = "<table class='calendar'><tr><th>CN</th><th>T2</th><th>T3</th><th>T4</th><th>T5</th><th>T6</th><th>T7</th></tr>"
        
        for week in cal:
            calendar_html += "<tr>"
            for day in week:
                if day != 0:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    tasks_for_day = [task for task in st.session_state.tasks if task['deadline'] == date_str]
                    task_count = len(tasks_for_day)
                    
                    today_class = " today" if date_str == datetime.now().strftime('%Y-%m-%d') else ""
                    task_count_html = f'<div class="task-count">{task_count} công việc</div>' if task_count > 0 else ''
                    calendar_html += f'<td class="{today_class}">{day}{task_count_html}</td>'
                else:
                    calendar_html += "<td></td>"
            calendar_html += "</tr>"
        
        calendar_html += "</table>"
        st.markdown(calendar_html, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📋 Thời gian biểu hàng ngày")
        selected_date = st.date_input("📅 Chọn ngày", datetime.now())
        date_str = selected_date.strftime('%Y-%m-%d')
        
        if date_str not in st.session_state.daily_planner:
            st.session_state.daily_planner[date_str] = []
        
        with st.form("daily_planner_form", clear_on_submit=True):
            time = st.time_input("🕒 Thời gian")
            activity = st.text_input("📝 Hoạt động")
            duration = st.number_input("⏱️ Thời lượng (phút)", min_value=1, value=30)
            
            if st.form_submit_button("➕ Thêm hoạt động", use_container_width=True):
                if activity:
                    new_activity = {
                        'time': time.strftime('%H:%M'),
                        'activity': activity,
                        'duration': duration
                    }
                    st.session_state.daily_planner[date_str].append(new_activity)
                    save_data()
                    log_activity("Thêm hoạt động", f"Thêm hoạt động: {activity} vào {date_str}")
                    st.success("✅ Đã thêm hoạt động mới!")
                    st.rerun()
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📅 Lịch trình trong ngày")
        if date_str in st.session_state.daily_planner:
            for i, activity in enumerate(sorted(st.session_state.daily_planner[date_str], key=lambda x: x['time'])):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        <div style="
                            background-color: white;
                            padding: 10px;
                            border-radius: 5px;
                            margin: 5px 0;
                            border-left: 4px solid #4CAF50;
                        ">
                            <div style="color: #4CAF50; font-weight: bold;">{activity['time']}</div>
                            <div>{activity['activity']}</div>
                            <div style="color: #666; font-size: 0.9em;">⏱️ {activity['duration']} phút</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("✏️ Chỉnh sửa", key=f"edit_activity_{i}"):
                            st.session_state.daily_planner[date_str][i]['is_editing'] = True
                            st.rerun()
                        
                        if st.button("🗑️ Xóa", key=f"delete_activity_{i}"):
                            st.session_state.daily_planner[date_str].pop(i)
                            save_data()
                            log_activity("Xóa hoạt động", f"Xóa hoạt động: {activity['activity']} vào {date_str}")
                            st.success("✅ Đã xóa hoạt động!")
                            st.rerun()
                
                # Form chỉnh sửa hoạt động
                if activity.get('is_editing'):
                    with st.form(f"edit_activity_form_{i}", clear_on_submit=True):
                        st.write("✏️ Chỉnh sửa hoạt động")
                        new_time = st.time_input("🕒 Thời gian", value=datetime.strptime(activity['time'], '%H:%M').time())
                        new_activity = st.text_input("📝 Hoạt động", value=activity['activity'])
                        new_duration = st.number_input("⏱️ Thời lượng (phút)", min_value=1, value=activity['duration'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("✅ Lưu"):
                                st.session_state.daily_planner[date_str][i].update({
                                    'time': new_time.strftime('%H:%M'),
                                    'activity': new_activity,
                                    'duration': new_duration,
                                    'is_editing': False
                                })
                                save_data()
                                log_activity("Chỉnh sửa hoạt động", f"Chỉnh sửa hoạt động: {new_activity} vào {date_str}")
                                st.success("✅ Đã cập nhật hoạt động!")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Hủy"):
                                st.session_state.daily_planner[date_str][i]['is_editing'] = False
                                st.rerun()
    
    with col4:
        st.subheader("📊 Báo cáo thời gian")
        if st.session_state.task_time_tracking:
            df = pd.DataFrame([
                {'task': task, 'time': data['total_time']}
                for task, data in st.session_state.task_time_tracking.items()
            ])
            
            fig = px.bar(df, x='task', y='time',
                        title='Thời gian dành cho mỗi công việc',
                        labels={'time': 'Thời gian (phút)', 'task': 'Công việc'},
                        color_discrete_sequence=['#4CAF50'])
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12),
                margin=dict(t=40, b=40, l=40, r=40),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

def finance_management():
    st.markdown("<h1 style='text-align: center;'>💰 Quản lý tài chính</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💳 Theo dõi thu chi")
        with st.form("transaction_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                transaction_type = st.selectbox("📊 Loại giao dịch", ["Thu", "Chi"])
                amount = st.number_input("💵 Số tiền", min_value=0)
            
            with col_b:
                category = st.selectbox("📁 Danh mục", 
                                    ["Lương", "Đầu tư", "Khác"] if transaction_type == "Thu" 
                                    else ["Ăn uống", "Di chuyển", "Mua sắm", "Hóa đơn", "Khác"])
                date = st.date_input("📅 Ngày")
            
            description = st.text_area("📝 Mô tả")
            
            if st.form_submit_button("➕ Thêm giao dịch", use_container_width=True):
                new_transaction = {
                    'type': transaction_type,
                    'amount': amount,
                    'category': category,
                    'description': description,
                    'date': date.strftime('%Y-%m-%d')
                }
                st.session_state.transactions.append(new_transaction)
                save_data()
                log_activity("Thêm giao dịch", f"Thêm giao dịch mới: {amount:,.0f} VND")
                st.success("✅ Đã thêm giao dịch mới!")
                st.rerun()
    
    with col2:
        st.subheader("💹 Quản lý ngân sách")
        current_month = datetime.now().strftime('%Y-%m')
        
        # Khởi tạo ngân sách cho tháng hiện tại nếu chưa có
        if current_month not in st.session_state.budgets:
            st.session_state.budgets[current_month] = {}
        
        # Hiển thị ngân sách hiện tại
        if st.session_state.budgets[current_month]:
            st.write("📊 Ngân sách hiện tại:")
            for category, amount in st.session_state.budgets[current_month].items():
                st.write(f"- {category}: {amount:,.0f} VND")
        
        with st.form("budget_form", clear_on_submit=True):
            category = st.selectbox("📁 Danh mục chi tiêu", 
                                ["Ăn uống", "Di chuyển", "Mua sắm", "Hóa đơn", "Khác"])
            budget_amount = st.number_input("💵 Số tiền ngân sách", min_value=0)
            
            if st.form_submit_button("➕ Thêm ngân sách", use_container_width=True):
                if budget_amount > 0:
                    st.session_state.budgets[current_month][category] = budget_amount
                    save_data()
                    log_activity("Thêm ngân sách", f"Thêm ngân sách mới: {budget_amount:,.0f} VND cho {category}")
                    st.success("✅ Đã thêm ngân sách mới!")
                    st.rerun()
                else:
                    st.error("❌ Số tiền ngân sách phải lớn hơn 0!")
    
    st.markdown("---")
    
    st.subheader("📊 Báo cáo tài chính")
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Biểu đồ thu chi theo tháng
        monthly_data = df.groupby([df['date'].dt.strftime('%Y-%m'), 'type'])['amount'].sum().unstack()
        fig = px.bar(monthly_data, 
                    title='Thu chi theo tháng',
                    labels={'value': 'Số tiền (VND)', 'date': 'Tháng'},
                    barmode='group',
                    color_discrete_map={'Thu': '#4CAF50', 'Chi': '#f44336'})
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            margin=dict(t=40, b=40, l=40, r=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tổng kết
        total_income = df[df['type'] == 'Thu']['amount'].sum()
        total_expense = df[df['type'] == 'Chi']['amount'].sum()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Tổng thu", f"{total_income:,.0f} VND", delta_color="normal")
        with col2:
            st.metric("💸 Tổng chi", f"{total_expense:,.0f} VND", delta_color="inverse")
        with col3:
            st.metric("💵 Số dư", f"{(total_income - total_expense):,.0f} VND", 
                     delta=f"{(total_income - total_expense):,.0f} VND",
                     delta_color="normal" if (total_income - total_expense) >= 0 else "inverse")
        
        # Biểu đồ phân bố chi tiêu theo danh mục
        expense_data = df[df['type'] == 'Chi'].groupby('category')['amount'].sum()
        fig = px.pie(values=expense_data.values, 
                    names=expense_data.index,
                    title='Phân bố chi tiêu theo danh mục',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            margin=dict(t=40, b=40, l=40, r=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Quản lý khoản vay
    st.subheader("💳 Quản lý khoản vay")
    with st.form("loan_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input("💵 Số tiền vay", min_value=0)
            interest_rate = st.number_input("📈 Lãi suất (%)", min_value=0.0, max_value=100.0)
        
        with col2:
            term_months = st.number_input("⏱️ Thời hạn (tháng)", min_value=1)
            start_date = st.date_input("📅 Ngày bắt đầu")
        
        if st.form_submit_button("➕ Thêm khoản vay", use_container_width=True):
            new_loan = {
                'amount': loan_amount,
                'interest_rate': interest_rate,
                'term_months': term_months,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'remaining_amount': loan_amount
            }
            st.session_state.loans.append(new_loan)
            save_data()
            log_activity("Thêm khoản vay", f"Thêm khoản vay mới: {loan_amount:,.0f} VND")
            st.success("✅ Đã thêm khoản vay mới!")
            st.rerun()

    # Hiển thị danh sách khoản vay
    if st.session_state.loans:
        for i, loan in enumerate(st.session_state.loans):
            with st.expander(f"💳 Khoản vay {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"💵 Số tiền: {loan['amount']:,.0f} VND")
                    st.write(f"📈 Lãi suất: {loan['interest_rate']}%")
                
                with col2:
                    st.write(f"⏱️ Thời hạn: {loan['term_months']} tháng")
                    st.write(f"📅 Ngày bắt đầu: {loan['start_date']}")
                    st.write(f"💰 Số tiền còn lại: {loan['remaining_amount']:,.0f} VND")
                
                if st.button("💸 Thanh toán", key=f"pay_loan_{i}"):
                    payment = st.number_input("💵 Số tiền thanh toán", min_value=0, 
                                            max_value=loan['remaining_amount'])
                    if st.button("✅ Xác nhận"):
                        loan['remaining_amount'] -= payment
                        save_data()
                        log_activity("Thanh toán khoản vay", f"Thanh toán {payment:,.0f} VND cho khoản vay {i+1}")
                        st.success("✅ Đã thanh toán thành công!")
                        st.rerun()

def log_activity(action, details):
    """Ghi lại hoạt động của người dùng"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    activity = {
        'timestamp': timestamp,
        'user': st.session_state.current_user,
        'action': action,
        'details': details
    }
    st.session_state.activity_log.append(activity)
    
    # Lưu vào file
    activity_file = f'activity_log_{st.session_state.current_user}.json'
    with open(activity_file, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.activity_log, f, ensure_ascii=False, indent=4)

def backup_data():
    """Tạo bản sao lưu dữ liệu"""
    # Tạo thư mục backups nếu chưa tồn tại
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Tạo tên file backup với timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'backup_{st.session_state.current_user}_{timestamp}.json'
    
    # Lưu dữ liệu hiện tại
    data = {
        'tasks': st.session_state.tasks,
        'notes': st.session_state.notes,
        'personal_info': st.session_state.personal_info,
        'transactions': st.session_state.transactions,
        'budgets': st.session_state.budgets,
        'loans': st.session_state.loans,
        'daily_planner': st.session_state.daily_planner,
        'task_time_tracking': st.session_state.task_time_tracking
    }
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Giữ tối đa 5 bản sao lưu
    backup_files = sorted(backup_dir.glob(f'backup_{st.session_state.current_user}_*.json'))
    if len(backup_files) > 5:
        for old_backup in backup_files[:-5]:
            old_backup.unlink()

def restore_data(backup_file):
    """Khôi phục dữ liệu từ bản sao lưu"""
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        st.session_state.tasks = data.get('tasks', [])
        st.session_state.notes = data.get('notes', [])
        st.session_state.personal_info = data.get('personal_info', {})
        st.session_state.transactions = data.get('transactions', [])
        st.session_state.budgets = data.get('budgets', {})
        st.session_state.loans = data.get('loans', [])
        st.session_state.daily_planner = data.get('daily_planner', {})
        st.session_state.task_time_tracking = data.get('task_time_tracking', {})
        
        # Lưu dữ liệu đã khôi phục
        save_data()

def main():
    if not st.session_state.is_logged_in:
        if st.session_state.show_register:
            register_page()
        else:
            login_page()
    else:
        st.markdown(f'<div class="welcome-title">Xin chào, {st.session_state.current_user}! 👋</div>', unsafe_allow_html=True)
        
        # Load dữ liệu khi khởi động
        load_data()
        
        # Menu chính
        menu = st.sidebar.selectbox(
            "Chọn chức năng",
            ["Quản lý công việc", "Quản lý thời gian", 
             "Quản lý tài chính", "Ghi chú", "Sao lưu & Khôi phục", "Thông tin cá nhân"]
        )
        
        if menu == "Quản lý công việc":
            task_management()
        
        elif menu == "Quản lý thời gian":
            time_management()
        
        elif menu == "Quản lý tài chính":
            finance_management()
        
        elif menu == "Ghi chú":
            st.header("📝 Ghi chú")
            with st.form("add_note_form", clear_on_submit=True):
                note_title = st.text_input("📌 Tiêu đề ghi chú")
                note_content = st.text_area("📄 Nội dung")
                
                if st.form_submit_button("➕ Thêm ghi chú"):
                    if note_title and note_content:
                        new_note = {
                            'title': note_title,
                            'content': note_content,
                            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        st.session_state.notes.append(new_note)
                        save_data()
                        log_activity("Thêm ghi chú", f"Thêm ghi chú mới: {note_title}")
                        st.success("✅ Đã thêm ghi chú mới!")
                        st.rerun()
            
            st.subheader("📋 Danh sách ghi chú")
            for i, note in enumerate(st.session_state.notes):
                with st.expander(f"📌 {note['title']}"):
                    st.write(note['content'])
                    st.write(f"⏰ Ngày tạo: {note['created_at']}")
                    if st.button("🗑️ Xóa", key=f"delete_note_{i}"):
                        st.session_state.notes.pop(i)
                        save_data()
                        log_activity("Xóa ghi chú", f"Xóa ghi chú: {note['title']}")
                        st.rerun()
        
        elif menu == "Sao lưu & Khôi phục":
            st.header("💾 Sao lưu & Khôi phục dữ liệu")
            
            # Tạo sao lưu
            if st.button("💾 Tạo bản sao lưu"):
                backup_data()
                log_activity("Sao lưu", "Tạo bản sao lưu dữ liệu")
                st.success("✅ Đã tạo bản sao lưu thành công!")
            
            # Khôi phục từ bản sao lưu
            st.subheader("🔄 Khôi phục dữ liệu")
            backup_dir = Path('backups')
            if backup_dir.exists():
                backup_files = list(backup_dir.glob('backup_*.json'))
                if backup_files:
                    selected_backup = st.selectbox(
                        "📁 Chọn bản sao lưu",
                        backup_files,
                        format_func=lambda x: x.stem
                    )
                    if st.button("🔄 Khôi phục"):
                        restore_data(selected_backup)
                        log_activity("Khôi phục", f"Khôi phục dữ liệu từ {selected_backup.name}")
                        st.success("✅ Đã khôi phục dữ liệu thành công!")
                        st.rerun()
                else:
                    st.info("📝 Chưa có bản sao lưu nào")
            else:
                st.info("📁 Chưa có thư mục sao lưu")
        
        elif menu == "Thông tin cá nhân":
            st.header("Thông tin cá nhân")
            if st.session_state.show_personal_info:
                with st.form("personal_info_form"):
                    name = st.text_input("Họ và tên", value=st.session_state.personal_info.get('name', ''))
                    phone = st.text_input("Số điện thoại", value=st.session_state.personal_info.get('phone', ''))
                    address = st.text_area("Địa chỉ", value=st.session_state.personal_info.get('address', ''))
                    
                    if st.form_submit_button("Lưu thông tin"):
                        st.session_state.personal_info = {
                            'name': name,
                            'phone': phone,
                            'address': address
                        }
                        save_data()
                        log_activity("Cập nhật thông tin", "Cập nhật thông tin cá nhân")
                        st.success("✅ Đã lưu thông tin thành công!")
                        st.session_state.show_personal_info = False
                        st.rerun()
            else:
                st.write(f"👤 Họ và tên: {st.session_state.personal_info.get('name', '')}")
                st.write(f"📱 Số điện thoại: {st.session_state.personal_info.get('phone', '')}")
                st.write(f"📍 Địa chỉ: {st.session_state.personal_info.get('address', '')}")
                if st.button("✏️ Chỉnh sửa thông tin"):
                    st.session_state.show_personal_info = True
                    st.rerun()
        
        # Nút đăng xuất
        if st.sidebar.button("🚪 Đăng xuất"):
            st.session_state.is_logged_in = False
            st.session_state.current_user = None
            log_activity("Đăng xuất", "Người dùng đăng xuất")
            st.rerun()

if __name__ == "__main__":
    main()