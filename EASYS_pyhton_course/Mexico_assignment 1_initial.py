# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 14:21:23 2022

@author: Flori
"""




import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


######################################### Part 1 ##################################################

temp_data = open('Mexico-TAVG-Trend.txt','r')

#%% TASK 1

int()

year_list = []

months_list = []

anommalie_list = []

for line in temp_data:
    if line.startswith("%")  == False:
        
            year_list.append(line[2:6])
            months_list.append(line[10:12])
            anommalie_list.append(line[16:22])

    break


year_list.pop(0)
months_list.pop(0)
anommalie_list.pop(0)



for i in range(len(year_list)):

    year_list[i] =int(year_list[i])
    months_list[i] =int(months_list[i])
    anommalie_list[i] = float(anommalie_list[i])
    
    
#%% TASK 2

subset_list_year = []
subset_list_month = []
subset_list_anommalie =[]


for i in range(year_list.index(1960),len(year_list)):
    
    subset_list_year.append(year_list[i])
    subset_list_month.append(months_list[i])
    subset_list_anommalie.append(anommalie_list[i])


#%% TASK 3

subset_list=[]

for i in range(len(subset_list_year)):
    subset_list.append([subset_list_year[i], subset_list_month[i], subset_list_anommalie[i]])
 
check_array = np.isnan(subset_list)


def checker (array):
    check_sum = 0
    check_array = np.isnan(array)
    for i in range(len(check_array)):
        for j in range(0,3):
            if check_array[i][j] == True:
                return("You have an error in data point:", i,j)
                check_sum= check_sum +1 
    return(check_sum/(len(check_array)*3), "% NaN margin")

print(checker(check_array))

#%% TASK 4


number_of_years = int(len(subset_list_anommalie)/12)


lower_boundary = [i*12 for i in range(61)]

upper_boundary = [j*12 for j in range(1,62) ]



aver_of_year_list =[]
stdev_of_year_list =[]


for i in range(number_of_years):
    aver_of_year_anom = 0
    stdev_of_year=0
    aver_of_year_anom = sum(subset_list_anommalie[lower_boundary[i]:upper_boundary[i]])/12
    stedv_of_year = np.std(subset_list_anommalie[lower_boundary[i]:upper_boundary[i]])
    stdev_of_year_list.append(stedv_of_year)
    aver_of_year_list.append(aver_of_year_anom)



temp_data.close()

#%% TASK 5

file= open('Mexico-TAVG-Trend.txt','r')

for line in file:
    if line.startswith("%%  Estimated"):
        aver_annual_abso = float(line[58:63])
        aver_annual_stand =float(line[69:73])
        
abso_year = [aver_of_year_list[i]+aver_annual_abso for i in range(len(aver_of_year_list))]

stdev_year = [stdev_of_year_list[i] +aver_annual_stand for i in range(len(stdev_of_year_list))]

percent_error_year = [stdev_of_year_list[i]/abso_year[i]*100 for i in range(len(aver_of_year_list))]



#%% TASK 6

year_plot_list = [1960+i for i in range(61)]

fig = plt.figure()

plt.figure(figsize=(8, 5), dpi=100)
plt.scatter(year_plot_list, abso_year, label = "Mean annual temperature", color="blue",)
#plt.errorbar(year_plot_list, abso_year, label = "Mean annual deviation",  yerr = stdev_year ,ecolor = 'red')


plt.xlabel("Year [a]")
plt.ylabel("Temperature [°C]")

plt.legend(loc ="lower right", ncol=1)

plt.savefig("Part 1 Task 6.png")

plt.close(fig)

############################################Part 2##################################################

#%%Task 1
    

run_mean_aver = []

years_run_mean = [1965+i for i in range(51)]

for i in range (5,len(abso_year)-5): 

    sum_run_mean = round(sum(abso_year[i-5:i+6])/11,3)
    run_mean_aver.append(sum_run_mean)


#%% Task 2

aver_dec = []
year_aver_dec = [1965+(10*i) for i in range(0,6)]

for i in range (5, len(abso_year)-5,10):
    sum_dec = 0
    sum_dec = round(sum(abso_year[i-5:i+5])/10,3)
    aver_dec.append(sum_dec)

if len(year_aver_dec)== len(aver_dec):
    print(True)

fig = plt.figure()

plt.figure(figsize=(8, 5), dpi=100)
plt.scatter(year_aver_dec, aver_dec, label = "Decadian Temperature Mean", color="green",)

plt.xlabel("Year [a]")
plt.xlim(1960,2020)
plt.ylabel("Temperature [C]")

plt.legend(loc ="lower right", ncol=1)

plt.savefig("Part 2 Task 2.png")

plt.close(fig)

#%% Task 3

linear_regressions =[]

for i in range(5):
    linear_regressions.append(stats.linregress(year_aver_dec[0:i+2],aver_dec[0:i+2]))


regress_value= []

for j in range(5):
    regress_value.append([linear_regressions[j][0]*i+linear_regressions[j][1] for i in range(1960,2021)])



fig = plt.figure()

plt.figure(figsize=(8, 5), dpi=100)
plt.scatter(year_plot_list, abso_year, label = "Annual Temperature Mean", color="blue",)

plt.plot(year_plot_list,regress_value[0], label ="Regression 1965-1975", color="green")
plt.plot(year_plot_list,regress_value[1], label ="Regression 1965-1985", color="red")
plt.plot(year_plot_list,regress_value[2], label ="Regression 1965-1995", color="orange")
plt.plot(year_plot_list,regress_value[3], label ="Regression 1965-2005", color="purple")
plt.plot(year_plot_list,regress_value[4], label ="Regression 1965-2015", color="yellow")

plt.xlabel("Year [a]")
plt.xlim(1960,2020)

plt.ylabel("Temperature [C]")

plt.legend(loc ="lower right", ncol=1)

plt.savefig("Part 2 Task 3.png")

plt.close(fig)





#%% Task 4 


fig = plt.figure()

plt.figure(figsize=(8, 5), dpi=100)

plt.scatter(year_aver_dec, aver_dec, label = "Decadian Temperature Mean", color="blue",)

plt.plot(years_run_mean,run_mean_aver, label ="11-year-running mean", color="green")

plt.plot(year_plot_list,regress_value[4], label ="Regression 1965-2015 "+", m="+str(round(linear_regressions[4][0],3)), color="red")


plt.xlabel("Year [a]")
plt.xlim(1960,2020)

plt.ylabel("Temperature [C]")

plt.legend(loc ="lower right", ncol=1)

plt.savefig("Part 2 Task 2.png")

plt.close(fig)


#%% Task 5

upper_sum = sum([regress_value[4][i]-abso_year[i] for i in range(len(abso_year))])

lower_sum = sum(abso_year)

pbias =100*upper_sum/lower_sum


#Formula used for NRMSE calculations: https://en.wikipedia.org/wiki/Root-mean-square_deviation


rmse = np.sqrt(round(sum([(abso_year[i]-regress_value[4][i])**2 for i in range(len(abso_year))]),3)/len(abso_year))

nrmse = round(rmse/np.mean(abso_year),3)
# I chose here average for normalization because it is more significant than max-min in terms of considerd data points


##############################################PART 3#######################################################



#%%Task 1
albedo_list = [i/1000 for i in range (200,425,25)]

solar_konst = 1361 #W/m^2

planck_konst = 5.67e-8 # W/(m2K4)

#Calculate TE dependent on A


f_array = np.zeros((len(abso_year),len(albedo_list)))



for i in range(len(f_array[:,0])):
    for j in range(len(f_array[0,:])):
        f_array[i,j]= 2*(1-(solar_konst*(1-albedo_list[j])/(4*planck_konst*(abso_year[i]+273.15)**4)))



#%% Task 2
corrupt_elements=[]        
        
for i in range(len(f_array[:,0])):
    for j in range(len(f_array[0,:])):
        if f_array[i,j]>1:
            
            f_array[i,j]=1

            corrupt_elements.append([abso_year[i],albedo_list[j]])
            
            
if len(corrupt_elements)==0:
    print('There are no corrupt values')
else:
    
    print('There are corrupt data Ti, Ai pairs')
    print(corrupt_elements)



#%% Task 3 I was not sure if we should calculate F[i,j] for each Intervall (Solution1) or only 1960-2020 (Solution 2)

#Solution1
delta_F = np.zeros((61,9))
    
for i in range(len(delta_F[:,0])):
    for j in range(len(delta_F[0,:])):
        delta_F[i,j]=(abso_year[i]-abso_year[0])*4*(1-f_array[i,j]/2)*planck_konst*(abso_year[0]+273.15)**3

#Solution2

delta_F_last = delta_F[60,:]

#%% *****************************************optional*****************************************************

deltaF_linear = stats.linregress(range(61),delta_F[:,5])


deltaF_linear_values = [deltaF_linear[0]*i +deltaF_linear[1] for i in range (61)]

fig = plt.figure()

plt.figure(figsize=(8, 5), dpi=100)

for i in range(len(albedo_list)):
    plt.plot(year_plot_list,delta_F[:,i], label ="A="+" "+str(albedo_list[i]))


plt.plot(year_plot_list,deltaF_linear_values, label ='Linear Regression for A=0.3')

plt.xlabel("Year [a]")
plt.xlim(1960,2020)

plt.ylabel("delta F [W/m^2]")


plt.legend( loc="upper left", ncol=2)


plt.savefig("Part 3 Task 3.png")

plt.close(fig)


#%%


albedo = np.arange(.2,.4,.025)

temperature = np.arange(250,300)


def f_function (albedo,temperature):
    solar_konst = 1361  # W/m^2
    planck_konst = 5.67e-8  # W/(m2K4)
    alb, temp = np.meshgrid(albedo,temperature)
    f = 2*(1-(solar_konst*(1-alb)/(4*planck_konst*(temp+273.15)**4)))

    return f


print(f_function(albedo,temperature))
