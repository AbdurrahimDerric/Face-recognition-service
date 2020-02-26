## Face Recognition Service


#### 1-Introduction:
A face recognition service for a remote trained model on server side, with a client posting an image containing a face picture needed to be recognized. The client receives a response with the name of the person In the picture.

#### 2-Requirements:
Following Python libraries are used in implementation the project:
-	Opencv, used in reading and writing images form/to storage.
-	face_recognition, used in detecting faces, encoding them and test comparsions.
-	Flask, used to implement the service.

#### 3- The Model:
The trained model that resides at the server side are created as follows:
*	 the labeled faces image dataset is read using OpenCV.
*	 using face_recognition library faces are detected using HOG algorithm 	(Singh, 2019). 
*	 the detected faces are then converted to a 128d embedding vector using the Facenet algorithm (Schroff, 2015), read 5. for further reading.
*	 these encodings are saved along with names of its people to the disk.

	
 
#### 4- Logic:

##### 4.1- client side:
The service doesn’t interfere with the logic in the client side as much as with the context it receives the image from the client.
For a web application sending an AJAX post to the service API designated for web apps, flask code here checks the request method POST, and receives the image content.	


##### 4.2- Server side:
when a post request is received at the specified address, the image is received and then converted to an RGB image. To recognize the face in this image:
*	 first we detect the face in the image using HOG algorithm , then we get the encodings of that face using FaceNet. 
*	 Hereby we have a 128d vector for the face in this picture. We compare this vector with every labeled vector we already have in our Model using Euclidean distance.
*	 by setting a threshold – default 1.1- for distances between vectors, we set True for the images that has a distance less than the threshold.
*	 for the classification purpose we use simple KNN to set this unknown face identity, simply getting the max number of True’s of each labels.
*	 we accept that the label- person name- with the higher number belongs to this received picture.
		
		
		
#### 5. Further reading on FaceNet:
“the method is based on learning a Euclidean embedding per image using a deep convolutional network. The network is trained such that the squared L2 distances in the embedding space directly correspond to face similarity: faces of the same person have small distances and faces of distinct people have large distances.”
##### This is done in two steps,
1 - getting embeddings of the face image through the deep convolutional network,
 



![Image description](https://miro.medium.com/max/1024/1*OmFw4wZx5Rx3w4TpB7hS-g.png) 




2 - Tuning the triplet loss so that the face pictures of the same person has similar vectors and those of different persons has a larger distance- more different vector.


![Image description](https://miro.medium.com/max/651/1*hWBNCVbG-ngJ2aAiqg4Nzw.png) 

For more details check the paper (Schroff, 2015).
 
### References: 
*	Schroff, F. (2015). FaceNet: A Unified Embedding for Face Recognition and Clustering.
*	Singh, A. (2019). Feature Engineering for Images: A Valuable Introduction to the HOG Feature Descriptor. Retrieved from https://www.analyticsvidhya.com/blog/2019/09/feature-engineering-images-introduction-hog-feature-descriptor/.

