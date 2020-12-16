import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Ricci:

    def __init__(self, verbose = True, config = 0):
        self.filename = "data/raw/ricci.csv"
        # print("Ricci dataset")

        if(config == 0):
            self.known_sensitive_attributes = ['Race']
        elif(config == 1):
            self.known_sensitive_attributes = ['Race', 'Position']
        elif(config == 2):
            self.known_sensitive_attributes = ['Position']
        else:
            raise ValueError(str(config)+ " is not a valid configuration for sensitive groups")
        # only a limited number of columns are considered
        self.keep_columns = [ 'Position', 'Oral', 'Written', 'Race', 'Combine', 'Class' ]
        self.categorical_attributes = [ 'Position', 'Race', 'Class']
        self.continuous_attributes = ['Oral', 'Written', 'Combine']
        self.verbose = verbose

    def get_df(self, repaired = False):

        
        df = pd.read_csv(self.filename)

        assert len(self.categorical_attributes) + len(self.continuous_attributes) == len(df.columns), "Error in classifying columns"

        
        # scale 
        scaler = MinMaxScaler()
        df[self.continuous_attributes] = scaler.fit_transform(df[self.continuous_attributes])
        
        df = df[self.keep_columns]
        df.rename(columns={'Class':'target'}, inplace=True)
        df['Race'] = df['Race'].map({"H" : 1, "W" : 0, "B" : 1})
        
        
        df.to_csv("data/raw/reduced_ricci.csv", index=False)

        if(repaired):
            df = pd.read_csv("data/raw/repaired_ricci.csv")

    
        if(self.verbose):
            print("-number of samples: (before dropping nan rows)", len(df))
        # drop rows with null values
        df = df.dropna()
        if(self.verbose):
            print("-number of samples: (after dropping nan rows)", len(df))
            
        return df
