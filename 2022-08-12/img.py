import requests
import shutil

img_url = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg"
filename = img_url.split("/")[-1]
r = requests.get(img_url,stream = True)
if r.status_code == 200:
	r.raw.decode_content = True
	with open(filename,'wb') as f:
		shutil.copyfileobj(r.raw,f)
	print("successful")
else:
	print("error")