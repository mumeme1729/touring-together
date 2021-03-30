from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = 'http://127.0.0.1:8000/api/register/'
CRETE_PROFILE_URL = 'http://127.0.0.1:8000/api/profile/'
MY_PROFILE_URL    = 'http://127.0.0.1:8000/api/myprofile/'
TOKEN_USRL        = 'http://127.0.0.1:8000/authen/jwt/create'

class AuthorizedUserApiTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(email='dummy@test.com',password='dummy')
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_1_create_user_profile(self):
        payload={
            'nickName':'test',
            'text':'dummy',  
            'base':'test',
        }
        res=self.client.post(CRETE_PROFILE_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(res.data['userProfile'],self.user.id)
        self.assertEqual(res.data['nickName'],'test')
        self.assertEqual(res.data['text'],'dummy')
        self.assertEqual(res.data['base'],'test')
    
    def test_1_2_create_user_profile(self):
        payload={
            'nickName':'',
            'text':'',  
            'base':'',
        }
        res=self.client.post(CRETE_PROFILE_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(res.data['userProfile'],self.user.id)
        

class UnauthorizedUserApiTests(TestCase):
    def setUp(self):
        self.client=APIClient()
    
    def test_2_create_new_user(self):
        payload={
            'email':'dummy@test.com',
            'password':'dummy',
        }
        res=self.client.post(REGISTER_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user=get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password',res.data)

    def test_3_create_new_user_by_ssame_email(self):
        payload={
            'email':'dummy@test.com',
            'password':'dummy',
        }
        get_user_model().objects.create_user(**payload)
        res=self.client.post(REGISTER_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_4_not_response_token_with_non_exist_user(self):
        payload={
            'email':'dummy@test.com',
            'password':'dummy',
        }
        res=self.client.post(TOKEN_USRL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

    
    def test_4_1_not_response_token_with_non_exist_user(self):
        payload={
            'email':'dummy@test.com',
            'password':'',
        }
        res=self.client.post(TOKEN_USRL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_5_not_get_profile_when_unauthorized(self):
        res=self.client.get(MY_PROFILE_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)





    

        
