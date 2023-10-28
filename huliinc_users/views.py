import json

import django.db.utils
from django.core import serializers as srs, serializers
from django.contrib.auth import get_user_model

# Create your views here.

from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from huliinc_users.models import CustomUserSerializer, CustomUserViewSerializer, CustomUser


class UserApiView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer = CustomUserSerializer()

    def get(self, request):
        user = get_user_model()
        data = [CustomUserViewSerializer(x).data for x in user.objects.all()]
        return HttpResponse(data,
                            status=200, content_type="application/json")

    def post(self, request):
        result = self.serializer.validate(request.data)
        if result:
            User = get_user_model()
            try:

                User.objects.create_user(email=result['email'], password=result['password'],
                                         user_information=result['user_information'])
            except django.db.utils.IntegrityError:
                return HttpResponse("User with this email already exists", status=409)
        return HttpResponse(status=200)

    def patch(self, request):
        User = get_user_model()
        result = self.serializer.validate(request.data)
        try:
            user = User.objects.get(email=result['email'])
            if 'password' in result:
                if not user.check_password(result['password']):
                    user.set_password(result['password'])
            if 'user_information' in result:
                user.user_information = result['user_information']
            # User.objects.update(user)
            user.save()
            return HttpResponse(status=200)
        except User.DoesNotExist as e:
            return HttpResponse('No such email in DB', status=404)


class MeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            "email": request.user.email,
            "is_verified": request.user.is_verified
        }
        return HttpResponse(json.dumps(data), status=200)


class RegisterApiView(APIView):
    def post(self, request):
        email_to_auth = request.query_params['email']
        User = get_user_model()
        try:
            user_to_verify = User.objects.get(email=email_to_auth)
            user_to_verify.is_verified = True
            user_to_verify.save()
            return HttpResponse(status=200)
        except User.DoesNotExist:
            return HttpResponse("No such email in DB", status=404)
