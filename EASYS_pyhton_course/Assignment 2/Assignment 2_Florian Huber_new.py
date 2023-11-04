# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 14:42:13 2022

@author: Flori

About handing this doc:
* In line aproxx. 94,95 you can switch human interventions (world with/without human on=TRUE, off=FALSE).
* Same for human reductions although the interpretation differs.
* The only print statement should be the calculation of the bonus part.


"""


import matplotlib.pyplot as plt

import numpy as np

from scipy.integrate import odeint

import time



#%%################################################################Part 1##############################################################


def land_use_change(t,l, switch_1, start_year_1):
    if t<150:
        emission_from_landuse = 0.0033 *t
    elif t<200:
        emission_from_landuse = 0.01 *(t-150) + 0.0033*150
    elif t>start_year_1 and switch_1 == True:
            emission_from_landuse = 0.01 *50 +0.0033*150 - l*(t-start_year_1)
    else:
        emission_from_landuse = 0.01 *50 +0.0033*150 
    
    return (emission_from_landuse)

def fossil_fuel(t,f, switch_2, start_year_2):
    if t<100:
        emission_from_fossil = 0
    elif t<200:
        emission_from_fossil =  0.01483*(t-100)
    elif t<start_year_2:
        emission_from_fossil = .1217*(t-200) +0.01483*100
    elif t>start_year_2 and switch_2==True:
        emission_from_fossil = .1217*(start_year_2-200) +.01483*100 - f*(t-start_year_2)
    else: 
        emission_from_fossil = .1217*(t-200) +0.01483*100
        
        
    return(emission_from_fossil)

emissions_fossil_overtime = []

emissions_land_use_overtime =[]


for year in range(271):
    emissions_fossil_overtime.append(fossil_fuel(year,0,False,0))
    emissions_land_use_overtime.append(land_use_change(year,0,False,0))



plt.figure()

plt.plot([i+1750 for i in range(271)],emissions_fossil_overtime, label="Emission from fossil fuels")
plt.plot([i+1750 for i in range(271)],emissions_land_use_overtime, label="Emission from land use change")


plt.xlabel("Time [yr]")
plt.ylabel("Rate of emissions [PgC/yr]")
plt.legend(loc='upper left')
plt.savefig('Emissions_fossil_land.png')

plt.close()


####################################################################Part 2##########################################################
#%%
#Flow convention: flow_from_to
#Pool convention: pool_(soil, bio, atmo, shall, deep, geo)_der (derivative) init (initial) curr(current)
#derivation convention d_(..)_dt
#the pool_init values are changing



###############################################################switchers###################################################################
switch_intervention = True # humane interventions on(True) off(false) # if switch_intervention == False no reduction is possible
switch_reduction    = True # here you can turn on/off different responses
##################################################################################################################################



#Model
def model(pool_init,t,pool_fossil_init,beta,k_gamma,switch,red_fos, red_land, switch_3, start_year):
    
    
    #should be twelve flows here
    flow_soil_atmo = 62/1250*pool_init[0]   
    flow_bio_soil = 62/730*pool_init[1]
    flow_atmo_shall = 70/600*pool_init[2]
    flow_shall_deep = 60/1000*pool_init[3]
    flow_deep_shall = 60/40000*pool_init[4]
    flow_deep_geo   = 0.2/40000* pool_init[4]
    flow_geo_atmo   = 0.2/(9e7)* pool_init[5]
    
    #Functions
    epsilon = 3.69 + (1.86e-2*(600/2.13))-(1.8e-6*(600/2.13)**2)
    flow_atmo_bio = pool_fossil_init*(1+(beta*np.log(pool_init[2]/600)))
    flow_shall_atmo = k_gamma*(1000+(epsilon*(pool_init[3]-1000)))
    
    #_antro fro antrophogenic
    if switch == True:
        flow_bio_soil_antro = land_use_change(t,red_land, switch_3, start_year)
        flow_bio_atmo_antro = land_use_change(t, red_land, switch_3, start_year)
        flow_geo_atmo_antro = fossil_fuel(t,red_fos, switch_3, start_year)
    else:
        flow_bio_soil_antro = 0
        flow_bio_atmo_antro = 0
        flow_geo_atmo_antro = 0
    
    #should be six mass balance equations here. Convent + Input - Output
    d_soil_dt = flow_bio_soil+flow_bio_soil_antro-flow_soil_atmo
    d_bio_dt  = flow_atmo_bio-flow_bio_atmo_antro-flow_bio_soil-flow_bio_soil_antro
    d_atmo_dt = flow_soil_atmo+flow_shall_atmo+flow_geo_atmo+flow_geo_atmo_antro-flow_atmo_bio-flow_atmo_shall
    d_shall_dt= flow_deep_shall+flow_atmo_shall-flow_shall_atmo-flow_shall_deep
    d_deep_dt = flow_shall_deep-flow_deep_shall-flow_deep_geo
    d_geo_dt  = flow_deep_geo-flow_geo_atmo-flow_geo_atmo_antro
    
    
    
    return [d_soil_dt,d_bio_dt,d_atmo_dt,d_shall_dt,d_deep_dt,d_geo_dt]


#Parameter

#Definition of initial System values. number= 6+3=9
pool_soil_init = 1250 #PgC
pool_bio_init = 730
pool_atmo_init = 600
pool_shall_init = 1000
pool_deep_init = 40000
pool_geo_init = 9e7

pool_initial = [pool_soil_init, pool_bio_init, pool_atmo_init, pool_shall_init, pool_deep_init, pool_geo_init]

#Parameter included as attributes in the function
pool_fossil_init=62 #PgC/yr
beta = .4 #-
k = .07 #yr-1

t=[i for i in range(0,350)]


#List of altering input values

reduction_fossilfuels =[0.1217,0.14,0.2]

reduction_landusechange =[0.01,0.02,0.03]

years_reduction_start =[275,290,305,325] 

pool_solution = []

for i in range(len(years_reduction_start)):
    	pool_solution.append(odeint(model,pool_initial,t,args=(pool_fossil_init,beta,k,switch_intervention,reduction_fossilfuels[0],reduction_landusechange[0],switch_reduction, years_reduction_start[i],)))

print ()

years = [i for i in range(1900,2100)]
years_all = [i for i in range(1750,2100)]


#FIGURES

fig, axes = plt.subplots(nrows=2,ncols=3, )

plt.rcParams['figure.figsize'] = [15, 12]


ax1 = axes[0,0]
ax2 = axes[0,1]
ax3 = axes[0,2]

ax4 = axes[1,0]
ax5 = axes[1,1]
ax6 = axes[1,2]

list_marker=["*","_",".","<"]

if switch_intervention == True and switch_reduction==True:
    
    for i in range(len(years_reduction_start)):
        
        #Study of degrowth rate
        # ax1.plot(years,pool_solution[i][:,0],label='Soil f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="blue", marker = list_marker[i])
        # ax2.plot(years,pool_solution[i][:,1], label='Biosphere f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="yellow", marker = list_marker[i])
        # ax3.plot(years,pool_solution[i][:,2], label='Atmosphere f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="red", marker = list_marker[i])
        # ax4.plot(years,pool_solution[i][:,3], label='Shallow Sea f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="green", marker = list_marker[i])
        # ax5.plot(years,pool_solution[i][:,4], label='Deep Sea f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="purple", marker = list_marker[i])
        # ax6.plot(years,pool_solution[i][:,5], label='Geosphere f='+str(reduction_fossilfuels[i])+"l="+str(reduction_landusechange[i]), c="black", marker = list_marker[i])
        
        #study of year dependence
        ax1.plot(years,pool_solution[i][150:,0],label=str(years_reduction_start[i]+1750), c="blue", marker = list_marker[i])
        ax1.set_title('Soil')
        ax2.plot(years,pool_solution[i][150:,1], label=str(years_reduction_start[i]+1750), c="yellow", marker = list_marker[i])
        ax2.set_title('Biosphere')
        ax3.plot(years,pool_solution[i][150:,2], label=str(years_reduction_start[i]+1750), c="red", marker = list_marker[i])
        ax3.set_title('Atmosphere')
        ax4.plot(years,pool_solution[i][150:,3], label=str(years_reduction_start[i]+1750), c="green", marker = list_marker[i])
        ax4.set_title('Shallow Ocean')
        ax5.plot(years,pool_solution[i][150:,4], label=str(years_reduction_start[i]+1750),c="purple", marker = list_marker[i])
        ax5.set_title('Deep Ocean')
        ax6.plot(years,pool_solution[i][150:,5], label=str(years_reduction_start[i]+1750), c="black", marker = list_marker[i])
        ax6.set_title('Geosphere')
        
        fig.text(0.5, 0.04, 'Year [yr]', ha='center', va='center')
        fig.text(0.06, 0.5, 'Carbon Stocks [PgC]', ha='center', va='center', rotation='vertical')

        
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        
        
        plt.savefig('Task 3_4.png')
        plt.close()
        
elif switch_intervention == True and switch_reduction==False: 
    i=1
    ax1.plot(years,pool_solution[i][150:,0],label='Soil ', c="blue")
    ax1.set_title('Soil')
    ax2.plot(years,pool_solution[i][150:,1],  c="yellow")
    ax2.set_title('Biosphere')
    ax3.plot(years,pool_solution[i][150:,2],  c="red")
    ax3.set_title('Atmosphere')
    ax4.plot(years,pool_solution[i][150:,3],  c="green")
    ax4.set_title('Shallow Sea')
    ax5.plot(years,pool_solution[i][150:,4],  c="purple")
    ax5.set_title('Deep Ocean')
    ax6.plot(years,pool_solution[i][150:,5],  c="black")
    ax6.set_title('Geosphere')
    
   
    
    fig.text(0.5, 0.04, 'Year [yr]', ha='center', va='center')
    fig.text(0.06, 0.5, 'Carbon Stocks [PgC]', ha='center', va='center', rotation='vertical')
    
    plt.savefig('Task 3_2.png')
    plt.close()

elif switch_intervention == False:
    
    i=0
    ax1.plot(years_all,pool_solution[i][:,0], c="blue")
    ax1.set_title('Soil')
    ax2.plot(years_all,pool_solution[i][:,1], c="yellow")
    ax2.set_title('Biosphere')
    ax3.plot(years_all,pool_solution[i][:,2], c="red")
    ax3.set_title('Atmosphere')
    ax4.plot(years_all,pool_solution[i][:,3], c="green")
    ax4.set_title('Shallow Ocean')
    ax5.plot(years_all,pool_solution[i][:,4], c="purple")
    ax5.set_title('Deep Sea')
    ax6.plot(years_all,pool_solution[i][:,5], c="black")
    ax6.set_title('Geosphere')
    
   

    fig.text(0.5, 0.04, 'Year [yr]', ha='center', va='center')
    fig.text(0.06, 0.5, 'Carbon Stock [PgC]', ha='center', va='center', rotation='vertical')

    plt.savefig('Task 2.png')
    plt.close()



#%%#Analysis of correlation shallow ocean atmosphere for ID4 2055

np.corrcoef(pool_solution[3][:,2],pool_solution[3][:,3]).round(5)



#%% ##############################################################BONUS#############################################################
# rather brutal but should work do calculations as long as Pool year 2100 is <300*2.13 then stop.
# true value should be between value n and n-1
# assumptions: No change in land use change 
# year 2055 start of reduction
# takes 16 sec time to run so be careful with the print statement :)
# makes only sense to to run this piece if interventions and reduction == True


reduction_fossil_bonus = [0.1217+i*0.001 for i in range(1000)]

list_last_year =[1000]

pool_solution_bonus =[]


list_of_goal =[300*2.13 for i in range(len(list_last_year))]

start_clock = time.time()

i=0

if switch_intervention == True and switch_reduction == True:
    while list_last_year[i]>300*2.13:
       	pool_solution_bonus.append(odeint(model,pool_initial,t,args=(pool_fossil_init,beta,k,switch_intervention,reduction_fossil_bonus[i],reduction_landusechange[0],switch_reduction, years_reduction_start[2],)))
        
        list_last_year.append(pool_solution_bonus[i][349,2])
        
        i = i+1
    
    print ('Reduction rate '+str(round(reduction_fossil_bonus[i],4))+" done in "+str(i-1)+" iterations and in "+str(round(time.time()-start_clock,))+"s")
else:
    print('It makes no sense to print this code. Please choose both switchs == TRUE')





#%%Figure BONUS


if switch_intervention == True and switch_reduction == True:
    years_bonus = [i+1750 for i in range(len(pool_solution_bonus[0][:,2]))]
    plt.figure()
  
    for i in range(len(pool_solution_bonus)):
        plt.plot(years_bonus,pool_solution_bonus[i][:,2])
        plt.xlabel('Year')
        plt.ylabel('Atmosphere Pool (PgC)')
  
    plt.savefig('Bonus_2055')
    plt.close() 
    
else:
    print('It makes no sense to print this code. Please choose both switchs line 92,93 == TRUE')




