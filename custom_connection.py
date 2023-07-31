from streamlit.connections import ExperimentalBaseConnection
import requests


class OpenWeatherApiConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()
        session.params['appid'] = kwargs['api_key']
        return session

    def get_weather_by_city_name(self, city_name):
        # API endpoint for getting weather by city name
        weather_url = "http://api.openweathermap.org/data/2.5/weather"

        # Set up the parameters
        params = {
            "q": city_name,
        }

        # Make the API call using the 'requests' library
        response = self._instance.get(weather_url, params=params)

        # Check if the API call was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            return None
