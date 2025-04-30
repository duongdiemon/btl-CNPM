import streamlit as st
from models.note import Note

class NoteController:
    def __init__(self):
        self.current_user = st.session_state.current_user

    def create_note(self, title, content, tags):
        """Tạo ghi chú mới"""
        note = Note(title, content, tags)
        self.current_user.notes.append(note)
        return True, "Tạo ghi chú thành công"

    def update_note(self, note_id, title, content, tags):
        """Cập nhật ghi chú"""
        if 0 <= note_id < len(self.current_user.notes):
            note = self.current_user.notes[note_id]
            note.title = title
            note.content = content
            note.tags = tags
            return True, "Cập nhật ghi chú thành công"
        return False, "Không tìm thấy ghi chú"

    def delete_note(self, note_id):
        """Xóa ghi chú"""
        if 0 <= note_id < len(self.current_user.notes):
            del self.current_user.notes[note_id]
            return True, "Xóa ghi chú thành công"
        return False, "Không tìm thấy ghi chú"

    def get_all_notes(self):
        """Lấy danh sách ghi chú"""
        return self.current_user.notes

    def search_notes(self, query):
        """Tìm kiếm ghi chú"""
        return [note for note in self.current_user.notes 
                if query.lower() in note.title.lower() 
                or query.lower() in note.content.lower()] 