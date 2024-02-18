from roboflow import Roboflow

rf = Roboflow(api_key="wHK5CIgjpIWIGFyTQKl6")
project = rf.workspace("oleksandr-tara").project("military-vehicle-detection-juleg")
dataset = project.version(7).download("yolov8")
