from .MLmodel import DemoModel
from . import chargingmodel
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
    
def simulate(date, cars):
    predicted_consumption, real_consumption, _, _ = predictConsumptie(date, 0)
    predicted_production, real_production, _, _ = predictProductie(date, 0)
    predicted_prices, real_prices, _, _ = predictPrijzen(date, 0)
    #print(len(predicted_consumption))
    #print(len(real_consumption))
    #print(len(predicted_production))
    #print(len(real_production))
    #print(len(predicted_prices))
    #print(len(real_prices))

    predicted_consumption = [float(x) * 0.8 for x in predicted_consumption]
    real_consumption = [float(x) * 0.9 for x in real_consumption]
    predicted_production = ([0] * (6*4)) + [float(x) for x in predicted_production] + ([0] * (2*4-1))
    real_production = ([0] * (6*4)) + [float(x) for x in real_production] + ([0] * (2*4-1))
    predicted_prices = ([0] * (6*4)) + [float(x) for i in range(4) for x in predicted_prices] + ([0] * (2*4))
    real_prices = ([0] * (6*4)) + [float(x) for i in range(4) for x in real_prices] + ([0] * ((2-1)*4))

    #print(len(predicted_consumption))
    #print(len(real_consumption))
    #print(len(predicted_production))
    #print(predicted_production)
    #print(len(real_production))
    #print(len(predicted_prices))
    #print(len(real_prices))


    return chargingmodel.simulate_day(date, cars, predicted_consumption, real_consumption, predicted_production, real_production, predicted_prices, real_prices)

