import pandas as pd
from qwak.feature_store.offline import OfflineFeatureStore

population_df = pd.DataFrame(
    data = [
        [42, '2017-01-03'],
        [55, '2017-01-03']
    ], columns = ['id', 'creation_date']
)

key_to_features = {'id': [
    'london_bike_sharing.wind_speed',
    'london_bike_sharing.timestamp'
]}

offline_feature_store = OfflineFeatureStore()

# help(offline_feature_store)

# retrieved = offline_feature_store.get_feature_values(
#     entity_key_to_features = key_to_features,
#     population = population_df,
#     point_in_time_column_name = 'creation_date'
# )

# print(retrieved)

samples = offline_feature_store.get_sample_data(feature_set_name='london_bike_sharing', number_of_rows=2000)

print(samples)
print(samples.columns)