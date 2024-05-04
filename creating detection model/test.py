import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from keras.models import load_model
import cv2
import numpy as np

test_data_paths = ['test_data_1', 'test_data_2']
image_size = 224

correct_predictions = 0
total_predictions = 0

label_lst = ['A','Aa','Ah','Ai','Am','Au','Ba','Bha','Ca','Cha','D_a','D_ha','Da','Dha','E','E_','Ee','Ee_','Ga','Gha','Ha','I','Ii','Ilh','Ill','In','Inh','Irr','Ja','Ka','Kha','La','Lha','Ma','N_a','Na','Nga','Nha','Nothing','O','Oo','Pa','Pha','R','Ra','Rha','Sa','Sha','Shha','Space','T_a','T_ha','Ta','Tha','U','U_','Uu','Uu_','Va','Ya','Zha']
NUM_CLASSES = len(label_lst)
REV_CLASS_MAP = {i:label_lst[i] for i in range(NUM_CLASSES)}

def mapper(val):
    return REV_CLASS_MAP[val]

model = load_model("train_data_combined_acc_54.keras")

for IMG_TEST_PATH in test_data_paths:
    for directory in os.listdir(IMG_TEST_PATH):
        path = os.path.join(IMG_TEST_PATH,directory)
        if not os.path.isdir(path):
            continue
        
        for file_name in os.listdir(path):
            # to make sure no hidden files get in our way
            if file_name.startswith("."):
                continue
            # to make sure only jpg is extracted
            if not file_name.endswith(".jpg"):
                continue

            image_path = os.path.join(path,file_name)
            # prepare the image
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (image_size, image_size))

            # predict the sign made
            pred = model.predict(np.array([img]))
            sign_code = np.argmax(pred[0])
            sign_name = mapper(sign_code)

            # Extract the ground truth label from the directory name
            ground_truth = directory

            # Compare predicted label with ground truth label
            if sign_name == ground_truth:
                correct_predictions += 1

            total_predictions += 1

            print(f"Predicted: {sign_name} for image {image_path}")

accuracy = correct_predictions / total_predictions
print(f"\n\nAccuracy: {accuracy * 100:.2f}%")
