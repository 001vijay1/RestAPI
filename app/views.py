
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from app.models import *
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
import random


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        context = {}
        data=request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        password = data.get('password')
        if first_name != '' and last_name != '' and username != '' and email != '' and phone != '' and address != '' and password != '':
            user = User.objects.filter(username=username)
            if len(user) == 0:
                u = User.objects.create_user(username,email,password)
                u.first_name = first_name
                u.last_name = last_name
                u.save()
                adrs = UserAddress(phone_number=phone,address=address)
                adrs.user_id = u.id
                adrs.save()
                context['status'] = status.HTTP_200_OK
                context['message'] = "User created successfully."
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "User already exists"
            return Response(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "field can not be blank"
            return Response(context)

class LoginView(APIView):
    def post(self, request):
        context = {}
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username and password:
            usr = authenticate(request,username=username,password=password)
            if usr is not None:
                login(request,usr)
                u = User.objects.get(username=username)
                data = {'name':f'{u.first_name} {u.last_name}','username':u.username}
                try:
                    u_adrs = UserAddress.objects.get(user=u.id)
                    data['phone'] = u_adrs.phone_number
                    data['address'] = u_adrs.address
                except:
                    data['phone'] = ''
                    data['address'] = ''
                context['status'] = status.HTTP_200_OK
                context['user'] = data
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "Authentication Error, Please try again."
            return Response(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "Username or password can not be blank"
            return Response(context)

class ForgotPasswordView(APIView):
    def post(self,request):
        context = {}
        data = request.data
        if data.get('username') != '':
            user = User.objects.filter(username=data.get('username'))
            if len(user) > 0:
                otp = random.randint(0000,9999)
                try:
                    user_verification = UserVerification(user=data.get('username'))
                    user_verification.otp = otp
                    user_verification.save()
                except:
                    user_verification = UserVerification(user=data.get('username'),otp=otp)
                    user_verification.save()
                context['status'] = status.HTTP_200_OK
                context['otp'] = otp
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "User does not exist."
            return Response(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "username can not be blank"
            return Response(context)

class ResetPasswordView(APIView):
    def post(self,request):
        context = {}
        data = request.data
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if new_password != confirm_password:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "Password does not match."
            return Response(context)
            
        if new_password != '' and confirm_password != '' and otp != '':
            try:
                verify_otp = UserVerification.objects.get(otp=otp)
                u = User.objects.get(username=verify_otp.user)
                u.set_password(confirm_password)
                u.save()
                verify_otp.otp = 0
                verify_otp.save()
                context['status'] = status.HTTP_200_OK
                context['message'] = "Password changed successfully"
            except:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "OTP does not match."
            return Response(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "field can not be blank"
            return Response(context)



class LogoutView(APIView):
    def get(self,request):
        context = {}
        logout(request)
        context['status'] = status.HTTP_200_OK
        context['message'] = "User logged successfully."
        return Response(context)

  