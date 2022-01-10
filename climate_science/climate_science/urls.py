from django.contrib import admin
from django.urls import path

from data.views import MonthlyDataView, SeasonalDataView, AnnualDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/<str:parameter>/monthly/<str:region>', MonthlyDataView.as_view()),
    path('api/data/<str:parameter>/seasonal/<str:region>', SeasonalDataView.as_view()),
    path('api/data/<str:parameter>/annual/<str:region>', AnnualDataView.as_view())
]
