import tkinter
import pandas as pd
import sys
import pickle

file_path = r"beer_reviews.csv"
beer_table = None
brewery_table = None
beer_style_table = None
profilename_table = None

def tablize(data):
    global beer_table
    beer_table = dict(zip(data["beer_name"],data["beer_beerid"]))
    global brewery_table
    brewery_table = dict(zip(data["brewery_name"],data["brewery_id"]))
    global beer_style_table
    beer_style_table = dict(zip(data["beer_style"].drop_duplicates(),range(data["beer_style"].drop_duplicates().size)))
    global profilename_table
    profilename_table = dict(zip(data["review_profilename"].drop_duplicates(),range(data["review_profilename"].drop_duplicates().size)))
    return data.drop(["beer_name","brewery_name"],axis=1)

def categorize_row(row):
    row["beer_style"] = beer_style_table[row["beer_style"]]
    row["review_profilename"] = profilename_table[row["review_profilename"]]
    return row 
    
def preprocess(data):
    data = data.dropna()
    data = data.apply(categorize_row,axis=1)
    return data

def main(path):
    reviews = None
    if path:
        reviews = pd.read_csv(path)
    else:
        reviews = pd.read_csv(file_path)
    reviews = tablize(reviews)
    reviews = preprocess(reviews)
    tables = {"beer":beer_table,"brewery":brewery_table,"style":beer_style_table,"profile":profilename_table}
    dataset = (reviews,tables)
    file = open("dataset",'wb')
    pickle.dump(dataset,file)
    file.close()
    return dataset

'''if __name__ == "__main__":
    main(sys.argv)'''
