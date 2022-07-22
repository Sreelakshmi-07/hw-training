from datetime import datetime
import json
​
​
class Login(object):
    def employee(self, emp_name, emp_id):
        self.emp_name = emp_name
        self.emp_id = emp_id
​
    def login(self):
​
        start = datetime.now()
        return start.strftime("%Y-%m-%d %H:%M")
​
    def logout(self):
        end = datetime.now()
        return end.strftime("%Y-%m-%d %H:%M")
​
    def add_task(self, task_title, task_description, task_success):
        self.task_title = task_title
        self.task_description = task_description
        self.task_success = task_success
        start = datetime.now()
        self.start_now = start.strftime("%Y-%m-%d %H:%M")
​
    def end_task(self):
        end = datetime.now()
        end_now = end.strftime("%Y-%m-%d %H:%M")
        emp_info = {
        "emp_name": self.emp_name,
        "emp_id" : self.emp_id,
        "start_time" : Login.login(self),
        "end_time" : Login.logout(self),
        "tasks": [
            {
                "task_title": self.task_title,
                "task_description": self.task_description,
                "start_time": self.start_now,
                "end_time": end_now,
                "task_success": self.task_success,
            }
        ]
        }
        filename = f"{self.emp_name}_{str(Login.login(self))}.json"
        with open(filename,"w")as f:
            f.write(json.dumps(emp_info,indent=4))
​
​
emp = Login()
emp.employee("emp", 101)
emp.add_task("amazon", "scrape", "true")
emp.end_task()