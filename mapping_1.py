#!/usr/bin/env python
# coding: utf-8

# # Watttime Interview Assessment

# In[22]:


import pandas as pd


# In[23]:


data_gppd = pd.read_csv("gppd.csv")


# In[24]:


data_entso = pd.read_csv("entso.csv")


# In[25]:


data_platts = pd.read_csv("platts.csv")


# In[ ]:





# #### Function to clen the country names

# In[26]:


def clean(x):
    x = x[:x.find("(")]
    return x   


# In[27]:


data_entso["country"] = data_entso["country"].apply(clean)


# #### Function to remove special characters from plants and unit names

# In[28]:


import re
def special_character(k):
    k = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    return k 


# In[29]:


data_platts["UNIT"] = data_platts["UNIT"].apply(special_character)


# In[30]:


data_entso["unit_name"] = data_entso["unit_name"].apply(special_character)


# In[31]:


data_gppd["plant_name"] = data_gppd["plant_name"].apply(special_character)


# In[32]:


data_entso["plant_name"] = data_entso["plant_name"].apply(special_character)


# #### Read the fuel_thesaurus.csv file 

# In[33]:


import csv
rows = []
with open("fuel_thesaurus.csv") as fuel_file:
    csvreader = csv.reader(fuel_file)
    for row in csvreader: 
        rows.append(row) 

u_fuel = []
p_fuel = []
for z in range(1,len(rows)):
    u_fuel.append(rows[z][0])
    p_fuel.append(rows[z][1])


# #### Function to convert unit fuel to primary fuel 

# In[34]:


def primary_fuel(y):
    if y.lower() in u_fuel:
        index = u_fuel.index(y.lower())
        y = p_fuel[index]
    return y
    


# In[35]:


data_entso["unit_fuel"] = data_entso["unit_fuel"].apply(primary_fuel)


# #### Maping Function

# ##### plant_name , plant primary fuel , country are the three conditions to map gppd.csv and entso.csv file ---> It gives 9 records of gpp_plant_id and entso_unit_id
# ##### wipp_id[plant_id] and unit names are the two conditions to map gppd.csv, entso.csv to platts.csv --> Final common rows for all the three files are two records

# In[36]:


def mapping(data_gppd,data_entso,data_platts):
    gppd_plant_id = []
    entso_unit_id = []
    platts_unit_id =[]

    for p in range(len(data_gppd["plant_id"])):
        for x in range(len(data_entso["plant_name"])):
            if data_gppd["plant_name"][p].lower() == data_entso["plant_name"][x].lower():
                if data_gppd["plant_primary_fuel"][p] == data_entso["unit_fuel"][x]:
                    if data_gppd["country_long"][p] == data_entso["country"][x].strip():
                        if type(data_gppd["wepp_id"][p]) == float:
                            continue
                        else:
                            for k in range(len(data_platts["unit_id"].tolist())): 
                                if int(data_gppd["wepp_id"][p]) == data_platts["plant_id"][k]:
                                    if data_entso["unit_name"][x].lower() == data_platts["UNIT"][k].lower():
                                    
                                        platts_unit_id.append(data_platts["unit_id"][k])
                                        gppd_plant_id.append(data_gppd["plant_id"][p])
                                        entso_unit_id.append(data_entso["unit_id"][x])
    
    
    return platts_unit_id,gppd_plant_id,entso_unit_id               
                        
                        
                    
        


# In[37]:


platts_unit_id,gppd_plant_id,entso_unit_id = mapping(data_gppd,data_entso,data_platts)


# In[38]:


print(platts_unit_id)           
print(entso_unit_id)
print(gppd_plant_id)


# #### Writing output into the mapping.csv file   

# In[39]:


dict = {'gppd_plant_id':gppd_plant_id,'entso_unit_id':entso_unit_id,'platts_unit_id':platts_unit_id}
df = pd.DataFrame(dict)   
df.to_csv('mapping.csv') 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




