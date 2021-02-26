import numpy as np
import pandas as pd
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
import scipy
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
import pymannkendall as mk
import statsmodels.api as sm

def treat_CEMADEN():
    for i in range(0, 62):
        if i == 0:
            CEMADEN_df = pd.read_csv('CEMADEN/data ({n}).csv'.format(n = i), sep = ';')
            #print(CEMADEN_df)
            #input()
        else:
            df = pd.read_csv('CEMADEN/data ({n}).csv'.format(n = i), sep = ';')
            CEMADEN_df = pd.concat([CEMADEN_df, df], ignore_index=True, sort=False)
            #print(CEMADEN_df)
            #input()
    
    CEMADEN_df.columns = ['1', '2', '3', '4', '5', '6', '7', '8']
    CEMADEN_df = CEMADEN_df[['5', '6', '7']]
    CEMADEN_df.columns = ['Site', 'Date', 'Precipitation']
    CEMADEN_df['Precipitation'] = CEMADEN_df['Precipitation'].str.replace(',', '.')
    CEMADEN_df['Site'] = CEMADEN_df['Site'].str.replace('-22,031', 'Jd_Sao_Paulo')
    CEMADEN_df['Site'] = CEMADEN_df['Site'].str.replace('-21,997', 'Cidade_Jardim')
    CEMADEN_df['Site'] = CEMADEN_df['Site'].str.replace('-21,898', 'Agua_Vermelha')
    CEMADEN_df[['Year', 'Month', 'Day_hour']] = CEMADEN_df.Date.str.split("-", expand=True)
    CEMADEN_df[['Day', 'Hour_min']] = CEMADEN_df.Day_hour.str.split(" ", expand=True)
    CEMADEN_df[['Hour', 'Min', 'Seg']] = CEMADEN_df.Hour_min.str.split(":", expand=True)
    CEMADEN_df = CEMADEN_df[['Site', 'Year', 'Month', 'Day', 'Hour', 'Precipitation']]
    CEMADEN_df['Precipitation'] = pd.to_numeric(CEMADEN_df['Precipitation'])
    CEMADEN_df['Year'] = pd.to_numeric(CEMADEN_df['Year'], downcast='integer')
    CEMADEN_df['Month'] = pd.to_numeric(CEMADEN_df['Month'], downcast='integer')
    CEMADEN_df['Day'] = pd.to_numeric(CEMADEN_df['Day'], downcast='integer')
    CEMADEN_df['Hour'] = pd.to_numeric(CEMADEN_df['Hour'], downcast='integer')
    
    #print(CEMADEN_df.head())
    #print(is_string_dtype(CEMADEN_df['Year']))
    
    jd_sp = CEMADEN_df[CEMADEN_df['Site']=='Jd_Sao_Paulo']
    cidade_jardim = CEMADEN_df[CEMADEN_df['Site']=='Cidade_Jardim']
    agua_vermelha = CEMADEN_df[CEMADEN_df['Site']=='Agua_Vermelha']
    
    return jd_sp, cidade_jardim, agua_vermelha

def treat_INMET():
    INMET_aut_df = pd.read_csv('INMET/data_aut_8h.csv', sep = ';')
    INMET_aut_df.columns = ['Date', 'Hour', 'Precipitation', 'Null']
    INMET_aut_df = INMET_aut_df[['Date', 'Hour', 'Precipitation']]
    INMET_aut_df[['Year', 'Month', 'Day']] = INMET_aut_df.Date.str.split("-", expand=True)
    INMET_aut_df['Hour'] = (INMET_aut_df['Hour']/100)
    INMET_aut_df = INMET_aut_df[['Year', 'Month', 'Day', 'Hour', 'Precipitation']]
    INMET_aut_df['Hour'] = pd.to_numeric(INMET_aut_df['Hour'], downcast='integer')
    INMET_aut_df['Year'] = pd.to_numeric(INMET_aut_df['Year'], downcast='integer')
    INMET_aut_df['Month'] = pd.to_numeric(INMET_aut_df['Month'], downcast='integer')
    INMET_aut_df['Day'] = pd.to_numeric(INMET_aut_df['Day'], downcast='integer')
    #print(INMET_aut_df)

    INMET_conv_df = pd.read_csv('INMET/data_conv_8h.csv', sep = ';')
    INMET_conv_df.columns = ['Date', 'Hour', 'Precipitation', 'Null']
    INMET_conv_df = INMET_conv_df[['Date', 'Hour', 'Precipitation']]
    INMET_conv_df[['Year', 'Month', 'Day']] = INMET_conv_df.Date.str.split("-", expand=True)
    INMET_conv_df['Hour'] = (INMET_conv_df['Hour']/100)
    INMET_conv_df = INMET_conv_df[['Year', 'Month', 'Day', 'Hour', 'Precipitation']]
    INMET_conv_df['Hour'] = pd.to_numeric(INMET_conv_df['Hour'], downcast='integer')
    INMET_conv_df['Year'] = pd.to_numeric(INMET_conv_df['Year'], downcast='integer')
    INMET_conv_df['Month'] = pd.to_numeric(INMET_conv_df['Month'], downcast='integer')
    INMET_conv_df['Day'] = pd.to_numeric(INMET_conv_df['Day'], downcast='integer')
    #print(INMET_conv_df)
    
    return INMET_aut_df, INMET_conv_df

def treat_INMET_daily():
    INMET_aut_df = pd.read_csv('INMET/data_aut_daily.csv', sep = ';') 
    INMET_aut_df.columns = ['Date', 'Precipitation', 'Null']
    INMET_aut_df = INMET_aut_df[['Date', 'Precipitation']]
    INMET_aut_df[['Year', 'Month', 'Day']] = INMET_aut_df.Date.str.split("-", expand=True)
    INMET_aut_df['Year'] = pd.to_numeric(INMET_aut_df['Year'], downcast='integer')
    INMET_aut_df['Month'] = pd.to_numeric(INMET_aut_df['Month'], downcast='integer')
    INMET_aut_df['Day'] = pd.to_numeric(INMET_aut_df['Day'], downcast='integer')
    
    INMET_conv_df = pd.read_csv('INMET/data_conv_daily.csv', sep = ';') 
    INMET_conv_df.columns = ['Date', 'Precipitation', 'Null']
    INMET_conv_df = INMET_conv_df[['Date', 'Precipitation']]
    INMET_conv_df[['Year', 'Month', 'Day']] = INMET_conv_df.Date.str.split("-", expand=True)
    INMET_conv_df['Year'] = pd.to_numeric(INMET_conv_df['Year'], downcast='integer')
    INMET_conv_df['Month'] = pd.to_numeric(INMET_conv_df['Month'], downcast='integer')
    INMET_conv_df['Day'] = pd.to_numeric(INMET_conv_df['Day'], downcast='integer')
    #print(INMET_conv_df)
    
    return INMET_aut_df, INMET_conv_df

def treat_MAPLU():
    for i in range(2015, 2019):
        if i == 2015:
            MAPLU_esc_df = pd.read_csv('MAPLU/escola{n}.csv'.format(n = i))
            #print(MAPLU_esc_df)
            #input()
            MAPLU_esc_df['Site'] = MAPLU_esc_df['Site'].str.replace('escola{n}'.format(n = i), 'Escola Sao Bento')
            
        else:
            df = pd.read_csv('MAPLU/escola{n}.csv'.format(n = i))
            MAPLU_esc_df = pd.concat([MAPLU_esc_df, df], ignore_index=True, sort=False)
            MAPLU_esc_df['Site'] = MAPLU_esc_df['Site'].str.replace('escola{n}'.format(n = i), 'Escola Sao Bento')
            #print(MAPLU_esc_df)
            #input()
    
    MAPLU_esc_df.columns = ['Site', 'Date', 'Precipitation']
    MAPLU_esc_df[['Year', 'Month', 'Day_hour']] = MAPLU_esc_df.Date.str.split("-", expand=True)
    MAPLU_esc_df[['Day', 'Hour_min']] = MAPLU_esc_df.Day_hour.str.split(" ", expand=True)
    MAPLU_esc_df[['Hour', 'Min']] = MAPLU_esc_df.Hour_min.str.split(":", expand=True)
    MAPLU_esc_df = MAPLU_esc_df[['Site', 'Year', 'Month', 'Day', 'Hour', 'Min', 'Precipitation']]
    MAPLU_esc_df['Precipitation'] = pd.to_numeric(MAPLU_esc_df['Precipitation'])
    MAPLU_esc_df['Year'] = pd.to_numeric(MAPLU_esc_df['Year'], downcast='integer')
    MAPLU_esc_df['Month'] = pd.to_numeric(MAPLU_esc_df['Month'], downcast='integer')
    MAPLU_esc_df['Day'] = pd.to_numeric(MAPLU_esc_df['Day'], downcast='integer')
    MAPLU_esc_df['Hour'] = pd.to_numeric(MAPLU_esc_df['Hour'], downcast='integer')
    MAPLU_esc_df['Min'] = pd.to_numeric(MAPLU_esc_df['Min'], downcast='integer')
    #print(MAPLU_esc_df)
    
    for i in range(2015, 2019):
        if i == 2015:
            MAPLU_post_df = pd.read_csv('MAPLU/postosaude{n}.csv'.format(n = i))
            #print(MAPLU_post_df)
            #input()
            MAPLU_post_df['Site'] = MAPLU_post_df['Site'].str.replace('postosaude{n}'.format(n = i), 'Posto Santa Felicia')
            
        else:
            df = pd.read_csv('MAPLU/postosaude{n}.csv'.format(n = i))
            MAPLU_post_df = pd.concat([MAPLU_post_df, df], ignore_index=True, sort=False)
            MAPLU_post_df['Site'] = MAPLU_post_df['Site'].str.replace('postosaude{n}'.format(n = i), 'Posto Santa Felicia')
            #print(MAPLU_post_df)
            #input()
    
    MAPLU_post_df.columns = ['Site', 'Date', 'Precipitation']
    MAPLU_post_df[['Year', 'Month', 'Day_hour']] = MAPLU_post_df.Date.str.split("-", expand=True)
    MAPLU_post_df[['Day', 'Hour_min']] = MAPLU_post_df.Day_hour.str.split(" ", expand=True)
    MAPLU_post_df[['Hour', 'Min']] = MAPLU_post_df.Hour_min.str.split(":", expand=True)
    MAPLU_post_df = MAPLU_post_df[['Site', 'Year', 'Month', 'Day', 'Hour', 'Min', 'Precipitation']]
    MAPLU_post_df['Precipitation'] = pd.to_numeric(MAPLU_post_df['Precipitation'])
    MAPLU_post_df['Year'] = pd.to_numeric(MAPLU_post_df['Year'], downcast='integer')
    MAPLU_post_df['Month'] = pd.to_numeric(MAPLU_post_df['Month'], downcast='integer')
    MAPLU_post_df['Day'] = pd.to_numeric(MAPLU_post_df['Day'], downcast='integer')
    MAPLU_post_df['Hour'] = pd.to_numeric(MAPLU_post_df['Hour'], downcast='integer')
    MAPLU_post_df['Min'] = pd.to_numeric(MAPLU_post_df['Min'], downcast='integer')
    #print(MAPLU_post_df)
    
    return MAPLU_esc_df, MAPLU_post_df

def aggregate(df, var):
    if var == 'Year':
        df_new = df.groupby([var]).Precipitation.sum().reset_index()
    if var == 'Month':
        df_new = df.groupby(['Year',var]).Precipitation.sum().reset_index()
    if var == 'Day':
        df_new = df.groupby(['Year', 'Month', var]).Precipitation.sum().reset_index()
    if var == 'Hour':
        df_new = df.groupby(['Year', 'Month', 'Day', var]).Precipitation.sum().reset_index()
    
    return df_new

def aggregate_to_csv(df, name):
    df_yearly = aggregate(df, 'Year')
    df_yearly.to_csv('Results/{n}_yearly.csv'.format(n = name), index = False)
    df_monthly = aggregate(df, 'Month')
    df_monthly.to_csv('Results/{n}_monthly.csv'.format(n = name), index = False)
    df_daily = aggregate(df, 'Day')
    df_daily.to_csv('Results/{n}_daily.csv'.format(n = name), index = False)
    df.to_csv('Results/{n}_hourly.csv'.format(n = name), index = False)

def aggregate_hourly_to_csv(df, name):
    df_hourly = aggregate(df, 'Hour')
    df_hourly.to_csv('Results/{n}_hourly.csv'.format(n = name), index = False)
    df.to_csv('Results/{n}_min.csv'.format(n = name), index = False)
    
def read_csv(name, var):
    df = pd.read_csv('Results/{n}_{v}.csv'.format(n = name, v = var))
    
    return df

def verification(name):
    df = name
    year_0 = df['Year'][0]
    year_i = df['Year'][len(df)-1]
    month_0 = df['Month'][0]
    month_i = df['Month'][len(df)-1]
    day_0 = df['Day'][0]
    day_i = df['Day'][len(df)-1]
    
    d0 = date(year_0, month_0, day_0)
    di = date(year_i, month_i, day_i)
    #print(d0)
    delta = di - d0
    ndays_verification = delta.days
    #print(ndays_verification)
    ndays_real = len(df)
    #ndays_real2 = df['Precipitation'].isnull().sum()
    #print(ndays_real)
    
    verif_number = ndays_verification - ndays_real
    if verif_number > 0:
        print('Fail - series incomplete / number of days missing = {d}'.format(d = verif_number))
    else:
        print('Series complete')
        
def set_date(name):
    df = name
    
    date_list = []
    for i in range(0, len(df)):
        year_i = df['Year'][i]
        #print(year_i)
        month_i = df['Month'][i]
        #print(month_i)
        day_i = df['Day'][i]
        #print(day_i)           
        di = date(year_i, month_i, day_i)
        #print(di)
        date_list.append(di)
         
    #print(date_list)
    #input()
    df['Date'] = date_list
    #print(df)
    df = df.set_index('Date')
    df['Date'] = date_list
    #print(df)
     
    return df

def complete_date_series(name, var):
    n = name
    v = var
    df_original = read_csv('{n}'.format(n = name), '{v}'.format(v = var))
    df = set_date(df_original)
    #print(df)
    
    d0 = df['Date'][0]
    di = df['Date'][len(df)-1]
    #print(d0, di)
    idx = pd.date_range(d0, di)
    
    df.index = pd.DatetimeIndex(df.index)
    df = df.reindex(idx)
    df['Date'] = df.index
    return df

def left_join_precipitation(left_df, right_df1, right_df2):
    left_df2 = left_df.merge(right_df1, on = 'Date', how = 'inner')
    #print(left_df2)
    left_df_final = left_df2.merge(right_df2, on = 'Date', how = 'inner')
    #print(left_df_final)
    df = left_df_final[['Date', 'Precipitation_x', 'Precipitation_y', 'Precipitation']]
    df.columns = ['Date', 'P_left', 'P_right1', 'P_right2']
    #print(df)
    return df


def correlation_plots(left_df, right_df1, right_df2):
    df = left_join_precipitation(left_df, right_df1, right_df2)
    df = df[['P_left', 'P_right1', 'P_right2']]
    sns.pairplot(df)
    plt.show()
    corr_pearson = df.corr(method = 'pearson')
    pvalues_pearson = df.corr(method = pearsonr_pval)
    print('')
    print('----- Pearson correlation -----')
    print('Correlation coefficient matrix')
    print(corr_pearson)
    print('')
    print('P-values matrix')
    print(pvalues_pearson)
    
def pearsonr_pval(x,y):
    return pearsonr(x,y)[1]    

def simple_linear_regression(left_df, right_df1, right_df2):
    df = left_join_precipitation(left_df, right_df1, right_df2)
    df = df[['P_left', 'P_right1', 'P_right2']]
    df = df.dropna()
    X1 = df[['P_right1']]
    X2 = df[['P_right2']]
    y = df['P_left']

    
    lr = LinearRegression()
    lr.fit(X1, y)
    
    yhat = lr.predict(X1)
    
    slr_slope = lr.coef_
    slr_intercept = lr.intercept_
    print('R-Squared_1 :', lr.score(X1, y))
    
    sns.scatterplot(x = 'P_right1', y = 'P_left', data = df, s = 150, alpha = 0.3, edgecolor = 'white')
    plt.plot(df['P_right1'], slr_slope*df['P_right1'] + slr_intercept, color = 'r', linewidth = 3)
    plt.ylabel('P_left', fontsize = 12)
    plt.xlabel('P_right1', fontsize = 12)    
    plt.show()
    
    lr.fit(X2, y)
    
    yhat = lr.predict(X1)
    
    slr_slope = lr.coef_
    slr_intercept = lr.intercept_
    print('R-Squared_2 :', lr.score(X1, y))
    
    sns.scatterplot(x = 'P_right1', y = 'P_left', data = df, s = 150, alpha = 0.3, edgecolor = 'white')
    plt.plot(df['P_right1'], slr_slope*df['P_right1'] + slr_intercept, color = 'r', linewidth = 3)
    plt.ylabel('P_left', fontsize = 12)
    plt.xlabel('P_right1', fontsize = 12)    
    plt.show()
    
def multiple_linear_regression(left_df, right_df1, right_df2):
    df = left_join_precipitation(left_df, right_df1, right_df2)
    df = df[['P_left', 'P_right1', 'P_right2']]
    df = df.dropna()
    X1 = df[['P_right1', 'P_right2']]
    y = df['P_left']
    
    lr = LinearRegression()
    lr.fit(X1, y)

    yhat = lr.predict(X1)
    print('R-Squared_2 :', lr.score(X1, y))
    
    mlr_slope = lr.coef_
    mlr_intercept = lr.intercept_
    print(mlr_slope, mlr_intercept)        

def trend_analysis(data, alpha_value):
    fig, ax = plt.subplots(figsize=(12, 8))
    sm.graphics.tsa.plot_acf(data, lags=20, ax=ax)
    plt.show()
    
    result_original = mk.original_test(data, alpha = alpha_value)
    result_hamed_rao = mk.hamed_rao_modification_test(data, alpha = alpha_value)
    result_yue_wang = mk.yue_wang_modification_test(data, alpha = alpha_value)
    result_trend_free = mk.trend_free_pre_whitening_modification_test(data, alpha = alpha_value)
    result_pre_whitening = mk.pre_whitening_modification_test(data, alpha = alpha_value)
    
    print('Original: ', result_original)
    print('Hamed_rao: ', result_hamed_rao)
    print('Yue_wang: ', result_yue_wang)
    print('Trend_free:', result_trend_free)
    print('Pre_whitening: ', result_pre_whitening)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    #res = mk.hamed_rao_modification_test(data)
    res = mk.pre_whitening_modification_test(data, alpha = alpha_value)
    trend_line = np.arange(len(data)) * res.slope + res.intercept
    
    ax.plot(data)
    ax.plot(data.index, trend_line)
    ax.legend(['data', 'trend line'])
    plt.show()
    
def p90_function(data):
    df = data[['Precipitation']]
    df = df[df.Precipitation != 0]
    df = df.sort_values('Precipitation')
    df = df.reset_index(drop = True)
    df['Order'] = list(range(1,len(df)+1))
    max_order = df['Order'][len(df)-1]
    df['Probability'] = (df['Order']/max_order)*100
    df['Probability_round'] = round(df['Probability'], 0)
    df_new = df.query('Probability_round == 90')
    P90 = (df_new['Precipitation'].iloc[0])
    
    sns.lineplot(x = 'Probability', y = 'Precipitation', data = df, palette = 'Black')
    plt.ylabel('Precipitation (mm)', fontsize = 12)
    plt.xlabel('Probability (%)', fontsize = 12)    
    plt.show()
    plt.title("Probability of non-exceedence")
    
    return P90

def distribution_plot(name, var):
    df = read_csv('{n}'.format(n = name), '{v}'.format(v = var))
    df = df.dropna()
    sns.distplot(df['Precipitation'], color = 'skyblue')
    plt.title('{n} - {v}'.format(n = name, v = var))
    plt.show()
    
def distribution_plot_df(df):
    df = df.dropna()
    sns.distplot(df['Precipitation'], color = 'skyblue')
    plt.show()

if __name__ == '__main__':
    print('Starting..')
    jd_sp, cidade_jardim, agua_vermelha = treat_CEMADEN()
    INMET_aut, INMET_conv = treat_INMET()
    MAPLU_esc, MAPLU_post = treat_MAPLU()
    
    aggregate_to_csv(jd_sp, 'jd_sp') 
    aggregate_to_csv(cidade_jardim, 'cidade_jardim') 
    aggregate_to_csv(agua_vermelha, 'agua_vermelha') 
    aggregate_to_csv(INMET_aut, 'INMET_aut') 
    aggregate_to_csv(INMET_conv, 'INMET_conv')        
    aggregate_to_csv(MAPLU_esc, 'MAPLU_esc') 
    aggregate_to_csv(MAPLU_post, 'MAPLU_post')
    aggregate_hourly_to_csv(MAPLU_esc, 'MAPLU_esc') 
    aggregate_hourly_to_csv(MAPLU_post, 'MAPLU_post')
    
    print('Done!')  