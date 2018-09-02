# -*- coding: utf-8 -*-
# @Author: jyt_Chiang
# @Date:   2018-08-26 14:17:38
# @Last Modified by:   jyt_Chiang
# @Last Modified time: 2018-08-29 00:12:22

import os
import sys
from imp import reload
import datetime
import numpy as np
import pandas as pd
import xlrd
import xlsxwriter
import heapq
from statsmodels.stats.multicomp import (pairwise_tukeyhsd,MultiComparison)
#from scipy import stats

"""
1.数据读取
This part referene from wwx_plot_graph_v4.py
"""

reload(sys)

dirr =sys.argv[1]
#dirr = 'F:\\temp_dat\\growth_dat\\0530\\5.30A\\A'
print(dirr)

"""
自定义函数计算List的均值、方差、标准差
get_average
get_variance
get_stddev
"""
# 获取平均数：average
def get_average(list):
    sum = 0
    for item in list:
        sum += item
    return sum/len(list)
# 方差
def get_variance(list):
    sum = 0
    average = get_average(list)
    for item in list:
        sum += (item - average)**2
    return sum/len(list)
# standard deviation
def get_stddev(list):
    average = get_average(list)
    sdsq = sum([(i - average) ** 2 for i in list])
    stdev = (sdsq / (len(list) - 1)) ** .5
    return stdev




#参数初始化
Const_Image_Format = [".xlsx",".xls"]   #目标数据文件格式
matlist=[]                              #汇总数据List
timelist=[]                             #时间List


#读取多个excel表格数据：同一个文件夹下
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
          
                excel_list.append(excel_rows)

           #在这里分组:六个碳源模板
            excel_array=np.array(excel_list)  
            #
            group_one=excel_array[0:5,0:3]
            group_onelist=np.nanmean(group_one,axis=1)
            #
            group_two=excel_array[0:5,3:6]
            group_twolist=np.nanmean(group_two,axis=1)
            #
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

            averlist=np.vstack((group_onelist,group_twolist,group_threelist,
                                group_fourlist,group_fivelist,group_sixlist))
            matlist.append(averlist)#合并均值

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
#print(test_time)

#求各碳源重复试验的均值：以时间为序
color_module=["yellow-module","red-module","blue-module",
              "orange-module","pink-module","FF9D6F-module"] 
reagent=["0","0.01","0.1","1","10"]
list_col=['标准差','增长率']
mat_y=[]

for i in range(0,6):#碳源模板块
    yl=[]   #存碳源对应五个浓度下的时间序列值   
    for j in range(0,5):#浓度
        y=[]
        for k in range(0,len(matlist)):#时间
            y.append(new_data[k][i,j])
        yl.append(y)
    mat_y.append(yl)


#计算标准差和增长率
std_lst = []
rate_list = []
for ty in mat_y:
    std_list = []
    grw_rate = []
    for ndu in ty:
        std_list.append(get_stddev(ndu))  #计算浓度下的标准差
        grw_rate.append( (get_average(heapq.nlargest(3, ndu[1:])) - y[0]) / y[0])  #最大三个值减去初始值
    std_lst.append(std_list)
    rate_list.append(grw_rate)



#输出结果
output_data=dirr+'_'+'diff'+'.xlsx'    
workbook = xlsxwriter.Workbook(output_data)    
worksheet = workbook.add_worksheet()
for i in range(0,6):
    j = 8 * i + 3
    k = j -1
    worksheet.write(8*i, 0, color_module[i])  
    worksheet.write_column('A'+str(j), reagent) 
    worksheet.write_column('B'+str(j), std_lst[i])
    worksheet.write_column('C'+str(j), rate_list[i])
    worksheet.write_row('B'+str(k),list_col)

workbook.close()

temp_df = pd.DataFrame(columns = ["reagent", "value"]) #创建一个空的dataframe
df2 = pd.DataFrame(columns = ["reagent", "value"]) 



f = open(dirr +'_' + 'Tukey_test' + '.txt','w')
for i in range(0,6):
    df = pd.DataFrame(mat_y[i])
    df1 = df.T
    df1.columns = ['grp_0','grp_001','grp_01','grp_1','grp_10']
    
    temp_df['value'] = df1['grp_0']
    temp_df['reagent'] = 'grp_0'
    df2 = pd.concat([df2,temp_df])
    
    temp_df['reagent'] = 'grp_001'
    temp_df['value'] = df1['grp_001']
    df2 = pd.concat([df2,temp_df])

    temp_df['reagent'] = 'grp_01'
    temp_df['value'] = df1['grp_01']
    df2 = pd.concat([df2,temp_df])
    
    temp_df['reagent'] = 'grp_1'
    temp_df['value'] = df1['grp_1']
    df2 = pd.concat([df2,temp_df])

    temp_df['reagent'] = 'grp_10'
    temp_df['value'] = df1['grp_10']
    df2 = pd.concat([df2,temp_df])
    
    
    multiComp = MultiComparison(df2['value'], df2['reagent'])
    tukey=multiComp.tukeyhsd()
    summary=multiComp.tukeyhsd().summary()

    q=tukey.q_crit
    
    print("碳源模板颜色为：%s" %color_module[i] , file = f)
    print(summary, file = f)
    print("q values:%2.4f "%q , file = f)
    print("============================================== \n\n" , file = f)
    
    
f.close()


print('finish')