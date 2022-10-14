import json
import pandas as pd
import numpy as np
f = 'houza.json'
df = pd.read_json('houza.json', lines=True)
# print(df)


def content(data):

    lst_total = []
    lst_col_avg = []
    data = df.replace('', np.nan)
    df_ = ['depth', 'sub_category_2', 'dtcm_licence', 'price_per']
    data[df_] = data[df_].replace(np.nan, 10)
    field_isnull = data.isna().sum()
    total = df.count()
    check_isnull = (field_isnull / total * 100)
    # print(check_isnull)
    field_notnull = data.notnull().sum()
    check_notnull = (field_notnull / total * 100)
    for type_notnull, type_isnull in zip(check_notnull, check_isnull):
        total_notnull = (str(int(type_notnull)) + '% : ')
        total_isnull = (str(int(type_isnull)) + '%')
        total_avg = total_notnull + total_isnull
        lst_total.append(total_avg)
    # print(lst1)
    column_headers = list(df.columns.values)
    lst_col_avg.append(dict(zip(column_headers, lst1)))
    # print(lst2)
    with open('testing_file.json','w') as f:
        f.write(json.dumps(lst_col_avg,indent = 4))



content(df)
