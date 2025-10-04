from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
import re , json
from .models import Todolist
from django.utils import timezone
from ToDoApp.function import validate_email , validate_pass, validate_username, firstAndLastName, LastName



def signupview(request):
    if request.method == 'POST':
        
        if not request.body.strip():
            return JsonResponse({"Error": "Enter The User Informations"}, status= 400)
        
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        
        if  username and  password and email and first_name:
                if  User.objects.filter(username=username).exists():
                    return JsonResponse({"Error" : "Username already exist, try another username"} , status = 409)
                
                
                elif not validate_pass(password):
                    return JsonResponse({"Error" : "Password is manadtory and Password must contain atleast a Uppercase, a lowercase , a special charcter and a number and minimum length must be 6"}, status= 400) 
                elif not validate_username(username):
                    return JsonResponse({"Error": "User name is mandatory and User must contain only lowercase characters"}, status= 400) 
                elif not validate_email(email):
                    return JsonResponse({"Error": "Email is manadtory and Enter a valid Email"}, status = 400)
                elif not firstAndLastName(first_name):
                    return JsonResponse({"Error": "First name is manadtory and First name must contain only alphabetical"}, status = 400)
                elif not LastName(last_name):
                    return JsonResponse({"Error":"Last name must contain only alphabetical"}, status = 400)
                else:
                    user= User.objects.create_user(
                        username = username,
                        password = password,
                        email = email,
                        first_name = first_name,
                        last_name = last_name
                    )
                    user.save()
                    return JsonResponse({"message" :"User Registerd Successfully",
                                        "username": username,
                                        "email" : email,
                                        "first name": first_name,
                                        "last name" :last_name
                                            }, status = 201)    
                    
        else:
                return JsonResponse({"Error": "Enter all required field"}, status=400)
    else :
       
        return JsonResponse({"error" :"method not allowed"}, status = 405)
    
    
    
    

def loginview(request):
    if request.method == 'POST':
        if  not request.body.strip():
                return JsonResponse({"Error": "Enter The Username and password"}, status= 400)
            
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
         
        if not username or not password:
                return JsonResponse({"Error": "username and password both manadtory"}, status=400)
        
        user = authenticate(request=request, username=username, password=password)
       
        if user is not None :
            login(request, user)
            return JsonResponse({"message": "User logged in successfully" }, status = 200)
        else:
            return JsonResponse({"message": "User or Password is incorrect"}, status = 401)
        


def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message" :"you are successfully logout"}, status = 200)
    else:
        return JsonResponse({"Error" :"User is not login"}, status = 400)
    
    
    
    
def createtask(request):
     if request.method == 'POST':
          if not request.body.strip():
            return JsonResponse({"Error": "Enter the task"}, status= 400)
        
          data = json.loads(request.body)
          
          title = data.get('title')
          print(request.user)
          discription = data.get('discription')
          if request.user.is_authenticated:
            if title and discription :
                todo= Todolist.objects.create(
                            title= title,
                            discription = discription,
                            user_id = request.user.id
                        )
                todo.save()
                return JsonResponse({"message": "Task added successfully"}, status =201)
            else :
                return JsonResponse({"Error": "Enter title and discription"}, status = 400)
          else:
             return JsonResponse({"Error": "user is not loged in"}, status = 400)
             
            
     else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
    




def readtask(request):
    if request.method == 'GET':
     if request.user.is_authenticated:
         x =Todolist.objects.filter(active =True, user_id = request.user.id).values("title", "discription", "create_date")  
         return JsonResponse({"Details": list(x)})
     else:
         return JsonResponse({"Error": "You are not Login"})
    else :
       return JsonResponse({"error" :"method not allowed"}, status = 405)
    
         
    


def updatetask(request):
      if request.method == 'PUT':
          if not request.body.strip():
            return JsonResponse({"Error": "Enter The User Informations"}, status= 400)
        
          data = json.loads(request.body)
          
          updateid = data.get('id')
          updateTitle= data.get('updateTitle')
          updatedis = data.get('updatedis')
          
        #   x= Todolist.objects.filter(title=title).values('id')
        #   print(x)
        
          
          if request.user.is_authenticated :
                if updateid is not None and updateTitle is not None and updatedis is None:
                 Todolist.objects.filter(id=updateid).update(title=updateTitle, up_date = timezone.now())
                 return JsonResponse({"Message": "Titile Updated successfully"}, status = 200)

             
             
                if updateid is not None and updatedis is not None and updateTitle is None:
                      Todolist.objects.filter(id =updateid).update(discription = updatedis, up_date = timezone.now())
                      return JsonResponse({"Message": "discription Updated successfully"}, status = 200)
                  
                if updateid is not None and updateTitle is not None and updatedis is not None:
                    Todolist.objects.filter(id = updateid).update(title = updateTitle, discription= updatedis, up_date = timezone.now())
                    return JsonResponse({"Message": "title and discription Updated successfully"}, status = 200)
                    
                else :
                     return JsonResponse({"Error": "task was not found"}, status = 400)
                    
            
          else:
                return JsonResponse({"Error": "You are not Login"}, status = 400)

      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
    

              
              
def deletetask(request):
      if request.method == 'DELETE':
          if not request.body.strip():
            return JsonResponse({"Error": "Enter The task which you want to delete"}, status= 400)
          
        
         
          data = json.loads(request.body)
          
          delid = data.get('id')
          
          if request.user.is_authenticated :
              
             if not delid :
                return JsonResponse({"Message": "id required"}, status = 400)
              
             if Todolist.objects.filter(id = delid , active = True):
             
              Todolist.objects.filter(id = delid).update(active= False, del_date = timezone.now())
             
              return JsonResponse({"Message": "User deleted successfully"})   
          
             else:  
              return JsonResponse({"Error": "invalid title"} , status = 400)
          else:  
              return JsonResponse({"Error": "You are not Login"} , status = 400)
          
      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
    

                      
          
          
        
    
        
    
    
    
             
        