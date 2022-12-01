#from preprocessing import main as preprocess
import pickle
import pandas as pd
import numpy as np
import os


def compare(vector1, vector2):
    AiBi, Ai, Bi = 0, 0, 0
    for col in vector1.index:
        if vector1[col] != 0 and vector2[col] != 0:
            AiBi += vector1[col]+vector2[col]
            Ai += vector1[col]**2
            Bi += vector2[col]**2
    vector1["score"] = AiBi/(Ai**0.5*Bi**0.5) if Ai != 0 and Bi != 0 else 0
    return vector1

def revert(row,table):
    row["beer_name"] = table["beer"][int(row["beer_name"])]
    row["beer_style"] = table["style"][int(row["beer_style"])]
    #row["review_profilename"] = table["profile"][int(row["review_profilename"])]
    return row


class BeerModel:
    def __init__(self, path=None):
        if path:
            self.path = path
        else:
            self.path = ""
        self.data = pickle.load(open(os.path.join(self.path, "reviews"), "rb"))
        self.table = pickle.load(open(os.path.join(self.path, "tables"), "rb"))
        self.users = pickle.load(open(os.path.join(self.path, "users"), "rb"))
        self.items = pickle.load(open(os.path.join(self.path, "items"), "rb"))
        #print(self.table.keys())
        self.reverse_table = {}
        for table in self.table:
            if table!="brewery":
                self.reverse_table[table] = {v:k for k, v in self.table[table].items()}
                #print(self.reverse_table[table])
        

    def __predict_by_users__(self, vector, topN):
        def preprocess_vector(vector):
            data = pd.Series(data=np.zeros(len(self.table["style"]), dtype=np.float16),
                             index=self.table["style"].keys())
            for col in data.index:
                filtered = vector[vector["beer_style"] == col]["review_overall"]
                if not filtered.empty:
                    data[col] = filtered.mean()/5
            return data

        vector = preprocess_vector(vector)
        data = self.users.copy(deep=True)\
            .apply(lambda x: compare(x, vector),axis=1)
        data = data[data["score"] > 0]\
            .sort_values(by=["score"], ascending=False)

        topUsers = data.head(topN).index.tolist()
        usersData = self.data[self.data["review_profilename"].isin(topUsers)]
        data = pd.DataFrame(data=np.zeros((usersData["beer_name"].unique().size, 6), dtype=np.float16), columns=["review_overall",
                                                                                                              "review_aroma",
                                                                                                              "review_appearance",
                                                                                                              "review_palate",
                                                                                                              "review_taste",
                                                                                                              "beer_abv"])
        data["beer_name"] = usersData["beer_name"].unique()
        def sumBeer(row):
            localData = data[data["beer_name"]==row["beer_name"]]
            for col in row.index:
                if col!="beer_name":
                    row[col] = localData[col].mean()/5
            return row
        data = data.apply(sumBeer,axis=1)
        data = data.sort_values(by=["review_overall"], ascending=False)
        return self.data[self.data["beer_name"].isin(data.head(topN)["beer_name"])][["beer_name","beer_abv","beer_style"]].drop_duplicates().reset_index()
        #add brewery
    def __predict_by_items__(self, vector, topN):
        def preprocess_vector(vector):
            data = pd.Series(data=np.zeros(6, dtype=np.float16), index=["review_overall",
                                                                               "review_aroma",
                                                                               "review_appearance",
                                                                               "review_palate",
                                                                               "review_taste",
                                                                               "beer_abv"])
            for col in data.index:
                filtered = vector[col]
                if not filtered.empty:
                    data[col] = filtered.mean()/5
            return data

        vector = preprocess_vector(vector)
        data = self.items.copy(deep=True)\
            .apply(lambda x: compare(x, vector),axis=1)
        data = data[data["score"] > 0]\
            .sort_values(by=["score"], ascending=False)
        return self.data[self.data["beer_name"].isin(data.head(topN).index.tolist())][["beer_name","beer_abv","beer_style"]].drop_duplicates().reset_index()

    def predict(self, vector, topN=3):
        vector = pd.DataFrame(data=vector).drop_duplicates()
        if vector.empty:
            def expand(row):
                row["beer_name"] = self.reverse_table["beer"][int(row.name)] 
                row["beer_style"] = self.reverse_table["style"][int(self.data[self.data["beer_name"]==row.name].iloc[0]["beer_style"])]
                return row
            data = self.items.sort_values(by=["review_overall"],ascending = False).head(topN*2).apply(expand,axis=1).reset_index()
            return {"general":data}
        users = self.__predict_by_users__(vector, topN).apply(lambda x:revert(x,self.reverse_table),axis=1)
        items = self.__predict_by_items__(vector, topN).apply(lambda x:revert(x,self.reverse_table),axis=1)

        return {"users":users,"items":items}


model = BeerModel()


def userInput(x):
    # _____________________ use (vector, topN(def))
    result = model.predict(vector=x)
    #return x['beer_name'].tolist()[:6]
    #print("@@@@@@@@@",result)
    return result