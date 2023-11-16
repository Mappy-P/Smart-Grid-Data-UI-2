from .MLmodel import DemoModel


linkconsumptie = (r'website/assets/model.h5')
linkconsumptiedata = (r'website/assets/data/consumption_EnergyVille.csv')

def predictConsumptie(start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    consumptieModel = DemoModel(linkconsumptie, linkconsumptiedata)
    predictie, echteWaarden = consumptieModel.predictValues(start, duration)
    return predictie, echteWaarden

def predictProductie(start, duration):
    file = open('./assets/optimisation/examples/energie2018-10-09.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    available_solar = []
    for row in csvreader:
        available_solar.append(float(row[0]))
    return available_solar, available_solar

def predictPrijzen(start, duration):
    file = open('./assets/optimisation/examples/stroomprijs1-01-18.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    new_energy_price = []
    for row in csvreader:
        new_energy_price.append(float(row[0])/100) #prijs in cent
    