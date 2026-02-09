from src.data.databaseManager import DatabaseManager
from src.data.features import Features 
from src.miniML.machLearnTools import MachLearnTools

class DataManager:
    def __init__(self, asset: str, timeframe: str) -> None:
        self.X_train = None 
        self.y_train = None 
        self.X_test = None 
        self.y_test = None 
        self.X_latest = None 
        self.X_features = None
        self.labels = None
        self.window = 10 # consider passing in value instead
        self.data_pipline(asset, timeframe)

    def update_data(self, asset: str, timeframe: str ) -> None:
        # Could possibly pass in window here if user wanted to change training 
        # and prediction window. Undecided.
        self.data_pipline(asset, timeframe)


    def data_pipline(self, asset, timeframe) -> None:
        dbm = DatabaseManager(asset, timeframe)
        print("Updating database in data pipeline")
        dbm.update_table()
        features = Features(dbm.get_dataframe())
        self.X_features, self.labels = features.run_features()
        mlt = MachLearnTools(self.X_features, self.labels)
        self.X_train, self.X_test, self.y_train, self.y_test = mlt.timeseries_pipeline(self.window)
        self.X_latest = mlt.latest_features(self.window)


    def get_training_set(self) -> tuple:
        return self.X_train, self.y_train

        
    def get_testing_set(self) -> tuple:
        return self.X_test, self.y_test

        
    def get_latest(self):
        return self.X_latest

    
    def get_X_features(self):
        return self.X_features


    def get_labels(self):
        return self.labels

