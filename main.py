import os
import pandas as pd
import sqlite3 as sql
import shutil


def find(invoice, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if invoice in file:
                return file, os.path.join(root, file)


conn = sql.connect('/Users/aleksejsaronov/Documents/2020_12_AT_soft/invoices.db')
df = pd.read_sql_query('SELECT * FROM Lot_Invoice_data', conn)

list_of_target = df['Lot'].drop_duplicates().values.tolist()
list_of_files = os.listdir('inv')

path = '/Volumes/alex/_INV'
path_new = os.path.abspath(os.getcwd()) + '/sorted/'

if not os.path.isdir(path_new):
    os.mkdir(os.path.join(os.path.abspath(os.getcwd()) + '/sorted'))

count = 0
for lot in list_of_target:
    df_chunk = df.loc[df['Lot'] == lot]
    inv_list = df_chunk['Invoice'].values.tolist()
    inv_list_copy = list(inv_list)

    for invoice in inv_list:
        try:
            name, origin_path = find(invoice, path)
            if not os.path.isdir(path_new + lot):
                os.mkdir(os.path.join(path_new + lot))

            destination_path = path_new + lot + '/' + name

            shutil.copyfile(origin_path, destination_path)

            inv_list_copy.remove(invoice)
        except:
            pass

    if len(inv_list_copy) > 0:
        print('in ', lot, ' remains', len(inv_list_copy), inv_list_copy, 'invoice(s)', '\n')