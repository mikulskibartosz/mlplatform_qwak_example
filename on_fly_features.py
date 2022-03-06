import pandas as pd
from qwak.feature_store.features import Metadata, OnTheFlyFeatureSet
from qwak.feature_store.features.functions import UdfFunction


def difference(series: pd.Series):
    return pd.DataFrame({'sum': series.diff().max()}, index=[0])

temp_diff_feature = OnTheFlyFeatureSet(
    name = 'london_bike_sharing_temp_diff',
    metadata=Metadata(
        display_name='Bike sharing data',
        description='Number of shares and weather',
        owner='mail@mikulskibartosz.name'
    ),
    entity='london_bike_sharing',
    function=UdfFunction(code=difference),
    requirements_file_name='requirements.txt'
)
