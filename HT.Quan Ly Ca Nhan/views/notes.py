import streamlit as st
from datetime import datetime
from models.note import Note

def notes_page():
    st.title("📝 Ghi chú")
    
    # Khởi tạo dữ liệu nếu chưa có
    if not hasattr(st.session_state.current_user, 'notes'):
        st.session_state.current_user.notes = []
    
    # Tab điều hướng
    tab1, tab2, tab3 = st.tabs(["📋 Danh sách ghi chú", "🔍 Tìm kiếm", "📊 Thống kê"])
    
    with tab1:
        # Form thêm ghi chú mới
        with st.expander("➕ Thêm ghi chú mới", expanded=True):
            with st.form("add_note_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Tiêu đề", placeholder="Nhập tiêu đề ghi chú")
                    category = st.text_input("Danh mục", placeholder="Nhập danh mục")
                with col2:
                    tags = st.text_input("Thẻ (cách nhau bằng dấu phẩy)", placeholder="Ví dụ: công việc, học tập")
                
                content = st.text_area("Nội dung", placeholder="Nhập nội dung ghi chú", height=200)
                
                submit_button = st.form_submit_button("Thêm ghi chú", use_container_width=True)
                
                if submit_button:
                    if title and content:
                        try:
                            # Tách các thẻ
                            tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
                            
                            new_note = Note(
                                title=title,
                                content=content,
                                category=category,
                                tags=tag_list
                            )
                            
                            st.session_state.current_user.notes.append(new_note.to_dict())
                            st.success("✅ Đã thêm ghi chú mới!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Lỗi khi thêm ghi chú: {str(e)}")
                    else:
                        st.error("❌ Vui lòng điền tiêu đề và nội dung!")
        
        # Hiển thị danh sách ghi chú
        if st.session_state.current_user.notes:
            # Sắp xếp ghi chú theo thời gian cập nhật mới nhất
            notes = sorted(
                [Note.from_dict(n) for n in st.session_state.current_user.notes],
                key=lambda x: x.updated_at,
                reverse=True
            )
            
            # Hiển thị từng ghi chú
            for i, note in enumerate(notes):
                with st.expander(f"📝 {note.title} - {note.updated_at.strftime('%d/%m/%Y %H:%M')}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"**Danh mục:** {note.category if note.category else 'Không có'}")
                        st.write(f"**Thẻ:** {', '.join(note.tags) if note.tags else 'Không có'}")
                        st.write(f"**Tạo lúc:** {note.created_at.strftime('%d/%m/%Y %H:%M')}")
                    with col2:
                        st.write("**Nội dung:**")
                        st.write(note.content)
                    
                    # Nút chỉnh sửa và xóa
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Chỉnh sửa", key=f"edit_{i}", use_container_width=True):
                            with st.form(f"edit_note_form_{i}"):
                                edited_title = st.text_input("Tiêu đề", value=note.title)
                                edited_content = st.text_area("Nội dung", value=note.content, height=200)
                                edited_category = st.text_input("Danh mục", value=note.category)
                                edited_tags = st.text_input("Thẻ", value=", ".join(note.tags))
                                
                                if st.form_submit_button("Lưu thay đổi", use_container_width=True):
                                    try:
                                        # Tách các thẻ
                                        tag_list = [tag.strip() for tag in edited_tags.split(",")] if edited_tags else []
                                        
                                        note.update(
                                            title=edited_title,
                                            content=edited_content,
                                            category=edited_category,
                                            tags=tag_list
                                        )
                                        st.session_state.current_user.notes[i] = note.to_dict()
                                        st.success("✅ Đã cập nhật ghi chú!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Lỗi khi cập nhật ghi chú: {str(e)}")
                    with col2:
                        if st.button("🗑️ Xóa", key=f"delete_{i}", use_container_width=True):
                            st.session_state.current_user.notes.pop(i)
                            st.success("✅ Đã xóa ghi chú!")
                            st.rerun()
        else:
            st.info("📝 Chưa có ghi chú nào!")
    
    with tab2:
        st.subheader("🔍 Tìm kiếm ghi chú")
        
        # Ô tìm kiếm
        search_query = st.text_input("Nhập từ khóa tìm kiếm", placeholder="Tìm kiếm theo tiêu đề, nội dung, danh mục hoặc thẻ")
        
        if search_query:
            # Tìm kiếm trong tiêu đề, nội dung, danh mục và thẻ
            search_results = []
            for note_data in st.session_state.current_user.notes:
                note = Note.from_dict(note_data)
                if (search_query.lower() in note.title.lower() or
                    search_query.lower() in note.content.lower() or
                    (note.category and search_query.lower() in note.category.lower()) or
                    any(search_query.lower() in tag.lower() for tag in note.tags)):
                    search_results.append(note)
            
            if search_results:
                st.write(f"Tìm thấy {len(search_results)} kết quả:")
                for note in search_results:
                    with st.expander(f"📝 {note.title} - {note.updated_at.strftime('%d/%m/%Y %H:%M')}"):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.write(f"**Danh mục:** {note.category if note.category else 'Không có'}")
                            st.write(f"**Thẻ:** {', '.join(note.tags) if note.tags else 'Không có'}")
                        with col2:
                            st.write("**Nội dung:**")
                            st.write(note.content)
            else:
                st.info("Không tìm thấy kết quả nào!")
    
    with tab3:
        st.subheader("📊 Thống kê ghi chú")
        
        if st.session_state.current_user.notes:
            # Thống kê số lượng ghi chú theo danh mục
            category_stats = {}
            tag_stats = {}
            total_notes = len(st.session_state.current_user.notes)
            
            for note_data in st.session_state.current_user.notes:
                note = Note.from_dict(note_data)
                category = note.category if note.category else "Không có danh mục"
                category_stats[category] = category_stats.get(category, 0) + 1
                
                for tag in note.tags:
                    tag_stats[tag] = tag_stats.get(tag, 0) + 1
            
            # Hiển thị thống kê
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Thống kê theo danh mục:**")
                for category, count in category_stats.items():
                    st.write(f"- {category}: {count} ghi chú")
            
            with col2:
                st.write("**Thống kê theo thẻ:**")
                for tag, count in tag_stats.items():
                    st.write(f"- {tag}: {count} ghi chú")
            
            st.write(f"**Tổng số ghi chú:** {total_notes}")
        else:
            st.info("Chưa có ghi chú nào để thống kê!") 