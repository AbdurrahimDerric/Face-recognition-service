from flask import render_template,url_for,request,escape,flash,redirect,abort,Flask
# from flask_cors import CORS, cross_origin
import base64
import pickle
import face_recognition
import cv2


app = Flask(__name__)
data = []
with open("dataset.pickle", "rb") as reader:
    data = pickle.load(reader)


@app.route('/api',methods = ["GET","POST","OPTIONS"])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def api():
    if request.method == "GET":
       print("get entered")
    elif request.method == "POST":
        image_data = request.form.get("content").split(",")[1]
        label_name = request.form.get("label")

        # image recieved here is 64base image, can change according to application
        image = base64.b64decode(image_data)
        name = recognize_face(image, data)
        print("reco ", name)
        print("name" ,name)
        with open("blog_user.png","wb") as f:
            f.write()
    return "ok"




def recognize_face(image,data):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("[INFO] recognizing faces...")


    #model can be set to "cnn" which is slower but more accurtate
    boxes = face_recognition.face_locations(rgb,model="hog")
    print(boxes)
    print("faces detected")

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    #compare this face encodings with the encoding of the labeled dataset
    for encoding in encodings:
      matches = face_recognition.compare_faces(data["encodings"],encoding)
      name = "unknown"
      if True in matches:
        matchedIdxs = [i for (i,b) in enumerate(matches) if b]
        counts = {}
        for i in matchedIdxs:
          name = data["names"][i]
          counts[name] = counts.get(name,0) + 1
        name = max(counts, key = counts.get)

      names.append(name)
      return names[0]

img= cv2.imread("darrige_pp.png")

print(recognize_face(img,data))