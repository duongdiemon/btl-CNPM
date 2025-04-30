import streamlit as st
from models.task import Task

class TaskController:
    def __init__(self):
        self.current_user = st.session_state.current_user

    def create_task(self, title, description, due_date, priority):
        """Tạo công việc mới"""
        task = Task(title, description, due_date, priority)
        self.current_user.tasks.append(task)
        return True, "Tạo công việc thành công"

    def update_task(self, task_id, title, description, due_date, priority):
        """Cập nhật công việc"""
        if 0 <= task_id < len(self.current_user.tasks):
            task = self.current_user.tasks[task_id]
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = priority
            return True, "Cập nhật công việc thành công"
        return False, "Không tìm thấy công việc"

    def delete_task(self, task_id):
        """Xóa công việc"""
        if 0 <= task_id < len(self.current_user.tasks):
            del self.current_user.tasks[task_id]
            return True, "Xóa công việc thành công"
        return False, "Không tìm thấy công việc"

    def get_all_tasks(self):
        """Lấy danh sách công việc"""
        return self.current_user.tasks 