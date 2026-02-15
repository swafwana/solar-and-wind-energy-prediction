import pandas
import numpy
p = "C:\\Users\\HK Technology\\PycharmProjects\\solar_and_wind_energy_prediction\\myapp\\Dataset\\Solar\\Weather_Data_reordered_all3.csv"
weatherdata = pandas.read_csv(p)
# print(weatherdata.values)
s = r"C:\Users\HK Technology\PycharmProjects\solar_and_wind_energy_prediction\myapp\Dataset\Solar\Solar_Energy_Generation2.csv"
# solardata=pandas.read_csv(s)
solardata = pandas.read_csv(s, sep="\t")

print(solardata.shape)

# print(solardata.values)









# a=pandas.concat([weatherdata,solardata],axis=0)

l=[]
from  datetime import  datetime
for i in weatherdata.values:
    for j in solardata.values:
        # print(i[1],j[2])

        dt_a = datetime.strptime(i[1], "%d/%m/%Y %H:%M")
        # dt_b = datetime.fromisoformat(j[2])
        dt_b = datetime.strptime(j[2], "%m/%d/%Y %H:%M")

        # print("=====",dt_a,dt_b)

        if dt_a==dt_b:

            m=[
                i[1],
                i[2],
                i[3],
                i[4],
                i[5],
                i[6],
                i[7],
                j[3],
            ]

            print(m,"==============")
            l.append(m)





    # print(i)

print(l)

import os


import pandas

a = ["Timestamp", "ApparentTemperature", "AirTemperature", "DewPointTemperature", "RelativeHumidity", "WindSpeed",
     "WindDirection", "SolarGeneration"]

fn = r'C:\Users\HK Technology\PycharmProjects\solar_and_wind_energy_prediction\myapp\Dataset\Solar\final.csv'

with open(fn, mode='w', encoding='utf-8') as f:
    f.write(','.join(a) + '\n')

with open(fn, mode='a', encoding='utf-8') as f:
    for i in l:
        j = ""
        for d in i:
            j = j + str(d) + ","

        f.write(j[:len(j) - 1] + '\n')

#############


mixed= pandas.read_csv(fn)

dfduplicatesemoved=mixed.drop_duplicates()

dfnullremoved=dfduplicatesemoved.dropna()




for c in dfnullremoved.columns():
    if dfnullremoved[c].dtype in [numpy.float64, numpy.int64]:
        median_value = dfnullremoved[c].median(skipna=True)
        dfnullremoved[c].fillna(median_value,inplace=True)



dfnullremoved.to_csv("C:\\Users\\HK Technology\\PycharmProjects\\solar_and_wind_energy_prediction\\myapp\\Dataset\\Solar\\preprocessed.csv")

