import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facial-recognition-b6693-default-rtdb.firebaseio.com/",
                                    'storageBucket':"facial-recognition-b6693.appspot.com"
                                    })

#importing the data images
folderPath='images1'
PathList=os.listdir(folderPath)
print(PathList)
imgList=[]
peopleIds=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))

    #print(path)
    #print(os.path.splitext(path)[0])
    peopleIds.append(os.path.splitext( path)[0])
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)



print(peopleIds)


def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print('encoding started....')
encodeListKnown=findEncodings(imgList)
print(encodeListKnown)
encodeListKnownWithIds=[encodeListKnown,peopleIds]
print('encoding complete')
file=open("EncodingFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("file saved")
