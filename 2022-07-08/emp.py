from datetime import datetime
import json

class Login():
	"""docstring for login"""
	def employee(self,emp_name,emp_id):
		self.emp_name = emp_name
		self.emp_id = emp_id
		start = datetime.now()
		start_now = start.strftime("%Y/%m/%d, %H:%M")


class Task(Login):

	def tasks(self,task_title,task_description):

		global task
		self.task_title = task_title 
		self.task_description = task_description
		task = []
		task.append(task_title)

	def task_state(self,task_success):

		self.task_success = task_success

	def logout(self):
		
		sol = ["emp_name",self.emp_name,"emp_id",self.emp_id,"start_now",start_now,"end_now",end_now,"tasks",task]
		res_dct = {sol[i]: sol[i + 1] for i in range(0, len(sol), 2)}
		print(res_dct)
		out_file = open("exm.json", "w")
		json.dump(res_dct, out_file, indent = 6)
		out_file.close()

	def save(self):

		task_info=["task_title",self.task_title,"task_description",self.task_description,"start_now",start_now,"end_now",end_now,"task_success",self.task_success]
		info_dct = {task_info[i]: task_info[i + 1] for i in range(0, len(task_info), 2)}
		print(info_dct)
		out_files = open("task_save.json", "w")
		json.dump(info_dct, out_files, indent = 6)
		out_files.close()


result = Task()
end = datetime.now()
end_now = end.strftime("%Y-%m-%d %H:%M")
start = datetime.now()
start_now = start.strftime("%Y-%m-%d %H:%M")
while True:
	print("***** \n 1.Login \n 2.Task \n 3.Task Success \n 4.Save \n 5.Logout \n ****")
	operation = input("Enter operation:")
	if operation == str(5):
		break
	else:
		if operation == str(1):
			result.employee(input("Enter name:"),input("Enter id:"))
		elif operation == str(2):
			result.tasks(input("Task title:"),input("Task descripition:"))
		elif operation == str(3):
			result.task_state(input("Enter True or False:"))
		elif operation == str(4):
			result.logout()
			result.save()
		else:
			print("error")

	
		