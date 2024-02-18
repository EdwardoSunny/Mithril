# given a directory of images (uploaded by user), perform detections, convert into yolov8 training format

import os
import shutil
import random
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def reorg_train_test_valid(path):
    train_path = os.path.join(path, "train")
    test_path = os.path.join(path, "test")
    valid_path = os.path.join(path, "valid")
    for dataset_path in [train_path, test_path, valid_path]:
        images_dir = os.path.join(dataset_path, "images")
        labels_dir = os.path.join(dataset_path, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for root, _, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    shutil.move(
                        os.path.join(root, file), os.path.join(images_dir, file)
                    )
                else:
                    shutil.move(
                        os.path.join(root, file), os.path.join(labels_dir, file)
                    )


def split_data(
    images_dir, labels_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15
):
    # Create output directories
    train_dir = os.path.join(output_dir, "train")
    val_dir = os.path.join(output_dir, "valid")
    test_dir = os.path.join(output_dir, "test")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Get list of image files
    image_files = [f for f in os.listdir(images_dir)]

    # Shuffle the list
    random.shuffle(image_files)

    # Calculate split sizes
    num_images = len(image_files)
    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    num_test = num_images - num_train - num_val

    # Split the lists
    train_files = image_files[:num_train]
    val_files = image_files[num_train : num_train + num_val]
    test_files = image_files[num_train + num_val :]

    # Move files to output directories
    for files, output in [
        (train_files, train_dir),
        (val_files, val_dir),
        (test_files, test_dir),
    ]:
        for file in files:
            image_path = os.path.join(images_dir, file)
            label_path = os.path.join(labels_dir, os.path.splitext(file)[0] + ".txt")
            shutil.copy(image_path, output)
            shutil.copy(label_path, output)


def copy_files(source_dir, destination_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Get list of files in source directory
    files = os.listdir(source_dir)

    # Copy each file to the destination directory
    for file in files:
        source_file_path = os.path.join(source_dir, file)
        destination_file_path = os.path.join(destination_dir, file)
        shutil.copy(source_file_path, destination_file_path)


# gets bounding boxes automatically for a dataset with unlabelled data, creates splits and stores in yolo_data
def get_yolo_auto_bounds(data_dir, output_dir):
    clean_up_for_next_batch()
    output_dir_labels = os.path.join(output_dir, "labels")
    if not os.path.exists(output_dir_labels):
        os.makedirs(output_dir_labels)
    image_files = [
        f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))
    ]

    for image_file in image_files:
        image_path = os.path.join(data_dir, image_file)
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        detections = model(image_path, save=True)
        ending = ""
        if ".jpg" in image_file:
            ending = ".jpg"
        if ".jpeg" in image_file:
            ending = ".jpeg"
        if ".png" in image_file:
            ending = ".png"
        with open(
            os.path.join(output_dir_labels, image_file.split(ending)[0] + ".txt"), "w"
        ) as f:
            for detection in range(len(detections[0].boxes)):
                label_idx = int(detections[0].boxes.cls[detection])
                x_center, y_center, bbox_width, bbox_height = detections[0].boxes.xywh[
                    detection
                ]

                x_top_left = (x_center - bbox_width / 2) / width
                y_top_left = (y_center - bbox_height / 2) / height
                norm_width = bbox_width / width
                norm_height = bbox_height / height

                f.write(
                    f"{label_idx} {x_top_left}, {y_top_left}, {norm_width}, {norm_height}\n"
                )

    if os.path.exists("yolo_data/runs"):
        shutil.rmtree("yolo_data/runs")
    shutil.move("runs/", "pix2pix_data/output_data")
    # at this point, bounding box images are stored at yolo_data/runs/detect/predict/
    # labels will be at yolo_data/labels
    os.makedirs("yolo_data/images")
    copy_files("user_data/", "yolo_data/images")
    os.makedirs("yolo_data_temp/")
    split_data("yolo_data/images", "yolo_data/labels", "yolo_data_temp/")
    shutil.rmtree("yolo_data/")
    os.rename("yolo_data_temp/", "yolo_data/")
    reorg_train_test_valid("yolo_data/")


# removes everything for next batch
def clean_up_for_next_batch():
    if os.path.exists("yolo_data/"):
        shutil.rmtree("yolo_data/")
    os.makedirs("yolo_data/")
