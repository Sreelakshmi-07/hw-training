from datetime import datetime,date
import json
​
​
class Login(object):
​
    def employee(self, emp_name, emp_id):
        self.emp_name = emp_name
        self.emp_id = emp_id
        start = datetime.now()
        self.log_in=start.strftime("%Y-%m-%d %H:%M")
​
    def add_task(self, task_title, task_description):
        self.task_title = task_title
        self.task_description = task_description
        start = datetime.now()
        self.start_now = start.strftime("%Y-%m-%d %H:%M")
​
    def task_examine(self,task_success):
​
        self.task_success = task_success
        end = datetime.now()
        self.end_now = end.strftime("%Y-%m-%d %H:%M")
​
    def end_task(self):
​
        global tasks
        tasks = [] 
        tasks.append(
            {
            "task_title": self.task_title,
            "task_description": self.task_description,
            "start_time": self.start_now,
            "end_time": self.end_now,
            "task_success": self.task_success,
            },
        )
        print(tasks)   
​
    def logout(self):
        end = datetime.now()
        log_out = end.strftime("%Y-%m-%d %H:%M")
        emp_info = {
        "emp_name": self.emp_name,
        "emp_id" : self.emp_id,
        "login_time" : self.log_in,
        "logout_time" : log_out,
        "tasks": tasks
        }
​
        filename = f"{self.emp_name}_{str(date.today())}.json"
        with open(filename,"w")as f:
            f.write(json.dumps(emp_info,indent=4))
​
emp = Login()
emp.employee("emp", 101)
emp.add_task("goo reads", "scrape")
emp.task_examine("true")
emp.end_task()
emp.add_task("good reads", "scrape")
emp.task_examine("true")
emp.end_task()
emp.logout()