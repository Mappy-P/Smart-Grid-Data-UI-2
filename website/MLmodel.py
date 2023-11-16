import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

def split_series(series, n_past, n_future):
  #
  # n_past ==> aantal voorgaande observaties (480 = 4*24*5)
  #
  # n_future ==> aantal volgende observaties (96 = 4*24)
  #
  X, y = list(), list()
  for window_start in range(0, len(series), 96):
    past_end = window_start + n_past
    future_end = past_end + n_future
    if future_end > len(series):
      break
    # de lijsten met voorgaande en te voorspellen data aanmaken uit de volledige data
    past, future = series[window_start:past_end], series[past_end:future_end]
    X.append(past)
    y.append(future)

  X, y = np.array(X), np.array(y)
  X = np.reshape(X, (X.shape[0], X.shape[1], 1))
  y = np.reshape(y, (y.shape[0], y.shape[1], 1))
  return X, y

class DemoModel:
  def __init__(self, model, data):
    self.scaler = MinMaxScaler(feature_range=(0, 1))
    self.model = keras.models.load_model(model)
    self.df = pd.read_csv(data)
    
  def createDataSet(self, start, duration):
    self.X, self.Y = split_series(self.df['Value'], 1440, 96)
    self.X = self.X[start:start + duration + 1]
    self.Y = self.Y[start:start + duration + 1]
    
  def getPredictionResults(self, start, duration):
    prediction = self.model.predict(self.X)
    yhat = list()
    for x in prediction:
      for y in x:
        lijst = list()
        lijst.append(y)
        yhat.append(lijst)
    yhat = np.array(yhat)
    yhat = self.scaler.inverse_transform(yhat)

    predictionInList = list()
    for x in yhat:
      for y in x:
        predictionInList.append(str(y))

    self.df['Value'] = self.scaler.inverse_transform(self.df[['Value']])
    realValues = self.df['Value'][start*96 + 1440: start*96 + 1440 + (duration + 1)*96]
    realValuesInList = list()
    for x in realValues:
      realValuesInList.append(str(x))

    return predictionInList, realValuesInList

  def predictValues(self, start, duration): #De duration is 0 als je voor 1 dag wilt voorspellen. x als je voor x extra dagen wilt voorspellen.
    self.df['Value'] = self.scaler.fit_transform(self.df[['Value']])
    self.createDataSet(start, duration)
    prediction, realValues = self.getPredictionResults(start, duration)
    return prediction, realValues