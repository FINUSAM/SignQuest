import os
import shutil

def merge_datasets(source1, source2, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    folders_source1 = [folder for folder in os.listdir(source1) if os.path.isdir(os.path.join(source1, folder))]
    folders_source2 = [folder for folder in os.listdir(source2) if os.path.isdir(os.path.join(source2, folder))]
    common_folders = set(folders_source1).intersection(folders_source2)

    for folder in common_folders:
        source_folder1 = os.path.join(source1, folder)
        source_folder2 = os.path.join(source2, folder)
        destination_folder = os.path.join(destination, folder)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        filenames_source1 = [filename for filename in os.listdir(source_folder1) if filename.endswith(".jpg")]
        filenames_source2 = [filename for filename in os.listdir(source_folder2) if filename.endswith(".jpg")]

        for filename in filenames_source1:
            source_path = os.path.join(source_folder1, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.copy(source_path, destination_path)

        for filename in filenames_source2:
            source_path = os.path.join(source_folder2, filename)
            destination_path = os.path.join(destination_folder, filename)
            base, extension = os.path.splitext(filename)
            if os.path.exists(destination_path):
                i = 1
                while os.path.exists(destination_path):
                    new_name = f"{i + 10}{extension}"  # Increment by 200
                    destination_path = os.path.join(destination_folder, new_name)
                    i += 1
            shutil.copy(source_path, destination_path)
            
# Example usage:
dataset1_path = r"C:\Users\fahee\Desktop\Programming\College Final Year Project\MSL Detection Model\test_data_1"
dataset2_path = r"C:\Users\fahee\Desktop\Programming\College Final Year Project\MSL Detection Model\test_data_2"
merged_dataset_path = r"C:\Users\fahee\Desktop\Programming\College Final Year Project\MSL Detection Model\test_data_combined"

merge_datasets(dataset1_path, dataset2_path, merged_dataset_path)
