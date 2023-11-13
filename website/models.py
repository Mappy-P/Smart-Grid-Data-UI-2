from MLmodel import DemoModel

linkconsumptie = (r'website/assets/model.h5')
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

consumptieModel = DemoModel(linkconsumptie, linkconsumptiedata)

def predictConsumptie(start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    predictie, echteWaarden = DemoModel.predict(start, duration)
    return predictie, echteWaarden

def predictProductie(start, duration):
    pass

def predictPrijzen(start, duration):
    pass