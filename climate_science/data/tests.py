
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.management import call_command

TEST_REGION = 'UK'
TOTAL_COUNT_TEMP = 1656
TOTAL_COUNT_RAINFALL = 1920
TOTAL_COUNT_SUNSHINE = 1236
PAGE_SIZE = 24
TOTAL_COUNT_RAINYDAYS = 1572
TOTAL_COUNT_AIRFROST = 744

class DataTests(APITestCase):
    def setUp(self):
        call_command('etl_data', '--region', TEST_REGION)
    
    def test_monthly_data_year_filter(self):
        """
        Tests Monthly year_range filter
        """
        url = '/api/data/Tmean/monthly/' + TEST_REGION +'?year_range=1970,2000'
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['data']['count'], 12 + (2000 - 1970) * 12)

    def test_monthly_data_year_filter_same_year(self):
        """
        Tests Monthly year_range filter for same year
        """
        url = '/api/data/Tmean/monthly/' + TEST_REGION +'?year_range=2000,2000'
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['data']['count'], 12)
        

    def test_default_page_limit(self):
        """
        Tests default pagination
        """
        url = '/api/data/Tmean/monthly/' + TEST_REGION 
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        print(resp_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)
    
    def test_page_limit(self):
        """
        Tests pagination limit parameter
        """
        url = '/api/data/Tmean/monthly/' + TEST_REGION +'?limit=50'
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_dict['data']['results']), 50)

    ################################################### MONTHLY DATA #########################################################
    def test_monthly_tmean_data(self):
        """
        Tests Monthly Tmean for a region
        """
        url = '/api/data/Tmean/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmean')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_TEMP)
    
    def test_monthly_tmax_data(self):
        """
        Tests Monthly Tmax for a region
        """
        url = '/api/data/Tmax/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmax')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_TEMP)
    
    def test_monthly_tmin_data(self):
        """
        Tests Monthly Tmin for a region
        """
        url = '/api/data/Tmin/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmin')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_TEMP)

    def test_monthly_rainfall_data(self):
        """
        Tests Monthly Rainfall for a region
        """
        url = '/api/data/Rainfall/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Rainfall')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_RAINFALL)
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_monthly_sunshine_data(self):
        """
        Tests Monthly Sunshine for a region
        """
        url = '/api/data/Sunshine/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Sunshine')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_SUNSHINE)
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_monthly_raindays1mm_data(self):
        """
        Tests Monthly Raindays1mm for a region
        """
        url = '/api/data/Raindays1mm/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Raindays1mm')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_RAINYDAYS)
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)
    
    def test_monthly_airfrost_data(self):
        """
        Tests Monthly AirFrost for a region
        """
        url = '/api/data/AirFrost/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'AirFrost')
        self.assertEqual(resp_dict['data']['count'], TOTAL_COUNT_AIRFROST)
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)


    ########################################### SEASONAL DATA ########################################################
    def test_seasonal_tmean_data(self):
        """
        Tests Seasonal Tmean for a region
        """
        url = '/api/data/Tmean/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmean')
    
    def test_seasonal_tmax_data(self):
        """
        Tests Seasonal Tmax for a region
        """
        url = '/api/data/Tmax/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmax')
    
    def test_seasonal_tmin_data(self):
        """
        Tests Seasonal Tmin for a region
        """
        url = '/api/data/Tmin/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmin')

    def test_seasonal_rainfall_data(self):
        """
        Tests Seasonal Rainfall for a region
        """
        url = '/api/data/Rainfall/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Rainfall')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_seasonal_sunshine_data(self):
        """
        Tests Seasonal Sunshine for a region
        """
        url = '/api/data/Sunshine/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Sunshine')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_seasonal_raindays1mm_data(self):
        """
        Tests Seasonal Raindays1mm for a region
        """
        url = '/api/data/Raindays1mm/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Raindays1mm')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)
    
    def test_seasonal_airfrost_data(self):
        """
        Tests Seasonal AirFrost for a region
        """
        url = '/api/data/AirFrost/seasonal/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'AirFrost')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)


    ################################################### ANNUAL DATA #########################################################
    def test_annual_tmean_data(self):
        """
        Tests Annual Tmean for a region
        """
        url = '/api/data/Tmean/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmean')
    
    def test_annual_tmax_data(self):
        """
        Tests Annual Tmax for a region
        """
        url = '/api/data/Tmax/monthly/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmax')
    
    def test_annual_tmin_data(self):
        """
        Tests Annual Tmin for a region
        """
        url = '/api/data/Tmin/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Tmin')

    def test_annual_rainfall_data(self):
        """
        Tests Annual Rainfall for a region
        """
        url = '/api/data/Rainfall/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Rainfall')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_annual_sunshine_data(self):
        """
        Tests Annual Sunshine for a region
        """
        url = '/api/data/Sunshine/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Sunshine')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)

    def test_annual_raindays1mm_data(self):
        """
        Tests Annual Raindays1mm for a region
        """
        url = '/api/data/Raindays1mm/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'Raindays1mm')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)
    
    def test_annual_airfrost_data(self):
        """
        Tests Annual AirFrost for a region
        """
        url = '/api/data/AirFrost/annual/' + TEST_REGION
   
        response = self.client.get(url,format='json')
    
        resp_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_dict['region'], TEST_REGION)
        self.assertEqual(resp_dict['parameter'], 'AirFrost')
        self.assertEqual(len(resp_dict['data']['results']), PAGE_SIZE)