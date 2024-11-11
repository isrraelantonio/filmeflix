#url - view -  template 
from django.urls import path, reverse_lazy
from .views import Homefilmes, Homepage, Detalhesfilmes,  Pesquisafilme, Paginaperfil, Criarconta
from django.contrib.auth import views as auth_view


app_name = 'filme'
urlpatterns = [

    path('', Homepage.as_view(), name= 'homepage'),
    path('filme/', Homefilmes.as_view(), name= 'homefilmes'),
    path('filme/<int:pk>', Detalhesfilmes.as_view(), name= 'detalhesfilmes'),
    path('pesquisa/', Pesquisafilme.as_view(), name =  'pesquisa'),
    path('login/', auth_view.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('editarperfil/<int:pk>', Paginaperfil.as_view(), name= 'editarperfil'),
    path('redefinrsenha', auth_view.PasswordChangeView.as_view( template_name = 'redefinirsenha.html', success_url= reverse_lazy('filme:homefilmes') ), name = 'redefinirsenha'),
    path('criarconta/', Criarconta.as_view(), name= 'criarconta'),
   

]