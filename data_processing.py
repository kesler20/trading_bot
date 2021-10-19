import pandas as pd
import numpy as np
import datetime 
import time
import threading 
import statsmodels

class DataProcessing(object):

    def __init__(self, data):
        self.data = data

    def get_datetime_from_twelve(self):
        data = pd.DataFrame(self.data)
        data.to_csv('batch.csv')
        data = pd.read_csv('batch.csv')
        print(data)
        try:
            t = data.datetime
        except KeyError:
            t = data.date
        return t

    def get_ticker_from_twelve(self):
        data = pd.DataFrame(self.data)
        print(data)
        data.to_csv('batch.csv')
        data0 = pd.read_csv('batch.csv')
        data = data.columns
        return data0[data[0]]

    def real_data_to_double(self,real_data):
        float_data = [float(x) for x in real_data]
        np_float_data = np.array(float_data)
        return np_float_data  
    
    def generate_n_lenght_list(self, n):
        t = []
        null = [t.append(i) for i in range(n)]
        return t

    def list_of_zeros(self, value):
        list_of_zeroes = []
        empty_container = [list_of_zeroes.append(0) for x in range(len(value) + 1)]
        return list_of_zeroes, empty_container
    
    def series_to_list(self, series):
        list1 = []
        for i in series:
            list1.append(i)
        return list1

    def remove_repeats(self, list1):
        list2 = []
        for i in list1:
            if i in list2:
                pass
            else:
                list2.append(i)
        return list2

    def find_location(self, value):
        i = self.data.isin([value])
        c = 0
        t = 0
        for p in i:
            c += 1
            if p == True:
                t = c
            else:
                pass
        return t

    def Convert(self, tup, di): 
        for a, b in tup: 
            di.setdefault(a, []).append(b) 
        return di 
    
    def seperate_even_location_odd_location(self, v_):
        def is_odd(x):
            return x%2 != 0
        def is_even(x):
            return x%2 == 0

        odd = list(filter(is_odd, v_)) 
        even = list(filter(is_even, v_))
        # the filter method will return the value only if the predefined 
        # condition of the function past ass an argument is met
        return even, odd

    def get_rounded_date(self):
        todays_date = datetime.datetime.now()
        rounded_sec = round(int(todays_date.strftime('%S')))
        if rounded_sec < 10:
            rounded_sec = '0{}'.format(rounded_sec)
        rounded_date = todays_date.strftime('%y-%m-%d %H:%M:{}'.format(rounded_sec))

        return rounded_date

    def timer_decorator(self, func, *a, **kw):
        def wrapper(*a, **kw):
            start_time = time.time()
            container = func(*a, **kw)
            total_time = time.time() - start_time
            print(f'the function took {total_time} to run seconds')
            return container
        return wrapper          

    def count_down(self,t):
        while t:
            mins = t // 60
            secs = t % 60
            timer= '{:02d}:{:02d}'.format(mins,secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
    
    def clean_columns_and_dataframe(self,dirty_dataframe):
        dirty_columns = self.series_to_list(dirty_dataframe.columns)
        clean_columns = []
        #make condition for removing random column of rangeindex
        check_col0 = pd.DataFrame([i for i in range(len(dirty_dataframe))])
        try:
            condition = check_col0 - dirty_dataframe['0']
        except KeyError:
            condition = check_col0

        if 'date' in dirty_columns:
            print('date has been set as index from:', dirty_columns)
            try:
                dirty_dataframe.set_index('date', inplace=True)
            except KeyError:
                pass
        elif 'datetime' in dirty_columns:
            print('datetime has been set as index from:', dirty_columns)
            try:
                dirty_dataframe.set_index('datetime', inplace=True)
            except KeyError:
                pass
        else:
            pass

        dirty_dataframe.fillna(0, inplace=True)

        for column in dirty_columns:
            if column.startswith('Unnamed: 0'):
                pass
            elif column.startswith('0') and condition == 0:
                pass
            elif column.startswith('close'):
                pass
            else:
                clean_columns.append(column)
        print('these are the columns of the dataframe: ', clean_columns)
        return clean_columns
    
    def dataframe_generator(self,**kw):
        generator_list = []
        for key in kw:
            generator_list.append((key,kw[key]))
        generator = {}
        generator = self.Convert(generator_list, generator)
        for key in kw:
            generator[key] = generator[key][0]
        df = pd.DataFrame(generator)
        return df

    def to_dataframe_text(self, message):
        df = pd.read_csv(r'data for trading\stocks to remove.csv')
        new = self.series_to_list(df['Stocks_to_remove'])
        new.append(message)
        df = self.dataframe_generator(Stocks_to_remove=new)
        print(df)
        df.to_csv(r'data for trading\stocks to remove.csv')
    
    def pp(self,message):
        print_thread = threading.Thread(target=print, args=(message,))
        print_thread.start()
    
    def statsmodels_exog_error_decorator(func,*a,**kw):
        def wrapper(*a,**kw):
            try:
                container = func(*a,**kw)
            except statsmodels.tools.sm_exceptions.MissingDataError as err:
                print(err)
                container = None
            except TypeError as err:
                container = None
            return container
        return wrapper
