from .MLmodel import DemoModel


linkconsumptie = (r'website\assets\model.h5')
linkconsumptiedata = (r'website\assets\data\consumption_EnergyVille.csv')

def predictConsumptie(start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    consumptieModel = DemoModel(linkconsumptie, linkconsumptiedata)
    predictie, echteWaarden = consumptieModel.predictValues(start, duration)
    return predictie, echteWaarden