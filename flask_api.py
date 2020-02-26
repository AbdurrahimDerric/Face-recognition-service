from flask import render_template,url_for,request,escape,flash,redirect,abort,Flask
import base64
import pickle
import face_recognition
import cv2
import werkzeug


app = Flask(__name__)
data = []
with open("dataset.pickle", "rb") as reader:
    data = pickle.load(reader)


@app.route('/api_web',methods = ["GET","POST","OPTIONS"])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def api_web():
    if request.method == "GET":
       print("get entered")
    elif request.method == "POST":
        image_data = request.form.get("content").split(",")[1]
        label_name = request.form.get("label")

        # image recieved here is 64base image, can change according to application
        image = base64.b64decode(image_data)
        name = recognize_face(image, data)

        with open("client_image.png","wb") as f:
            f.write()
    return name



@app.route('/api_mobile', methods = ['GET', 'POST'])
def api_mobile():
    imagefile = request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)

    #check image type here before recognzing
    name = recognize_face(imagefile, data)

    #save to disk
    imagefile.save("client_image.png")

    return name




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

app.run(host="0.0.0.0", port=5000, debug=True)