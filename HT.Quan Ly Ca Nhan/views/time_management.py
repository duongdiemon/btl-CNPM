import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import calendar
from models.event import Event

def time_management_page():
    st.title("⏰ Quản lý thời gian")
    
    # Khởi tạo danh sách sự kiện nếu chưa có
    if not hasattr(st.session_state.current_user, 'events'):
        st.session_state.current_user.events = []
    
    # Tab điều hướng
    tab1, tab2, tab3 = st.tabs(["📅 Lịch biểu", "📝 Thời gian biểu", "⏱️ Theo dõi thời gian"])
    
    with tab1:
        st.subheader("📅 Lịch biểu")
        
        # Hiển thị lịch tháng 5 năm 2025
        st.markdown("""
            <div style='text-align: center; font-size: 24px; margin-bottom: 20px;'>
                Tháng 5 năm 2025
            </div>
        """, unsafe_allow_html=True)
        
        # Header của lịch
        st.markdown("""
            <div style='display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: bold; margin-bottom: 10px;'>
                <div>T2</div>
                <div>T3</div>
                <div>T4</div>
                <div>T5</div>
                <div>T6</div>
                <div>T7</div>
                <div>CN</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Các ngày trong tháng
        st.markdown("""
            <div style='display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; gap: 10px;'>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>1</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>2</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>3</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>4</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>5</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>6</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>7</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>8</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>9</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>10</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>11</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>12</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>13</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>14</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>15</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>16</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>17</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>18</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>19</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>20</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>21</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>22</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>23</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>24</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>25</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>26</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>27</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>28</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>29</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>30</div>
                <div style='padding: 10px; background-color: #f0f0f0; border-radius: 5px;'>31</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Form thêm sự kiện mới
        with st.expander("➕ Thêm sự kiện mới", expanded=True):
            with st.form("add_event_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Tiêu đề")
                    event_type = st.selectbox(
                        "Loại sự kiện",
                        ["Sự kiện", "Cuộc hẹn", "Hoạt động"]
                    )
                with col2:
                    date = st.date_input("Ngày", value=datetime.now().date())
                    start_time = st.time_input("Thời gian bắt đầu", value=datetime.now().time())
                    end_time = st.time_input("Thời gian kết thúc", value=(datetime.now() + timedelta(hours=1)).time())
                
                description = st.text_area("Mô tả")
                
                submit_button = st.form_submit_button("Thêm")
                
                if submit_button:
                    if title and start_time < end_time:
                        start_datetime = datetime.combine(date, start_time)
                        end_datetime = datetime.combine(date, end_time)
                        new_event = Event(
                            title=title,
                            description=description,
                            start_time=start_datetime,
                            end_time=end_datetime,
                            event_type=event_type
                        )
                        st.session_state.current_user.events.append(new_event.to_dict())
                        st.success("✅ Đã thêm sự kiện mới!")
                        st.rerun()
                    else:
                        st.error("Vui lòng điền đầy đủ thông tin và kiểm tra thời gian!")
        
        # Hiển thị lịch và sự kiện
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Hiển thị lịch tháng
            now = datetime.now()
            cal = calendar.monthcalendar(now.year, now.month)
            
            st.subheader(f"{calendar.month_name[now.month]} {now.year}")
            
            # Hiển thị tên các ngày trong tuần
            week_days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
            st.write(" ".join(week_days))
            
            # Hiển thị các ngày trong tháng
            for week in cal:
                week_str = []
                for day in week:
                    if day == 0:
                        week_str.append("  ")
                    else:
                        week_str.append(f"{day:2d}")
                st.write(" ".join(week_str))
        
        with col2:
            # Hiển thị sự kiện
            events = [Event.from_dict(e) for e in st.session_state.current_user.events]
            
            # Lọc sự kiện theo ngày
            selected_date = st.date_input("Chọn ngày", value=now.date())
            day_events = [e for e in events if e.start_time.date() == selected_date]
            
            if day_events:
                for event in day_events:
                    with st.expander(f"🕒 {event.start_time.strftime('%H:%M')} - {event.title}"):
                        st.write(f"**Loại:** {event.event_type}")
                        st.write(f"**Thời gian:** {event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}")
                        st.write(f"**Mô tả:** {event.description}")
                        
                        # Nút chỉnh sửa và xóa
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✏️ Chỉnh sửa", key=f"edit_{event.title}"):
                                # TODO: Thêm chức năng chỉnh sửa
                                pass
                        with col2:
                            if st.button("🗑️ Xóa", key=f"delete_{event.title}"):
                                st.session_state.current_user.events.remove(event.to_dict())
                                st.success("✅ Đã xóa sự kiện!")
                                st.rerun()
            else:
                st.info("📝 Không có sự kiện nào trong ngày này!")
    
    with tab2:
        st.subheader("📝 Thời gian biểu hàng ngày")
        
        # Hiển thị thời gian biểu cho ngày hôm nay
        today = datetime.now().date()
        today_events = [e for e in events if e.is_today()]
        
        if today_events:
            # Sắp xếp sự kiện theo thời gian
            today_events.sort(key=lambda x: x.start_time)
            
            # Tạo timeline
            for event in today_events:
                st.write(f"🕒 **{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}**")
                st.write(f"**{event.title}** ({event.event_type})")
                st.write(f"*{event.description}*")
                st.write("---")
        else:
            st.info("📝 Chưa có hoạt động nào cho hôm nay!")
        
        # Form thêm hoạt động mới
        with st.expander("➕ Thêm hoạt động mới", expanded=True):
            with st.form("add_activity_form", clear_on_submit=True):
                title = st.text_input("Tiêu đề hoạt động")
                description = st.text_area("Mô tả")
                time = st.time_input("Thời gian", value=datetime.now().time())
                
                submit_button = st.form_submit_button("Thêm")
                
                if submit_button:
                    if title:
                        new_event = Event(
                            title=title,
                            description=description,
                            start_time=datetime.combine(today, time),
                            end_time=datetime.combine(today, time) + timedelta(hours=1),
                            event_type="Hoạt động"
                        )
                        st.session_state.current_user.events.append(new_event.to_dict())
                        st.success("✅ Đã thêm hoạt động mới!")
                        st.rerun()
    
    with tab3:
        st.subheader("⏱️ Theo dõi thời gian")
        
        # Hiển thị thống kê thời gian
        if events:
            # Tạo DataFrame từ danh sách sự kiện
            df = pd.DataFrame([e.to_dict() for e in events])
            
            # Tính tổng thời gian cho mỗi loại hoạt động
            time_stats = df.groupby('event_type')['time_spent'].sum().reset_index()
            
            # Hiển thị biểu đồ
            st.bar_chart(time_stats, x='event_type', y='time_spent')
            
            # Hiển thị danh sách hoạt động
            st.subheader("Danh sách hoạt động")
            for event in events:
                if event.time_spent is not None:
                    with st.expander(f"⏱️ {event.title} - {event.time_spent} phút"):
                        st.write(f"**Loại:** {event.event_type}")
                        st.write(f"**Thời gian:** {event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}")
                        st.write(f"**Mô tả:** {event.description}")
                        
                        # Form cập nhật thời gian thực tế
                        with st.form(f"update_time_{event.title}"):
                            new_time = st.number_input(
                                "Thời gian thực tế (phút)",
                                min_value=0,
                                value=event.time_spent or event.get_duration()
                            )
                            submit_button = st.form_submit_button("Cập nhật")
                            if submit_button:
                                event.time_spent = new_time
                                st.session_state.current_user.events = [e.to_dict() for e in events]
                                st.success("✅ Đã cập nhật thời gian!")
                                st.rerun()
        else:
            st.info("📝 Chưa có hoạt động nào được theo dõi!") 