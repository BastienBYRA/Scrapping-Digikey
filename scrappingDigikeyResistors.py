#Bibliotheque disponible par defaut
from random import *
import requests
from time import sleep
import re
import os.path
import csv
import sqlite3
import datetime

#Biblotheque a installer
try:
    from selenium import webdriver
except:
    os.system('cmd /c "py -m pip install selenium"')
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from seleniumwire import webdriver
except:
    os.system('cmd /c "py -m pip install selenium-wire"')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////

    #Variable

#Les chemins
# url = 'https://www.digikey.com/en/products/filter/chassis-mount-resistors/54?s=N4IgjCBcpgnAHLKoDGUBmBDANgZwKYA0IA9lANogAMIAusQA4AuUIAykwE4CWAdgOYgAvkOIBWZCAZQwjaZDBUqIoA'
url = 'https://digikey.com/'

csvpath = 'D:/SCRAPPING/PCBComposantScrapCSV.csv' #Chemin pour le fichier CSV
Chromepath = 'D:/SCRAPPING/chromedriver.exe' #Chemin pour le chromedriver

#Variable lié a la navigation a travers les différentes pages, currentpage etant la page actuelle, numpage etant les pages de types de resistances
currentpage, numpage = 1, 2

#Variable de vérificarion d'arriver jusqu'au bout, et empeche de continuer si il manque des informations
arriver, dataEnt, arret = False, False, 0

#Nom de la base
dbname = 'PCBComposantScrapDB'

#Variable lié aux noms des catégories de Resistances
categorieResistance = "Vide"
catRes = "Vide"

            #Les tableaux + leurs colonnes
#Différentes listes ou l'on stock les valeurs
nbProdAffiche = 100 #Nombre de resultats afficher dans une page sur le site
tabRef = [None] * nbProdAffiche #Mfr Part
tabQtte = [None] * nbProdAffiche #Stock
tabFab = [None] * nbProdAffiche #Mfr
tabDesc = [None] * nbProdAffiche #Mfr Part
tabOhms = [None] * nbProdAffiche #Resistance
tabOhmsUnite = [None] * nbProdAffiche #Resistance
tabWatts = [None] * nbProdAffiche #Power (Watts)
tabWattsUnite = [None] * nbProdAffiche #Power (Watts)
tabTole = [None] * nbProdAffiche #Tolerance
tabTemperatureMin = [None] * nbProdAffiche #Operating Temperature
tabTemperatureMax = [None] * nbProdAffiche #Operating Temperature
tabTempCoef = [None] * nbProdAffiche #Temperature Coefficient
tabDegres = [None] * nbProdAffiche #Temperature Coefficient
tabCompo = [None] * nbProdAffiche #Composition
tabFeature = [None] * nbProdAffiche #Feature
tabRating = [None] * nbProdAffiche #Ratings
tabSeries = [None] * nbProdAffiche #Series
tabTermination = [None] * nbProdAffiche #Number of Terminations
tabCodeCaisse = [None] * nbProdAffiche #Supplier Device Package / #Package / Case
tabPackage = [None] * nbProdAffiche #Packaging
tabLength = [None] * nbProdAffiche #Size/Dimension
tabWidth = [None] * nbProdAffiche #Size/Dimension
tabDiametre = [None] * nbProdAffiche #Size/Dimension
tabHeight = [None] * nbProdAffiche #Height
tabCoating = [None] * nbProdAffiche #Coating, Housing Type
tabMountingFeature = [None] * nbProdAffiche #Mounting Feature
tabMountingType = [None] * nbProdAffiche #Mounting Type
tabLead = [None] * nbProdAffiche #Lead Style
tabCircuit = [None] * nbProdAffiche #Circuit Type
tabNumRes = [None] * nbProdAffiche #Number of Resistors
tabPins = [None] * nbProdAffiche #Number of Pins
tabMatchingRadio = [None] * nbProdAffiche #Resistor Matching Ratio
tabRadioDrift = [None] * nbProdAffiche #Resistor-Ratio-Drift
tabApplication = [None] * nbProdAffiche #Applications
tabType = [None] * nbProdAffiche #Type

#Recherche groupé ou l'on prend les valeurs tels quels
ListID = ["tr-manufacturer", "CLS 16", "tr-series", "CLS 174", "CLS 5", "CLS 707", "CLS 1349", "CLS 1061", "CLS 69", "CLS 4", "CLS 9", "CLS 2314", "CLS 10","CLS 405", "CLS 183", "CLS 1127"]
listeTab = [tabFab, tabCodeCaisse, tabSeries, tabCompo, tabFeature, tabRating, tabCoating, tabMountingFeature, tabMountingType, tabLead, tabCircuit, tabNumRes, tabPins, tabApplication, tabType, tabTermination]

#Tableaux pour éviter de faire plusieurs fois les memes lignes de code dans l'update sqlite
nomUpdate = ['Fabriquant', 'Description', 'Quantites', 'Ohms','UniteOhms', 'Watts', 'UniteWatts', 'Tolerance', 'Series', 'Package','Rating', 'Feature', 'TemperatureMin', 'TemperatureMax', 'CoefficientTemperature', 'Degres','CompoTechno', 'Terminaison', 'Longueur', 'Largeur', 'Hauteur', 'Diametre', 'Coating', 'MountingFeature', 'MountingType', 'Lead',  'Circuit', 'NombrePins', 'NombreResistance', 'MatchingRadio', 'RadioDrift', 'Application', 'Type', 'CodeCaisse']
tabUpdate = [tabFab, tabDesc, tabQtte, tabOhms, tabOhmsUnite,tabWatts, tabWattsUnite, tabTole, tabSeries, tabPackage,tabRating, tabFeature, tabTemperatureMin, tabTemperatureMax,tabTempCoef, tabDegres,tabCompo, tabTermination, tabLength, tabWidth, tabHeight, tabDiametre, tabCoating, tabMountingFeature, tabMountingType, tabLead, tabCircuit, tabPins, tabNumRes, tabMatchingRadio, tabRadioDrift, tabApplication, tabType, tabCodeCaisse]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////

    #Initialisation de Selenium

chrome_options = Options()

#Divers arguments permettant le bon fonctionnement
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-extensions")         
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--allow-running-insecure-content')

# #Pour ne pas charger les images
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

#Cette partie me permet de pouvoir me debloquer des "Access Denied"
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options, executable_path=Chromepath)

driver.get(url)

    #Verification de l'existance et creation du fichier CSV

if os.path.isfile(csvpath):
    pass
else:
    with open(csvpath,'w',newline='') as unFichierCSV:
        writer = csv.writer(unFichierCSV)
        writer.writerow(['Reference', 'Site', 'Fabriquant', 'Description', 'Quantites', 'Categorie de Resistance' 'Ohms','Unite des Ohms', 'Watts', 'Unite des Watts', 'Voltage', 'Unite du Voltage', 'Frequence', 'Tolerance', 'Series', 'Package','Rating', 'Feature', 'Temperature Minimum', 'Temperature Maximum', 'Coefficient de Temperature', 'Degres','Compo/Technologie', 'Raccordement', 'Terminaison', 'Longueur', 'Largeur', 'Hauteur', 'Diametre', 'Nombre de Tour', 'Coating','Mounting Feature', 'Mounting Type', 'Lead', 'Espacement des fils', 'Diametre du fil de sortie', 'Circuit', 'Nombre de Resistance', 'Nombre de Pins / Broche', 'Broche', 'Matching Radio','Radio Drift', 'Application', 'Type', 'Style de Montage', 'Bande Resistive', 'Orientation', 'Type Element', 'Type Arbre', 'Longueur Arbre', 'Unite de la longueur Arbre', 'Diametre Arbre', 'Unite de diametre Arbre', 'Nombre de Crans', 'Type Interrupteur','Duree de Vie', 'Heure/Cycle de Vie', 'Classe IP', 'Linearite', 'Reglage', 'Cadre', 'Fonction', 'NombreVoie', 'Code de Caisse / Package / Case'])


    #Creation et connexion de la base de données
con = sqlite3.connect(dbname + '.db')
cur = con.cursor()

try:
    cur.execute('''CREATE TABLE IF NOT EXISTS Resistance(
        Reference text NOT NULL,
        SiteWeb text NOT NULL,
        Fabricant text,
        Description text,
        Quantites int,
        CategorieDeResistance text,
        Ohms real,
        UniteOhms text,
        Watts real,
        UniteWatts text,
        Voltage real,
        UniteVoltage text,
        Frequence real,
        Tolerance real,
        Series text,
        Package text,
        Rating text,
        Feature text,
        TemperatureMin int,
        TemperatureMax int,
        CoefficientTemperature real,
        Degres text,
        CompoTechno text,
        StyleRaccordement text,
        Terminaison int,
        Longueur real,
        Largeur real,
        Hauteur real,
        Diametre real,
        NombreTours real,
        Coating text,
        MountingFeature text,
        MountingType text,
        Lead text,
        EmplacementFils real,
        DiametreFils real,
        Circuit text,
        NombrePins int,
        NombreResistance real,
        MatchingRadio real,
        RadioDrift real,
        Application text,
        Type text,
        StyleMontage text,
        BandeResistive text,
        Orientation text,
        TypeElement text,
        TypeArbre text,
        LongueurArbre real,
        UniteLongArb text,
        DiametreArbre real,
        UniteDiamArbre text,
        NombreCrans real,
        TypeInterrupteur text,
        DureeVie real,
        HeureCycleVie text,
        ClasseIP text,
        Linearite text,
        Reglage text,
        Cadre text,
        Fonction text,
        NombreVoie real,
        CodeCaisse text,
        PRIMARY KEY (Reference, SiteWeb))
    ''');
except:
    pass

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////

#Connection au différentes pages de Ress

def status(undriver): #Permet de cliquer et appliquer le status "active", ainsi qu'afficher 100 résultats
    #cliquer et appliquer le status "active"
    sleep(15)
    # undriver.find_element_by_xpath('//div[@class="MuiBox-root jss200 jss156"]/div/fieldset/div/div/div/span/span').click()
    undriver.find_element_by_xpath('//section[@data-testid="filter-page"]/div/section/div[2]/div/div[4]/div/div[2]/div/fieldset/div/div/div/span/span').click()
    undriver.find_element_by_xpath('//button[@data-testid="apply-all-button"]').click()
    sleep(5)
    #affiche 100 résultats
    driver.find_element_by_xpath('//div[@data-testid="per-page-selector"]/div').click()
    sleep(2)
    driver.find_element_by_xpath('//ul[@class="MuiList-root MuiMenu-list MuiList-padding"]/li[3]').click()
    sleep(5)

if url == "https://digikey.com/":
	#Pour cliquer sur Resistors dans le menu Products View All
	driver.find_element_by_xpath("//div[@id='leftColumn']/div/ul[2]/li[6]/h3/a").click()
	sleep(5)
	catRes = driver.find_element_by_xpath('//div[@data-testid="parent-category-container-2"]/ul[@data-testid="subcategories-container"]/li[2]/a/span')
	categorieResistance = catRes.text
	# categorieResistance.text
	driver.find_element_by_xpath('//div[@data-testid="parent-category-container-2"]/ul[@data-testid="subcategories-container"]/li[2]/a').click()
	#li[2] par exemple signifie le deuxieme menu de Res (Chassis mount resistors, le premier qui nous intéresse en l'occurence)
	status(driver)
else:
	pass

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////

    #Recherche des différentes valeurs voulues
while(1): #Boucle toujours vrai, pour faire toutes les pages


    #Refresh toutes les 30 pages, car perd de la vitesse au fur et a mesure du traversement des pages
    if currentpage%31 == 0:
        curl = driver.current_url
        driver.quit()
        sleep(3)
        driver = webdriver.Chrome(options=chrome_options, executable_path=Chromepath)
        driver.get(curl)
    else:
        pass

    if arriver == False:
            try:  
                begin_time = datetime.datetime.now()

                #Permet de récuperer le nombre d'article afficher dans la page actuel (seulement utile pour la dernière page)
                nbArticle = len(driver.find_elements_by_xpath("//a[@data-testid='data-table-0-product-number']"))

                arriver = False

                #Reference
                elements = driver.find_elements_by_xpath("//a[@data-testid='data-table-0-product-number']")
                cptTour=0
                for element in elements:    
                    tabRef[cptTour] = "".join(element.text)
                    cptTour = cptTour+1

                # Description
                elements = driver.find_elements_by_xpath("//div[@data-testid='data-table-0-product-description']")
                cptTour=0
                for element in elements:    
                    tabDesc[cptTour] = "".join(element.text)
                    cptTour = cptTour+1

                # Quantite
                elements = driver.find_elements_by_xpath("//td[@data-atag='tr-qtyAvailable']")
                cptTour=0
                for element in elements:    
                    #Permet de ne récupérer que la quantité
                    elementsplit = element.text.split()
                    nombreqtte = elementsplit[0]
                    if "," in nombreqtte:
                        value = nombreqtte.replace(",", "")
                        tabQtte[cptTour] = "".join(value)
                        cptTour = cptTour+1
                    elif nombreqtte != "-":
                        tabQtte[cptTour] = "".join(nombreqtte)
                        cptTour = cptTour+1
                    else:
                        tabQtte[cptTour] = None
                        cptTour = cptTour+1

                # Res, Nombre et Unité
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 2085']")
                cptTour=0
                for element in elements:    
                    valeurRes = element.text.split()
                    if len(valeurRes)>1 or valeurRes[0] != "-":

                        valeurResfloat = 0
                        valeurOhms = valeurRes[0]
                        uniteOhms = valeurRes[1]

                        if '.' in valeurOhms:
                            valeurResfloat = round(float(valeurOhms), 2) #round permet d'arrondir, pour ne pas avoir des resultat comme '6.800000190734863'
                            tabOhms[cptTour] = "".join(str(valeurResfloat))
                            tabOhmsUnite[cptTour] = "".join(uniteOhms)
                            cptTour+=1
                        else:
                            tabOhms[cptTour] = "".join(valeurOhms)
                            tabOhmsUnite[cptTour] = "".join(uniteOhms)
                            cptTour = cptTour + 1
                    else:
                        tabOhms[cptTour] = None
                        tabOhmsUnite[cptTour] = None
                        cptTour = cptTour+1


                #Tolerance
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 3']")
                cptTour=0
                for element in elements:
                    valeurTole = element.text.split()
                    if valeurTole[0] != "-" and len(valeurTole)> 0:

                        valeurTolerance = valeurTole[0]

                        if valeurTolerance == "Jumper":
                            tabTole[cptTour] = 0
                            cptTour = cptTour+1
                        elif len(valeurTole) == 1:
                            val = valeurTolerance.replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('%', "")
                            tabTole[cptTour] = val
                            cptTour = cptTour+1
                        elif len(valeurTole) > 1 and valeurTolerance == "0%," or valeurTolerance == "-0%,":
                            valeurTolerance2 = valeurTole[1]
                            val = valeurTolerance2.replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('%', "")
                            tabTole[cptTour] = val
                            cptTour = cptTour+1
                        else:
                            val = valeurTolerance.replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('%', "")
                            tabTole[cptTour] = val
                            cptTour = cptTour+1
                    else:
                        tabTole[cptTour] = None
                        cptTour = cptTour+1

                # Watts
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 2']")
                cptTour=0
                for element in elements:    
                    valeurColWatts = element.text.split()
                    if len(valeurColWatts)>0 and valeurColWatts[0] != "-":

                        valeurWatts = valeurColWatts[0].strip(",")
                        valeurWatts = valeurWatts.strip("W")
                        uniteWatts = valeurColWatts[0].join(filter(str.isalpha, valeurColWatts[0]))

                        tabWatts[cptTour] = str(valeurWatts)
                        tabWattsUnite[cptTour] = str(uniteWatts)
                        cptTour = cptTour+1
                    else:
                        tabWatts[cptTour] = None
                        tabWattsUnite[cptTour] = None
                        cptTour = cptTour+1

                # Operating Temperature, Minimum et Maximum
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 252']")
                cptTour=0
                for element in elements:    
                    valeurColTempMin = element.text.split()
                    if valeurColTempMin[0] == "-": #Si il n'y a rien de renseigné
                        tabTemperatureMin[cptTour] = None
                        tabTemperatureMax[cptTour] = None
                        cptTour = cptTour+1
                    else:
                        temperatureMin = valeurColTempMin[0]
                        temperatureMax = valeurColTempMin[-1]

                        #Valeur froid (negative)
                        temperatureMin = re.findall('\d+', temperatureMin)
                        temperatureMin[0] = "-" + temperatureMin[0]
                        tabTemperatureMin[cptTour] = temperatureMin[0]

                        #Valeur chaud (positive)
                        temperatureMax = re.findall('\d+', temperatureMax)
                        tabTemperatureMax[cptTour] = temperatureMax[0]
                        cptTour = cptTour+1

                # Coefficient de temperature
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 17']")
                cptTour=0
                for element in elements:
                    #Permet de recupérer que le nombre utile
                    if element.text != "-":
                        valeurCoefficientDeTemperature = element.text.strip('±')
                        valeurCoefficientDeTemperature = valeurCoefficientDeTemperature.strip('ppm/°C')

                        if str(valeurCoefficientDeTemperature).isdigit():
                            tabTempCoef[cptTour] = "".join(valeurCoefficientDeTemperature)
                            tabDegres[cptTour] = "Celsius"
                            cptTour = cptTour+1

                        elif "0/" in valeurCoefficientDeTemperature:
                            valeurCoefficientDeTemperature = re.findall('\-{0,1}\d+', valeurCoefficientDeTemperature)

                            if valeurCoefficientDeTemperature[0] != '0':
                                tabTempCoef[cptTour] = "".join(valeurCoefficientDeTemperature[0])
                                tabDegres[cptTour] = "Celsius"
                                cptTour = cptTour+1

                            else:
                                tabTempCoef[cptTour] = "".join(valeurCoefficientDeTemperature[1])
                                tabDegres[cptTour] = "Celsius"
                                cptTour = cptTour+1
                        else:
                            tabTempCoef[cptTour] = "".join(valeurCoefficientDeTemperature)
                            tabDegres[cptTour] = "Celsius"
                            cptTour = cptTour+1
                    else:
                        tabTempCoef[cptTour] = None
                        tabDegres[cptTour] = None
                        cptTour = cptTour+1

                #Le fabriquant, le code caisse, les series, la compositionn les feature, le rating
                for a in range(len(ListID)):
                    cptTour=0
                    elements = driver.find_elements_by_xpath("//td[@data-atag='"+ListID[a]+"']")
                    for element in elements: 
                        if element.text != "-":
                            valeurBrutDesCateg = element.text.replace(",", "")
                            valeurBrutDesCateg = valeurBrutDesCateg.replace('"', "")
                            listeTab[a][cptTour] = "".join(valeurBrutDesCateg)
                            cptTour = cptTour+1
                        else:
                            listeTab[a][cptTour] = None
                            cptTour = cptTour+1

                # Package
                elements = driver.find_elements_by_xpath("//td[@data-atag='tr-packaging']")
                cptTour=0
                for element in elements: 
                    if element.text != "-":
                        tabPackage[cptTour] = "".join(element.text.splitlines())
                        tabPackage[cptTour] = tabPackage[cptTour].strip("®")
                        cptTour = cptTour+1
                    else:
                        tabPackage[cptTour] = None
                        cptTour = cptTour+1

                #Longueur et Largeur et Diametre
                cptTour=0
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 46']")
                for element in elements:
                    if element.text != "-":
                        value = element.text.split() #value peut, selon le résultats, etre un résultat diamètre, longueur ou largeur.

                        if value[1] == "Dia":
                            if len(value) < 4:
                                val = value[2].replace("(", "")
                                val = val.replace(")", "")
                                val = val.replace("mm", "")
                                tabDiametre[cptTour] = val
                                cptTour=cptTour+1
                            else:
                                if value[4] == "W":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabDiametre[cptTour] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabWidth[cptTour] = val
                                    cptTour=cptTour+1
                                elif value[4] == "L":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabDiametre[cptTour] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabLength[cptTour] = val
                                    cptTour=cptTour+1
                                else:
                                    pass

                        elif value[1] == "W":
                            if value[4] == "Dia":
                                val = value[5].replace("(", "")
                                val = val.replace("mm", "")
                                tabWidth[cptTour] = val
                                val = value[7].replace(")", "")
                                val = val.replace("mm", "")
                                tabDiametre[cptTour] = val
                                cptTour=cptTour+1
                            elif value[4] == "L":
                                val = value[5].replace("(", "")
                                val = val.replace("mm", "")
                                tabWidth[cptTour] = val
                                val = value[7].replace(")", "")
                                val = val.replace("mm", "")
                                tabLength[cptTour] = val
                                cptTour=cptTour+1

                        elif value[1] == "L":
                            if value[4] == "Dia":
                                val = value[5].replace("(", "")
                                val = val.replace("mm", "")
                                tabLength[cptTour] = val
                                val = value[7].replace(")", "")
                                val = val.replace("mm", "")
                                tabDiametre[cptTour] = val
                                cptTour=cptTour+1
                            elif value[4] == "W":
                                val = value[5].replace("(", "")
                                val = val.replace("mm", "")
                                tabLength[cptTour] = val
                                val = value[7].replace(")", "")
                                val = val.replace("mm", "")
                                tabWidth[cptTour] = val
                                cptTour=cptTour+1


                #Hauteur
                cptTour=0
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 1500']")
                for element in elements:
                    if element.text != "-":
                        valeurHauteur = element.text.split("(")
                        valeurHauteur = valeurHauteur[1].replace("mm", "")
                        valeurHauteur = valeurHauteur.replace(")", "")
                        tabHeight[cptTour] = "".join(valeurHauteur)
                        cptTour = cptTour+1
                    else:
                        tabHeight[cptTour] = None
                        cptTour = cptTour+1

                #tabRadioDrift => Network Array
                cptTour=0
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 2294']")
                for element in elements:

                    #Permet de recupérer que le nombre utile
                    if element.text != "-":
                        valeurRadioDrift = element.text.strip('±')
                        valeurRadioDrift = valeurRadioDrift.strip('ppm/°C')
                        if str(valeurRadioDrift).isdigit():
                            tabRadioDrift[cptTour] = "".join(valeurRadioDrift)
                            cptTour = cptTour+1
                        else:
                            tabRadioDrift[cptTour] = None
                            cptTour = cptTour+1
                    else:
                        tabRadioDrift[cptTour] = None
                        cptTour = cptTour+1

                #tabMatchingRadio => Network Array
                cptTour=0
                elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 2293']")
                for element in elements:
                    #Permet de recupérer que le nombre utile
                    valeurColMatchingRadio = element.text.split()
                    if valeurColMatchingRadio[0] != "-" and len(valeurColMatchingRadio)> 0:
                        valeurMatchRad = valeurColMatchingRadio[0].replace('±', '')
                        valeurMatchRad = valeurMatchRad.replace('%', '')
                        tabMatchingRadio[cptTour] = "".join(valeurMatchRad)
                        cptTour = cptTour+1
                    else:
                        tabMatchingRadio[cptTour] = None
                        cptTour = cptTour+1

                if numpage == 4:
                    # Watts => Network Array
                    cptTour=0
                    elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 8']")
                    for element in elements:
                        if element.text != "-" and 'mW' in element.text:
                            valeurColWattsrWatts = element.text.split('mW')
                            tabWatts[cptTour] = valeurColWattsrWatts[0]
                            tabWattsUnite[cptTour] = 'mW'
                            cptTour+=1
                        elif element.text != "-" and 'W' in element.text:
                            valeurColWattsrWatts = element.text.split('W')
                            tabWatts[cptTour] = valeurColWattsrWatts[0]
                            tabWattsUnite[cptTour] = 'W'
                            cptTour+=1
                else:
                    pass
                   
                # Ohms => Network Array
                if numpage == 4:
                    cptTour=0
                    elements = driver.find_elements_by_xpath("//td[@data-atag='CLS 1']")
                    for element in elements:
                        if element.text != "-":
                            # val = element.text.replace(",", "")
                            val = element.text.split(",")
                            if len(val) == 1:
                                if str(val[0]).isdigit() or re.findall('\d+\.\d+', val[0]):
                                    tabOhms[cptTour] = "".join(val[0])
                                    tabOhmsUnite[cptTour] = "".join("Ohms")
                                    cptTour+=1
                                elif "k" in str(val[0]) and str(val[0]).isdigit() or re.findall('\d+\.\d+', val[0]):
                                    val = val[0].replace("k", "")
                                    tabOhms[cptTour] = "".join(val)
                                    tabOhmsUnite[cptTour] = "".join("kOhms")
                                    cptTour+=1
                                elif "M" in str(val[0]) and str(val[0]).isdigit() or re.findall('\d+\.\d+', val[0]):
                                    val = val[0].replace("M", "")
                                    tabOhms[cptTour] = "".join(val)
                                    tabOhmsUnite[cptTour] = "".join("MOhms")
                                    cptTour+=1                             
                                elif "G" in str(val[0]) and str(val[0]).isdigit() or re.findall('\d+\.\d+', val[0]):
                                    val = val[0].replace("G", "")
                                    tabOhms[cptTour] = "".join(val)
                                    tabOhmsUnite[cptTour] = "".join("GOhms")
                                    cptTour+=1
                                else:
                                    tabOhms[cptTour] = None
                                    tabOhmsUnite[cptTour] = None
                                    cptTour+=1
                            else:
                                tabOhms[cptTour] = None
                                tabOhmsUnite[cptTour] = None 
                                cptTour+=1          
                else:
                    pass 


                # # Variable pour valider l'arriver jusqu'a la fin
                arriver = True
         except Exception as e: #Probleme avec la récupération des données
            print(e)
            print("Erreur lors de la collecte des données, veuillez patientez")
    else: #dataEnt veut dire l'on n'arrive pas inscrire les données, mais elle sont déja dans les tableaux.
        pass

       

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Ouverture et écriture des données dans le fichier CSV et dans une bases SQLITE3
        if arriver == True:

            for i in range(int(nbArticle)):

                #Ouvre le fichier CSV est ecrit ses résultats
                with open(csvpath,'a',newline='') as unFichierCSV:
                    writer=csv.writer(unFichierCSV)
                    writer.writerow([tabRef[i], "Digikey", tabFab[i], tabDesc[i], tabQtte[i], categorieResistance, tabOhms[i], tabOhmsUnite[i],tabWatts[i], tabWattsUnite[i],None, None, None, tabTole[i], tabSeries[i], tabPackage[i],tabRating[i], tabFeature[i], tabTemperatureMin[i], tabTemperatureMax[i],tabTempCoef[i], tabDegres[i],tabCompo[i], None, tabTermination[i], tabLength[i], tabWidth[i], tabHeight[i], tabDiametre[i], None, tabCoating[i], tabMountingFeature[i], tabMountingType[i], tabLead[i],None, None, tabCircuit[i], tabPins[i], tabNumRes[i], tabMatchingRadio[i], tabRadioDrift[i], tabApplication[i], tabType[i],None, None, None, None, None,None,None,None, None, None, None, None, None, None, None, None, None,None, None, tabCodeCaisse[i]])

                    #Entre les resultats dans une base, si Ref non existante, l'écrit, sinon, l'update
                    insertdata = '''INSERT INTO Resistance VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                    data = (tabRef[i], "Digikey", tabFab[i], tabDesc[i], tabQtte[i], categorieResistance, tabOhms[i], tabOhmsUnite[i],tabWatts[i], tabWattsUnite[i],None, None, None, tabTole[i], tabSeries[i], tabPackage[i],tabRating[i], tabFeature[i], tabTemperatureMin[i], tabTemperatureMax[i],tabTempCoef[i], tabDegres[i],tabCompo[i], None, tabTermination[i], tabLength[i], tabWidth[i], tabHeight[i], tabDiametre[i], None, tabCoating[i], tabMountingFeature[i], tabMountingType[i], tabLead[i],None, None, tabCircuit[i], tabPins[i], tabNumRes[i], tabMatchingRadio[i], tabRadioDrift[i], tabApplication[i], tabType[i],None, None, None, None, None,None,None,None, None, None, None, None, None, None, None, None, None,None, None, tabCodeCaisse[i])

                    try: #Entrer les valeurs une première fois
                        cur.execute(insertdata, data)
                        con.commit()
                    except sqlite3.IntegrityError: #Permet de pouvoir entrer les valeurs actuels pour une reference déja entrer

                        #Update seulement si les valeurs sont non vides, permet de ne pas update a des valeurs existante avec des null
                        for nom in nomUpdate: #Fabriquant descri
                            # numerotableau = categorie.index(nom) #index de categorie correspondant a nom
                            nbcat = nomUpdate.index(nom)
                            try:
                                if tabUpdate[nbcat][i] != None:
                                    insertdata = '''UPDATE Resistance SET '''+nom+''' = ? WHERE Reference = ? AND SiteWeb = ?;'''
                                    # print(insertdata)
                                    # print(tabUpdate[nbcat][i])
                                    data = (tabUpdate[nbcat][i], tabRef[i], 'Digikey')
                                    cur.execute(insertdata, data)
                                    con.commit()
                                else:
                                    pass

                                if categorieResistance != None:
                                    insertdata = '''UPDATE Resistance SET CategorieDeResistance = ? WHERE Reference = ? AND SiteWeb = ?;'''
                                    data = (categorieResistance, tabRef[i], 'Digikey')
                                    cur.execute(insertdata, data)
                                    con.commit()
                                else:
                                    pass

                            except sqlite3.OperationalError: #Si les deux script envoie trop de données en meme temps
                                print("Base en cours d'utilisation")
                                sleep(randint(3, 10))

                    except sqlite3.OperationalError: #Si les deux script envoie trop de données en meme temps
                        print("Base en cours d'utilisation")
                        sleep(randint(3, 10))

            dataEnt = True

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

            if dataEnt == True:
                #Cette partie permet passer a la page suivante
                print("page " + str(currentpage) + " fini ! " + str(datetime.datetime.now() - begin_time))
                print(driver.current_url)
                currentpage = currentpage + 1
                pagesuivante = "btn-page-" + str(currentpage)
                arret = 0
                dataEnt = False
                arriver = False
                try:
                    clicksuivant = driver.find_element_by_xpath("//button[@data-testid='btn-next-page']")
                    driver.execute_script("arguments[0].click();", clicksuivant)
                    sleep(15)
                except:
                    try:
                        driver.find_element_by_xpath("//div[@class='MuiGrid-root MuiGrid-container MuiGrid-align-items-xs-center MuiGrid-justify-xs-space-between']/div/div/nav/ol/li[3]/a").click()
                        sleep(10)
                        numpage += 1
                        currentpage = 1
                        catRes = driver.find_element_by_xpath('//div[@data-testid="parent-category-container-2"]/ul[@data-testid="subcategories-container"]/li[2]/a/span')
                        categorieResistance = catRes.text
                        driver.find_element_by_xpath('//div[@data-testid="parent-category-container-2"]/ul[@data-testid="subcategories-container"]/li['+str(numpage)+']/a').click()
                        status(driver)
                    except:
                        driver.quit()
            else:
                pass

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        #Permet de refresh si il y a eu des probleme, voir d'arreter le programme, en evitant que currentpage s'incrémente.
        else:
            print("Probleme lors de la récupération des données, refresh de la page a venir.")
            arret = arret+1
            if arret == 5:
                driver.save_screenshot("erreurDIGIKEY.png")
                sleep(2)
                print("Probleme persistant, arret du script a la page ." + str(currentpage))
                print(driver.current_url)
                driver.quit()
            elif arret>2:
                driver.refresh()
                sleep(15)
            else:
                driver.refresh()
                sleep(5)