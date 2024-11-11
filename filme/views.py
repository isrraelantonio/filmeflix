from django.shortcuts import render, redirect, reverse
from.models import Filme, Usuario
from .forms import CriarContaForms, FormsHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin







# Create your views here.
#def homepage(request):
    #return render(request, "homepage.html")

class Homepage(FormView):
     template_name = "homepage.html"
     form_class = FormsHomepage

     def get(self, request, *args, **kwargs):
          if request.user.is_authenticated: # Verifico ao entrar nessa página se o usuário já está autenticado. caso positivo ele vai diretamente ao seu home filmes 
               return redirect('filme:homefilmes')
          else:
               return super().get(request, *args, **kwargs) # edm caso negativo o usuário será direcionado a homepage
    
     def get_success_url(self):
          email = self.request.POST.get('email')
          usuarios = Usuario.objects.filter(email = email)
          if usuarios:
               return reverse('filme:login')
          else:
               return reverse('filme:criarconta')




#def homefilmes(request):
    # context = {}
    # lista_filmes = Filme.objects.all()
     #context['lista_filmes'] = lista_filmes
    # return render(request, "homefilmes.html", context)


class Homefilmes(LoginRequiredMixin, ListView):
     template_name = "homefilmes.html"
     model = Filme  # essse é o nosso objetct list


class Detalhesfilmes(LoginRequiredMixin, DetailView):
     template_name = "detalhesfilmes.html"
     model = Filme # o nosso object será apenas um oljeto da nossa lista
     

     def get(self, request, *args, **kwargs):
          #Descobrir qual o filme o usuário está acessando e contabiliza
          filme =  self.get_object()
          filme.visualizacoes +=1 
          filme.save() # salva a contabilização ao banco de dados 
          usuario = request.user
          usuario.filmes_vistos.add(filme)
          return super().get(request, *args, **kwargs) #terorna ao usuário o url final do site
     


     def get_context_data(self, **kwargs):
           context = super(Detalhesfilmes, self).get_context_data(**kwargs)
           #filtrar a tabelade filmes pegando os filmes com categorias relacionadas
           filmes_relacionados = Filme.objects.filter(categoria =  self.get_object().categoria)[0:6]
           context['filmes_relacionados'] = filmes_relacionados
           return context
     

class Pesquisafilme(LoginRequiredMixin, ListView):
      template_name = "pesquisa.html"
      model = Filme

      def get_queryset(self):
           termo_pesquisa = self.request.GET.get('query')
           if termo_pesquisa: 
                object_list = self.model.objects.filter(titulo__icontains = termo_pesquisa)
                return object_list
           else: 
                return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
     template_name = 'editarperfil.html'
     model = Usuario
     fields = ['first_name', 'last_name', 'email']

     def test_func(self):
        user = self.get_object()
        return self.request.user == user

     def get_success_url(self):
          return reverse('filme:homefilmes')



class Criarconta(FormView):
     template_name = 'criarconta.html'
     form_class = CriarContaForms

     def form_valid(self, form):
         form.save()
         return super().form_valid(form)

     def get_success_url(self):
        return reverse('filme:login')
     

     
# irei usar essa solução para um teste em relaão a quem tenta editar o perfil e tenta digitar o id de outra pessoa


#class EditarPerfil(LoginRequiredMixin, UpdateView):
    #template_name = 'editar_perfil.html'
    #model = Usuario
    #fields = ['first_name', 'last_name', 'email']

    #def dispatch(self, request, *args, **kwargs):
       #if self.request.user.is_authenticated:
            #if self.request.user.id != self.kwargs['pk']:
               # return self.redirect_to_own_profile()
       #else:
        #    #return HttpResponseRedirect(reverse('filme:login'))
        #return super().dispatch(request, *args, **kwargs)

    #def redirect_to_own_profile(self):
        #own_profile_url = reverse('filme:editar-perfil', kwargs={'pk': self.request.user.id})
       #return HttpResponseRedirect(own_profile_url)
    
    #def get_success_url(self):
       # return reverse('filme:home_dhytpix')