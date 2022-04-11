# RestAPI
User authentication
pip install -r requirements.txt
python manage.py runserver

1. --------------Register Api url & parameter ------------- 
2. url  - https://letsgoapi.herokuapp.com/register/
3. parameter - 
 {
  "first_name":"",
  "last_name":"",
  "username":"",
  "email":"",
  "phone":"",
  "address":"",
  "password":""
}

---------------Login Api url & parameter ------------
url - https://letsgoapi.herokuapp.com
parameter - 
{
  "username":"001vijay",
  "password":"vijay@123"
}

------------------Logout Api----------------
url  - https://letsgoapi.herokuapp.com/logout/

-------------Forgot password api url & parameter -------------
url - https://letsgoapi.herokuapp.com/forgot-password/
{
"username":""
}

--------------Reset password api url & parameter -----------------
url - https://letsgoapi.herokuapp.com/reset-password/

{
"otp":"",
"new_password":"",
"confirm_password":""
}
