import pandas as pd
from pyinaturalist import *
import inspect
from pyinaturalist_convert import *
import os

# getData,
# this function will use the pinaturalist package to 
# scrap the inaturalist website and get data,
# it will concatenate each page result to one dataset
# @param,
# @keyWord, the keyword / phrase to search

names_list = ["observed_on_details.date", "species_guess", "public_positional_accuracy", "quality_metrics", "taxon.name", "geojson.coordinates", "owners_identification_from_vision", "identifications_count", "num_identification_disagreements", "location", "place_guess"]

def getData(keyWord):
    dfList = []
    try:
        for page in range(1, 100):
            # tmp = get_observations(q="Harmonia Axyridis", d1 = "01/01/2018", d2 = "30/11/2022", lat=53.94220, lng=-3.96803, radius=511, per_page=400, page = page)
            tmp = get_observations(q=keyWord, d1 = "01/01/2018", d2 = "30/11/2022", lat=53.94220, lng=-3.96803, radius=511, per_page=400, page = page)
            dfList.append(to_dataframe(tmp))
    except Exception as e: 
        df = pd.concat(dfList)
        df = [names_list].copy()
        df.to_csv("inat_data_query24.csv", sep=",", index="False")
        
    print("data collection complete")


    
    
# filter Data,
# this function filter the dataset obtain in  the getData function
# to keep only columns of interest,
# it also convert the location column to latitude and longitude
# finally, it standardise the column name of our two dataset
def filterData():
    inat_df = pd.read_csv("inat_data_query24.csv")
    inat_df = inat_df [names_list]
        
    latitude = []
    # print(inat_df.location.tolist())
    for vala in inat_df.location.tolist():
        lat = float(str(vala).split(",")[0].replace("[", "").replace("]","").replace(",", ""))
        latitude.append(lat)
    
    longitude= []
    for valo in inat_df.location.tolist():
        lon= float(str(valo).split(",")[1].replace("[", "").replace("]","").replace(",", ""))
        longitude.append(lon)

    inat_df= inat_df.assign(latitude = latitude)
    inat_df= inat_df.assign(longitude = longitude)

    article_df = pd.read_csv("article_data.csv")
    article_df.columns = article_df.columns.str.lower()
    article_df.to_csv("article_data.csv", sep=",", index=False)
    inat_df.to_csv("inat_data_filtered.csv", sep=",", index=False)


# getGrid,
# this function is a try of chunking a big density dataset to a usable for us

def getGrid():
    latList, longList, densityList = [], [], []
    for i,chunk in enumerate(pd.read_csv("population_gbr_2019-07-01.csv", chunksize=10000)):
        latList.append(round(chunk.tail(1).Lat.values[0], 3))
        longList.append(round(chunk.tail(1).Lon.values[0], 3))
        densityList.append(chunk.Population.sum())
    
    data = {"latitude": latList, "longitude":longList, "density":densityList}
    df = pd.DataFrame.from_dict(data)
    df.to_csv("density_try.csv", sep=",", index=False)
    
    # main,
    # main function to run our data collection and cleaning
def main():
    if not os.path.isfile("inat_data_query24.csv"): getData()
    filterData()
    # getGrid()
    
    
if __name__ == '__main__':
    main()