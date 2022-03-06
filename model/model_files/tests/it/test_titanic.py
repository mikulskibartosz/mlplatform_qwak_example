import pandas as pd
from qwak_mock import real_time_client


def test_realtime_api(real_time_client):
    feature_vector = [
        {
            'london_bike_sharing.wind_speed': 1.0,
            'london_bike_sharing.t1': 20.0, 
            'london_bike_sharing.t2': 24.0,
            'london_bike_sharing.hum': 0.0,
            'london_bike_sharing.weather_code': 3,
            'london_bike_sharing.season': 1,
            'london_bike_sharing.is_holiday': 1,
            'london_bike_sharing.is_weekend': 1
        }]

    result: pd.DataFrame = real_time_client.predict(feature_vector)
    assert result.values[0][0] > 0
