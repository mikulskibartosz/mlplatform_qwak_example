from qwak.feature_store.entities import Entity, ValueType
from qwak.feature_store.sources.data_sources import SnowflakeSource
from qwak.feature_store.features.feature_sets import BatchFeatureSet, Metadata, Backfill
from qwak.feature_store.features.functions import SqlFunction
from datetime import datetime



snowflake_source = SnowflakeSource(
     name = 'london_bike_sharing',
     description = 'Bike sharing data',
     date_created_column = 'CREATION_DATE',
     host = 'taa51111.snowflakecomputing.com',
     username_secret_name = 'qwak_secret_snowflake_user_gal',
     password_secret_name = 'qwak_secret_snowflake_password_gal',
     database = 'QWAK_DB',
     schema = 'BLOG_AND_WORKSHOP',
     warehouse = 'COMPUTE_WH',
     table = 'london_bike_sharing'
)

bike_sharing = Entity(
    name='london_bike_sharing',
    keys=['id'],
    description='Bike sharing',
    value_type=ValueType.INTEGER
)

batch_feature_set = BatchFeatureSet(
    name='london_bike_sharing',
    metadata=Metadata(
        display_name='Bike sharing data',
        description='Number of shares and weather',
        owner='mail@mikulskibartosz.name'
    ),
    entity='london_bike_sharing',
    data_sources=['london_bike_sharing'],
    backfill=Backfill(
        start_date=datetime(2015, 1, 4)
    ),
    scheduling_policy='@daily',
    function=SqlFunction("""
            select id, creation_date, timestamp, cnt, t1, t2, hum, wind_speed, weather_code, is_holiday, is_weekend, season from london_bike_sharing
    """)
)
