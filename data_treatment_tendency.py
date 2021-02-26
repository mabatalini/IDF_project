import pandas as pd
from functions_treatment import *

# # dados com base mensal
# agua_vermelha = read_csv('agua_vermelha', 'monthly')
# jd_sp = read_csv('jd_sp', 'monthly')
# INMET_aut = read_csv('INMET_aut', 'monthly')
# INMET_conv = read_csv('INMET_conv', 'monthly')
# MAPLU_esc = read_csv('MAPLU_esc', 'monthly')

# dados com base diaria
# agua_vermelha = read_csv('agua_vermelha', 'daily')
# jd_sp = read_csv('jd_sp', 'daily')
# INMET_aut = read_csv('INMET_aut', 'daily')
# INMET_conv = read_csv('INMET_conv', 'daily')
# MAPLU_esc = read_csv('MAPLU_esc', 'daily')

# ## Distribution plots
# 
# distribution_plot('agua_vermelha', 'hourly')
# distribution_plot('agua_vermelha', 'daily')
# distribution_plot('agua_vermelha', 'monthly')
# distribution_plot('agua_vermelha', 'yearly')
# 
# distribution_plot('jd_sp', 'hourly')
# distribution_plot('jd_sp', 'daily')
# distribution_plot('jd_sp', 'monthly')
# distribution_plot('jd_sp', 'yearly')
# 
# distribution_plot('INMET_aut', 'hourly')
# distribution_plot('INMET_aut', 'daily')
# distribution_plot('INMET_aut', 'monthly')
# distribution_plot('INMET_aut', 'yearly')
# 
# distribution_plot('INMET_conv', 'hourly')
# distribution_plot('INMET_conv', 'daily')
# distribution_plot('INMET_conv', 'monthly')
# distribution_plot('INMET_conv', 'yearly')
# 
# distribution_plot('MAPLU_esc', 'hourly')
# distribution_plot('MAPLU_esc', 'daily')
# distribution_plot('MAPLU_esc', 'monthly')
# distribution_plot('MAPLU_esc', 'yearly')

# ## P90 ANALYSIS
# print('P90 CEMADEN / Agua Vermelha: ', p90_function(agua_vermelha))
# print('P90 CEMADEN / Jardim Sao Paulo: ', p90_function(jd_sp))
# print('P90 INMET / Automatic: ', p90_function(INMET_aut))
# print('P90 INMET / Conventional: ', p90_function(INMET_conv))
# print('P90 MAPLU / Escola Sao Bento: ', p90_function(MAPLU_esc))

# ## ANALISE DE TENDENCIA
# agua_vermelha_mk = agua_vermelha[['Precipitation']]
# jd_sp_mk = jd_sp[['Precipitation']]
# INMET_aut_mk = INMET_aut[['Precipitation']]
# INMET_conv_mk = INMET_conv[['Precipitation']]
# MAPLU_esc_mk = MAPLU_esc[['Precipitation']]
# 
# alpha_value = 0.5
# 
# print('--- CEMADEN / AGUA VERMELHA ----')
# print('')
# trend_analysis(agua_vermelha_mk, alpha_value)
# 
# print('')
# print('--- CEMADEN / JARDIM SAO PAULO ----')
# print('')
# trend_analysis(jd_sp_mk, alpha_value)
# 
# print('')
# print('--- INMET / AUTOMATICO ----')
# print('')
# trend_analysis(INMET_aut_mk, alpha_value)
# 
# print('')
# print('--- INMET / CONVENCIONAL ----')
# print('')
# trend_analysis(INMET_conv_mk, alpha_value)
# 
# print('')
# print('--- MAPLU / ESCOLA SAO BENTO ----')
# print('')
# trend_analysis(MAPLU_esc_mk, alpha_value)

## DUPLA MASSA - ANALISE DE CONSISTENCIA
# 
# df = pd.merge(agua_vermelha, jd_sp, how='left', on=['Year', 'Month'])
# df = pd.merge(df, INMET_aut, how='left', on=['Year', 'Month'])
# df = pd.merge(df, INMET_conv, how='left', on=['Year', 'Month'])
# df = pd.merge(df, MAPLU_esc, how='left', on=['Year', 'Month'])
# df.columns = ['Year', 'Month', 'P_av', 'P_jdsp', 'P_inmet_aut', 'P_inmet_conv', 'P_maplu']
# df = df.dropna()
# df['P_average'] = df[['P_av', 'P_jdsp', 'P_inmet_aut', 'P_inmet_conv', 'P_maplu']].mean(axis=1)
# df['Pacum_av'] = np.nan
# df['Pacum_jdsp'] = np.nan
# df['Pacum_inmet_aut'] = np.nan
# df['Pacum_inmet_conv'] = np.nan
# df['Pacum_maplu'] = np.nan
# df['Pacum_average'] = np.nan
# 
# for i in range(len(df)):
#     if i == 0:
#         df['Pacum_av'][i] = df['P_av'][i]
#         df['Pacum_jdsp'][i] = df['P_jdsp'][i]
#         df['Pacum_inmet_aut'][i] = df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['P_inmet_conv'][i]
#         df['Pacum_maplu'][i] = df['P_maplu'][i]
#         df['Pacum_average'][i] = df['P_average'][i]
#     else:
#         df['Pacum_av'][i] = df['Pacum_av'][i-1]+df['P_av'][i]
#         df['Pacum_jdsp'][i] = df['Pacum_jdsp'][i-1]+df['P_jdsp'][i]
#         df['Pacum_inmet_aut'][i] = df['Pacum_inmet_aut'][i-1]+df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['Pacum_inmet_conv'][i-1]+df['P_inmet_conv'][i]
#         df['Pacum_maplu'][i] = df['Pacum_maplu'][i-1]+df['P_maplu'][i]
#         df['Pacum_average'][i] = df['Pacum_average'][i-1]+df['P_average'][i]

# ## ONLY CEMADEN AND INMET
# df.columns = ['Year', 'Month', 'P_av', 'P_jdsp', 'P_inmet_aut', 'P_inmet_conv']
# df = df.dropna()
# df['P_average'] = df[['P_av', 'P_jdsp', 'P_inmet_aut', 'P_inmet_conv']].mean(axis=1)
# df['Pacum_av'] = np.nan
# df['Pacum_jdsp'] = np.nan
# df['Pacum_inmet_aut'] = np.nan
# df['Pacum_inmet_conv'] = np.nan
# df['Pacum_average'] = np.nan
# for i in range(len(df)):
#     if i == 0:
#         df['Pacum_av'][i] = df['P_av'][i]
#         df['Pacum_jdsp'][i] = df['P_jdsp'][i]
#         df['Pacum_inmet_aut'][i] = df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['P_inmet_conv'][i]
#         df['Pacum_average'][i] = df['P_average'][i]
#     else:
#         df['Pacum_av'][i] = df['Pacum_av'][i-1]+df['P_av'][i]
#         df['Pacum_jdsp'][i] = df['Pacum_jdsp'][i-1]+df['P_jdsp'][i]
#         df['Pacum_inmet_aut'][i] = df['Pacum_inmet_aut'][i-1]+df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['Pacum_inmet_conv'][i-1]+df['P_inmet_conv'][i]
#         df['Pacum_average'][i] = df['Pacum_average'][i-1]+df['P_average'][i]
#  
# print(df)
# df.to_csv('Results/dupla_massa_CEMADEN.csv', index = False)

# ## ONLY MAPLU AND INMET
# df = pd.merge(MAPLU_esc, INMET_aut, how='left', on=['Year', 'Month'])
# df = pd.merge(df, INMET_conv, how='left', on=['Year', 'Month'])
# df.columns = ['Year', 'Month', 'P_maplu', 'P_inmet_aut', 'P_inmet_conv']
# df = df.dropna()
# df['P_average'] = df[['P_maplu', 'P_inmet_aut', 'P_inmet_conv']].mean(axis=1)
# df['Pacum_maplu'] = np.nan
# df['Pacum_inmet_aut'] = np.nan
# df['Pacum_inmet_conv'] = np.nan
# df['Pacum_average'] = np.nan
#  
# for i in range(len(df)):
#     if i == 0:
#         df['Pacum_inmet_aut'][i] = df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['P_inmet_conv'][i]
#         df['Pacum_maplu'][i] = df['P_maplu'][i]
#         df['Pacum_average'][i] = df['P_average'][i]
#     else:
#         df['Pacum_inmet_aut'][i] = df['Pacum_inmet_aut'][i-1]+df['P_inmet_aut'][i]
#         df['Pacum_inmet_conv'][i] = df['Pacum_inmet_conv'][i-1]+df['P_inmet_conv'][i]
#         df['Pacum_maplu'][i] = df['Pacum_maplu'][i-1]+df['P_maplu'][i]
#         df['Pacum_average'][i] = df['Pacum_average'][i-1]+df['P_average'][i]
# 
# print(df)
# df.to_csv('Results/dupla_massa_MAPLU.csv', index = False)

# df = pd.read_csv('Results/dupla_massa.csv')
# #df = pd.read_csv('Results/dupla_massa_CEMADEN.csv')
# #df = pd.read_csv('Results/dupla_massa_MAPLU.csv')
# sns.set_context("talk", font_scale=0.8)
# plt.figure(figsize=(8,6))
# sns.scatterplot(x="Pacum_average", 
#                 y="Pacum",
#                 hue = 'Station', 
#                 data=df)
# plt.xlabel("Pacum Average (mm)")
# plt.ylabel("Pacum (mm)")
# plt.title("Average")
# # plt.savefig("default_legend_position_Seaborn_scatterplot.png",
# #                     format='png',dpi=150)
# plt.show()
#   
# sns.set_context("talk", font_scale=0.8)
# plt.figure(figsize=(8,6))
# sns.scatterplot(x="Pacum_inmet_aut", 
#                 y="Pacum",
#                 hue = 'Station', 
#                 data=df)
# plt.xlabel("Pacum inmet_aut (mm)")
# plt.ylabel("Pacum (mm)")
# plt.title("INMET_aut")
#   
# plt.show()


# ## COMPLETAR FALHAS
# INMET_aut = complete_date_series('INMET_aut', 'daily')
# INMET_conv = complete_date_series('INMET_conv', 'daily')
# 
# agua_vermelha = complete_date_series('agua_vermelha', 'daily')
# agua_vermelha.to_csv('Results/agua_vermelha_daily_completo.csv', index = False)
# jd_sp = complete_date_series('jd_sp', 'daily')
# jd_sp.to_csv('Results/jd_sp_daily_completo.csv', index = False)
# MAPLU_esc = complete_date_series('MAPLU_esc', 'daily')
# MAPLU_esc.to_csv('Results/MAPLU_esc_daily_completo.csv', index = False)
# 
# df = left_join_precipitation(agua_vermelha, INMET_aut, INMET_conv)
# df.to_csv('Results/VERIFICAR_agua_vermelha.csv', index = False)
# df = left_join_precipitation(jd_sp, INMET_aut, INMET_conv)
# df.to_csv('Results/VERIFICAR_jd_sp.csv', index = False)
# df = left_join_precipitation(MAPLU_esc, INMET_aut, INMET_conv)
# df.to_csv('Results/VERIFICAR_MAPLU_esc.csv', index = False)


#correlation_plots(agua_vermelha, INMET_aut, INMET_conv)
#multiple_linear_regression(agua_vermelha, INMET_aut, INMET_conv)

# ## VERIFICACAO DE FALHAS
# cidade_jardim = read_csv('cidade_jardim', 'daily')   
# verification(cidade_jardim) 
# 
# jd_sp = read_csv('jd_sp', 'daily')   
# verification(jd_sp) 
# 
# INMET_aut = read_csv('INMET_aut', 'daily')   
# verification(INMET_aut)
# 
# INMET_conv = read_csv('INMET_conv', 'daily')   
# verification(INMET_conv)
# 
# MAPLU_esc = read_csv('MAPLU_esc', 'daily')   
# verification(MAPLU_esc)
# 
# MAPLU_post = read_csv('MAPLU_post', 'daily')   
# verification(MAPLU_post)




