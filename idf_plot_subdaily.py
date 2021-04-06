import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

def get_df_to_plot(station_name, disag_factor, dist_type, save_table = False):
    
    if station_name == 'Base_IDF':
        df_idf_table = []
        df_IDF_params = pd.read_csv('IDF_params.csv')
        disag_factor = 'original'
        dist_type = 'Gumbel'
    elif station_name == 'INMET_aut_daily':
        df_idf_table = []
        df_IDF_params = pd.read_csv('IDF_params.csv')
        disag_factor = 'original'
        station_name = 'INMET_aut'        
    elif station_name == 'Average':
        df_idf_table = pd.read_csv('Results/IDF_table_INMET_GenLogistic_average.csv')
        df_IDF_params = pd.read_csv('IDF_params.csv')
        disag_factor = 'original'
        dist_type = 'GenLogistic'        
    else:
        if disag_factor == 'bl':
            df_idf_table = pd.read_csv('Results/IDF_tables_dist/IDFsubdaily_table_complete_{n}_{dist}_{disag}.csv'.format(n = station_name, dist = dist_type, disag = disag_factor))
            df_IDF_params = pd.read_csv('IDF_params_subdaily.csv')
            disag_factor = '_' + disag_factor
    
        else:
            df_idf_table = pd.read_csv('Results/IDF_tables_dist/IDFsubdaily_table_{n}_{dist}_{disag}.csv'.format(n = station_name, dist = dist_type, disag = disag_factor))
            df_IDF_params = pd.read_csv('IDF_params_subdaily.csv')
            disag_factor = '_' + disag_factor
    
    #print(df_IDF_params)
    #print(station_name)
    #print(disag_factor)
    #print(dist_type)
    df_selected = df_IDF_params.loc[df_IDF_params['Station'] == station_name]
    df_selected = df_selected.loc[df_selected['Disag_factors'] == disag_factor]
    df_selected = df_selected.loc[df_selected['Dist_Type'] == dist_type]
    df_selected = df_selected.reset_index()
    #print(disag_factor)
    #print(dist_type)
    #print(df_selected)
    K = df_selected['K'][0]
    t0 = df_selected['t0'][0]
    m = df_selected['m'][0]
    n = df_selected['n'][0]
    #input()
    return_period_list = [2, 5, 10, 25, 50, 100]
    if disag_factor == 'nan':
        duration_list = [10, 20, 30, 60, 180, 360, 480, 600, 720, 1440]
    else:
        duration_list = [5, 10, 20, 30, 60, 180, 360, 480, 600, 720, 1440]
    
    i_final = []
    P_final = []
    for RP in return_period_list:
        #print(RP)
        i_list = []
        P_list = []
        for d in duration_list:
            i_prec =  K*RP**m/(d + t0)**n
            i_list.append(i_prec)
            P = i_prec * d/60
            P_list.append(P)
        #print(i_list)
        #print(P_list)
        i_final.append(i_list)
        P_final.append(P_list)
     
    df_intensity = pd.DataFrame(i_final)
    df_intensity = df_intensity.transpose()
    df_intensity.columns = ['i_RP_2', 'i_RP_5', 'i_RP_10', 'i_RP_25', 'i_RP_50', 'i_RP_100']
    df_intensity['d'] = duration_list
     
    df_precipitation = pd.DataFrame(P_final)
    df_precipitation = df_precipitation.transpose()
    df_precipitation.columns = ['P_RP_2', 'P_RP_5', 'P_RP_10', 'P_RP_25', 'P_RP_50', 'P_RP_100']
    df_precipitation['d'] = duration_list
    
    #print(df_idf_table)
    if save_table == True:
        df_precipitation.to_csv('Results/IDF_tables_calc/{n}_{dis}_precipitationfromIDF_subdaily.csv'.format(n = station_name, dis = disag_factor), index = False)
        df_intensity.to_csv('Results/IDF_tables_calc/{n}_{dis}_intensityfromIDF_subdaily.csv'.format(n = station_name, dis = disag_factor), index = False)
    
    return df_idf_table, df_intensity, df_precipitation


def plot_comparison_IDF_disag_factors(station_name, dist_type):
    disag_factor = 'nan'
    data_observed,i_observed, p_observed = get_df_to_plot('INMET_aut', disag_factor, dist_type)
    
    disag_factor = 'ger'
    data_original,i_original, p_original = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'm0.2'
    data_m20, i_m20, p_m20 = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'p0.2'
    data_p20, i_p20, p_p20 = get_df_to_plot(station_name, disag_factor, dist_type)

    disag_factor = 'bl'
    data_bl, i_bl, p_bl = get_df_to_plot(station_name, disag_factor, dist_type)
    
    disag_factor = 'otimizado'
    data_opt, i_opt, p_opt = get_df_to_plot('INMET_aut', disag_factor, dist_type)
    
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,0].plot('d', 'i_RP_2', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,0].plot('d', 'i_RP_2', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,0].plot('d', 'i_RP_2', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,0].plot('d', 'i_RP_2', data = i_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,0].plot('d', 'i_RP_2', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,1].plot('d', 'i_RP_5', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,1].plot('d', 'i_RP_5', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,1].plot('d', 'i_RP_5', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,1].plot('d', 'i_RP_5', data = i_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,1].plot('d', 'i_RP_5', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'i_RP_10', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,2].plot('d', 'i_RP_10', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,2].plot('d', 'i_RP_10', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,2].plot('d', 'i_RP_10', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,2].plot('d', 'i_RP_10', data = i_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,2].plot('d', 'i_RP_10', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'i_RP_25', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,0].plot('d', 'i_RP_25', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,0].plot('d', 'i_RP_25', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,0].plot('d', 'i_RP_25', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,0].plot('d', 'i_RP_25', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'i_RP_50', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,1].plot('d', 'i_RP_50', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,1].plot('d', 'i_RP_50', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,1].plot('d', 'i_RP_50', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,1].plot('d', 'i_RP_50', data = i_bl, linestyle = '-', label = 'BL adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[1,1].plot('d', 'i_RP_50', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'i_RP_100', data = i_original, linestyle = '-', label = 'Original adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,2].plot('d', 'i_RP_100', data = i_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,2].plot('d', 'i_RP_100', data = i_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,2].plot('d', 'i_RP_100', data = i_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,2].plot('d', 'i_RP_100', data = i_bl, linestyle = '-', label = 'BL adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[1,2].plot('d', 'i_RP_100', data = i_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,2].set_title('RP = 100 years')
    #axs[1,2].legend(loc='upper right')
    #axs[1,2].legend(bbox_to_anchor=(-0.1, -0.05), fontsize='small', ncol=4)
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Intensity (mm/h)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_idf_subdaily_disag_{s}_{dist}_cbl.png'.format(s = station_name, dist = dist_type), dpi=300, format='png')

def plot_comparison_PDF_disag_factors(station_name, dist_type):
    disag_factor = 'nan'
    data_observed,i_observed, p_observed = get_df_to_plot('INMET_aut', disag_factor, dist_type)

    disag_factor = 'ger'
    data_original,i_original, p_original = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'm0.2'
    data_m20, i_m20, p_m20 = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'p0.2'
    data_p20, i_p20, p_p20 = get_df_to_plot(station_name, disag_factor, dist_type)
    
    disag_factor = 'bl'
    data_bl, i_bl, p_bl = get_df_to_plot(station_name, disag_factor, dist_type)
        
    disag_factor = 'otimizado'
    data_opt, i_opt, p_opt = get_df_to_plot('INMET_aut', disag_factor, dist_type)
    
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,0].plot('d', 'P_RP_2', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,0].plot('d', 'P_RP_2', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,0].plot('d', 'P_RP_2', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,0].plot('d', 'P_RP_2', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,0].plot('d', 'P_RP_2', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,1].plot('d', 'P_RP_5', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,1].plot('d', 'P_RP_5', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,1].plot('d', 'P_RP_5', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,1].plot('d', 'P_RP_5', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,1].plot('d', 'P_RP_5', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'P_RP_10', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_original, marker = 'o', label = 'Original points')
    axs[0,2].plot('d', 'P_RP_10', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,2].plot('d', 'P_RP_10', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,2].plot('d', 'P_RP_10', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[0,2].plot('d', 'P_RP_10', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[0,2].plot('d', 'P_RP_10', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'P_RP_25', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,0].plot('d', 'P_RP_25', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,0].plot('d', 'P_RP_25', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,0].plot('d', 'P_RP_25', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,0].plot('d', 'P_RP_25', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[1,0].plot('d', 'P_RP_25', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'P_RP_50', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,1].plot('d', 'P_RP_50', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,1].plot('d', 'P_RP_50', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,1].plot('d', 'P_RP_50', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,1].plot('d', 'P_RP_50', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[1,1].plot('d', 'P_RP_50', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'P_RP_100', data = p_original, linestyle = '-', label = 'Original adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_original, marker = 'o', label = 'Original points')
    axs[1,2].plot('d', 'P_RP_100', data = p_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,2].plot('d', 'P_RP_100', data = p_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,2].plot('d', 'P_RP_100', data = p_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_opt, marker = 'd', label = 'Optimized points')
    axs[1,2].plot('d', 'P_RP_100', data = p_bl, linestyle = '-', label = 'BL adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_bl, marker = 'd', label = 'BL points')
    axs[1,2].plot('d', 'P_RP_100', data = p_observed, linestyle = '-', label = 'Observed adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_observed, marker = 'd', label = 'Observed points')
    axs[1,2].set_title('RP = 100 years')
    #axs[1,2].legend(loc='upper right')
    #axs[1,2].legend(bbox_to_anchor=(-0.1, -0.05), fontsize='small', ncol=4)
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Precipitation (mm)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_pdf_subdaily_disag_{s}_{dist}_cbl.png'.format(s = station_name, dist = dist_type), dpi=300, format='png')
    
def plot_comparison_IDF_distributions(station_name, disag_factor):
    data_normal, i_normal, p_normal = get_df_to_plot(station_name, disag_factor, 'Normal')  
    data_GL, i_GL, p_GL = get_df_to_plot(station_name, disag_factor, 'GenLogistic')
    data_gumbel, i_gumbel, p_gumbel = get_df_to_plot(station_name, disag_factor, 'Gumbel') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,0].plot('d', 'i_RP_2', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,0].plot('d', 'i_RP_2', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,1].plot('d', 'i_RP_5', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,1].plot('d', 'i_RP_5', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'i_RP_10', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,2].plot('d', 'i_RP_10', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,2].plot('d', 'i_RP_10', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'i_RP_25', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,0].plot('d', 'i_RP_25', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[1,0].plot('d', 'i_RP_25', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'i_RP_50', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,1].plot('d', 'i_RP_50', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[1,1].plot('d', 'i_RP_50', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'i_RP_100', data = i_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,2].plot('d', 'i_RP_100', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[1,2].plot('d', 'i_RP_100', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Intensity (mm/h)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])

    fig.savefig('Graphs/IDF_plots/comparison_idf_subdaily_dist_{s}_{disag}_cbl.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')

def plot_comparison_PDF_distributions(station_name, disag_factor):
    data_normal, i_normal, p_normal = get_df_to_plot(station_name, disag_factor, 'Normal') 
    data_GL, i_GL, p_GL = get_df_to_plot(station_name, disag_factor, 'GenLogistic') 
    data_gumbel, i_gumbel, p_gumbel = get_df_to_plot(station_name, disag_factor, 'Gumbel') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,0].plot('d', 'P_RP_2', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,0].plot('d', 'P_RP_2', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,1].plot('d', 'P_RP_5', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,1].plot('d', 'P_RP_5', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'P_RP_10', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[0,2].plot('d', 'P_RP_10', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[0,2].plot('d', 'P_RP_10', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'P_RP_25', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,0].plot('d', 'P_RP_25', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,0].plot('d', 'P_RP_25', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'P_RP_50', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,1].plot('d', 'P_RP_50', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[1,1].plot('d', 'P_RP_50', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'P_RP_100', data = p_normal, linestyle = '-', label = 'Normal adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_normal, marker = 'o', label = 'Normal points')
    axs[1,2].plot('d', 'P_RP_100', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel, marker = 'v', label = 'Gumbel points')
    axs[1,2].plot('d', 'P_RP_100', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Precipitation (mm)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])

    fig.savefig('Graphs/IDF_plots/comparison_pdf_subdaily_dist_{s}_{disag}_cbl.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')


def plot_comparison_IDF_daily_subdaily(disag_factor, station_name = 'INMET_aut'):
    data_normal, i_normal, p_normal = get_df_to_plot('INMET_aut', disag_factor, 'Normal')  
    data_GL, i_GL, p_GL = get_df_to_plot('INMET_aut', disag_factor, 'GenLogistic')
    data_gumbel_daily, i_gumbel_daily, p_gumbel_daily = get_df_to_plot('INMET_aut_daily', 'original', 'Gumbel')
    data_GEV_daily, i_GEV_daily, p_GEV_daily = get_df_to_plot('INMET_aut_daily', 'original', 'GEV')
    data_GL_daily, i_GL_daily, p_GL_daily = get_df_to_plot('INMET_aut_daily', 'original', 'GenLogistic') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,0].plot('d', 'i_RP_2', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,0].plot('d', 'i_RP_2', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,0].plot('d', 'i_RP_2', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,0].plot('d', 'i_RP_2', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,1].plot('d', 'i_RP_5', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,1].plot('d', 'i_RP_5', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,1].plot('d', 'i_RP_5', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,1].plot('d', 'i_RP_5', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')

    axs[0,2].plot('d', 'i_RP_10', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,2].plot('d', 'i_RP_10', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,2].plot('d', 'i_RP_10', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,2].plot('d', 'i_RP_10', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,2].plot('d', 'i_RP_10', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')

    axs[1,0].plot('d', 'i_RP_25', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,0].plot('d', 'i_RP_25', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,0].plot('d', 'i_RP_25', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,0].plot('d', 'i_RP_25', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,0].plot('d', 'i_RP_25', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')

    axs[1,1].plot('d', 'i_RP_50', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,1].plot('d', 'i_RP_50', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,1].plot('d', 'i_RP_50', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,1].plot('d', 'i_RP_50', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,1].plot('d', 'i_RP_50', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 20 years')

    axs[1,2].plot('d', 'i_RP_100', data = i_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,2].plot('d', 'i_RP_100', data = i_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,2].plot('d', 'i_RP_100', data = i_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,2].plot('d', 'i_RP_100', data = i_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,2].plot('d', 'i_RP_100', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')

                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Intensity (mm/h)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_idf_subdaily_daily_{s}_{disag}_cbl.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')

def plot_comparison_PDF_daily_subdaily(disag_factor, station_name = 'INMET_aut'):
    data_normal, i_normal, p_normal = get_df_to_plot('INMET_aut', disag_factor, 'Normal')  
    data_GL, i_GL, p_GL = get_df_to_plot('INMET_aut', disag_factor, 'GenLogistic')
    data_gumbel_daily, i_gumbel_daily, p_gumbel_daily = get_df_to_plot('INMET_aut_daily', 'original', 'Gumbel')
    data_GEV_daily, i_GEV_daily, p_GEV_daily = get_df_to_plot('INMET_aut_daily', 'original', 'GEV')
    data_GL_daily, i_GL_daily, p_GL_daily = get_df_to_plot('INMET_aut_daily', 'original', 'GenLogistic') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,0].plot('d', 'P_RP_2', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,0].plot('d', 'P_RP_2', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,0].plot('d', 'P_RP_2', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,0].plot('d', 'P_RP_2', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,1].plot('d', 'P_RP_5', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,1].plot('d', 'P_RP_5', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,1].plot('d', 'P_RP_5', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,1].plot('d', 'P_RP_5', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')

    axs[0,2].plot('d', 'P_RP_10', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[0,2].plot('d', 'P_RP_10', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[0,2].plot('d', 'P_RP_10', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[0,2].plot('d', 'P_RP_10', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[0,2].plot('d', 'P_RP_10', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')

    axs[1,0].plot('d', 'P_RP_25', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,0].plot('d', 'P_RP_25', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,0].plot('d', 'P_RP_25', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,0].plot('d', 'P_RP_25', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,0].plot('d', 'P_RP_25', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')

    axs[1,1].plot('d', 'P_RP_50', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,1].plot('d', 'P_RP_50', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,1].plot('d', 'P_RP_50', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,1].plot('d', 'P_RP_50', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,1].plot('d', 'P_RP_50', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 20 years')

    axs[1,2].plot('d', 'P_RP_100', data = p_normal, linestyle = '-', label = 'Normal subdaily')
    axs[1,2].plot('d', 'P_RP_100', data = p_GL, linestyle = '-', label = 'GenLogistic subdaily')
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel_daily, linestyle = '-', label = 'Gumbel daily')
    axs[1,2].plot('d', 'P_RP_100', data = p_GEV_daily, linestyle = '-', label = 'GEV daily')
    axs[1,2].plot('d', 'P_RP_100', data = p_GL_daily, linestyle = '-', label = 'GL daily')
    axs[1,2].plot('d', 'P_RP_100', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')

                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Intensity (mm/h)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_pdf_subdaily_daily_{s}_{disag}_cbl.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')
    
def plot_comparison_IDF_average():
    data_obs, i_obs, p_obs = get_df_to_plot('INMET_aut', 'nan', 'Gumbel') 
    data_average, i_average, p_average = get_df_to_plot('Average', 'original', 'GenLogistic')
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,0].plot('d', 'i_RP_2', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,0].plot('d', 'i_RP_2', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,1].plot('d', 'i_RP_5', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,1].plot('d', 'i_RP_5', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'i_RP_10', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,2].plot('d', 'i_RP_10', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,2].plot('d', 'i_RP_10', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'i_RP_25', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,0].plot('d', 'i_RP_25', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,0].plot('d', 'i_RP_25', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'i_RP_50', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,1].plot('d', 'i_RP_50', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,1].plot('d', 'i_RP_50', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'i_RP_100', data = i_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,2].plot('d', 'i_RP_100', data = i_average, linestyle = '-', label = 'Average adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,2].plot('d', 'i_RP_100', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Intensity (mm/h)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_idf_average.png')

def plot_comparison_PDF_average():
    data_obs, i_obs, p_obs = get_df_to_plot('INMET_aut', 'nan', 'Gumbel') 
    data_average, i_average, p_average = get_df_to_plot('Average', 'original', 'GenLogistic')
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,0].plot('d', 'P_RP_2', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,0].plot('d', 'P_RP_2', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,1].plot('d', 'P_RP_5', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,1].plot('d', 'P_RP_5', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'P_RP_10', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[0,2].plot('d', 'P_RP_10', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_average, marker = 'v', label = 'Average points')
    axs[0,2].plot('d', 'P_RP_10', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')

    axs[1,0].plot('d', 'P_RP_25', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,0].plot('d', 'P_RP_25', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,0].plot('d', 'P_RP_25', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')

    axs[1,1].plot('d', 'P_RP_50', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,1].plot('d', 'P_RP_50', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,1].plot('d', 'P_RP_50', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')

    axs[1,2].plot('d', 'P_RP_100', data = p_obs, linestyle = '-', label = 'INMET_aut observed adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_obs, marker = 'o', label = 'INMET_aut observed points')
    axs[1,2].plot('d', 'P_RP_100', data = p_average, linestyle = '-', label = 'Average adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_average, marker = 'v', label = 'Average points')
    axs[1,2].plot('d', 'P_RP_100', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,2].set_title('RP = 100 years')
                                 
    for ax in axs.flat:
        ax.set(xlabel='duration (min)', ylabel='Precipitation (mm)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.legend(loc=7)
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.ylim([0, 250])
    #plt.show()
    fig.savefig('Graphs/IDF_plots/comparison_pdf_average.png')

if __name__ == '__main__':  
    
    station_name = 'INMET_conv'
    #station_name = 'Base_IDF'
    #dist_type = 'Gumbel'
    #dist_type = 'GenLogistic'
    #dist_type = 'Normal'
    disag_factor = 'bl'
    
    #plot_comparison_IDF_disag_factors(station_name, dist_type)
    #plot_comparison_PDF_disag_factors(station_name, dist_type)
    
    plot_comparison_IDF_distributions(station_name, disag_factor)
    plot_comparison_PDF_distributions(station_name, disag_factor)
    
    #get_df_to_plot(station_name, disag_factor, dist_type, save_table = True)
    
    #plot_comparison_IDF_daily_subdaily(disag_factor, station_name)
    #plot_comparison_PDF_daily_subdaily(disag_factor, station_name)
    
    #get_df_to_plot('Average', 'original', 'GenLogistic', save_table = True)
    #plot_comparison_IDF_average()
    #plot_comparison_PDF_average()
    
    
    print('Done!')