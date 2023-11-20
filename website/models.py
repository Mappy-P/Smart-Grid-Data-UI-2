from .MLmodel import DemoModel
import csv


linkconsumptie = (r'website/assets/model.h5') #Het ML model van consumptie
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

linkproductie = (r'website/assets/Solar_model.h5') #Het ML model van solar productie
linkproductiedata = (r'website/assets/data/Solar_6totenmet10.csv')

linkprijzen = (r'website/assets/Belpex_model.h5') #Het ML model van Belpex prijzen
linkprijzendata = (r'website/assets/data/Belpex_6tot10.csv')
 #Predict voor 24 uur
def predictConsumptie(start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    consumptieModel = DemoModel(linkconsumptie, linkconsumptiedata)
    predictie, echteWaarden, soort, dates = consumptieModel.predictValues(start, duration)
    return predictie, echteWaarden, soort, dates

#Predict 6 tot en met 22:00
def predictProductie(start, duration):
    productieModel = DemoModel(linkproductie, linkproductiedata)
    predictie, echteWaarden, soort, dates = productieModel.predictValues(start, duration)
    return predictie, echteWaarden, soort, dates

 #Predict 6 tot en met 22:00 (per uur)
def predictPrijzen(start, duration):
    prijzenModel = DemoModel(linkprijzen, linkprijzendata)
    predictie, echteWaarden, soort, dates = prijzenModel.predictValues(start, duration)
    return predictie, echteWaarden, soort, dates
    