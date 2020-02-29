from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate, APITestCase
from .models import Homes
import json
from uuid import uuid4

class Homes_Tests(APITestCase):

    url = '/api/homes/'

    def test_Post(self):

        home_T = {
            'adress': "Никольская улица, д 15",
            'number_bricks': 2000000,
            'year': 1988
            }

        response = self.client.post(self.url, home_T, format = 'json')
        self.assertEqual(201, response.status_code)

    def test_Get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class Home_Tests(APITestCase):

    url = '/api/home/'

    def setUp(self):

        self.adress = "Сиреневый бульвар, д 21"
        self.number_bricks = 3000000
        self.year = 1920

        self.Home_1, created = Homes.objects.get_or_create(
            adress = self.adress,
            number_bricks = self.number_bricks,
            year = self.year
        )


    def test_Get_One(self):
        print(self.Home_1.uuid)
        uuid_T = self.Home_1.uuid
        response = self.client.get(self.url + f'{uuid_T}')
        self.assertEqual(200, response.status_code)


    def test_Patch(self):

        self.Home_1, created = Homes.objects.get_or_create(
            adress = self.adress,
            number_bricks = self.number_bricks,
            room_id = self.room_id
        )

        uuid_T = self.Home_1.uuid

        home_P = {
            'adress' : self.adress,
            'number_bricks' : 2000010,
            'year' : self.year
        }

        response = self.client.patch(self.url + f'{uuid_T}', data = home_P, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_Delete(self):

        uuid_T = self.Home_1.uuid
        response = self.client.delete(self.url + f'{uuid_T}')
        self.assertEqual(204, response.status_code)
