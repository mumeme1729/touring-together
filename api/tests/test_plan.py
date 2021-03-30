from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from ..models import Plan,Prefectures
from ..serializers import PlanSerializer,SearchPlanSerializer

CREATE_NEW_PLAN = 'http://127.0.0.1:8000/api/plan/'

def create_prefecture(name):
    return Prefectures.objects.create(name=name)

def create_plan(user,id):
    prefecture=Prefectures.objects.get(id=id)
    defaults={
        'title':'test',
        'destination':'test',
        'prefecture':prefecture,
        'departure':'test',
        'date':'2021-03-23',
        'text':'test'
    }
    

    return Plan.objects.create(userPlan=user,**defaults)

class AuthorizedPlanApiTest(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(email='dummy@test.com',password='dummy')
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_1_create_new_plan(self):
        prefecture=create_prefecture('長野').id
        payload={
            'title':'test',
            'destination':'test',
            'prefecture':prefecture,
            'departure':'test',
            'date':'2021-03-23',
            'text':'test',
        }
        res=self.client.post(CREATE_NEW_PLAN,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_2_get_all_plan(self):
        pref1=create_prefecture('長野').id
        pref2=create_prefecture('東京').id
        create_plan(user=self.user,id=pref1)
        create_plan(user=self.user,id=pref2)

        res=self.client.get(CREATE_NEW_PLAN)
        plans=Plan.objects.all()
        serializer=PlanSerializer(plans,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    