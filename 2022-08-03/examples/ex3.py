import ast  
import datetime
import time

expression = '13 + 4'  
code = ast.parse(expression, mode='eval')  
print(code)
print(ast.dump(code))  
now = datetime.datetime.now()
print("today",now)
current_time = time.time()
print(current_time)
