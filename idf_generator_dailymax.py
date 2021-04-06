import pandas as pd
from functions_treatment import *
from functions_get_distribution import *
from scipy.optimize import minimize_scalar


def get_theoretical_max_precipitations(name_file, MY_DISTRIBUTIONS, return_period_list, plot_graph = False):
    data_df_original = pd.read_csv('Results/max_daily_{n}_2.csv'.format(n = name_file))
     
    data_df_2 = data_df_original.sort_values('Precipitation', ascending=False).reset_index()[['Year', 'Precipitation']].reset_index()
    data_df_2['Frequency'] = (data_df_2['index'] + 1)/(len(data_df_2)+1)
    data_df_2['RP'] = 1/data_df_2['Frequency']
    #print(data_df_2)
     
    data_df = data_df_original[['Precipitation']]
    mean = data_df.iloc[:,0].mean()
    data = data_df.values.ravel()
    #print(data)
     
    #MY_DISTRIBUTIONS = [st.norm, st.lognorm, st.genextreme, st.gumbel_r]
    
    results = fit_data(data, MY_DISTRIBUTIONS) ## Usar qdo nao eh GEV para INMET_aut
    #df_parameters = get_parameters(data, results, 5) ## Usar qdo nao eh GEV para INMET_aut
    df_parameters = pd.read_csv('Results/INMET_aut_GEV_params.csv') ##Usar qdo eh GEV para INMET_aut
    #print(df_parameters)
    #input()
     
    dist = MY_DISTRIBUTIONS[0]
    c = df_parameters['c'][0]
    loc = df_parameters['loc'][0]
    scale = df_parameters['scale'][0]
    #print(c, loc, scale)
    
    if math.isnan(c) == True:
        prob_function_obj = dist(loc, scale)
    else:
        prob_function_obj = dist(c, loc, scale)

    #x_in = np.linspace(0,1,200)
    RP_list = return_period_list
    probabilities = [1 - 1/RP for RP in RP_list]
    #print(probabilities)
    precipitations_dist = prob_function_obj.ppf(probabilities)
    #print(y_out)
    if plot_graph == True:
        if dist == st.gumbel_r:
            dist_n = 'Gumbell'
        elif dist == st.lognorm:
            dist_n = 'Lognormal'
        elif dist == st.genextreme:
            dist_n = 'GEV'
        elif dist == st.norm:
            dist_n = 'Normal'
        elif dist == st.genlogistic:
            dist_n = 'Generalized Logistic'
        else:
            dist_n = dist
            
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(RP_list, precipitations_dist) # graphically check the results of the inverse CDF
        ax.plot(data_df_2['RP'], data_df_2['Precipitation'])
        ax.set(ylabel = 'Precipitation (mm)', xlabel = 'Return Period (Years)', title = dist_n)
        #ax.grid(color = 'gray')
        #ax.set_facecolor('white')
        plt.show()
        fig.savefig('Graphs/distributions/quantile_plot_{n}_{d}.png'.format(n = name_file, d = dist_n))

    return precipitations_dist

def get_idf_table(name_file, MY_DISTRIBUTIONS, name_disag_file, disag_type, dist, save_table = False):
    df_disagreg_factors = pd.read_csv('{n}.csv'.format(n = name_disag_file))
    disagreg_factors_list = df_disagreg_factors['CETESB_ger'].to_list()
    duration = df_disagreg_factors['Min/day'].to_list()
    #print(disagreg_factors_list)
    #print(duration)
    return_period_list = [1.1, 2, 5, 10, 25, 50, 100]
    
    precipitations_dist = get_theoretical_max_precipitations(name_file, MY_DISTRIBUTIONS, return_period_list)
    P_2Years = precipitations_dist[1]
    P_RP_2Years = [P_2Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_2Years = [P*60/d for P, d in zip(P_RP_2Years, duration)] 
    ln_i_RP_2Years = [np.log(i) for i in i_RP_2Years]
    
    P_5Years = precipitations_dist[2]
    P_RP_5Years = [P_5Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_5Years = [P*60/d for P, d in zip(P_RP_5Years, duration)] 
    ln_i_RP_5Years = [np.log(i) for i in i_RP_5Years]
    
    P_10Years = precipitations_dist[3]
    P_RP_10Years = [P_10Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_10Years = [P*60/d for P, d in zip(P_RP_10Years, duration)] 
    ln_i_RP_10Years = [np.log(i) for i in i_RP_10Years]
    
    P_25Years = precipitations_dist[4]
    P_RP_25Years = [P_25Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_25Years = [P*60/d for P, d in zip(P_RP_25Years, duration)] 
    ln_i_RP_25Years = [np.log(i) for i in i_RP_25Years]
    
    P_50Years = precipitations_dist[5]
    P_RP_50Years = [P_50Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_50Years = [P*60/d for P, d in zip(P_RP_50Years, duration)] 
    ln_i_RP_50Years = [np.log(i) for i in i_RP_50Years]
    
    P_100Years = precipitations_dist[6]
    P_RP_100Years = [P_100Years*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_100Years = [P*60/d for P, d in zip(P_RP_100Years, duration)] 
    ln_i_RP_100Years = [np.log(i) for i in i_RP_100Years]
    
    if save_table == True:
        dict_ = {'duration' : duration,
                'P_RP_2Years' : P_RP_2Years, 
                'P_RP_5Years' : P_RP_5Years, 
                'P_RP_10Years' : P_RP_10Years, 
                'P_RP_25Years' : P_RP_25Years,
                'P_RP_50Years' : P_RP_50Years,
                'P_RP_100Years' : P_RP_100Years, 
                'i_RP_2Years' : i_RP_2Years,
                'i_RP_5Years' : i_RP_5Years,
                'i_RP_10Years' : i_RP_10Years,
                'i_RP_25Years' : i_RP_25Years,
                'i_RP_50Years' : i_RP_50Years,
                'i_RP_100Years' : i_RP_100Years
            }
        df = pd.DataFrame(dict_)
        df.to_csv('Results/IDF_table_{n}_{dist}_{disag}.csv'.format(n = name_file, dist = distribution, disag = disag_type), index = False)
    
    return duration, ln_i_RP_2Years, ln_i_RP_5Years, ln_i_RP_10Years, ln_i_RP_25Years, ln_i_RP_50Years, ln_i_RP_100Years

def get_idf_for_fit(name_file, MY_DISTRIBUTIONS, name_disag_file, return_period_list):
    df_disagreg_factors = pd.read_csv('{n}.csv'.format(n = name_disag_file))
    disagreg_factors_list = df_disagreg_factors['CETESB_ger'].to_list()
    duration = df_disagreg_factors['Min/day'].to_list()
    #print(disagreg_factors_list)
    #print(duration)
    
    precipitations_dist = get_theoretical_max_precipitations(name_file, MY_DISTRIBUTIONS, return_period_list)
    P_ = precipitations_dist[0]
    P_RP_ = [P_*disag_factor for disag_factor in disagreg_factors_list]
    i_RP_ = [P*60/d for P, d in zip(P_RP_, duration)] 
    ln_i_RP_ = [np.log(i) for i in i_RP_]
    
    return duration, ln_i_RP_


def get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, return_period_list):
    duration, ln_i_RP_ = get_idf_for_fit(name_file, MY_DISTRIBUTIONS, name_disag_file, return_period_list)
    
    ln_cte_list = [np.log(t0+d) for d in duration] #cte = ln(d * t0) (for IDF linearization)
    
    x = np.array(ln_cte_list).reshape((-1, 1))
    y = np.array(ln_i_RP_)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    ln_cte2 = model.intercept_
    n = model.coef_[0] 
    return r_sq, ln_cte2, n

def min_sum_r_sq(t0):
    r_sq_2 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [2])[0]
    r_sq_5 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [5])[0]
    r_sq_10 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [10])[0]
    r_sq_25 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [25])[0]
    r_sq_50 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [50])[0]
    r_sq_100 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [100])[0]
    
    sum = r_sq_2 + r_sq_5 + r_sq_10 + r_sq_25 + r_sq_50 + r_sq_100
    return -sum

def get_t0(name_file, MY_DISTRIBUTIONS, name_disag_file):
    res = minimize_scalar(min_sum_r_sq)
    return res.x

def get_idf_params2(t0, name_file, MY_DISTRIBUTIONS, name_disag_file):
    ln_cte2_list = []
    ln_cte2_2 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [2])[1]
    ln_cte2_list.append(ln_cte2_2)
    ln_cte2_5 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [5])[1]
    ln_cte2_list.append(ln_cte2_5)
    ln_cte2_10 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [10])[1]
    ln_cte2_list.append(ln_cte2_10)
    ln_cte2_25 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [25])[1]
    ln_cte2_list.append(ln_cte2_25)
    ln_cte2_50 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [50])[1]
    ln_cte2_list.append(ln_cte2_50)
    ln_cte2_100 = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [100])[1]
    ln_cte2_list.append(ln_cte2_100)
    #print(ln_cte2_list)
    return_period_list = [2, 5, 10, 25, 50, 100]

    ln_RP_list = [np.log(RP) for RP in return_period_list] 
    #print(ln_RP_list)
    
    x = np.array(ln_RP_list).reshape((-1, 1))
    y = np.array(ln_cte2_list)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    ln_K = model.intercept_
    K = np.exp(ln_K)
    m = model.coef_[0] 
    
    return r_sq, K, m    

def get_final_idf_params(name_file, MY_DISTRIBUTIONS, name_disag_file, save_file = False):
    #t0 = 11.827
    t0 = get_t0(name_file, MY_DISTRIBUTIONS, name_disag_file)
    n = get_idf_params1(t0, name_file, MY_DISTRIBUTIONS, name_disag_file, [2])[2]
    n = abs(n)
    #print(t0, n)
    K = get_idf_params2(t0, name_file, MY_DISTRIBUTIONS, name_disag_file)[1]
    m = get_idf_params2(t0, name_file, MY_DISTRIBUTIONS, name_disag_file)[2]
    #print(K, m)
    
    if save_file == True:
        dict_ = {'t0' : t0,
                'n' : n, 
                'K' : K, 
                'm' : m
                }
        df = pd.DataFrame(dict_)
        df.to_csv('Results/IDF_params_{n}.csv'.format(n = name_file), index = False)        
    
    return t0, n, K, m

if __name__ == '__main__':
    name_file = 'INMET_aut'
    MY_DISTRIBUTIONS = [st.genextreme]  ##Para INMET_aut GEV peguei os valores dos parametros do R
    name_disag_file = 'fatores_desagregacao_opt'
    disag_type = 'opt'
    distribution = 'GEV'
    return_period_list = [1.1, 2, 5, 10, 25, 50, 100]  ## Default return_period_list for get_idf_table
    get_theoretical_max_precipitations(name_file, MY_DISTRIBUTIONS, return_period_list, plot_graph = True)
    get_idf_table(name_file, MY_DISTRIBUTIONS, name_disag_file, disag_type, distribution, save_table = True)
    t0, n, K, m = get_final_idf_params(name_file, MY_DISTRIBUTIONS, name_disag_file)
    print('K: ', K)
    print('t0: ', t0)
    print(' m: ', m)
    print('n: ', n)