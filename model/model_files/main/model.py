from html import entities
import os

import numpy as np
import pandas as pd
import qwak
from catboost import CatBoostRegressor, Pool, cv
from qwak.model.base import QwakModelInterface
from qwak.model.schema import ExplicitFeature, ModelSchema, Prediction, BatchFeature, Entity
from sklearn.model_selection import train_test_split
from qwak.feature_store.offline import OfflineFeatureStore


class LondonBikeSharePrediction(QwakModelInterface):

    def __init__(self):
        loss_function=os.getenv('loss_fn','RMSE')
        learning_rate=os.getenv('learning_rate',None)
        if learning_rate:
            learning_rate = int(learning_rate)
        iterations=int(os.getenv('iterations',1000))

        self.model = CatBoostRegressor(iterations=iterations,
                                        loss_function=loss_function,
                                        learning_rate=learning_rate)

        qwak.log_param({'loss_function' : loss_function,
                            'learning_rate' : learning_rate,
                            'iterations' : iterations,
                        })

    def build(self):
        offline_feature_store = OfflineFeatureStore()
        samples = offline_feature_store.get_sample_data(feature_set_name='london_bike_sharing', number_of_rows=2000)

        x = samples[[
            'london_bike_sharing.wind_speed', 
            'london_bike_sharing.t1', 
            'london_bike_sharing.t2',
            'london_bike_sharing.hum',
            'london_bike_sharing.weather_code',
            'london_bike_sharing.season',
            'london_bike_sharing.is_holiday',
            'london_bike_sharing.is_weekend'
        ]]
        y = samples[['london_bike_sharing.cnt']]

        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=.85, random_state=42)

        cate_features_index = [4, 5]

        self.model.fit(x_train, y_train, cat_features=cate_features_index, eval_set=(x_test, y_test))

        # Cross validating the model (5-fold)
        cv_data = cv(Pool(x, y, cat_features=cate_features_index), self.model.get_params(), fold_count=5)
        print('the best cross validation RMSE is :{}'.format(np.max(cv_data["test-RMSE-mean"])))
        qwak.log_metric({"val_rmse" : np.max(cv_data["test-RMSE-mean"])})

    def schema(self):
        entity_id = Entity(name='london_bike_sharing', type=str)
        model_schema = ModelSchema(
            entities=[entity_id],
            features=[
                BatchFeature(entity=entity_id, name='london_bike_sharing.wind_speed'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.t1'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.t2'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.hum'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.weather_code'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.season'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.is_holiday'),
                BatchFeature(entity=entity_id, name='london_bike_sharing.is_weekend')
            ],
            predictions=[
                Prediction(name='cnt', type=int)
            ])
        return model_schema

    @qwak.analytics()
    def predict(self, df) -> pd.DataFrame:
        return pd.DataFrame(self.model.predict(df))
