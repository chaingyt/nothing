# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 08:21:56 2017

@author: lc

# @Last Modified by:   jyt_Chiang
# @Last Modified time: 2018-08-27 23:48:51
"""


import os
import sys
from imp import reload
import datetime
import numpy as np
import xlrd
import xlsxwriter
import matplotlib.pyplot as plt
"""
1.数据读取
This part referene from wwx_plot_graph_v4.py
"""

reload(sys)

dirr =sys.argv[1]
#dirr = 'F:\\temp_dat\\growth_dat\\0530\\5.30A\\A'
print(dirr)


#参数初始化
Const_Image_Format = [".xlsx",".xls"]   #目标数据文件格式
matlist=[]                              #汇总数据List
timelist=[]                             #时间List
j=1

original_path=dirr+'_'+'original\\'
os.mkdir(original_path)

outputdata=original_path+'original'+'.xlsx'
workbook = xlsxwriter.Workbook(outputdata)
worksheet = workbook.add_worksheet()

for file in os.listdir(dirr):
    newdir=os.path.join(dirr,file)
    if os.path.isfile(newdir):
        #符合目标格式
        if newdir and (os.path.splitext(newdir)[1]) in Const_Image_Format:
            uipath =newdir
            data = xlrd.open_workbook(uipath) 
            table = data.sheet_by_index(0)
            nrows = table.nrows#hang
            ncols = table.ncols#lie
            
            rowname='A'+str(j)
            worksheet.write_row(rowname,file)
            j+=1
            
           #time
            testtime1=xlrd.xldate.xldate_as_datetime(table.cell(6,1).value,0)
            testtime2=xlrd.xldate.xldate_as_datetime(table.cell(7,1).value,0)
            date1=testtime1.date()
            time1=testtime2.time()
            dt = datetime.datetime.combine(date1, time1)    
            timelist.append(dt)
           #read mat
            excel_list = []
            for row in range(24, nrows):
                excel_rows = []
                output_rows=[]
                for col in range(2,ncols-1):
                    cell_value = table.cell(row, col).value
                    output_rows.append(cell_value)
                    if cell_value=='':
                       cell_value=np.nan
                           
                    excel_rows.append(cell_value)           
                                          #excel_rows.append(cell_value.encode('UTF-8'))             
                excel_list.append(excel_rows)
                
                rowname='A'+str(j)
                worksheet.write_row(rowname,output_rows)
                j+=1

           #在这里分组份,
            excel_array=np.array(excel_list)  
            #
            group_one=excel_array[0:5,0:3]
            group_onelist=np.nanmean(group_one,axis=1)
            #
            group_two=excel_array[0:5,3:6]
            group_twolist=np.nanmean(group_two,axis=1)
            #averlist=np.vstack((group_onelist,group_twolist))
            group_three=excel_array[0:5,6:9]
            group_threelist=np.nanmean(group_three,axis=1)
            #
            group_four=excel_array[0:5,9:12]
            group_fourlist=np.nanmean(group_four,axis=1)
            #
            group_five=excel_array[5:8,0:5]
            group_five=np.transpose(group_five)
            group_fivelist=np.nanmean(group_five,axis=1)
            #
            group_six=excel_array[5:8,5:10]
            group_six=np.transpose(group_six)
            group_sixlist=np.nanmean(group_six,axis=1)

            averlist=np.vstack((group_onelist,group_twolist,
                                group_threelist,group_fourlist,group_fivelist,group_sixlist))
            matlist.append(averlist)#合并
workbook.close()

#时间处理
new_timelist=np.sort(timelist)
new_data=[None]*(len(matlist))
test_time=[]     #outputdata,hour
time_labels=[]
i=0
for ls in new_timelist:
    date1=''
    date2=''
    position=timelist.index(ls)
    new_data[i]=matlist[position]
    timess=((ls-new_timelist[0]).total_seconds())//60
    test_time.append((timess/60))
    time_labels.append(ls)
    i+=1
#module
print(test_time)





"""
2.均值画折线图
"""

png_path=dirr+'_'+'png\\'
os.mkdir(png_path)
avg_path=dirr+'_'+'avg\\'
os.mkdir(avg_path)

color_module=["yellow-module","red-module","blue-module",
              "orange-module","pink-module","FF9D6F-module"] 
reagent=["0","0.01","0.1","1","10"]
for i in range(0,6):#碳源模板块
    output_data=avg_path+dirr[-1]  + '_'  +color_module[i]+'.xlsx'
    workbook = xlsxwriter.Workbook(output_data)
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A2', reagent)
    worksheet.write_row('B1',test_time)

    yl=[]
    for j in range(0,5):#浓度
        y=[]
        for k in range(0,len(matlist)):#时间
            y.append( new_data[k][i,j])
            worksheet.write(j+1,k+1,new_data[k][i,j])    
        yl.append(y)         
    workbook.close()
    
    plt.figure(figsize=(12,7))#创建绘图对象
    a= plt.subplot(1,1,1)
    ax = plt.gca()

    a1 = a.plot(test_time, yl[0], 'bx-', label = reagent[0])
    a2 = a.plot(test_time, yl[1], 'm^-', label = reagent[1])
    a3 = a.plot(test_time, yl[2], 'gv-', label = reagent[2])
    a4 = a.plot(test_time, yl[3], 'ko-', label = reagent[3])
    a4 = a.plot(test_time, yl[4], 'r*-', label = reagent[4])
    plt.gcf().autofmt_xdate()

    plt.xlabel("Time(h)") #X轴标签
    plt.ylabel("OD(600)")  #Y轴标签
    plt.title(color_module[i]) #图标题
    a.tick_params(pad=10)#参数pad用于设置刻度线与标签间的距离
    #图例
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles[::-1], labels[::-1])
    outputfile=png_path+dirr[-1] + '_' +color_module[i]+'.png'
    plt.savefig(outputfile)  
 ##好到这里基本结束  

print ('OK' )

