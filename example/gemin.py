
# AIzaSyCusOKyWzNtDaAKFyUxB4BJJOnwJLN0KSk


import google.generativeai as genai
import PIL.Image
import os

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

genai.configure(api_key="AIzaSyCusOKyWzNtDaAKFyUxB4BJJOnwJLN0KSk")

# img = PIL.Image.open('path/to/image.png')

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(["What is in this the meaning of life in 1 sentance?"])
print(response.text)