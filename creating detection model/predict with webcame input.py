import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
import numpy as np
import cv2

image_size = 224
model = load_model("retrained_model_AAaE_only_with_early_stopping.keras")

def mapper(val):
    label_lst = ['A','Aa','E']#'Ah','Ai','Am','Au','Ba','Bha','Ca','Cha','D_a','D_ha','Da','Dha','E','E_','Ee','Ee_','Ga','Gha','Ha','I','Ii','Ilh','Ill','In','Inh','Irr','Ja','Ka','Kha','La','Lha','Ma','N_a','Na','Nga','Nha','Nothing','O','Oo','Pa','Pha','R','Ra','Rha','Sa','Sha','Shha','Space','T_a','T_ha','Ta','Tha','U','U_','Uu','Uu_','Va','Ya','Zha']
    NUM_CLASSES = len(label_lst)
    REV_CLASS_MAP = {i:label_lst[i] for i in range(NUM_CLASSES)}
    return REV_CLASS_MAP[val]

def preprocess(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (image_size, image_size))
    return img

def predict(image):
    image = preprocess(image)
    pred = model.predict(np.array([image]))
    sign_code = np.argmax(pred[0])
    sign_name = mapper(sign_code)
    return sign_name

# Access webcam
cap = cv2.VideoCapture(0)

# Variables for FPS control
fps = 1  # Number of frames per second
prev_time = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Calculate time elapsed
    current_time = cv2.getTickCount()
    time_elapsed = (current_time - prev_time) / cv2.getTickFrequency()

    # Process frame if FPS condition met
    if time_elapsed > 1.0 / fps:
        # Reset previous time
        prev_time = current_time

        # Prediction
        prediction = predict(frame)
        print('Prediction:', prediction)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
