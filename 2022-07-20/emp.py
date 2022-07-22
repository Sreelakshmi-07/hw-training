from datetime import datetime, date
import json


class Login():

    def employee(self, emp_name, emp_id):

        self.task_list = []

        self.emp_name = emp_name
        self.emp_id = emp_id
        start = datetime.now()
        self.log_in = start.strftime("%Y-%m-%d %H:%M")

    def add_task(self, task_title, task_description):

        self.task_title = task_title
        self.task_description = task_description
        start = datetime.now()
        self.start_now = start.strftime("%Y-%m-%d %H:%M")


    def end_task(self, task_success):

        self.task_success = task_success
        end = datetime.now()
        self.end_now = end.strftime("%Y-%m-%d %H:%M")

        self.task_list.append(
            {
                "task_title": self.task_title,
                "task_description": self.task_description,
                "start_time": self.start_now,
                "end_time": self.end_now,
                "task_success": self.task_success,
            },
        )

    def logout(self):

        end = datetime.now()
        log_out = end.strftime("%Y-%m-%d %H:%M")
        emp_info = {
            "emp_name": self.emp_name,
            "emp_id": self.emp_id,
            "login_time": self.log_in,
            "logout_time": log_out,
            "tasks": self.task_list
        }

        filename = f"{self.emp_name}_{str(date.today())}.json"
        with open(filename, "w")as f:
            f.write(json.dumps(emp_info, indent=4))


emp = Login()
emp.employee("emp", 101)
emp.add_task("good reads", "scrape")
emp.end_task(True)
emp.add_task("amazon reads", "scrape")
emp.end_task(True)
emp.logout()
