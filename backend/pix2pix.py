import PIL
import shutil
import os
import torch
from diffusers import (
    StableDiffusionInstructPix2PixPipeline,
    EulerAncestralDiscreteScheduler,
)


def get_image(input_path, output_path):
    model_id = "timbrooks/instruct-pix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16, safety_checker=None
    )
    pipe.to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    prompts = {
        "snow": (
            "What would it look like if there were heavy snow?",
            "s",
        ),
        "rain": ("What would it look like if it were rainy with visible rain?", "r"),
        "foggy": ("What would it look like if it there were fog?", "f"),
        "dusty": (
            "What would it look like if there was a lot of dust in the air?",
            "d",
        ),
    }
    input_path_img = os.path.join(input_path, "images")
    input_path_label = os.path.join(input_path, "labels")
    output_path_img = os.path.join(output_path, "images")
    output_path_label = os.path.join(output_path, "labels")
    for filename in os.listdir(input_path_img):
        # Get the full path of the file
        filepath = os.path.join(input_path_img, filename)
        # Check if the filepath is a file (not a directory)
        if os.path.isfile(filepath):
            image = PIL.Image.open(filepath)
            image = PIL.ImageOps.exif_transpose(image)
            image = image.convert("RGB")

            for key in prompts.keys():
                p = prompts[key][0]
                id = prompts[key][1]
                # snow good
                if id == "s" or id == "r":
                    images = pipe(
                        p,
                        image=image,
                        num_inference_steps=50,
                        image_guidance_scale=1,
                    ).images
                else:
                    images = pipe(
                        p,
                        image=image,
                        num_inference_steps=150,
                        image_guidance_scale=0.8,
                    ).images
                if not (os.path.exists(output_path_img)):
                    os.makedirs(output_path_img)
                ending = ""
                if ".jpg" in filename:
                    ending = ".jpg"
                if ".jpeg" in filename:
                    ending = ".jpeg"
                if ".png" in filename:
                    ending = ".png"
                save_path_img = os.path.join(
                    output_path_img,
                    str(filename.split(ending)[0]) + "_" + id + ending,
                )
                input_path_l = os.path.join(
                    input_path_label,
                    str(filename.split(ending)[0]) + ".txt",
                )
                save_path_label = os.path.join(
                    output_path_label,
                    str(filename.split(ending)[0]) + "_" + id + ".txt",
                )
                # save images
                image.save(os.path.join(output_path_img, filename))
                images[0].save(save_path_img)
                # save labels
                if not (os.path.exists(output_path_label)):
                    os.makedirs(output_path_label)
                shutil.copy(input_path_l, save_path_label)
