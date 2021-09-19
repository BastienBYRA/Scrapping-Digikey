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
# url = 'https://www.digikey.com/en/products/filter/aluminum-polymer-capacitors/69?s=N4IgjCBcpgnAHLKoDGUBmBDANgZwKYA0IA9lANogAMIAusQA4AuUIAykwE4CWAdgOYgAviKA'
url = 'https://digikey.com/'

csvpath = 'D:/SCRAPPING/PCBCondansateurCSV.csv' #Chemin pour le fichier CSV
Chromepath = 'D:/SCRAPPING/chromedriver.exe' #Chemin pour le chromedriver

#Différentes listes ou l'on stock les valeurs
nbProdAffiche = 100 #Nombre de resultats afficher dans une page sur le site

#Variable lié aux noms des catégories de Resistances
categorieResistance = "Vide"
catRes = "Vide"

#Les tableaux + leurs colonnes
# tabRef = tabQtte = tabFab = tabDesc =tabOhms =tabOhmsUnite =tabWatts =tabWattsUnite =tabTole =tabTempsUtiDeb =tabTempsUtiFin =tabTempCoef =tabDegres =tabCompo =tabFeature =tabRating =tabSeries =tabTermination =tabCodeCaisse =tabPackage =tabSize =tabHeight =tabCoating =tabMountingFeature = tabMountingType =tabLead =tabCircuit =tabNumRes =tabPins =tabMatchingRadio =tabRadioDrift =tabApplication =tabType = [None] * nbProdAffiche
tabRef = [None] * nbProdAffiche #Référence
tabFab = [None] * nbProdAffiche #Fabricant
tabDesc = [None] * nbProdAffiche #Description
tabQtte = [None] * nbProdAffiche #Disponibilité
tabOhms = [None] * nbProdAffiche #ESR
tabOhmsUnite = [None] * nbProdAffiche #ESR
tabVolt = [None] * nbProdAffiche #
tabVoltUnite = [None] * nbProdAffiche #
tabFrequence = [None] * nbProdAffiche #
tabFreqUnite = [None] * nbProdAffiche #
tabVoltAC = [None] * nbProdAffiche #
tabUniteAC = [None] * nbProdAffiche #
tabVoltDC = [None] * nbProdAffiche #
tabUniteDC = [None] * nbProdAffiche #
tabCapacitance = [None] * nbProdAffiche #
tabCapacitanceUnite = [None] * nbProdAffiche #
tabDureeVie = [None] * nbProdAffiche #Durée de vie
tabHoursCycles = [None] * nbProdAffiche #
tabTole = [None] * nbProdAffiche #Tolerance
tabLeakage = [None] * nbProdAffiche #
tabDissipationFactor = [None] * nbProdAffiche #
tabSeries = [None] * nbProdAffiche #Series
tabPackage = [None] * nbProdAffiche #Packaging
tabRating = [None] * nbProdAffiche #Ratings
tabFeature = [None] * nbProdAffiche #Feature
tabTempsUtiDeb = [None] * nbProdAffiche #Température de fonctionnement min.
tabTempsUtiFin = [None] * nbProdAffiche #Température de fonctionnement max.
tabLowAmpere = [None] * nbProdAffiche #
tabLowAmpereUnite = [None] * nbProdAffiche #
tabLowHZ = [None] * nbProdAffiche #
tabHighAmpere = [None] * nbProdAffiche #
tabHighAmpereUnite = [None] * nbProdAffiche #
tabHighGHZ = [None] * nbProdAffiche #
tabLength = [None] * nbProdAffiche #Longueur
tabWidth = [None] * nbProdAffiche #Largeur
tabDiametre = [None] * nbProdAffiche #Diamètre
tabHeight = [None] * nbProdAffiche #Hauteur
tabThickness = [None] * nbProdAffiche #
tabMountingType = [None] * nbProdAffiche #Mounting Type
tabApplication = [None] * nbProdAffiche #Applications
tabCircuit = [None] * nbProdAffiche #Circuit Type
tabNbCap = [None] * nbProdAffiche #Number of Capacitors
tabTempCoef = [None] * nbProdAffiche #Temperature Coefficient
tabType = [None] * nbProdAffiche #Type
tabLead = [None] * nbProdAffiche #Lead
tabPolari = [None] * nbProdAffiche #
tabQ = [None] * nbProdAffiche #
tabQfreq = [None] * nbProdAffiche #
tabDielectric = [None] * nbProdAffiche #
tabLeadStyle = [None] * nbProdAffiche #
tabTermination = [None] * nbProdAffiche #Termination STRING
tabESL = [None] * nbProdAffiche #
tabManufacturerCode = [None] * nbProdAffiche #Code caisse du fabricant
tabAdjustment = [None] * nbProdAffiche #
tabCodeCaisse = [None] * nbProdAffiche #Package/Boîte   Code de caisse - po

#Nom de la base
dbname = 'PCBComposantScrapDB'

#Variable lié a la navigation a travers les différentes pages, currentpage etant la page actuelle, numpage etant les pages de types de resistances
currentpage, numpage = 1, 2

#Variable de vérificarion d'arriver jusqu'au bout, et empeche de continuer si il manque des informations
arriver, dataEnt, arret = False, False, 0

                                    #Tableau pour ajout grouper dans des tableaux
#Valeur sans réel modification
ListID = ["tr-manufacturer", "CLS 16", "tr-series", "CLS 707", "CLS 69", "CLS 405", "CLS 183", "CLS 52", "CLS 589", "CLS 909", "CLS 5", "CLS 987", "CLS 989", "CLS 26", "CLS 9", "CLS 17", "CLS 2315", "CLS 4", "CLS 24"]
listeTab = [tabFab, tabCodeCaisse, tabSeries, tabRating, tabMountingType, tabApplication, tabType, tabPolari, tabTermination, tabDielectric, tabFeature, tabManufacturerCode, tabDissipationFactor, tabCapacitance, tabCircuit, tabTempCoef, tabNbCap, tabLeadStyle, tabAdjustment]

#Valeur avec leurs unités (ayant un espace entre leurs nombres et unités)
nomValUnit = ["CLS 2049", "CLS 2079", "CLS 2080", "CLS 2082", "CLS 2131", "CLS 1292", "CLS 1293"]
tabVal = [tabCapacitance, tabVolt, tabOhms, tabOhms, tabVolt, tabVoltAC, tabVoltDC]
tabUnit = [tabCapacitanceUnite, tabVoltUnite, tabOhmsUnite, tabOhmsUnite, tabVoltUnite, tabUniteAC, tabUniteDC]

#Valeur en mm
nomValmm = ["CLS 1501", "CLS 1500", "CLS 508", "CLS 329"]
tabValmm = [tabThickness, tabHeight, tabLead, tabHeight]

#Les mesures (Longueur Largeur et Diametre) ont différents CLS selon les types de Capacitors
tabMesureBoucle = ["CLS 46", "CLS 884", "CLS 2097"]

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
        writer.writerow(['Reference', 'Site', 'Fabricant', 'Description', 'Categorie de Resistance', 'Quantites', 'Ohms','Unite des Ohms', 'Voltage', 'Unite des Volt', 'Frequence', 'Unite de Frequence', 'Voltage AC', 'Unite de volt AC', 'Frequence de voltage AC','Voltage DC', 'Unite de volt DC', 'Frequence de voltage DC', 'Capacitance', 'Unite de capacitance', 'Duree de Vie', 'Heure/Cycle de Vie', 'Tolerance', 'Leakage', 'Facteur de dissipation', 'Series', 'Package', 'Type de Package', 'Rating', 'Feature', 'Temperature Minimum', 'Temperature Maximum', 'Courant de rejection', 'Unite du courant de rejection', 'Courant nominal', 'Unite du courant nominal', 'Courant de fuite', 'Unite du courant de fuite','Courant d ondulation faible', 'Unite du courant faible', 'Frequence du courant faible','Courant d ondulation haute', 'Unite du courant haute', 'Frequence du courant haute','Longueur', 'Largeur',  'Diametre', 'Hauteur', 'Thickness', 'Mounting Type', 'Application','Circuit', 'Nombre de condensateurs', 'Coefficient de Temperature', 'Type','Lead', 'Style de boitier', 'Polarisation', 'Q', 'Q @ Freq', 'Dielectric','Lead Style', 'Raccordement', 'Terminaison', 'ESL', 'Code de fabricant', 'Ajustement','Nombre de broches', 'Nombre d element', 'Produit', 'Espacement des fils','Unite espacement des fils', 'Fil de sortie', 'Borne de terre', 'Profondeur / Epaisseur', 'Orientation', 'Code de Caisse / Package / Case'])


    #Creation et connexion de la base de données
con = sqlite3.connect(dbname + '.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Condensateur(
    Reference text NOT NULL,
    SiteWeb text NOT NULL,
    Fabricant text,
    Description text,
    Categorie text,
    Quantites int,
    Ohms real,
    UniteOhms text,
    Volt real,
    UniteVolt text,
    Frequence real,
    UniteFrequence text,
    VoltageAC real,
    UniteAC text,
    VoltageDC real,
    UniteDC text,
    Capacitance real,
    UniteCapacitance text,
    DureeDeVie real,
    HeureOuCycle text,
    Tolerance real,
    Leakage real,
    DissipationFactor real,
    Series text,
    Package text,
    TypePackage text,
    Rating text,
    Feature text,
    TemperatureMin int,
    TemperatureMax int,
    CourantDeRejection real,
    UniteCourantRejection text,
    CourantNominal real,
    UniteCourantNominal text,
    CourantFuite real,
    UniteCourantFuite text,
    AmpereLowHZ real,
    AmpereLowUnite text,
    LowFrequence real,
    AmpereHighKHZ real,
    AmpereHighUnite text,
    HighFrequence real,
    Longueur real,
    Largeur real,
    Diametre real,
    Hauteur real,
    Thickness real,
    MountingType text,
    Application text,
    Circuit text,
    NombreCapacitors real,
    TemperatureCoef text,
    Type text,
    Lead text,
    StyleBoitier text,
    Polarization text,
    Q real,
    QFrequence real,
    Dielectric text,
    LeadStyle text,
    Raccordement text,
    Terminaison text,
    ESLph real,
    ManufacturerCode text,
    Ajustement text,
    NombreBroche real,
    NombreElement real,
    Produit text,
    EspacementFil real,
    UniteEspacementFil text,
    FilSortie text,
    BorneDeTerre real,
    ProfondeurEpaisseur real,
    Orientation text,
    CodeCaisse text,
    PRIMARY KEY (Reference, SiteWeb))
''');

nomUpdate = ['Fabricant','Description','Quantites','Ohms','UniteOhms','Volt','UniteVolt','Frequence','UniteFrequence','VoltageAC','UniteAC','VoltageDC','UniteDC','Capacitance','UniteCapacitance','DureeDeVie','HeureOuCycle', 'Tolerance', 'Leakage', 'DissipationFactor', 'Series', 'Package','Rating', 'Feature', 'TemperatureMin', 'TemperatureMax', 'AmpereLowHZ','AmpereLowUnite','LowFrequence','AmpereHighKHZ','AmpereHighUnite','HighFrequence','Longueur', 'Largeur', 'Diametre','Hauteur', 'Thickness', 'MountingType','Application','Circuit','NombreCapacitors','TemperatureCoef','Type','Lead','Polarization','Q','QFrequence','Dielectric','LeadStyle','Terminaison','ESLph','ManufacturerCode','Ajustement', 'CodeCaisse']
tabUpdate = [tabFab, tabDesc, tabQtte,tabOhms, tabOhmsUnite,tabVolt, tabVoltUnite, tabFrequence,tabFreqUnite, tabVoltAC, tabUniteAC,tabVoltDC, tabUniteDC,tabCapacitance, tabCapacitanceUnite, tabDureeVie, tabHoursCycles, tabTole,tabLeakage,tabDissipationFactor,tabSeries,tabPackage, tabRating, tabFeature,tabTempsUtiDeb,tabTempsUtiFin, tabLowAmpere, tabLowAmpereUnite, tabLowHZ, tabHighAmpere, tabHighAmpereUnite, tabHighGHZ, tabLength, tabWidth, tabDiametre,tabHeight,tabThickness, tabMountingType, tabApplication, tabCircuit, tabNbCap, tabTempCoef, tabType, tabLead, tabPolari, tabQ, tabQfreq,tabDielectric,tabLeadStyle, tabTermination, tabESL, tabManufacturerCode, tabAdjustment,tabCodeCaisse]
# # #//////////////////////////////////////////////////////////////////////////////////////////////////////////

#Connection au différentes pages de Ress

def status(undriver): #Permet de cliquer et appliquer le status "active", ainsi qu'afficher 100 résultats
    #cliquer et appliquer le status "active"
    sleep(5)
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
    driver.find_element_by_xpath("//div[@id='leftColumn']/div/ul[2]/li[1]/h3/a").click()
    sleep(2)
    catRes = driver.find_element_by_xpath('//div[@data-testid="parent-category-container-3"]/ul[@data-testid="subcategories-container"]/li[2]/a/span')
    categorieResistance = catRes.text
    driver.find_element_by_xpath('//div[@data-testid="parent-category-container-3"]/ul[@data-testid="subcategories-container"]/li[2]/a').click()
    status(driver)
else:
    pass

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////

    #Recherche des différentes valeurs voulues
while(1): #Boucle toujours vrai, pour faire toutes les pages
        # try:

        #Refresh toutes les 15 pages, car perd de la vitesse au fur et a mesure du traversement des pages
        if currentpage%15 == 0:
            curl = driver.current_url
            driver.quit()
            sleep(3)
            driver = webdriver.Chrome(options=chrome_options, executable_path=Chromepath)
            driver.get(curl)
        else:
            pass


        sleep(5)


        if arriver == False:

                #Recherche a faire sur site
                ref1 = driver.find_elements_by_xpath("//a[@data-testid='data-table-0-product-number']")
                ref2 = driver.find_elements_by_xpath("//div[@data-testid='data-table-0-product-description']")
                ref3 = driver.find_elements_by_xpath("//td[@data-atag='tr-qtyAvailable']")
                ref4 = driver.find_elements_by_xpath("//td[@data-atag='CLS 2085']")
                ref5 = driver.find_elements_by_xpath("//td[@data-atag='CLS 3']")
                ref6 = driver.find_elements_by_xpath("//td[@data-atag='CLS 2']")
                ref7 = driver.find_elements_by_xpath("//td[@data-atag='CLS 252']")
                ref8 = driver.find_elements_by_xpath("//td[@data-atag='CLS 17']")

                begin_time = datetime.datetime.now()

                #Permet de récuperer le nombre d'article afficher dans la page actuel (seulement utile pour la dernière page)
                nbArticle = len(driver.find_elements_by_xpath("//a[@data-testid='data-table-0-product-number']"))

                arriver = False

                #Reference
                i=0
                for element in ref1:    
                    tabRef[i] = "".join(element.text)
                    i = i+1

                # Description
                i=0
                for element in ref2:    
                    tabDesc[i] = "".join(element.text)
                    i = i+1

                # Quantite
                i=0
                for element in ref3:    
                    #Permet de ne récupérer que la quantité
                    s = element.text.split()
                    if "," in s[0]:
                        value = s[0].replace(",", "")
                        tabQtte[i] = "".join(value)
                        i = i+1
                    elif s[0] != "-":
                        tabQtte[i] = "".join(s[0])
                        i = i+1
                    else:
                        tabQtte[i] = None
                        i = i+1

                #Tolerance
                i=0
                for element in ref5:
                    r = element.text.split()
                    if r[0] != "-" and len(r)> 0:   
                        if r[0] == "Jumper":
                            tabTole[i] = 0
                            i = i+1
                        elif len(r) == 1:
                            val = r[0].replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('pF', "")
                            val = val.replace('%', "")
                            tabTole[i] = val
                            i = i+1
                        elif len(r) > 1 and r[0] == "0%," or r[0] == "-0%,":
                            val = r[1].replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('%', "")
                            tabTole[i] = val
                            i = i+1
                        else:
                            val = r[0].replace('±', "")
                            val = val.replace('+', "")
                            val = val.replace(',', "")
                            val = val.replace('%', "")
                            tabTole[i] = val
                            i = i+1
                    else:
                        tabTole[i] = None
                        i = i+1

                # Operating Temperature, Minimum et Maximum
                i=0
                for element in ref7:    
                    r = element.text.split()
                    if r[0] == "-": #Si il n'y a rien de renseigné
                        tabTempsUtiDeb[i] = None
                        tabTempsUtiFin[i] = None
                        i = i+1
                    else:
                        #Valeur froid (negative)
                        value = r[0]
                        rep = re.findall('\d+', value)
                        rep[0] = "-" + rep[0]
                        tabTempsUtiDeb[i] = rep[0]
                        #Valeur chaud (positive)
                        value = r[-1]
                        rep = re.findall('\d+', value)
                        tabTempsUtiFin[i] = rep[0]
                        i = i+1

                # Coefficient de temperature
                i=0
                for element in ref8:

                    #Permet de recupérer que le nombre utile
                    if element.text != "-":
                        res = element.text.strip('±')
                        res = res.strip('ppm/°C')
                        if str(res).isdigit():
                            tabTempCoef[i] = "".join(res)
                            tabDegres[i] = "Celsius"
                            i = i+1
                        elif "0/" in res:
                            res = re.findall('\-{0,1}\d+', res)
                            if res[0] != '0':
                                tabTempCoef[i] = "".join(res[0])
                                tabDegres[i] = "Celsius"
                                i = i+1
                            else:
                                tabTempCoef[i] = "".join(res[1])
                                tabDegres[i] = "Celsius"
                                i = i+1
                        else:
                            tabTempCoef[i] = "".join(res)
                            tabDegres[i] = "Celsius"
                            i = i+1
                    else:
                        tabTempCoef[i] = None
                        tabDegres[i] = None
                        i = i+1

                #Le fabriquant, le code caisse, les series, la compositionn les feature, le rating
                for a in range(len(ListID)):
                    # print(a)
                    i=0
                    ref = driver.find_elements_by_xpath("//td[@data-atag='"+ListID[a]+"']")
                    for element in ref: 
                        if element.text != "-":
                            # print(element.text)
                            val = element.text.replace(",", "")
                            val = val.replace('"', "")
                            listeTab[a][i] = "".join(val)
                            # print(str(ListID[a]) + " pour " + str(i) + " " + str(listeTab[a][i]))
                            i = i+1
                        else:
                            listeTab[a][i] = None
                            i = i+1


                # Package
                ref = driver.find_elements_by_xpath("//td[@data-atag='tr-packaging']")
                i=0
                for element in ref: 
                    if element.text != "-":
                        tabPackage[i] = "".join(element.text.splitlines())
                        tabPackage[i] = tabPackage[i].strip("®")
                        i = i+1
                    else:
                        tabPackage[i] = None
                        i = i+1


                for a in range(len(tabMesureBoucle)):
                    i=0
                    ref = driver.find_elements_by_xpath("//td[@data-atag='"+tabMesureBoucle[a]+"']")
                    for element in ref:
                        if element.text != "-":
                            # try:
                            value = element.text.split()
                            if value[1] == "Dia":
                                if len(value) < 5:
                                    val = value[2].replace("(", "")
                                    val = val.replace(")", "")
                                    val = val.replace("mm", "")
                                    tabDiametre[i] = val
                                    # print(tabDiametre[i])
                                    i=i+1
                                else:
                                    if value[4] == "W":
                                        val = value[5].replace("(", "")
                                        val = val.replace("mm", "")
                                        tabDiametre[i] = val
                                        val = value[7].replace(")", "")
                                        val = val.replace("mm", "")
                                        tabWidth[i] = val
                                        # print(tabDiametre[i])
                                        # print(tabWidth[i])
                                        i=i+1
                                    elif value[4] == "L":
                                        val = value[5].replace("(", "")
                                        val = val.replace("mm", "")
                                        tabDiametre[i] = val
                                        val = value[7].replace(")", "")
                                        val = val.replace("mm", "")
                                        tabLength[i] = val
                                        # print(tabDiametre[i])
                                        # print(tabLength[i])
                                        i=i+1
                                    else:
                                        pass

                            elif value[1] == "W":
                                if value[4] == "Dia":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabWidth[i] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabDiametre[i] = val
                                    # print(tabWidth[i])
                                    # print(tabDiametre[i])
                                    i=i+1
                                elif value[4] == "L":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabWidth[i] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabLength[i] = val
                                    # print(tabWidth[i])
                                    # print(tabLength[i])
                                    i=i+1

                            elif value[1] == "L":
                                if value[4] == "Dia":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabLength[i] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabDiametre[i] = val
                                    # print(tabLength[i])
                                    # print(tabDiametre[i])
                                    i=i+1
                                elif value[4] == "W":
                                    val = value[5].replace("(", "")
                                    val = val.replace("mm", "")
                                    tabLength[i] = val
                                    val = value[7].replace(")", "")
                                    val = val.replace("mm", "")
                                    tabWidth[i] = val
                                    # print(tabLength[i])
                                    # print(tabWidth[i])
                                    i=i+1

                for a in range(len(tabValmm)):
                    i=0
                    ref = driver.find_elements_by_xpath("//td[@data-atag='"+nomValmm[a]+"']")
                    for element in ref:
                        if element.text != "-":
                            value = element.text.split("(")
                            val = value[1].replace("mm", "")
                            val = val.replace(")", "")
                            tabValmm[a][i] = "".join(val)
                            i = i+1
                        else:
                            tabValmm[a][i] = None
                            i = i+1

                #Ripple Current @ Low Frequency
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 2253']")
                for element in ref:
                    if element.text != "-":
                        value = element.text.split()
                        tabLowAmpere[i] = value[0]
                        tabLowAmpereUnite[i] = value[1]
                        tabLowHZ[i] = value[3]
                        i = i+1
                    else:
                        tabLowAmpere[i] = None
                        tabLowAmpereUnite[i] = None
                        tabLowHZ[i] = None
                        i = i+1

                #Ripple Current @ High Frequency
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 2260']")
                for element in ref:
                    if element.text != "-":
                        value = element.text.split()
                        tabHighAmpere[i] = value[0]
                        tabHighAmpereUnite[i] = value[1]
                        tabHighGHZ[i] = value[3]
                        i = i+1
                    else:
                        tabHighAmpere[i] = None
                        tabHighAmpereUnite[i] = None
                        tabHighGHZ[i] = None
                        i = i+1

                #Valeur avec Unite simple
                for a in range(len(tabVal)):
                    i=0
                    ref = driver.find_elements_by_xpath("//td[@data-atag='"+nomValUnit[a]+"']")
                    for element in ref: 
                        if element.text != "-":
                            val = element.text.split()
                            tabVal[a][i] = "".join(val[0])
                            tabUnit[a][i] = "".join(val[1])
                            i = i+1
                        else:
                            tabVal[a][i] = None
                            tabUnit[a][i] = None
                            i = i+1

                #ESR (Equivalent Series Resistance)
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 724']")
                for element in ref:
                    if element.text != "-":
                        val = re.findall('(\d{0,9}.{0,1}\d+|[A-Za-z]+)', element.text)
                        tabOhms[i] = val[0]
                        tabOhmsUnite[i] = val[1]
                        if "@" in element.text:
                            val2 = element.text.split()
                            valtemp1 = re.findall('(\d{0,9}.{0,1}\d+)', val2[2])
                            valtemp2 = re.findall('([a-zA-Z]+)', val2[2])
                            tabFrequence[i] = "".join(valtemp1)
                            tabFreqUnite[i] = "".join(valtemp2)
                        else:
                            tabFrequence[i] = None
                            tabFreqUnite[i] = None
                        i = i+1
                    else:
                        tabOhms[i] = None
                        tabOhmsUnite[i] = None
                        tabFrequence[i] = None
                        tabFreqUnite[i] = None
                        i = i+1

                #Lifetime
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 725']")
                for element in ref:
                    if element.text != "-":
                        val = element.text.split()
                        tabDureeVie[i] = val[0]
                        if 'Hrs' in val[1]:
                            tabHoursCycles[i] = "Hours"
                        elif 'Cycl' in val[1]:
                            tabHoursCycles[i] = "Cycles"
                        else:
                            tabHoursCycles[i] = val[1]
                        i = i+1
                    else:
                        tabDureeVie[i] = None
                        i = i+1

                #Capacitance NETWORK ARRAY
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 13']")
                for element in ref:
                    if element.text != "-":
                        val = re.findall('(\d{0,9}.{0,1}\d+|[A-Za-z]+)', element.text)
                        tabCapacitance[i] = val[0]
                        tabCapacitanceUnite[i] = val[1]
                        i = i+1
                    else:
                        tabCapacitance[i] = None
                        tabCapacitanceUnite[i] = None
                        i = i+1

                #ESL (Equivalent Series Inductance)
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 1564']")
                for element in ref:
                    if element.text != "-":
                        val = re.findall("\d{0,9}.{0,1}\d+|[A-Za-z]+", element.text)
                        # '([0-9]{0,9}.{0,9}[0-9]+)'
                        tabESL[i] = val[0]
                        i = i+1
                    else:
                        tabESL[i] = None
                        i = i+1

                #Q @ Freq
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 705']")
                for element in ref:
                    if element.text != "-":
                        val = element.text.split()
                        tabQ[i] = val[0]
                        valFreq = re.findall("\d{0,9}.{0,1}\d+", val[2])
                        tabQfreq[i] = valFreq[0]
                        i = i+1
                    else:
                        tabQ[i] = None
                        tabQfreq[i] = None
                        i = i+1


                #Voltage (Ceramic)
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 14']")
                for element in ref:
                    if element.text != "-":
                        val = re.findall("\d{0,9}.{0,1}\d+|[A-Za-z]+", element.text)
                        tabVolt[i] = val[0]
                        tabVoltUnite[i] = val[1]
                        i = i+1
                    else:
                        tabVolt[i] = None
                        tabVoltUnite[i] = None
                        i = i+1

                #Leakage
                i=0
                ref = driver.find_elements_by_xpath("//td[@data-atag='CLS 2083']")
                for element in ref:
                    if element.text != "-":
                        val = element.text.split()
                        tabLeakage[i] = val[0]
                        i = i+1
                    else:
                        tabLeakage[i] = None
                        i = i+1




                # # Variable pour valider l'arriver jusqu'a la fin
                arriver = True

        else: #dataEnt veut dire l'on n'arrive pas inscrire les données, mais elle sont déja dans les tableaux.
            pass

        # except: #Probleme avec la récupération des données
        #   print("Erreur lors de la collecte des données, veuillez patientez")

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Ouverture et écriture des données dans le fichier CSV et dans une bases SQLITE3
        if arriver == True:
            
            for i in range(int(nbArticle)):

                #Ouvre le fichier CSV est ecrit ses résultats
                with open(csvpath,'a',newline='') as unFichierCSV:
                    writer=csv.writer(unFichierCSV)
                    writer.writerow([tabRef[i], "Digikey",tabFab[i], tabDesc[i],categorieResistance, tabQtte[i],tabOhms[i], tabOhmsUnite[i],tabVolt[i], tabVoltUnite[i], tabFrequence[i],tabFreqUnite[i], tabVoltAC[i], tabUniteAC[i],tabVoltDC[i], tabUniteDC[i],tabCapacitance[i], tabCapacitanceUnite[i], tabDureeVie[i], tabHoursCycles[i], tabTole[i],tabLeakage[i],tabDissipationFactor[i],tabSeries[i],tabPackage[i],None, tabRating[i], tabFeature[i],tabTempsUtiDeb[i],tabTempsUtiFin[i],None,None,None,None,None,None, tabLowAmpere[i], tabLowAmpereUnite[i], tabLowHZ[i], tabHighAmpere[i], tabHighAmpereUnite[i], tabHighGHZ[i], tabLength[i], tabWidth[i], tabDiametre[i],tabHeight[i],tabThickness[i], tabMountingType[i], tabApplication[i], tabCircuit[i], tabNbCap[i], tabTempCoef[i], tabType[i], tabLead[i],None, tabPolari[i], tabQ[i], tabQfreq[i],tabDielectric[i],tabLeadStyle[i], None,tabTermination[i], tabESL[i], tabManufacturerCode[i], tabAdjustment[i],None,None,None,None,None,None,None,None,None,tabCodeCaisse[i]])

                    try:
                        #Entre les resultats dans une base, si Ref non existante, l'écrit, sinon, l'update
                        insertdata = '''INSERT INTO Condensateur VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
                        data = (tabRef[i], "Digikey",tabFab[i], tabDesc[i],categorieResistance, tabQtte[i],tabOhms[i], tabOhmsUnite[i],tabVolt[i], tabVoltUnite[i], tabFrequence[i],tabFreqUnite[i], tabVoltAC[i], tabUniteAC[i],tabVoltDC[i], tabUniteDC[i],tabCapacitance[i], tabCapacitanceUnite[i], tabDureeVie[i], tabHoursCycles[i], tabTole[i],tabLeakage[i],tabDissipationFactor[i],tabSeries[i],tabPackage[i],None, tabRating[i], tabFeature[i],tabTempsUtiDeb[i],tabTempsUtiFin[i],None,None,None,None,None,None, tabLowAmpere[i], tabLowAmpereUnite[i], tabLowHZ[i], tabHighAmpere[i], tabHighAmpereUnite[i], tabHighGHZ[i], tabLength[i], tabWidth[i], tabDiametre[i],tabHeight[i],tabThickness[i], tabMountingType[i], tabApplication[i], tabCircuit[i], tabNbCap[i], tabTempCoef[i], tabType[i], tabLead[i],None, tabPolari[i], tabQ[i], tabQfreq[i],tabDielectric[i],tabLeadStyle[i], None,tabTermination[i], tabESL[i], tabManufacturerCode[i], tabAdjustment[i],None,None,None,None,None,None,None,None,None,tabCodeCaisse[i])
                    except sqlite3.IntegrityError: #Permet de pouvoir entrer les valeurs actuels pour une reference déja entrer
                        #Update seulement si les valeurs sont non vides, permet de ne pas update a des valeurs existante avec des null
                        for nom in nomUpdate: #Fabriquant descri
                            # numerotableau = categorie.index(nom) #index de categorie correspondant a nom
                            nbcat = nomUpdate.index(nom)
                            try:
                                if tabUpdate[nbcat][i] != None:
                                    insertdata = '''UPDATE Resistance SET '''+nom+''' = ? WHERE Reference = ? AND SiteWeb = ?;'''
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
                    sleep(5)
                except:
                    driver.find_element_by_xpath("//div[@class='MuiGrid-root MuiGrid-container MuiGrid-align-items-xs-center MuiGrid-justify-xs-space-between']/div/div/nav/ol/li[3]/a").click()
                    sleep(5)
                    numpage += 1
                    currentpage = 1
                    categorieResistance = driver.find_element_by_xpath('//div[@data-testid="parent-category-container-3"]/ul[@data-testid="subcategories-container"]/li['+str(numpage)+']/a/span')
                    driver.find_element_by_xpath('//div[@data-testid="parent-category-container-3"]/ul[@data-testid="subcategories-container"]/li['+str(numpage)+']/a').click()
                    status(driver)
            else:
                pass

# # //////////////////////////////////////////////////////////////////////////////////////////////////////////

        #Permet de refresh si il y a eu des probleme, voir d'arreter le programme, en evitant que currentpage s'incrémente.
        else:
            print("Probleme lors de la récupération des données, refresh de la page a venir.")
            arret = arret+1
            if arret == 5:
                print("Probleme persistant, arret du script a la page ." + str(currentpage))
                print(driver.current_url)
                driver.quit()
            elif arret>2:
                driver.refresh()
                sleep(15)
            else:
                driver.refresh()
                sleep(5)