import requests

url = "http://www.africau.edu/images/default/sample.pdf"
r = requests.get(url, allow_redirects=True, stream = True)

#save downloaded file
with open("python.pdf","wb") as pdf:
     for chunk in r.iter_content(chunk_size=1024):
         # writing one chunk at a time to pdf file
         if chunk:
              pdf.write(chunk)
# import requests

# url = "http://www.africau.edu/images/default/sample.pdf"

# file_name = "file1.pdf"
# def download_pdf(url, file_name):

#     # Send GET request
#     response = requests.get(url)

#     # Save the PDF
#     if response.status_code == 200:
#         with open(file_name, "wb") as f:
#             f.write(response.content)
#     else:
#         print(response.status_code)


#     # Download image
# download_pdf(url, file_name)