from django.db import models

class MonthlyData(models.Model):
    region = models.CharField(max_length=64, db_index=True)
    time = models.DateField()
    parameter = models.CharField(max_length=64, db_index=True)
    value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.region + ' - ' + str(self.time) + ' - ' + self.parameter + ': ' + str(self.value)

class SeasonalData(models.Model):
    region = models.CharField(max_length=64, db_index=True)
    time = models.DateField()
    parameter = models.CharField(max_length=64, db_index=True)
    value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.region + ' - ' + str(self.time) + ' - ' + self.parameter + ': ' + str(self.value)

class AnnualData(models.Model):
    region = models.CharField(max_length=64, db_index=True)
    time = models.DateField()
    parameter = models.CharField(max_length=64, db_index=True)
    value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.region + ' - ' + str(self.time) + ' - ' + self.parameter + ': ' + str(self.value)
