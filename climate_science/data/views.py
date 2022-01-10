from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import MonthlyData, SeasonalData, AnnualData
from .serializers import MonthlyDataSerializer, SeasonDataSerializer, AnnualDataSerializer
from .pagination import PaginationHandlerMixin
from climate_science import settings

PAGE_SIZE = settings.PAGE_SIZE
VALID_START_YEAR = settings.VALID_START_YEAR
VALID_END_YEAR = settings.VALID_END_YEAR

class DataPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE

class MonthlyDataView(APIView, PaginationHandlerMixin):
    serializer_class = MonthlyDataSerializer
    pagination_class = DataPagination
    
    def get(self, request, parameter, region):
        query_filters = {'parameter': parameter, 'region': region}
        if request.GET.get('year_range'):
            years = request.GET.get('year_range').split(',')
            if len(years) == 2:
                start_year, end_year =  request.GET.get('year_range').split(',')
                if start_year.isdigit() and end_year.isdigit() and (int(start_year) >=VALID_START_YEAR and int(start_year) <=VALID_END_YEAR)\
                                        and (int(end_year) >=VALID_START_YEAR and int(end_year) <=VALID_END_YEAR):
                    start_date = start_year + '-01-01'
                    end_date = end_year + '-12-31'
                    query_filters['time__range']= [start_date, end_date]
                    print(query_filters)
                else:
                    return Response({"error": "Invalid year_range param values."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid year_range param values."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = MonthlyData.objects.filter(**query_filters).order_by('time')
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response({"region":region,"parameter":parameter,"data":serializer.data }, status=status.HTTP_200_OK)

class SeasonalDataView(APIView, PaginationHandlerMixin):
    serializer_class = SeasonDataSerializer
    pagination_class = DataPagination

    def get(self, request, parameter, region):
        queryset = SeasonalData.objects.filter(parameter=parameter,region=region).order_by('time')
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response({"region":region,"parameter":parameter,"data":serializer.data }, status=status.HTTP_200_OK)

class AnnualDataView(APIView, PaginationHandlerMixin):
    serializer_class = AnnualDataSerializer
    pagination_class = DataPagination

    def get(self, request, parameter, region):
        queryset = AnnualData.objects.filter(parameter=parameter,region=region).order_by('time')
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response({"region":region,"parameter":parameter,"data":serializer.data }, status=status.HTTP_200_OK)
