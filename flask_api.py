from flask import render_template,url_for,request,escape,flash,redirect,abort,Flask
import base64
import pickle
from recognition import recognize_face
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


# the add_encoding api, with simple database procedcure
def add_encoding_api():
    if request.method == "GET":
       return "no pic"
    elif request.method == "POST":
        image_data = request.form.get("content").split(",")[1]
        name = request.form.get("label")

        this_user = User.query.filter_by(username=name).first()
        counter = this_user.login_pic_number + 1

        image_path = "flasky/Dataset/" + name + "/" + name + "_" +counter.__str__() + ".png"
        with open(image_path,"wb") as f:
            f.write(base64.b64decode(image_data))

        global data
        data = add_encoding(image_path,name)
        # write_counter(folder_path,counter)
        this_user.login_pic_number = counter
        db.session.commit()
        return "pic saved"
    return "done"



    
img= cv2.imread("darrige_pp.png")
print(recognize_face(img,data))

app.run(host="0.0.0.0", port=5000, debug=True)
