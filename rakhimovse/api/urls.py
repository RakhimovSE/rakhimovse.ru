from django.urls import include, path

urlpatterns = [
    path('rakhimovse_blog/', include('rakhimovse.api.rakhimovse_blog.urls'))
]
