from functions_treatment import *
from scipy.stats import gumbel_r
from scipy.stats import genextreme
from scipy.stats import lognorm
from scipy.stats import norm
from scipy.stats import genpareto
from scipy import stats

#Funcao para obter maximos anuais e remocao de outliers
def max_annual_precipitation(df):
    df = df.dropna()
    df_new = df.groupby(['Year'])['Precipitation'].max().reset_index()
    #med = df_new['Precipitation'].median()
    q1 = df_new['Precipitation'].quantile(0.25)
    q3 = df_new['Precipitation'].quantile(0.75)
    IQR =  q3 - q1
    L0 = IQR*1.5
    L_low = q1 - L0
    L_high = q3 + L0
    #print(L_low, L_high)
    df_new = df_new[df_new.Precipitation > L_low]
    df_new = df_new[df_new.Precipitation < L_high]
    
    return df_new

def df_to_lists(df):
    df = df['Precipitation'].sort_values().reset_index()
    #print(df)
    mean = df['Precipitation'].mean()
    std = df['Precipitation'].std()
    max = df['Precipitation'].max()
    min = df['Precipitation'].min()
    total = df['Precipitation'].count()

    data = df['Precipitation'].tolist()
    x = np.linspace(max, min, total)  
    return data, x

def get_fit_params(df, dist):
    data, x = df_to_lists(df)
    
    if dist == 'Gumbel':
        c = ''
        loc, scale = gumbel_r.fit(data)
    if dist == 'GEV':
        c, loc, scale = genextreme.fit(data)
    if dist == 'LogNormal':
        c, loc, scale = lognorm.fit(data)
    if dist == 'Normal':
        c = ''
        loc, scale = norm.fit(data)
    if dist == 'GPD':
        c, loc, scale = genpareto.fit(data)
    
    return c, loc, scale

def get_pdf(df, dist):
    data, x = df_to_lists(df)
    
    if dist == 'Gumbel':
        c, loc, scale = get_fit_params(df, dist)
        y_pdf = gumbel_r.pdf(data, loc, scale)
    if dist == 'GEV':
        c, loc, scale = get_fit_params(df, dist)
        y_pdf = genextreme.pdf(data, c, loc, scale)
    if dist == 'LogNormal':
        c, loc, scale = get_fit_params(df, dist)
        y_pdf = lognorm.pdf(data, c, loc, scale)
    if dist == 'Normal':
        c, loc, scale = get_fit_params(df, dist)
        y_pdf = norm.pdf(data, loc, scale)
    if dist == 'GPD':
        c, loc, scale = get_fit_params(df, dist)
        y_pdf = genpareto.pdf(data, c, loc, scale)
    
    return y_pdf

def get_cdf(df, dist):
    data, x = df_to_lists(df)
    
    if dist == 'Gumbel':
        c, loc, scale = get_fit_params(df, dist)
        y_cdf = gumbel_r.cdf(data, loc, scale)
    if dist == 'GEV':
        c, loc, scale = get_fit_params(df, dist)
        y_cdf = genextreme.cdf(data, c, loc, scale)
    if dist == 'LogNormal':
        c, loc, scale = get_fit_params(df, dist)
        y_cdf = lognorm.cdf(data, c, loc, scale)
    if dist == 'Normal':
        c, loc, scale = get_fit_params(df, dist)
        y_cdf = norm.cdf(data, loc, scale)
    if dist == 'GPD':
        c, loc, scale = get_fit_params(df, dist)
        y_cdf = genpareto.cdf(c, data, loc, scale)
    
    return y_cdf

def plot_hist (df):
    data, x = df_to_lists(df)
    sns.histplot(data, stat="density", bins = 30)
    #plt.hist(data, density=True, histtype='stepfilled', alpha=0.2)
    
def plot_pdf(df, dist):
    data, x = df_to_lists(df)
    #print(data)
    y_pdf = get_pdf(df, dist)
    plt.plot(data, y_pdf, label = 'loc x scale')
    plt.title(dist)
    #plt.show()

def plot_cdf(df, dist):
    data, x = df_to_lists(df)
    y_cdf = get_cdf(df, dist)
    plt.plot(data, y_cdf, label = 'loc x scale')
    plt.title(dist)
    #plt.show()
     
def KS_goodness_of_fit(df, dist):
    data, x = df_to_lists(df)
    #print(data)
    cdf = get_cdf(df, dist)
    print(stats.kstest(data, 'norm'))

    
    
    
    
    
if __name__ == '__main__':
    print('Starting..')
    print('')
    
    df_conv = read_csv('INMET_conv', 'daily')
    #df_aut, df_conv = treat_INMET_daily()
           
    df = max_annual_precipitation(df_conv)
    df.to_csv('Results/max_daily.csv')
    #print(df)
    plot_hist(df)
    #plt.show()
    plot_pdf(df, 'Normal')      ## Olha so o ajuste ai comparado com o histograma, ta dando pessimo
    #plot_pdf(df, 'GPD')        ##Pareto ta dando zuado
    plot_pdf(df, 'GEV')         ## Normal eh o azul, GEV eh o verde
    
    plt.show()
    #s, pvalue = KS_goodness_of_fit(df, 'GEV')
    #print(s, pvalue)

    print('')
    print('Done!')