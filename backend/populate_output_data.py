import os
import pix2pix
import yolov8_auto_annotate


# returns 0 for not annotated, 1 for annotated data
def check_input_folder_type():
    directories_to_check = ["test", "train", "valid"]

    root = "user_data/"
    t = 0
    for dir in directories_to_check:
        if (
            dir in os.listdir(root)
            and "images" in os.listdir(root + dir + "/")
            and "labels" in os.listdir(root + dir + "/")
        ):
            t = 1
            print(f"The directory {dir} exists")

    return t


# try catch to not crash if input folder isn't right format


def populate():
    # 0 for not annotated, 1 for annotated
    t = check_input_folder_type()
    if t == 1:  # if is annotated, run pix2pix directly and populate output_data
        pix2pix.get_image(
            "user_data/test/", "pix2pix_data/output_data/test/"
        )  # if empty, will create
        pix2pix.get_image("user_data/train/", "pix2pix_data/output_data/train/")
        pix2pix.get_image("user_data/valid/", "pix2pix_data/output_data/valid/")
    else:  # means is not annotated, but also don't know if its just files, could contain random stuff if user is stupid
        # then, try run yolo autodetect on all images in user_data, output into yolo_data
        yolov8_auto_annotate.get_yolo_auto_bounds("user_data/", "yolo_data/")
        # run pix2pix on yolo_data to populate output_data
        pix2pix.get_image(
            "yolo_data/test/", "pix2pix_data/output_data/test/"
        )  # if empty, will create
        pix2pix.get_image("yolo_data/train/", "pix2pix_data/output_data/train/")
        pix2pix.get_image("yolo_data/valid/", "pix2pix_data/output_data/valid/")
