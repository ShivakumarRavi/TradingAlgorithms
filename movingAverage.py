from flask import Flask
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math 

app = Flask(__name__)

@app.route('/')
def movingAverageAlogirithmSMA():
    with open('config.json') as f:
        data = json.load(f)
    with open('sampleData.json') as sf:
        # r = requests.get(data['tradeURL']).json()
        r = json.load(sf)
        df = pd.DataFrame(r['chart'])
    smaShortPeriod = CalculateSMA(df['close'], data['windowSize'])
    plt.plot(df["date"], df["close"])
    plt.plot(df["date"], smaShortPeriod, label='AAPL '+ str(data['windowSize']) +' Day SMA', color='orange')
    plt.legend(loc='upper left')
    plt.show()    
    return ""

def CalculateSMA(data, rollingPeriod):
    rollingMean = []
    index = 0
    for dataPoint in data:
        dataRange = data[index : (rollingPeriod + index)]
        index = index + 1
        averageValue = sum(dataRange)/len(dataRange)
        rollingMean.append(averageValue)

    return rollingMean

@app.route('/ema')
def movingAverageAlogirithmEMA():
    with open('config.json') as f:
        data = json.load(f)
    with open('sampleData.json') as sf:
        r = json.load(sf)
        df = pd.DataFrame(r['chart'])
    emaShortPeriod = CalculateEMA(df['close'], data['windowSize'])
    plt.plot(df["date"], df["close"])
    plt.plot(df["date"], emaShortPeriod, label='AAPL '+ str(data['windowSize']) +' Day EMA', color='orange')
    plt.legend(loc='upper left')
    plt.show()    
    return ""

def CalculateEMA(data, rollingPeriod):
    rollingMean = []
    index = len(data) - 1

    firstSMASet = data[0:rollingPeriod]
    firstSMASetValue = sum(firstSMASet)/len(firstSMASet)
    
    smoothing = 2/(rollingPeriod + 1)
    previousEMA = (((data[index] - firstSMASetValue) * smoothing) + firstSMASetValue)
    rollingMean.append(previousEMA)

    for dataPoint in data[0:(index)]:
        ema = (data[index] - previousEMA) * smoothing + previousEMA
        index = index - 1
        rollingMean.append(ema)
        previousEMA = ema

    return rollingMean

@app.route('/bollingerbands')
def bollingerBands():
    with open('config.json') as f:
        data = json.load(f)
    with open('sampleData.json') as sf:
        r = json.load(sf)
        df = pd.DataFrame(r['chart'])
    smaShortPeriod = CalculateSMA(df['close'], data['windowSize'])
    upperBollingerBand, lowerBollinerBand = calculateStanderdDevation(df['close'], data['windowSize'])
    plt.plot(df["date"], df["close"])
    plt.plot(df["date"], smaShortPeriod, label='AAPL '+ str(data['windowSize']) +' Day SMA', color='orange')
    plt.plot(df["date"], upperBollingerBand, label='AAPL '+ str(data['windowSize']) +' Day Upper BB', color='green')
    plt.plot(df["date"], lowerBollinerBand, label='AAPL '+ str(data['windowSize']) +' Day Lower BB', color='red')
    plt.legend(loc='upper left')
    plt.show()    
    return ""

def calculateStanderdDevation(data, rollingPeriod):
    upperBollinerBand = []
    lowerBollinerBand = []
    sma = []
    index = 0
    for dataPoint in data:
        dataRange = data[index : (rollingPeriod + index)]
        index = index + 1
        averageValue = sum(dataRange)/len(dataRange)
        for eachDataPoint in dataRange:
            squaredValue = []
            if (eachDataPoint - averageValue) > 0:
                squaredValue.append(math.sqrt(eachDataPoint - averageValue))
            else:
                squaredValue.append(0)
        standerdDevaition = (sum(squaredValue) / len(squaredValue))
        upperBollinerBand.append( averageValue + (2 * standerdDevaition) )
        lowerBollinerBand.append( averageValue - (2 * standerdDevaition) )
    return upperBollinerBand, lowerBollinerBand

if __name__ == '__main__':
    app.run()
