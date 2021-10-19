from numpy.lib.npyio import load
from check_for_returns import get_daily_prices
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow.lite as tflite
import time
import random
from data_processing import DataProcessing
dp = DataProcessing([])
from yahoo_fin.stock_info import get_quote_table

class NeuralNetwork:

    def __init__(self, number_of_labels, labels, data, train_data_provided):
        self.number_of_labels = number_of_labels
        self.labels = labels
        self.data = data
        self.train_data_provided = train_data_provided
        self.processing = DataProcessing(self.data)
        
    def clean_data(self):    
        p = self.data
        X = p.drop([self.labels], axis=1)
        Y = p[self.labels]
        if self.train_data_provided:
            pass
        else:
            train_labels, train_samples = shuffle(X,Y)            
        return train_labels, train_samples

    def initialize_model(self, X, Y):
        model = Sequential([
            Dense(units=len(self.data.columns), activation='relu'),
            Dense(units=32, activation='relu'),
            Dense(units=32, activation='relu'),
            Dense(units=self.number_of_labels, activation='softmax')
        ])

        X = np.asarray(X).astype('float32')
        model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy']) 

        model.fit(X, Y, epochs=30, shuffle=True, batch_size=30, use_multiprocessing=True, verbose=2)
        return model

    def save_best_model(self, x_data, y_data, repeats=12):
        model = self.initialize_model(x_data, y_data)
        best = (0, None)
        for n in range(repeats):
            x_train, x_test, y_train, y_test = train_test_split(x_data, y_data)
            model.fit(x_train, y_train, epochs=30, shuffle=True, batch_size=30, use_multiprocessing=True)
            acc = model.evaluate(x_data, y_data, use_multiprocessing=True)[1]
            if acc > best[0]:
                best = (acc, model)
        print(f'Best was {best[0] * 100}%')
        best[1].save('model2.tf')
        lite_model = tflite.TFLiteConverter.from_keras_model(best[1])
        open("model2.tflite", "wb").write(lite_model.convert())
        model = load_model('model2.tf')
        return model, acc

    def iterate_predictions(self, X, Y):
        model = load_model('model2.tf')
        while True:
            labels = self.labels
            position = random.randint(0,len(X))
            n = X.loc[position]
            h = []
            h.append(n)
            n = np.asarray(n).astype('float32')
            print(n)
            n = np.array(h, dtype='float32')
            prediction = model.predict(n)
            predicted_label = np.argmax(prediction)
            actual_label = Y.loc[position]
            print(f"prediction : {predicted_label}, actual : {actual_label}")
            time.sleep(2)
    
class DeepLearningStrategy(NeuralNetwork):
    
    def __init__(self, data):
        self.data = data
        self.model = 0

    def construct_dictionary_of_classes(self, tickers):
        classes = []
        for ticker in tickers:
            try:
                price_change = get_quote_table(ticker)
            except IndexError:
                price_change = get_quote_table(ticker)
            if price_change['Quote Price'] - price_change['Previous Close'] > 0:
                classes.append((ticker, 1))
            else:
                classes.append((ticker,0))
        dict_classes = {}
        dict_classes = dp.Convert(classes, dict_classes)
        df = pd.DataFrame(dict_classes)
        print(df)
        df.to_csv(r'data for trading\dictionary of classes.csv')
        return df

    def init_training_data(self):
        classes_mapped_to_tickers = pd.read_csv(r'data for trading\dictionary of classes.csv')
        tickers = dp.clean_columns_and_dataframe(classes_mapped_to_tickers)
        print(tickers)
        print(self.data)
        samples = []
        classes = []
        for i in range(len(tickers)):
            ticker = tickers[i]
            if classes_mapped_to_tickers[ticker][0] == 1:
                for _ in range(len(self.data)):
                    classes.append(1)
            else:
                for _ in range(len(self.data)):
                    classes.append(0) 
            dt = dp.series_to_list(self.data[ticker])
            for i in dt:
                samples.append(i)
            
        training_data = pd.DataFrame(samples)
        training_data['classes'] = pd.DataFrame(classes)
        print(training_data)
        return training_data

    def market_prediction(self, X):
        self.model = load_model('model2.tf') 
        sell = 0
        buy = 0
        for price in X:
            n = price
            h = []
            h.append(n)
            n = np.asarray(n).astype('float32')
            print(n)
            n = np.array(h, dtype='float32')
            prediction = self.model.predict(n)
            predicted_direction = np.argmax(prediction)
            if predicted_direction == 0:
                sell += 1
            elif predicted_direction == 1:
                buy += 1
            else:
                pass
        if buy > sell:
            return 'buy'
        else:
            return 'sell'



