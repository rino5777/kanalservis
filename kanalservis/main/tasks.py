from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from .models import  Data_google
import gspread
import pandas as pd
from pycbrf.toolbox import ExchangeRates
from datetime import date
from datetime import datetime
import telegram_send
import xlsxwriter
import os
from django.shortcuts import render


@shared_task 
def timemanager():
    
    

    def is_actual(d_l): # сравнивает сегонешнюю дату с датой со списком (bool)
    
        dt_obj1 =  '/'.join(d_l.split('.')) 
        dt_lst = datetime.strptime(dt_obj1, '%d/%m/%Y') #преобразованная дата со списка
        dt_now = datetime.now()
        if (dt_lst - dt_now ).days > 0: 
            return True
        else:
            return False

    def data_from_google_sheets(): #вытаскивает все данные из google sheets и помещает их в список 
        rates = ExchangeRates(date.today())
        
        gs = gspread.service_account(filename='main/json_f/testp-350822-853614e7357c.json')  # подключаем файл с ключами и пр.
        sh = gs.open_by_key('1qvz1ZhzZTZz5Y8Rqb_HdPCSMQVMJZELuA6fDUAFpZRY')  # подключаем таблицу по ID
        worksheet = sh.sheet1
        res = worksheet.get_all_values()
        # res1 = worksheet.row_values(1)
        # col= len(worksheet.col_values(1))-1 #коллич. строк в таблице
        course = float(rates['USD'].rate) # аактуальный курс
 
        a_list = []
        for i in res[1::]:
            a_list.append(i + [round(float(i[2])*course, 1)])
        #----------ДАТАФРЕЙМ
        # df = pd.DataFrame(a_list,  columns=['№','заказ №', 'стоимость,$', 'срок поставки','стоимость в руб']) #  создание датафрейма из данных
        # df.drop(df.columns[[0]], axis = 1)
        
        return a_list
    # есть 2 представления данных (1: список a_list  
    #                              2: дата df)



    overdue = []
    Data_google.objects.all().delete() #удаление старой базы
    for i in data_from_google_sheets(): #обновление базы
        if is_actual(i[3]) is True:
            d = Data_google( num = int(i[0]), order=int(i[1]), priceUSD = float(i[2]), date_arr = i[3], priceRUB = float(i[4])) 
            d.save()
        else:
            d = Data_google( num = i[0], order=i[1], priceUSD = i[2], date_arr = i[3], priceRUB = i[4], actual = False) 
            d.save()
            overdue.append([i[0],i[1],i[2],i[3],i[4]]) #список заказов срок которых прошел
           
    data = Data_google.objects.all()
  
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('xlsx/overdue.xlsx')
    workxl = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    workxl.set_column('A:A', 20)
    workxl.set_column('B:A', 20)
    workxl.set_column('C:C', 20)
    workxl.set_column('D:D', 20)
    workxl.set_column('E:E', 20)
    bold = workbook.add_format({'bold': True})
    workxl.write('A1', '№',bold)
    workxl.write('B1', 'заказ №',bold)
    workxl.write('C1', 'стоимость,$',bold)
    workxl.write('D1', 'срок поставки',bold)
    workxl.write('E1', 'стоимость в руб',bold)
    
    i = 0
    for index in overdue:
        i +=1   
        workxl.write(i,0, index[0])
        workxl.write(i,1, index[1])
        workxl.write(i,2, index[2])
        workxl.write(i,3, index[3])
        workxl.write(i,4, index[4])

    workbook.close()
    telegram_send.send(messages=['заказы срок которых прошел ' ])
    with open('xlsx/overdue.xlsx', "rb") as f:
        telegram_send.send(files =[f])
    return  data



def telegram_xlsx():
    pass
