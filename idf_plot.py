import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style

def get_df_to_plot(station_name, disag_factor, dist_type):
    df_IDF_params = pd.read_csv('IDF_params.csv')
    if station_name == 'Base_IDF':
        df_idf_table = []
    else:
        df_idf_table = pd.read_csv('Results/IDF_table_{n}_{dist}_{disag}.csv'.format(n = station_name, dist = dist_type, disag = disag_factor))

    
    #print(df_IDF_params)
    df_selected = df_IDF_params.loc[df_IDF_params['Station'] == station_name]
    df_selected = df_selected.loc[df_selected['Disag_factors'] == disag_factor]
    df_selected = df_selected.loc[df_selected['Dist_Type'] == dist_type]
    df_selected = df_selected.reset_index()
    #print(df_selected)
    K = df_selected['K'][0]
    t0 = df_selected['t0'][0]
    m = df_selected['m'][0]
    n = df_selected['n'][0]
    #input()
    return_period_list = [2, 5, 10, 25, 50, 100]
    duration_list = [5, 10, 20, 30, 60, 360, 480, 600, 720, 1440]
    
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
    
    return df_idf_table, df_intensity, df_precipitation


def plot_comparison_IDF_disag_factors(station_name, dist_type):
    disag_factor = 'original'
    data_gumbel_original,i_gumbel_original, p_gumbel_original = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'm_20'
    data_gumbel_m20, i_gumbel_m20, p_gumbel_m20 = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'p_20'
    data_gumbel_p20, i_gumbel_p20, p_gumbel_p20 = get_df_to_plot(station_name, disag_factor, dist_type)
    
    disag_factor = 'opt'
    data_gumbel_opt, i_gumbel_opt, p_gumbel_opt = get_df_to_plot(station_name, disag_factor, dist_type)
    
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
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

    fig.savefig('Graphs/IDF_plots/comparison_idf_disag_{s}_{dist}.png'.format(s = station_name, dist = dist_type), dpi=300, format='png')

def plot_comparison_PDF_disag_factors(station_name, dist_type):
    disag_factor = 'original'
    data_gumbel_original,i_gumbel_original, p_gumbel_original = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'm_20'
    data_gumbel_m20, i_gumbel_m20, p_gumbel_m20 = get_df_to_plot(station_name, disag_factor, dist_type) 
    
    disag_factor = 'p_20'
    data_gumbel_p20, i_gumbel_p20, p_gumbel_p20 = get_df_to_plot(station_name, disag_factor, dist_type)
    
    disag_factor = 'opt'
    data_gumbel_opt, i_gumbel_opt, p_gumbel_opt = get_df_to_plot(station_name, disag_factor, dist_type)
    
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel_original, linestyle = '-', label = 'Original adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel_original, marker = 'o', label = 'Original points')
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel_m20, linestyle = '-', label = 'Minus 20% adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel_m20, marker = 'x', label = 'Minus 20% points')
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel_p20, linestyle = '-', label = 'Plus 20% adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel_p20, marker = 'v', label = 'Plus 20% points')
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel_opt, linestyle = '-', label = 'Optimized adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel_opt, marker = 'd', label = 'Optimized points')
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
    fig.savefig('Graphs/IDF_plots/comparison_pdf_disag_{s}_{dist}.png'.format(s = station_name, dist = dist_type), dpi=300, format='png')
    
def plot_comparison_IDF_distributions(station_name, disag_factor):
    data_gumbel, i_gumbel, p_gumbel = get_df_to_plot(station_name, disag_factor, 'Gumbel') 
    data_GEV, i_GEV, p_GEV = get_df_to_plot(station_name, disag_factor, 'GEV') 
    data_GL, i_GL, p_GL = get_df_to_plot(station_name, disag_factor, 'GenLogistic') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'i_RP_2', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,0].plot('d', 'i_RP_2', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,0].plot('d', 'i_RP_2', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,0].scatter('duration', 'i_RP_2Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,0].plot('d', 'i_RP_2', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'i_RP_5', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,1].plot('d', 'i_RP_5', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,1].plot('d', 'i_RP_5', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,1].scatter('duration', 'i_RP_5Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,1].plot('d', 'i_RP_5', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'i_RP_10', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,2].plot('d', 'i_RP_10', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,2].plot('d', 'i_RP_10', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,2].scatter('duration', 'i_RP_10Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,2].plot('d', 'i_RP_10', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'i_RP_25', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,0].plot('d', 'i_RP_25', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,0].plot('d', 'i_RP_25', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,0].scatter('duration', 'i_RP_25Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,0].plot('d', 'i_RP_25', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'i_RP_50', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,1].plot('d', 'i_RP_50', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,1].plot('d', 'i_RP_50', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,1].scatter('duration', 'i_RP_50Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,1].plot('d', 'i_RP_50', data = i_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'i_RP_100', data = i_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,2].plot('d', 'i_RP_100', data = i_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,2].plot('d', 'i_RP_100', data = i_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,2].scatter('duration', 'i_RP_100Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
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

    fig.savefig('Graphs/IDF_plots/comparison_idf_dist_{s}_{disag}.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')

def plot_comparison_PDF_distributions(station_name, disag_factor):
    data_gumbel, i_gumbel, p_gumbel = get_df_to_plot(station_name, disag_factor, 'Gumbel') 
    data_GEV, i_GEV, p_GEV = get_df_to_plot(station_name, disag_factor, 'GEV') 
    data_GL, i_GL, p_GL = get_df_to_plot(station_name, disag_factor, 'GenLogistic') 
    data_base, i_base, p_base = get_df_to_plot('Base_IDF', 'original', 'Gumbel')
        
    fig, axs = plt.subplots(2, 3, sharex = True, sharey= True, figsize=(15, 6))
    axs[0,0].plot('d', 'P_RP_2', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,0].plot('d', 'P_RP_2', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,0].plot('d', 'P_RP_2', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,0].scatter('duration', 'P_RP_2Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,0].plot('d', 'P_RP_2', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,0].set_title('RP = 2 years')
    
    axs[0,1].plot('d', 'P_RP_5', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,1].plot('d', 'P_RP_5', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,1].plot('d', 'P_RP_5', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,1].scatter('duration', 'P_RP_5Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,1].plot('d', 'P_RP_5', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,1].set_title('RP = 5 years')
    
    axs[0,2].plot('d', 'P_RP_10', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[0,2].plot('d', 'P_RP_10', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[0,2].plot('d', 'P_RP_10', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[0,2].scatter('duration', 'P_RP_10Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[0,2].plot('d', 'P_RP_10', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[0,2].set_title('RP = 10 years')
    
    axs[1,0].plot('d', 'P_RP_25', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,0].plot('d', 'P_RP_25', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,0].plot('d', 'P_RP_25', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,0].scatter('duration', 'P_RP_25Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,0].plot('d', 'P_RP_25', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,0].set_title('RP = 25 years')
    
    axs[1,1].plot('d', 'P_RP_50', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,1].plot('d', 'P_RP_50', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,1].plot('d', 'P_RP_50', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,1].scatter('duration', 'P_RP_50Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
    axs[1,1].plot('d', 'P_RP_50', data = p_base, linestyle = '--', label = 'Base IDF')
    axs[1,1].set_title('RP = 50 years')
    
    axs[1,2].plot('d', 'P_RP_100', data = p_gumbel, linestyle = '-', label = 'Gumbel adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_gumbel, marker = 'o', label = 'Gumbel points')
    axs[1,2].plot('d', 'P_RP_100', data = p_GEV, linestyle = '-', label = 'GEV adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_GEV, marker = 'x', label = 'GEV points')
    axs[1,2].plot('d', 'P_RP_100', data = p_GL, linestyle = '-', label = 'GenLogistic adjusted')
    axs[1,2].scatter('duration', 'P_RP_100Years', data = data_GL, marker = 'v', label = 'GenLogistic points')
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

    fig.savefig('Graphs/IDF_plots/comparison_pdf_dist_{s}_{disag}.png'.format(s = station_name, disag = disag_factor), dpi=300, format='png')

#station_name = 'INMET_conv'
station_name = 'INMET_aut'
#dist_type = 'Gumbel'
#dist_type = 'GenLogistic'
#dist_type = 'GEV'
disag_factor = 'original'

#plot_comparison_IDF_disag_factors(station_name, dist_type)
#plot_comparison_PDF_disag_factors(station_name, dist_type)

plot_comparison_IDF_distributions(station_name, disag_factor)
plot_comparison_PDF_distributions(station_name, disag_factor)

print('Done!')