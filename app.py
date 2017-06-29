import os
from flask import *
import mlab
from mongoengine import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
mlab.connect()

#lấy đường dẫn
app.config["IMG_PATH"] = os.path.join(app.root_path, "images")

image="http://cdn.playbuzz.com/cdn/5d41f0c6-2688-47fe-85cf-82890ef6d91d/45611be8-42f9-4d02-9b63-f7195c0dc18c_560_420.jpg"
title="Red rose"
price=10000

#design db
class Flower(Document): #khai bao kieu cua bien
    image= StringField()
    title= StringField()
    price= FloatField()

flower1= Flower(
    image="https://upload.wikimedia.org/wikipedia/commons/6/60/Single_lavendar_flower02.jpg",
    title= "Lavender",
    price= 50000
)

#dumb data
#flower1.save()
flowers=[
    {
        "image":"http://cdn.playbuzz.com/cdn/5d41f0c6-2688-47fe-85cf-82890ef6d91d/45611be8-42f9-4d02-9b63-f7195c0dc18c_560_420.jpg",
        "title":"Red Rose",
        "price":10000
    },
    {
        "image":"https://upload.wikimedia.org/wikipedia/commons/4/44/Tulip_-_floriade_canberra.jpg",
        "title":"Tulip",
        "price":20000
    },
    {
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/60/Single_lavendar_flower02.jpg",
        "title": "Laveder",
        "price": 50000
    }
]
@app.route('/')
def index():
    return render_template("index.html",
                           flowers = Flower.objects())
@app.route('/images/<image_name>')
def image(image_name):
    return send_from_directory(app.config["IMG_PATH"],image_name)

@app.route('/add_flower', methods=["GET","POST"])
def add_flower():
    if request.method=="GET": #FORM REQUEST:
        return render_template("add_flower.html")
    elif request.method=="POST":
        #1: GET DATA (PRICE, IMAGE, TITLE)
        form = request.form
        title=form["title"]
        #image = form["image"]
        price = form["price"]
        image = request.files["image"]
        filename=secure_filename(image.filename) #tu import secure filename
        print(os.path.join(app.config["IMG_PATH"], filename))
        image.save(os.path.join(app.config["IMG_PATH"], filename))
        #2: SAVE DATA INTO DB
        new_flower= Flower(title=title,
                           image="/images/{0}".format(filename),
                           price=price)
        new_flower.save()

        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()