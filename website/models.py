from .MLmodel import DemoModel
from . import chargingmodel
import csv


linkconsumptie = (r'website/assets/model.h5') #Het ML model van consumptie
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

linkproductie = (r'website/assets/Solar_model.h5') #Het ML model van solar productie
linkproductiedata = (r'website/assets/data/Solar_6tot10.csv')

linkprijzen = (r'website/assets/Belpex_model.h5') #Het ML model van Belpex prijzen
linkprijzendata = (r'website/assets/data/Belpex_6tot10.csv')

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
    
def simulate(date, cars):
    predicted_consumption, real_consumption = predictConsumptie(date, 0)
    predicted_production, real_production = predictProductie(date, 0)
    predicted_prices, real_prices = predictPrijzen(date, 0)
    print(predicted_consumption)
    print(real_consumption)
    print(predicted_production)
    print(real_production)
    print(predicted_prices)
    print(real_prices)


    predicted_consumption = [float(x) * 0.8 for x in predicted_consumption]
    real_consumption = [float(x) * 0.8 for x in real_consumption]
    predicted_production = [float(x) for x in predicted_consumption]
    real_production = [float(x) for x in real_consumption]
    predicted_prices = [float(x) for x in predicted_prices]
    real_prices = [float(x) for x in real_prices]

    chargingmodel.simulate_day(date, cars, predicted_consumption, real_consumption, predicted_production, real_production, predicted_prices, real_prices)
