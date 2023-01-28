from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('', include('app.urls'))
]

if settings.DEBUG == True or settings.DEBUG == False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header  =  "Dashboard"  
admin.site.site_title  =  "Dashboard"
admin.site.index_title  =  "Dashboard"

handler404 = 'app.views.page_error_404'
handler500 = 'app.views.page_error_500'