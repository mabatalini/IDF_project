import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from sklearn.linear_model import LinearRegression


def get_idf_for_fit(name_file, return_period):
    df = pd.read_csv(name_file)
    #print(df)    
    i_RP_ = df['i_RP_{rp}Years'.format(rp = return_period)].to_list()
    ln_i_RP_ = [np.log(i) for i in i_RP_]
    duration = df['duration'].to_list()

    return duration, ln_i_RP_


def get_idf_params1(t0, name_file, return_period):
    duration, ln_i_RP_ = get_idf_for_fit(name_file, return_period)
    
    ln_cte_list = [np.log(t0+d) for d in duration] #cte = ln(d * t0) (for IDF linearization)
    
    x = np.array(ln_cte_list).reshape((-1, 1))
    y = np.array(ln_i_RP_)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    ln_cte2 = model.intercept_
    n = model.coef_[0] 
    return r_sq, ln_cte2, n

def min_sum_r_sq(t0):
    r_sq_2 = get_idf_params1(t0, name_file, 2)[0]
    r_sq_5 = get_idf_params1(t0, name_file, 5)[0]
    r_sq_10 = get_idf_params1(t0, name_file, 10)[0]
    r_sq_25 = get_idf_params1(t0, name_file, 25)[0]
    r_sq_50 = get_idf_params1(t0, name_file, 50)[0]
    r_sq_100 = get_idf_params1(t0, name_file, 100)[0]
    
    sum = r_sq_2 + r_sq_5 + r_sq_10 + r_sq_25 + r_sq_50 + r_sq_100
    return -sum

def get_t0(name_file):
    res = minimize_scalar(min_sum_r_sq)
    return res.x

def get_idf_params2(t0, name_file):
    ln_cte2_list = []
    ln_cte2_2 = get_idf_params1(t0, name_file, 2)[1]
    ln_cte2_list.append(ln_cte2_2)
    ln_cte2_5 = get_idf_params1(t0, name_file, 5)[1]
    ln_cte2_list.append(ln_cte2_5)
    ln_cte2_10 = get_idf_params1(t0, name_file, 10)[1]
    ln_cte2_list.append(ln_cte2_10)
    ln_cte2_25 = get_idf_params1(t0, name_file, 25)[1]
    ln_cte2_list.append(ln_cte2_25)
    ln_cte2_50 = get_idf_params1(t0, name_file, 50)[1]
    ln_cte2_list.append(ln_cte2_50)
    ln_cte2_100 = get_idf_params1(t0, name_file, 100)[1]
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

def get_final_idf_params(name_file, id_file = 'INMET_average', save_file = False):
    #t0 = 11.827
    t0 = get_t0(name_file)
    n = get_idf_params1(t0, name_file, 2)[2]
    n = abs(n)
    #print(t0, n)
    K = get_idf_params2(t0, name_file)[1]
    m = get_idf_params2(t0, name_file)[2]
    #print(K, m)
    
    if save_file == True:
        dict_ = {'t0' : t0,
                'n' : n, 
                'K' : K, 
                'm' : m
                }
        df = pd.DataFrame(dict_)
        df.to_csv('Results/IDF_params_{n}.csv'.format(n = id_file), index = False)        
    
    return t0, n, K, m

if __name__ == '__main__':
    name_file = 'Results/IDF_table_INMET_GenLogistic_average.csv'
   
    t0, n, K, m = get_final_idf_params(name_file)

    print('K: ', K)
    print('t0: ', t0)
    print(' m: ', m)
    print('n: ', n)

    