from django.contrib import admin
from .models import Filme, Epsodio, Usuario # importamos o nosso banco de dados do nosso model 
from django.contrib.auth.admin import UserAdmin

# Register your models here.
#aqui vamos registar os nosso banco de dados do nosso filme 


#isso aqui só irá existir porque precisamos adicionar esses campos a nossa administração
campos = list(UserAdmin.fieldsets)
campos.append(
    
    ('Histórico' , {'fields' : ('filmes_vistos',)})

)
UserAdmin.fieldsets = tuple(campos)

admin.site.register(Filme)
admin.site.register(Epsodio)
admin.site.register(Usuario, UserAdmin)

