import requests
import os

KERAS_REST_API_URL = "https://x-ray-api.herokuapp.com/api/v1/classify"

imagePath = os.path.join(os.getcwd(), "X_Ray_App/uploads/x_ray_images")

for image_name in os.listdir(imagePath):
    IMAGE_PATH = os.path.join(imagePath, image_name) # image path
    image = open(IMAGE_PATH, "rb").read()
    r_person = requests.post(KERAS_REST_API_URL, files={"image": image})
    response_data = r_person.json()
    result = response_data["result"]
    print("Prediction for Image file '{0}': {1}".format(image_name, result))
