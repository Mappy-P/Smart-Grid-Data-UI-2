from .MLmodel import DemoModel
import csv


linkconsumptie = (r'website/assets/model.h5') #Het ML model van consumptie
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

linkproductie = (r'website/assets/Solar_model.h5') #Het ML model van solar productie
linkproductiedata = (r'website/assets/data/solar_PV_EnergyVille.csv')

linkprijzen = (r'website/assets/Belpex_model.h5') #Het ML model van Belpex prijzen
linkprijzendata = (r'website/assets/data/Belpex_20182023.csv')

def predictConsumptie(start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    consumptieModel = DemoModel(linkconsumptie, linkconsumptiedata)
    predictie, echteWaarden = consumptieModel.predictValues(start, duration)
    return predictie, echteWaarden

def predictProductie(start, duration):
    productieModel = DemoModel(linkproductie, linkproductiedata)
    predictie, echteWaarden = productieModel.predictValues(start, duration)
    return predictie, echteWaarden

def predictPrijzen(start, duration):
    prijzenModel = DemoModel(linkprijzen, linkprijzendata)
    predictie, echteWaarden = prijzenModel.predictValues(start, duration)
    return predictie, echteWaarden
    