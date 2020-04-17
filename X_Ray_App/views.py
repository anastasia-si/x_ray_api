import json
import numpy as np
from .apps import XRayAppConfig
from .models import XRay
from .serializers.xray import XRaySerializer
from django.http import HttpResponse
from keras.preprocessing.image import img_to_array
from PIL import Image
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

class XRayPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class XRayListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list
    """
    serializer_class = XRaySerializer
    queryset = XRay.objects.all()
    pagination_class = XRayPagination

class XRayCreateAPIView(CreateAPIView):
    serializer_class = XRaySerializer


class XRayDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete x-ray instance
    """
    serializer_class = XRaySerializer
    queryset = XRay.objects.all()
    lookup_field = 'id'


class NetworkModelView(APIView):
    serializer_class = XRaySerializer

    #def get(self, request): #, request, pk
    #    return HttpResponse(json.dumps({"message": "Hello, world!"}))

    def post(self, request):
        if request.method == 'POST':
            result = {"success": False}
            if request.FILES["image"]:
                try:
                    xray_image = Image.open(request.FILES['image'])
                    #image = request.FILES["image"].read()
                    #image = Image.open(io.BytesIO(image))
                    xray_image = self.prepare_image(xray_image, (64, 64))
                    prediction = XRayAppConfig.cnn_model.predict(xray_image)[0][0]
                    prediction_label = XRayAppConfig.LABEL_MAP[prediction]
                    result['prediction'] = str(prediction)
                    result['prediction_label'] = prediction_label
                    result["success"] = True
                except:
                    pass

                return  HttpResponse(json.dumps({"result": result}), content_type="application/json") #JsonResponse(response)

    # resize the input image and preprocess it
    def prepare_image(self, img, target):
        if img.mode != "RGB":
            img = img.convert("RGB")

        img = img.resize(target)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)

        return img