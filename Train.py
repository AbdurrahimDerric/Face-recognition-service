# from imutils import paths
import face_recognition
import pickle
import cv2
import os


# grab the paths to the input images in our dataset
# Dataset here is a folder with subfolders conatining image pics with person belongs to this subfolder name
paths = []
cats = [f.path for f in os.scandir("Dataset/") if f.is_dir() ]

# cats = [p.split("/")[-1] for p in cats]
print(cats)
for cat in cats:
  image_paths = [f.path for f in os.scandir(cat)]
  for ip in image_paths:
    paths.append(ip)
print(paths)
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(paths):
	  # extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,len(paths)))
	name = imagePath.split(os.path.sep)[-2]
	# load the input image and convert it from BGR (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb, model="cnn")
	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)
	# loop over the encodings
	for encoding in encodings:  #more than one face
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("dataset.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
