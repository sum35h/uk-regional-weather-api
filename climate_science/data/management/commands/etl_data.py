import time
from datetime import datetime
import concurrent.futures
import os
import requests

from django.core.management.base import BaseCommand

from data.models import MonthlyData, SeasonalData, AnnualData
from climate_science import settings

REGIONS = settings.REGIONS
PARAMETERS = settings.PARAMETERS
FILE_READ_CHUNK_SIZE = settings.FILE_READ_CHUNK_SIZE
MAX_WORKERS = settings.MAX_WORKERS
BASE_DATA_URL = settings.BASE_DATA_URL

class Command(BaseCommand):
    help = '''Extract Transform Load Data
            '''
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
              '--region',
               nargs='?',
               help='Select a specific Region from ' + str(REGIONS)
        )
    def download_file(self, url:str):
        """Downloads text file in chunks locally.
        """
        url_split = url.split('/')
        local_filename = url_split[-3] + '-' + url_split[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=FILE_READ_CHUNK_SIZE): 
                    f.write(chunk)
        return local_filename

    def process_row(self, row:str, region:str, parameter:str):
        """Parses each row in the file.
        """
        monthly = []
        seasonal = []
        annual =[]
        clean_row = row.rstrip().split()
        for i, r in enumerate(clean_row):
            try:
                value = float(r)
            except:
                value = None
            if i==0:
                year = int(r)
            elif i>0 and i<=12:
                time = datetime(year,i,1)
                data_row = {
                    "region": region,
                    "time": time,
                    "parameter": parameter,
                    "value": value
                    }
                monthly.append(data_row)
            elif i>12 and i<=16:
                months = [2,5,8,11]
                index = i-13
                month = months[index]
                time = datetime(year,month,1)
                data_row = {
                    "region": region,
                    "time": time,
                    "parameter": parameter,
                    "value": value
                    }
                seasonal.append(data_row)
            else:
                time = datetime(year,12,1)
                data_row = {
                    "region": region,
                    "time": time,
                    "parameter": parameter,
                    "value": value
                    }
                annual.append(data_row)
        return monthly,seasonal,annual

    def extract(self, url:str):
        """Downloads the data and generates a line of the file
        """
        filename = self.download_file(url)
        with open(filename) as f:
            [next(f) for i in range(6)] # skip the header rows
            for row in f:
                yield row

    def transform(self, region:str, type:str, url:str):
        """Generates a processed data row
        """
        for row in self.extract(url):
            yield self.process_row(row, region, type)
    
    def load(self, region:str, parameter:str, url:str):
        """Loads the monthly, seasonal and annual data to the database
        """
        for monthly, seasonal, annual in self.transform(region, parameter, url):
            monthly_data = [MonthlyData(**kwargs) for kwargs in monthly]
            seasonal_data = [SeasonalData(**kwargs) for kwargs in seasonal]
            MonthlyData.objects.bulk_create(monthly_data)
            SeasonalData.objects.bulk_create(seasonal_data)
            AnnualData.objects.create(**annual[0])
        return('ETL successful: Region: ' + region + ' - Parameter: ' + parameter )
        
    def db_cleanup(self, regions):
        MonthlyData.objects.filter(region__in=regions).delete()
        SeasonalData.objects.filter(region__in=regions).delete()
        AnnualData.objects.filter(region__in=regions).delete()

    def handle(self, *args, **options):
        """Command handler to perform the ETL asynchrously
        """
        os.chdir(os.path.join(settings.BASE_DIR,'data','ingest_files'))
        regions = REGIONS # default: ingest all regions 
        if options['region']: # ingest one specific region
            if options.get('region') in REGIONS:
                regions = options['region']
            else:
                self.stdout.write(self.style.ERROR("Error: Invalid Region, choose one of " + str(region)))
                raise SystemExit

        t = time.time()
        self.db_cleanup(regions)
        future_to_load = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for region in regions:
                for parameter in PARAMETERS:
                    future_to_load.append(executor.submit(self.load, region, parameter, BASE_DATA_URL.format(parameter, region)))
            # future_to_load = [executor.submit(self.load, region, metric_type, url.format(parameter, region)) for region, metric_type in zip(REGIONS,PARAMETERS)]
            for future in concurrent.futures.as_completed(future_to_load):
                try:
                    res_msg = future.result()
                except Exception as exc:
                    self.stdout.write(self.style.ERROR('Exception: ' + str(exc)))
                else:
                    self.stdout.write(self.style.SUCCESS(res_msg))
        print('time = ' + str(time.time() - t))
