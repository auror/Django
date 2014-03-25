from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from rlp.models import movie


class movieAdmin(admin.ModelAdmin):
    #list_display = ('name', 'year_released', 'revenue', 'director', 'producer', 'actor', 'actress', 'user')
    
    fields = ('name', 'year_released', 'revenue', 'director', 'producer', 'actor', 'actress')
    readonly_fields = ()
    
    def queryset(self, request):
        qs = super(movieAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_staff:
            movieAdmin.fields = ('name', 'year_released', 'actor', 'actress')
            return qs
        else:
            movieAdmin.fields = ('name', 'year_released', 'actor', 'actress')
            movieAdmin.readonly_fields = ('name', 'year_released', 'actor', 'actress')
            return qs.filter(user = request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        elif request.user.is_staff:
            return True
        else:
            return False


admin.site.register(movie, movieAdmin)

