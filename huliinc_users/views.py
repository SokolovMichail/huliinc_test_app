import json

from django.contrib.auth import get_user_model

# Create your views here.

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from huliinc_users.models import CustomUserSerializer


class UserApiView(APIView):
    #permission_classes = (IsAuthenticated,)
    serializer = CustomUserSerializer()

    def get(self,request):
        user = get_user_model()
        data = user.objects.all()
        return HttpResponse(data,status=200)

    def post(self,request):
        result = self.serializer.validate(request.data)
        if result:
            User = get_user_model()
            User.objects.create_user(email=result['email'], password=result['password'])
        return HttpResponse(status=200)

    def patch(self,request):
        return HttpResponse(status=200)

class MeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            "email": request.user.email,
            "is_verified": request.user.is_verified
        }
        return HttpResponse(json.dumps(data), status=200)