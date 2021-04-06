# IDF_project
Procedures to treat rainfall to construction of IDF curves

functions_treatment.py - Tem as funcoes que eu uso para fazer o tratamento dos dados brutos e colocar no intervalo temporal que eu preciso

data_treatment_tendency.py - Só tem as execucoes das funcoes de tratamento, para tratar os dados e fazer analise de tendencia.

functions_get_distribution.py - Tem as funcoes que eu criei para fazer o ajuste de distribuicoes. Ele calcula o SSE e os parametros das funçoes. Pegar o SSE para cada uma e para cada estação e anotar em uma planilha separada. Calculei depois a IDF para as tres funcoes com maiores ajustes (e para subdaily eu calculei para GenLogistic e Normal, que foram as que deram melhor no geral).

idf_generator_dailymax.py - Tem as funcoes para gerar a IDF (tabela e parametros ajustados) a partir de dados diários maximos previamente calculados. Eh necessario informar a funcao de ajuste de distribuicao a ser usada (calculada previamente com functions_get_distribution).

idf_generator_subdailymax.py - Tem as funcoes para gerar a IDF (tabela e parametros ajustados) a partir de dados subdiarios maximos previamente calculados. Eh necessario informar a funcao de ajuste de distribuicao a ser usada (calculada previamente com functions_get_distribution).

idf_from_table.py - Tem as funcoes para obter os parametros ajustados da IDF a partir de uma tabela já ajustada a uma funcao de distribuicao. Usei esse codigo para poder calcular os parametros da IDF media, em que calculei a media dos valores de precipitacao para cada duracao e cada TR das diferentes desagregacoes anteriores.

idf_plot.py - Tem as funcoes para gerar os graficos das IDFs e PDFs comparativas, obtidas dos dados maximos diarios.

idf_plot_subdaily.py - Tem as funcoes para gerar os graficos das IDFs e PDFs comparativas, obtidas dos dados maximos subdiarios.

bartlett_lewis.py - Tem a funcao para colocar os dados obtidos do codigo de BL do R no formato necessario para calcular a IDF nesse codigo.

Results/ - É a pasta em que eu estou salvando os resultados. Alguns dos resultados do tratamento sao puxados para fazer a analise de distribuiçao (principalmente dps para os dados do cemaden e maplu, que não tem dados diarios ja contabilizados)

Results/IDF_tables_dist - É a pasta que tem que colocar os resutados de IDF_table e IDFsubdaily_table para fazer os plots.

Results/IDF_tables_calc - É a pasta para colocar os resutados das tabelas IDFs calculadas a partir dos parametros ajustados, usado para fazer os plots.

Graphs/ - É a pasta onde salva os gráficos (ver certinho qual pasta tem que ser criada para cada tipo de grafico)

bartlet_lewis/ - É a pasta que eu coloco o resultado do codigo de BL do R e que coloca no formato certo para o resto do código. O resto do cálculo da IDF para BL fica salvando nesta pasta, então tem que transferir depois para a basta

CEMADEN/ - Contem os dados brutos do CEMADEN

INMET/ - Contem os dados brutos do INMET

MAPLU/ - Contem os dados discretizados para 1min dos pluvis do MAPLU
