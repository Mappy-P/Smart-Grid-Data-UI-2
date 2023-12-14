from .MLmodel import DemoModel
from . import chargingmodel
import csv


linkconsumptie = (r'website/assets/model.h5') #Het ML model van consumptie
linkconsumptie12 = (r'website/assets/consumption_model12u2.h5')
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

linkproductie = (r'website/assets/Solar_model.h5') #Het ML model van solar productie
linkproductie12 = (r'website/assets/Solar_model12u-3.h5')
linkproductiedata = (r'website/assets/data/Solar_6totenmet10.csv')

linkprijzen = (r'website/assets/Belpex_model.h5') #Het ML model van Belpex prijzen
linkprijzen12 = (r'website/assets/Belpex_finaal12u.h5')
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

def predictConsumptie12(start, duration):
    consumptieModel = DemoModel(linkconsumptie12, linkconsumptiedata)
    predictie, echteWaarden, soort, dates = consumptieModel.predictValues(start, duration)
    return predictie, echteWaarden, soort, dates

def predictProductie12(start, duration):
    productieModel = DemoModel(linkproductie12, linkproductiedata)
    predictie, echteWaarden, soort, dates = productieModel.predictValues(start, duration)
    return predictie, echteWaarden, soort, dates

def predictPrijzen12(start, duration):
    prijzenModel = DemoModel(linkprijzen12, linkprijzendata)
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
    predicted_consumption12, _, _, _ = predictConsumptie12(date, 0)
    predicted_production12, _, _, _ = predictProductie12(date, 0)
    predicted_prices12, _, _, _ = predictPrijzen12(date, 0)

    predicted_consumption = [float(x) * 0.9 for x in predicted_consumption]
    real_consumption = [float(x) * 0.9 for x in real_consumption]
    predicted_production = ([0] * (6*4)) + [float(x) for x in predicted_production] + ([0] * (2*4-1))
    real_production = ([0] * (6*4)) + [float(x) for x in real_production] + ([0] * (2*4-1))
    predicted_prices = ([0] * (6*4)) + [float(x) for i in range(4) for x in predicted_prices] + ([0] * ((2-1)*4))
    real_prices = ([0] * (6*4)) + [float(x) for i in range(4) for x in real_prices] + ([0] * ((2-1)*4))

    

    predicted_consumption12 = ([0] * (12*4)) + [float(x) * 0.9 for x in predicted_consumption12]
    predicted_consumption12 = predicted_consumption12[:96]
    predicted_production12 = ([0] * (12*4)) + [float(x) for x in predicted_production12]
    predicted_production12 = predicted_production12[:96]
    predicted_prices12 = ([0] * (12*4)) + [float(x) for i in range(4) for x in predicted_prices12]
    predicted_prices12 = predicted_prices12[:96]

    print(predicted_consumption12)
    print(predicted_production12)
    print(predicted_prices12)
    print(len(predicted_consumption12))
    print(len(predicted_production12))
    print(len(predicted_prices12))
    print(len(predicted_consumption))
    print(len(predicted_production))
    print(len(predicted_prices))


    #print(len(predicted_consumption))
    #print(len(real_consumption))
    #print(len(predicted_production))
    #print(predicted_production)
    #print(len(real_production))
    #print(len(predicted_prices))
    #print(len(real_prices))

    return chargingmodel.simulate_day(date, cars, predicted_consumption, predicted_consumption12, real_consumption, predicted_production, predicted_production12, real_production, predicted_prices, predicted_prices12, real_prices)

