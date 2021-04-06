import pandas as pd

def complete_table(name_file):
    df = pd.read_csv('bartlet_lewis\{n}_B_rodada1.txt'.format(n = name_file), delimiter = "\t", header = None)
    
    day_list = []
    month_list = []
    year_list = []
    hour_list = []
    minute_list = []
    prec_list = []
    
    col_list = list(range(4,292))
    row_list = list(range(0, len(df)))
    
    for row in row_list:
        #print('row: ', row)
        day = df[0][row] 
        month = df[1][row]
        year = df[2][row]
        hour = 0
        min = 0
        #input()
        
        for col in col_list:
            #print('col: ', col)
            prec = df[col][row]
            #print('prec', prec)
            #print('date: ', day, month, year)
            #print('hour/min: ', hour, min)
            
            day_list.append(day)
            month_list.append(month)
            year_list.append(year)
            hour_list.append(hour)
            minute_list.append(min)
            prec_list.append(prec)
    
            min = min + 5
            if min == 60:
                min = 0
                hour = hour + 1        
            #input()
            
    dict_ = {'Year' : year_list,
            'Month' : month_list, 
            'Day' : day_list, 
            'Hour' : hour_list,
            'Min': minute_list,
            'Precipitation': prec_list
                    }
            
    df_complete = pd.DataFrame(dict_)
    #print(df_complete)
    df_complete.to_csv('bartlet_lewis/{n}_disag.csv'.format(n = name_file), index = False)        
    
    return df_complete

if __name__ == '__main__':
    print('Starting..')
    
    #complete_table('MAPLU')
    #complete_table('INMET')
    complete_table('INMETconv')
    
    print('Done!')