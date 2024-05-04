print('importing libraries.....')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from keras.models import load_model
import numpy as np
import cv2
from PIL import Image 
print('libraries imported successfully')

image_size = 224
model = load_model("keras_model.keras")

def mapper(val):
    label_lst = ['A','Aa','Ah','Ai','Am','Au','Ba','Bha','Ca','Cha','D_a','D_ha','Da','Dha','E','E_','Ee','Ee_','Ga','Gha','Ha','I','Ii','Ilh','Ill','In','Inh','Irr','Ja','Ka','Kha','La','Lha','Ma','N_a','Na','Nga','Nha','Nothing','O','Oo','Pa','Pha','R','Ra','Rha','Sa','Sha','Shha','Space','T_a','T_ha','Ta','Tha','U','U_','Uu','Uu_','Va','Ya','Zha']
    NUM_CLASSES = len(label_lst)
    REV_CLASS_MAP = {i:label_lst[i] for i in range(NUM_CLASSES)}
    return REV_CLASS_MAP[val]

def preprocess(image):
    img = cv2.imread(image)#np.array(image)#
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (image_size, image_size))
    return img

def predict(image):
    image = preprocess(image)
    pred = model.predict(np.array([image]))
    sign_code = np.argmax(pred[0])
    sign_name = mapper(sign_code)
    return sign_name

filenames = ["predict_input_image.jpg", "predict_input_image2.jpg", "predict_input_image3.jpg"]

for filename in filenames:
    prediction = predict(filename)
    print('prediction is ', prediction)