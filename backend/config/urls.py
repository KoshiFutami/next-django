"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('showcase.interface.urls')),
]

handler400 = "showcase.interface.error_handlers.bad_request"
handler403 = "showcase.interface.error_handlers.permission_denied"
handler404 = "showcase.interface.error_handlers.page_not_found"
handler500 = "showcase.interface.error_handlers.server_error"
