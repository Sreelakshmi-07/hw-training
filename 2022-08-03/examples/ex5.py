import os 
import ftplib
 

cwd = os.getcwd() 
print("Current working directory:", cwd) 

note = "hello word"
filename = f"note.text"
with open(filename,'w') as f:
	f.write(note)

file= open(filename, "r")
print('File Content:', file.read())