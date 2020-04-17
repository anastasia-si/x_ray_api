import os

from django.urls import reverse

from ..serializers.xray import XRaySerializer
from django.conf import settings
from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from rest_framework.views import status
from X_Ray_App.models import XRay

CREATE_URL = reverse('xray:create-xray')
LIST_URL = reverse('xray:list-xray')
CLASSIFY_URL = reverse('xray:classify-xray')


class XRayListTestCase(APITestCase):
    """ Test module for GET all x-ray images API """

    def setUp(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg')
        with open(photo_path, 'rb') as photo_data:
            self.example_1 = XRay.objects.create(image=ImageFile(photo_data))
            self.example_2 = XRay.objects.create(image=ImageFile(photo_data))

    def tearDown(self):
        # remove created test images
        os.remove(self.example_1.image.path)
        os.remove(self.example_2.image.path)

    def test_list_xrays(self):
        xrays_count = XRay.objects.count()
        response = self.client.get(LIST_URL)#('/api/v1/xrays/')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], xrays_count)
        self.assertEqual(len(response.data['results']), xrays_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class XRayGetTestCase(APITestCase):
    """ Test module for GET single x-ray API """

    def setUp(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg')
        with open(photo_path, 'rb') as photo_data:
            self.example_1 = XRay.objects.create(image=ImageFile(photo_data))
            self.example_2 = XRay.objects.create(image=ImageFile(photo_data))

    def tearDown(self):
        # remove created test images
        os.remove(self.example_1.image.path)
        os.remove(self.example_2.image.path)

    def test_get_valid_single_xray(self):
        xray_id = self.example_1.pk
        response = self.client.get(reverse('xray:detail-xray',args=(xray_id,))) #('/api/v1/xrays/{}/'.format(xray_id))
        xray = XRay.objects.get(pk=xray_id)
        serializer = XRaySerializer(xray)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_invalid_single_xray(self):
        response = self.client.get(reverse('xray:detail-xray',args=(777,))) #('/api/v1/xrays/{}/'.format(777))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class XRayCreateTestCase(APITestCase):
    """ Test module for creating a new x-ray record """

    def setUp(self) -> None:
        pass

    def test_create_xray(self):
        initial_count = XRay.objects.count()

        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg')  # os.path.join(settings.MEDIA_ROOT, 'products', 'vitamin-iron.jpg')
        with open(photo_path, 'rb') as photo_data:
            response = self.client.post(CREATE_URL, {'image': photo_data}, format='multipart') #('/api/v1/xrays/new', {'image': photo_data}, format='multipart')

        self.assertEqual(
           response.status_code,
           status.HTTP_201_CREATED)

        self.assertEqual(
            XRay.objects.count(),
            initial_count + 1,
        )

        try:
            created = XRay.objects.first() #XRay.objects.get(id=response.data['pk'])
            expected_photo = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image')
            self.assertTrue(created.image.path.startswith(expected_photo))
        finally:
            os.remove(created.image.path)

class XRayUpdateTestCase(APITestCase):
    """ Test module for updating an existing x-ray record """

    def setUp(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg')
        with open(photo_path, 'rb') as photo_data:
            self.example_1 = XRay.objects.create(image=ImageFile(photo_data))

    def tearDown(self):
        # remove created test images
        os.remove(self.example_1.image.path)

    def test_update_xray_photo(self):
        xray = XRay.objects.first()
        original_photo = xray.image
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg') #os.path.join(settings.MEDIA_ROOT, 'products', 'pic.jpg')
        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch(reverse('xray:detail-xray',args=(xray.id,)), { #('/api/v1/xrays/{}/'.format(xray.id), {
                'image': photo_data,
            }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['image'], original_photo)
        try:
            updated = XRay.objects.get(id=xray.id)
            expected_photo = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image')
            self.assertTrue(updated.image.path.startswith(expected_photo))
        finally:
            os.remove(updated.image.path)



class XRayDestroyTestCase(APITestCase):
    """ Test module for deleting an existing x-ray record """

    def setUp(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images', 'test_image.jpg')
        with open(photo_path, 'rb') as photo_data:
            self.example_1 = XRay.objects.create(image=ImageFile(photo_data))

    def tearDown(self):
        # remove created test images
        os.remove(self.example_1.image.path)

    def test_delete_valid_xray(self):

        initial_count = XRay.objects.count()
        xray_id = XRay.objects.first().id
        response = self.client.delete(reverse('xray:detail-xray',args=(xray_id,))) #('/api/v1/xrays/{}/'.format(xray_id))
        self.assertEqual(
            XRay.objects.count(),
            initial_count - 1,
        )
        self.assertRaises(
            XRay.DoesNotExist,
            XRay.objects.get, id=xray_id,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_xray(self):
        response = self.client.delete(reverse('xray:detail-xray',args=(777,))) #('/api/v1/xrays/{}/'.format(777))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class XRayClassifyTestCase(APITestCase):
    """ Test module for classifying x-ray record """

    def test_classify(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'x_ray_images',
                                  'norm_test.jpeg')
        with open(photo_path, 'rb') as photo_data:
            response = self.client.post(CLASSIFY_URL, {'image': photo_data}, format='multipart') #('/api/v1/classify', {'image': photo_data}, format='multipart')


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK)

        response = response.json()
        expected_response = {'success': True, 'prediction': '0.0', 'prediction_label': 'No pneumonia'}

        self.assertEqual(
            response['result'],
            expected_response)