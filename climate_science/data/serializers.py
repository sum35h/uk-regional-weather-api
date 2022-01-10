from rest_framework import serializers
from .models import MonthlyData, SeasonalData, AnnualData
from climate_science import settings

class MonthlyDataSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_year(self, obj):
        return obj.time.year

    def get_month(self, obj):
        return obj.time.strftime(settings.DATA_MONTH_FORMAT)

    class Meta:
        model = MonthlyData
        fields = ['year', 'month', 'value']

class SeasonDataSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()

    def get_year(self, obj):
        return obj.time.year

    def get_season(self, obj):
        month_season_map = {2: "win", 5: "spr" , 8: "sum", 11: "aut"}
        return month_season_map.get(obj.time.month)

    class Meta:
        model = SeasonalData
        fields = ['year', 'season', 'value']

class AnnualDataSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()

    def get_year(self, obj):
        return obj.time.year

    class Meta:
        model = AnnualData
        fields = ['year', 'value']