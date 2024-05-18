#zoho Final
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    # -------------------------------Company section--------------------------------
 
    path('stock_summary', views.stock_summary, name='stock_summary'),
    path('customize_stock_summary/',views.customize_stock_summary, name='customize_stock_summary'),
    path('shareStockSummaryToEmail/', views.shareStockSummaryToEmail, name='shareStockSummaryToEmail'),
    
]
