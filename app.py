from flask import Flask, render_template, request
from PIL import Image, ImageFont, ImageDraw

import cv2
import cv2.cv as cv

import numpy as np

import cStringIO
import base64

app = Flask(__name__)
app.debug = True

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/image", methods=['POST'])
def image():
	st = request.form['image']
	st = st[st.find("base64,") + 7:]
	image_string = cStringIO.StringIO(base64.b64decode(st))
	image = Image.open(image_string)

	dr = ImageDraw.Draw(image)
	npImage = np.array(image)

	faces = cascade.detectMultiScale(npImage, 1.3, 5)
	(x, y, w, h) = faces[0]
	dr.rectangle(((x, y, x+w, y+h)), outline="blue")

	image.save("face.jpg")
	return "Hello"

if __name__ == "__main__":
	app.run()