from django.urls import path
from ToDoApp.views import signupview, loginview, logoutview , createtask, readtask, updatetask, deletetask


urlpatterns = [
    path('signup/', signupview),
    path('login/', loginview),
    path('logout/', logoutview),
    path('addtask/', createtask),
    path('readtask/', readtask),
    path('update/', updatetask),
    path('delete/', deletetask),
    
]