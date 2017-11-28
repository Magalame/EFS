
# coding: utf-8

# In[1]:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os.path
import time


# In[ ]:

#variables qu'on utilisera tout le temps
groupe_to_index = {"O-":1,"A-":2,"B-":3,"AB-":4,"O+":5,"A+":6,"B+":7,"AB+":8}
niveau_to_index = {"near_zero":1,"half":2,"completed":3}
efs = "https://dondesang.efs.sante.fr/barometre"


# In[ ]:

def get_date():
    utc = datetime.utcnow()
    date = str(utc.day)+"-"+str(utc.month)+"-"+str(utc.year)
    return date


# In[ ]:

def entree_existe(database_name,date):
    if not (os.path.isfile(database_name)):
        return False

    pfichier = open(database_name, "r", newline='')
    database = csv.reader(pfichier)

    for row in database:
        if row[0] == date:
            print("There already us a data point for this day")
            return True

    return False


# In[2]:

def preparer_page(url):#prépare le tout: télécharge la page et la change en beautifulsoup object
    page = urlopen(url)
    soupe = BeautifulSoup(page, "html.parser")

    #print(soupe.prettify) #debug

    #on se concentre sur tous les groupe item: les groupes sanguins
    return soupe.find_all('div',class_="group-item")
    #print(groupes_to_parse) #debug


# In[3]:

#count = 0
#groupes = []
def extract_info(groupes_to_parse):

    ligne = [None]*9
    ligne[0] = get_date()

    for i in groupes_to_parse:
#    print("-------------------------------------")
#    print(i)
#    print("-------------------------------------")
        data_groupe = i.find_all('img')[0]
        groupe = data_groupe.get("alt")
        niveau = data_groupe.get("src").split('/')[-1].split('.')[0]
    #groupes.append([groupe,niveau])
#    print(groupe,niveau)
 #   print(groupe_to_index[groupe], niveau_to_index[niveau])
        ligne[groupe_to_index[groupe]] = str(niveau_to_index[niveau])

    return ligne



# In[4]:

def sauver_donnee(ligne, nom_fichier):
    nouveau_fichier = False

    if not (os.path.isfile(nom_fichier)):
        nouveau_fichier = True

    pfichier = open("database_efs.csv", "a", newline='') #on fait en sort que le charac return soit rien, autrement on obtient une ligne vide après chaque entrée
    database = csv.writer(pfichier)

    if nouveau_fichier:
        database.writerow(["Date","O-","A-","B-","AB-","O+","A+","B+","AB+"]) #if new file

    database.writerow(ligne)
    pfichier.close()


# In[5]:




# In[11]:

def entree_existe(database_name,date):
    if not (os.path.isfile(database_name)):
        return False

    pfichier = open(database_name, "r", newline='')
    database = csv.reader(pfichier)

    for row in database:
        if row[0] == date:
            print("There already is a data point for this day")
            return True

    return False


# In[19]:

def barometre():
        while True:
                if not entree_existe("database_efs.csv",get_date()):
                        sauver_donnee(extract_info(preparer_page(efs)),"database_efs.csv")
                time.sleep(86400)



# In[20]:

if __name__ == '__main__':
    barometre()