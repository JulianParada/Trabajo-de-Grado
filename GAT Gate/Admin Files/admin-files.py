from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import sched, time, requests, shutil
from datetime import datetime
import json
from datetime import date
from datetime import datetime
from datetime import timedelta
import pyrebase
import os
import numpy as np
import pandas as pd
from collections import namedtuple

# Relative path files
path = '../OSFDocuments/informestecnicos'
path2 = '../OSFDocuments/pofi'

# Express server with connection to OSF Server
URLOC = "http://localhost:3000"

# Express server with connection to SQL Datbase in azure
URL = "http://localhost:8081"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Jg1kTOynmuFNuWRy0wFOqTUUXZOVxE4H5XICq-XvwDw'
SAMPLE_RANGE_NAME = 'Elements!A1:AD197'

def clean_directory(path):
    for elem in path:
        try:
            shutil.rmtree(elem)
            print("directory clean")
        except OSError as e:
            print(f"Error:{ e.strerror}")

def start_process(sc, index, fechita, esPrimera, index2): 
    dirPath = {'../OSFDocuments/informestecnicos', '../OSFDocuments/pofi'}
    clean_directory(dirPath)
    print("Doing download...")
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}
    # sending get request and saving the response as response object
    
    r = requests.get(url = URLOC, params = PARAMS)
    # extracting data in json format
    data = r.json()
    print(data[1:17], datetime.now())
    #print(data['results'][0])

    operacion = datetime.today()-fechita
    
    r = requests.get(url = URL+"/Begin_Connection", params = {})
    data = r.json()
    print(data[1:17])

    
    
    if operacion.days >= 95 or esPrimera:
        
        descargar_kumu()

        nuevoIndex = limpieza_informes(index,index2)
        
        df = pd.read_excel('../OSFDocuments/pofi/osfstorage/Resumen_Fortalecimiento.xlsx', sheet_name= ['POFI', 'Avances'])
        clean_persist_POFI(df)

        upload_files_storage()

        r = requests.get(url = URL+"/End_Connection", params = {})
        data = r.json()
        print(data[1:16])

        s.enter(604800, 1, start_process, (sc, nuevoIndex[0], datetime.today(), False, nuevoIndex[1],))
    else:
        r = requests.get(url = URL+"/End_Connection", params = {})
        data = r.json()
        print(data[1:16])

        s.enter(604800, 1, start_process, (sc, index, datetime.today(), False, index2,))

def descargar_kumu():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        DATA = values.copy()
        print('Data Ready')
        insertar_info_kumu(DATA)
        #print(len(DATA[176]))
        #s.enter(60, 1, main, (sc,))
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s, %s' % (row[0], row[4]))

def insertar_info_kumu(DATA):
    personArr = []
    grupoArr = []
    organizationArr = []
    plantaArr = []
    proyectoArr = []
    proyectoMacroArr = []

    acronimos = [['PUJ Bogotá', 'PUJ'], ['Fundación Univesitaria Juan N Corpas', 'JUAN N CORPAS'],
                ['PROCAPS', 'PROCAPS'], ['Universidad Federal de Rio de Janeiro', 'UFRJ'],
                ['PUJ- Cali', 'PUJC'], ['USCO', 'USCO'],
                ['HUSI', 'HUSI'], ['Universidad de Antioquia', 'UdeA'],
                ['Universidad de Sao Paulo', 'USP'], ['Universidad de Nantes Francia', 'UNF'],
                ['Instituto Ludwig', 'ILUD'], ['Instituto Motffit', 'IMOT'],
                ['Universidad La Sorbona', 'PSU'], ['Imperial College London', 'ICL'],
                ['Universidad College of London', 'UCL'], ['ITP' , 'ITP'],
                ['UNIVALLE', 'VALLE'], ['CULS', 'CULS'],
                ['Universidad Nacional de Colombia', 'UNAL']]
                
    for row in DATA:
        if row[1] == 'Person':
            personArr.append(row)
        if row[1] == 'Grupo':
            grupoArr.append(row)
        if row[1] == 'Organization':
            organizationArr.append(row)
        if row[1] == 'Planta':
            plantaArr.append(row)
        if row[1] == 'Proyecto':
            proyectoArr.append(row)
        if row[1] == 'Proyecto Macro':
            proyectoMacroArr.append(row)

    proyecto(proyectoArr)
    organization(organizationArr, acronimos) #Institucion
    person(personArr)
    grupo(grupoArr, personArr)
    planta(plantaArr)
    #proyectoMacro(proyectoMacroArr)
    print('Data actualizada')

def person(personArr):
    # Get all personas
    # Recorro personArr contra Gerall y si exite lo edito con el id y no existe busco su orga/institucion por nombre y lo ingreso
    # saco el id de la persona que ingrese y busco el proyecto por por el numero, si es vacio no lo meto, y si tiene algo lo busco saco el id y meto en PROYECTO_PERSONA
    
    desactivar = []
    
    table = "PERSONA|ID|NOMBRE"
    PARAMS = {'data':table}
    urlF = URL + "/getAll_Specs"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())

    for otrico in personArr:
        flag = False
        estoy = -1
        for otro in respuesta:
            estoy = otro['ID']
            if otrico[0] == otro['NOMBRE']:
                flag = True
                break
        if flag == False and estoy != -1:
            desactivar.append(estoy['ID'])
    
    if len(desactivar) != 0:
        for opt in desactivar:
            query = "PERSONA|"+opt+ "|INTIS_ACTIVE=0"
            PARAMS2 = {'data':query}
            urlF2 = URL + "/update_One"
            requests.get(url = urlF2, params = PARAMS2)
       
    table2 = "INSTITUCION"
    PARAMS2 = {'data':table2}
    urlF2 = URL + "/getAll"
    r2 = requests.get(url = urlF2, params = PARAMS2)
    respuesta2 = json.loads(r2.json())

    table3 = "PROYECTO"
    PARAMS3 = {'data':table3}
    urlF3 = URL + "/getAll"
    r3 = requests.get(url = urlF3, params = PARAMS3)
    respuesta3 = json.loads(r3.json())

    auxiliar = []
    for elem in personArr:
        aux = elem[19].split(" | ")
        auxiliar.append(aux)
        if elem[3] == '':
            elem[3]='NULL'
        for elemento in respuesta2:
            if elem[3] == elemento['NOMBRE']:
                elem[3] = elemento['ID']
                break
    
    for elem in personArr:
        for i in range(len(elem)):
            if elem[i]=='':
                elem[i] = 'NULL'
    
    for i in range(len(auxiliar)):
        for j in range(len(auxiliar[i])):
            for e in respuesta3:
                if auxiliar[i][j] == e['NOMBRE']:
                    auxiliar[i][j] = e['ID']
                    break

    if len(respuesta)==0:
        cont = 0
        for element in personArr:
            query = "PERSONA|STR" + element[0] + "|STR" + element[10] + "|STR" + element[7]+ "|STR" + element[17] + "|STR" + element[11] + "|STR" + element[8] + "|STR" + element[1] + "|STR" + element[18] + "|STR" + element[9] + "|STR" + element[12] + "|STR" + element[15] + "|INT1" + "|INT" + element[3] + "|STR" + element[6] + "|STR" + element[29]
            #print(query)
            PARAMS2 = {'data':query}
            urlF2 = URL + "/add_One"
            requests.get(url = urlF2, params = PARAMS2)

            query = "PERSONA|NOMBRE|STR" + element[0]
            PARAMS2 = {'data':query}
            urlF2 = URL + "/getOne"
            r4 = requests.get(url = urlF2, params = PARAMS2)
            respuesta4 = json.loads(json.loads(json.dumps(r4.json()).replace('\\n',' ')))
            
            idpersona = None
            for elemento in respuesta4:
                idpersona = elemento['ID']
        
            for pos in auxiliar[cont]:
                today = date.today()
                #print(today.strftime("%Y-%m-%d"))
                query = "PROYECTO_PERSONA|INT" + idpersona + "|INT" + pos + "|DAT" + today.strftime("%Y-%m-%d")
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)
            
            cont = cont + 1
    else:
        cont2 = 0
        for element in personArr:
            bandera = False
            idcp = None
            for elem in respuesta:
                if element[0] == elem['NOMBRE']:
                    # EXITE -> EDITO
                    bandera = True
                    idcp = elem['ID']
                    break
            if bandera == True:
                query = "PERSONA|"+idcp+"|STRNOMBRE=" + element[0] + "|STREMAIL=" + element[10] + "|STRROL=" + element[7]+ "|STRROL_PROGRAMA=" + element[17] + "|STRNIVEL_ACADEMICO=" + element[11] + "|STRCATEGORIA_INV=" + element[8] + "|STRTIPO=" + element[1] + "|STRFUNCIONES=" + element[18] + "|STRFORMACION=" + element[9] + "|STRCVLAC=" + element[12] + "|STRGRUPO_LAC=" + element[15] + "|INTINSTITUCION_ID=" + element[3] + "|STRURL_IMAGEN=" + element[6] + "|STRGENERO=" + element[29]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/update_One"
                requests.get(url = urlF2, params = PARAMS2)

                for pos in auxiliar[cont2]:
                    today = date.today()
                    #print(idcp)
                    #print(today.strftime("%Y-%m-%d"))
                    query = "PROYECTO_PERSONA|INT" + idcp + "|INT" + pos + "|DAT" + today.strftime("%Y-%m-%d")
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)
            else:
                query = "PERSONA|STR" + element[0] + "|STR" + element[10] + "|STR" + element[7]+ "|STR" + element[17] + "|STR" + element[11] + "|STR" + element[8] + "|STR" + element[1] + "|STR" + element[18] + "|STR" + element[9] + "|STR" + element[12] + "|STR" + element[15] + "|INT1" + "|INT" + element[3] + "|STR" + element[6] + "|STR" + element[29]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)
                ''' '''
                query = "PERSONA|NOMBRE|STR" + element[0]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/getOne"
                r4 = requests.get(url = urlF2, params = PARAMS2)
                respuesta4 = json.loads(r4.json())

                idpersona = None
                for elemento in respuesta4:
                    idpersona = elemento['ID']

                for pos in auxiliar[cont2]:
                    today = date.today()
                    #print(idcp)
                    #print(today.strftime("%Y-%m-%d"))
                    query = "PROYECTO_PERSONA|INT" + idpersona + "|INT" + pos + "|DAT" + today.strftime("%Y-%m-%d")
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)
            cont2 = cont2 + 1

def grupo(grupoArr, personArr):
    # Get all grupos
    # Recorro grupoArr contra Gerall y si exite lo edito con el id y no existe busco su orga/institucion por nombre y lo ingreso
    
    table = "GRUPO_INV|ID|NOMBRE"
    PARAMS = {'data':table}
    urlF = URL + "/getAll_Specs"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json(), strict=False)

    table2 = "INSTITUCION"
    PARAMS2 = {'data':table2}
    urlF2 = URL + "/getAll"
    r2 = requests.get(url = urlF2, params = PARAMS2)
    respuesta2 = json.loads(r2.json())

    for elem in grupoArr:
        if elem[3] == '':
            elem[3]='NULL'
        for elemento in respuesta2:
            if elem[3] == elemento['NOMBRE']:
                elem[3] = elemento['ID']
                break
    
    for element in grupoArr:
        if len(element)<15:
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')
            element.append('NULL')

    for elem in grupoArr:
        for i in range(len(elem)):
            if elem[i]=='':
                elem[i] = 'NULL'
            elif "|" in elem[i]:
                elem[i] = elem[i].replace(' | ', ' & ')

    if len(respuesta)==0:

        for element in grupoArr:
            query = "GRUPO_INV|STR" + element[0] +  "|STR" + element[1]+ "|STR" + element[14] + "|INT" + element[3] + "|STR" + element[4]
            #print(query)
            PARAMS2 = {'data':query}
            urlF2 = URL + "/add_One"
            requests.get(url = urlF2, params = PARAMS2)

            query = "GRUPO_INV|NOMBRE|STR" + element[0]
            PARAMS2 = {'data':query}
            urlF2 = URL + "/getOne"
            r4 = requests.get(url = urlF2, params = PARAMS2)
            respuesta4 = json.loads(r4.json(), strict=False)
            
            idgrupoinv = None
            for elemento in respuesta4:
                idgrupoinv = elemento['ID']
        
            for ele in personArr:
                if ele[13] == element[0]:

                    query = "PERSONA|NOMBRE|STR" + ele[0]
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/getOne"
                    r4 = requests.get(url = urlF2, params = PARAMS2)
                    respuesta4 = json.loads(r4.json(), strict=False)
                    
                    idperson = None
                    for elemento in respuesta4:
                        idperson = elemento['ID']
                    
                    #print(idperson)
                    #print(idgrupoinv)

                    today = date.today()
                    query = "PERSONA_GRUPO_INV|INT" + idgrupoinv + "|INT" + idperson + "|DAT" + today.strftime("%Y-%m-%d")
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)
            
    else:

        for element in grupoArr:
            bandera = False
            idcp = None
            for elem in respuesta:
                if element[0] == elem['NOMBRE']:
                    # EXITE -> EDITO
                    bandera = True
                    idcp = elem['ID']
                    break
            if bandera == True:
                query = "GRUPO_INV|"+idcp+"|STRNOMBRE=" + element[0] +  "|STRTIPO=" + element[1]+ "|STRCLASIFICACION_COLCIENCIAS=" + element[14] + "|INTINSTITUCION_ID=" + element[3] + "|STRTAGS=" + element[4] 
                PARAMS2 = {'data':query}
                urlF2 = URL + "/update_One"
                requests.get(url = urlF2, params = PARAMS2)

                for ele in personArr:
                    if ele[13] == element[0]:

                        query = "PERSONA|NOMBRE|STR" + ele[0]
                        PARAMS2 = {'data':query}
                        urlF2 = URL + "/getOne"
                        r4 = requests.get(url = urlF2, params = PARAMS2)
                        respuesta4 = json.loads(r4.json(), strict=False)
                        
                        idperson = None
                        for elemento in respuesta4:
                            idperson = elemento['ID']

                        today = date.today()
                        query = "PERSONA_GRUPO_INV|INT" + idcp + "|INT" + idperson + "|DAT" + today.strftime("%Y-%m-%d")
                        PARAMS2 = {'data':query}
                        urlF2 = URL + "/add_One"
                        requests.get(url = urlF2, params = PARAMS2)
            else:
                query = "GRUPO_INV|STR" + element[0] + "|STR" + element[1]+ "|STR" + element[14] + "|INT" + element[3] + "|STR" + element[4]
                #print(query)
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)

                query = "GRUPO_INV|NOMBRE|STR" + element[0]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/getOne"
                r4 = requests.get(url = urlF2, params = PARAMS2)
                respuesta4 = json.loads(r4.json(), strict=False)
                
                idgrupoinv = None
                for elemento in respuesta4:
                    idgrupoinv = elemento['ID']
            
                for ele in personArr:
                    if ele[13] == element[0]:

                        query = "PERSONA|NOMBRE|STR" + ele[0]
                        PARAMS2 = {'data':query}
                        urlF2 = URL + "/getOne"
                        r4 = requests.get(url = urlF2, params = PARAMS2)
                        respuesta4 = json.loads(r4.json(), strict=False)
                        
                        idperson = None
                        for elemento in respuesta4:
                            idperson = elemento['ID']

                        today = date.today()
                        query = "PERSONA_GRUPO_INV|INT" + idgrupoinv + "|INT" + idperson + "|DAT" + today.strftime("%Y-%m-%d")
                        PARAMS2 = {'data':query}
                        urlF2 = URL + "/add_One"
                        requests.get(url = urlF2, params = PARAMS2)

def organization(organizationArr, acronimos):
    table = "INSTITUCION"
    PARAMS = {'data':table}
    urlF = URL + "/getAll"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())
    # print(len(respuesta))

    if len(respuesta)==0:
        for element in organizationArr:
            
            acro = None

            for aux in acronimos:
                if element[0] == aux[0]:
                    acro = aux[1]

            query = "INSTITUCION|STR" + element[0] + "|STR" + acro + "|STR" + element[1] + "|STR" + element[5]+ "|FLTNULL" + "|STR" + element[6]
            PARAMS2 = {'data':query}
            urlF2 = URL + "/add_One"
            requests.get(url = urlF2, params = PARAMS2)
    else:
        for element in organizationArr:
            bandera = False
            idcp = None

            acro = None

            for aux in acronimos:
                if element[0] == aux[0]:
                    acro = aux[1]

            for elem in respuesta:
                if element[0] == elem['NOMBRE']:
                    # EXITE -> EDITO
                    bandera = True
                    idcp = elem['ID']
                    break
            if bandera == True:
                query = "INSTITUCION|"+idcp+"|STRNOMBRE=" + element[0] + "|STRACRONIMO=" + acro +"|STRTIPO=" + element[1] + "|STRTIPO_ORG=" + element[5]+ "|STRURL_IMAGEN=" + element[6]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/update_One"
                requests.get(url = urlF2, params = PARAMS2)
            else:
                query = "INSTITUCION|STR" + element[0] + "|STR"+ acro + "|STR" + element[1] + "|STR" + element[5]+ "|FLTNULL" + "|STR" + element[6]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)

def planta(plantaArr):

    table = "PLANTA_SITIO"
    PARAMS = {'data':table}
    urlF = URL + "/Clean_Table"
    requests.get(url = urlF, params = PARAMS)
    
    table = "PLANTA|ID|NOMBRE"
    PARAMS = {'data':table}
    urlF = URL + "/getAll_Specs"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json(), strict=False)

    table3 = "PROYECTO"
    PARAMS3 = {'data':table3}
    urlF3 = URL + "/getAll"
    r3 = requests.get(url = urlF3, params = PARAMS3)
    respuesta3 = json.loads(r3.json())

    table7 = "SITIO"
    PARAMS7 = {'data':table7}
    urlF7 = URL + "/getAll"
    r7 = requests.get(url = urlF7, params = PARAMS7)
    respuesta7 = json.loads(r7.json())

    auxiliar = []
    auxiliar2 = []
    for elem in plantaArr:
        aux = elem[27].split(" | ")
        auxiliar.append(aux)
        aux2 = elem[26].split(" | ")
        auxiliar2.append(aux2)

    for elem in plantaArr:
        for elemento in respuesta7:
            if elem[28] == elemento['NOMBRE']:
                elem[28] = elemento['ID']
                break

    for i in range(len(auxiliar)):
        for j in range(len(auxiliar[i])):
            for e in respuesta3:
                if auxiliar[i][j] == e['NOMBRE']:
                    auxiliar[i][j] = e['ID']
                    break
    
    for i in range(len(auxiliar2)):
        for j in range(len(auxiliar2[i])):
            for e in respuesta7:
                if auxiliar2[i][j] == e['NOMBRE']:
                    auxiliar2[i][j] = e['ID']
                    break
    
    for elem in plantaArr:
        for i in range(len(elem)):
            if elem[i]=='':
                elem[i] = 'NULL'
            elif "|" in elem[i]:
                elem[i] = elem[i].replace(' | ', ' & ')

    if len(respuesta)==0:
        cont = 0

        for element in plantaArr:
            query = "PLANTA|STR" + element[0] + "|STR" + element[1] + "|STR" + element[22] + "|INT" + element[28] + "|STR" + element[23] + "|STR" + element[24] + "|STR" + element[25]
            #print(query)
            PARAMS2 = {'data':query}
            urlF2 = URL + "/add_One"
            requests.get(url = urlF2, params = PARAMS2)

            query = "PLANTA|NOMBRE|STR" + element[0]
            PARAMS2 = {'data':query}
            urlF2 = URL + "/getOne"
            r4 = requests.get(url = urlF2, params = PARAMS2)
            respuesta4 = json.loads(r4.json(), strict=False)
            
            idplanta = None
            for elemento in respuesta4:
                idplanta = elemento['ID']
        
            for pos in auxiliar[cont]:
                today = date.today()
                query = "PROYECTO_PLANTA|INT" + pos + "|INT" + idplanta + "|DAT" + today.strftime("%Y-%m-%d")
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)

            for pos2 in auxiliar2[cont]:
                query = "PLANTA_SITIO|INT" + idplanta + "|INT" + pos2 
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)

            cont = cont + 1
    else:
        cont2 = 0
        for element in plantaArr:
            bandera = False
            idcp = None
            for elem in respuesta:
                if element[0] == elem['NOMBRE']:
                    # EXITE -> EDITO
                    bandera = True
                    idcp = elem['ID']
                    break
            if bandera == True:
                query = "PLANTA|"+idcp+"|STRNOMBRE=" + element[0] + "|STRTIPO=" + element[1] + "|STRORIGEN=" + element[22] + "|INTSITIO_UNICO_OBT_ID=" + element[28] + "|STRREG_INVIMA=" + element[23] + "|STRREG_INTERNACIONAL=" + element[24] + "|STRENCARGADO_RECOLECTA=" + element[25]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/update_One"
                requests.get(url = urlF2, params = PARAMS2)

                for pos in auxiliar[cont2]:
                    today = date.today()
                    query = "PROYECTO_PLANTA|INT" + pos + "|INT" + idcp + "|DAT" + today.strftime("%Y-%m-%d")
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)
                
                for pos in auxiliar2[cont2]:
                    query = "PLANTA_SITIO|INT" + idcp + "|INT" + pos
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)

            else:
                query = "PLANTA|STR" + element[0] + "|STR" + element[1] + "|STR" + element[22] + "|INT" + element[28] + "|STR" + element[23] + "|STR" + element[24] + "|STR" + element[25]
                #print(query)
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)
                ''' '''
                query = "PLANTA|NOMBRE|STR" + element[0]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/getOne"
                r4 = requests.get(url = urlF2, params = PARAMS2)
                respuesta4 = json.loads(r4.json(), strict=False)

                idplanta = None
                for elemento in respuesta4:
                    idplanta = elemento['ID']
            
                for pos in auxiliar[cont2]:
                    today = date.today()
                    query = "PROYECTO_PLANTA|INT" + pos + "|INT" + idplanta + "|DAT" + today.strftime("%Y-%m-%d")
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)

                for pos in auxiliar2[cont2]:
                    query = "PLANTA_SITIO|INT" + idplanta + "|INT" + pos 
                    PARAMS2 = {'data':query}
                    urlF2 = URL + "/add_One"
                    requests.get(url = urlF2, params = PARAMS2)
            cont2 = cont2 + 1

def proyecto(proyectoArr):
    table = "PROYECTO"
    PARAMS = {'data':table}
    urlF = URL + "/getAll"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())
    # print(len(respuesta))

    for element in proyectoArr:
        if len(element)<21:
            element.append("NULL")
            element.append("NULL")
        if element[0] == 'Fortalecimiento Institucional':
            element[1] = 'POFI'

    if len(respuesta)==0:
        for element in proyectoArr:
            query = "PROYECTO|STR" + element[0] + "|STR" + element[1] + "|STR" + element[20] + "|STR" + element[21]+ "|STR" + element[4]+ "|STR" + element[6]
            PARAMS2 = {'data':query}
            urlF2 = URL + "/add_One"
            requests.get(url = urlF2, params = PARAMS2)
    else:
        for element in proyectoArr:
            bandera = False
            idcp = None
            for elem in respuesta:
                if element[0] == elem['NOMBRE']:
                    # EXITE -> EDITO
                    bandera = True
                    idcp = elem['ID']
                    break
            if bandera == True:
                query = "PROYECTO|"+idcp+"|STRNOMBRE=" + element[0] + "|STRTIPO=" + element[1] + "|STRFASE_INV_TRAS=" + element[20] + "|STRETAPA=" + element[21]+ "|STRTAGS=" + element[4]+ "|STRURL_IMAGEN=" + element[6]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/update_One"
                requests.get(url = urlF2, params = PARAMS2)
            else:
                query = "PROYECTO|STR" + element[0] + "|STR" + element[1] + "|STR" + element[20] + "|STR" + element[21]+ "|STR" + element[4]+ "|STR" + element[6]
                PARAMS2 = {'data':query}
                urlF2 = URL + "/add_One"
                requests.get(url = urlF2, params = PARAMS2)

def proyectoMacro(proyectoMacroArr):
    # Get all grupos
    # Recorro gruppoArr contra Gerall y si exite lo edito con el id y no existe lo ingreso
    print(len(proyectoMacroArr))

def upload_files_storage():
    config = {
    "apiKey": "AIzaSyBZThYVPbazuWT0W654I2ZS5BDDN_yDyAc",
    "authDomain": "gat-gate.firebaseapp.com",
    "projectId": "gat-gate",
    "storageBucket": "gat-gate.appspot.com",
    "databaseURL": "",
    "servideAccount": "serviceAccountKey.json"
    }

    firebase_storage = pyrebase.initialize_app(config)
    storage = firebase_storage.storage()

    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            #print(os.path.join(root, name))
            #print(name)
            aux = root.split("\\")
            ruta = ""
            for i in range(1, len(aux)):
                ruta = ruta + aux[i] + "/"
            print("informestecnicos/" + ruta + name)
            storage.child("informestecnicos/" + ruta  + name).put(os.path.join(root, name))

    for root, directories, files in os.walk(path2, topdown=False):
        for name in files:
            #print(os.path.join(root, name))
            #print(name)
            aux = root.split("\\")
            ruta = ""
            for i in range(1, len(aux)):
                ruta = ruta + aux[i] + "/"
            print("pofi/" + ruta + name)
            storage.child("pofi/" + ruta  + name).put(os.path.join(root, name))

def clean_persist_POFI(df):
        
    for key, value in df.items():
        if key == 'POFI':
            #print(value.columns.tolist())
            POFI = value.drop(columns=['PRESUPUESTO ','-','INDICADOR CUANTITATIVO ', 'Tipología de MinCiencias', 'OBSERVACIONES', 'Unnamed: 12','Unnamed: 6', 'Unnamed: 7','OBSERVACIONES'])
        if key == 'Avances':
            print(value.columns.tolist())
            Avances = value.drop(columns=['Avance'])
        #print(key, '->', value)# .drop(columns=['PRESUPUESTO',  'OBSERVACIONES']))

    #POFI.index = pd.Series(POFI.index).fillna(method='ffill')
    #print(POFI.at[2,'INSTITUCIÓN'])
    for i in range(len(POFI.index.tolist())-1,0,-1):
        if (pd.isna(POFI.at[i,'INSTITUCIÓN'])):
            POFI.at[i,'INSTITUCIÓN'] = 'Todas'
        elif ( not pd.isna(POFI.at[i,'INSTITUCIÓN'])):
            print (POFI.at[i,'INSTITUCIÓN'])
            break
    #end _for

    for i in range(0,len(POFI.index.tolist())):
        aux_val = str (POFI.at[i,'FECHAS DE SEGUMIENTO PARA LOS  ENTREGABLES \nAÑOS'])
        if "Todos" in aux_val :
            POFI.at[i,'FECHAS DE SEGUMIENTO PARA LOS  ENTREGABLES \nAÑOS'] = 'Todos'
        elif "Año" in aux_val : 
            POFI.at[i,'FECHAS DE SEGUMIENTO PARA LOS  ENTREGABLES \nAÑOS'] = aux_val[0:5]
    #end_for

    values ={ "RESPONSABLE ": "Todos los proyectos", 'FECHAS DE SEGUMIENTO PARA LOS  ENTREGABLES \nAÑOS' : "Todos" }
    POFI =POFI.fillna(value=values)
    POFI = POFI.ffill(axis=0)

    values ={ "Institucion": "Todos", 'Porcentaje' : 0 }
    Avances =Avances.fillna(value=values)

    for i in range(0,len(Avances.index.tolist()),1):
        aux_val = str (Avances.at[i,'Referencia'])
        aux_actividad = str (Avances.at[i,'Actividad'])
        resultado = "FI Informe "
        resultado = resultado + aux_val[11: len(aux_val)] 
        Avances.at[i,'Referencia'] = resultado
        if "A" in aux_actividad:
            Avances.at[i,'Actividad'] = aux_actividad[1:3]
    #end_for

    #POFI.to_excel("C:\\Users\\HP\\Desktop\\PUJ SPL\\Data GAT Gate\\output.xlsx") 
    #Avances.to_excel("C:\\Users\\HP\\Desktop\\PUJ SPL\\Data GAT Gate\\output2.xlsx") 
    #print(POFI.index.tolist())
    #print(Avances)

    #HASTA AQUI ES LIMPIEZA DE DATA


    #Recuperar ID del Proyecto POFI
    chain = "PROYECTO|TIPO|STRPOFI"
    PARAMS = {'data':chain}
    urlF = URL + "/getOne"
    print (urlF)
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())
    print(respuesta)

    idPOFI= None
    for elemento in respuesta:
        idPOFI = elemento['ID']


    #Recuperar todas las actividades
    chain = "ACTIVIDAD|ID|NUMERO|TIPO"
    PARAMS = {'data':chain}
    urlF = URL + "/getAll_Specs"
    print (urlF)
    r = requests.get(url = urlF, params = PARAMS)
    respuestaACT = json.loads(r.json())
    print(respuesta)

    actividades_bd = { 'id':[],'numero':[]}
    for elemento in respuestaACT:
        actividades_bd['id'].append(elemento['ID'])
        actividades_bd['numero'].append(elemento['NUMERO'])


    #INSERTAR LAS ACTIVIDADES
    actividades = []
    for index, row in POFI.iterrows():
        if str(int(row['NÚMERO DE ACTIVIDAD '])) not in actividades_bd['numero'] :
            cadena_actividad=  "ACTIVIDAD|INT"+ str (idPOFI) + "|STR" +str(row['ACTIVIDAD']).replace('|','/') + "|STRPOFI|STR" + str(row['OBJETIVO POFI ']) + "|INT"+ str(int(row['NÚMERO DE ACTIVIDAD ']))
            #print(cadena_actividad)
            actividades.append(str(int(row['NÚMERO DE ACTIVIDAD '])))
            PARAMS = {'data':cadena_actividad}
            urlF = URL + "/add_One"
            r = requests.get(url = urlF, params = PARAMS)
            #respuesta = json.loads(r.json())
        else: 
            aux_indice = actividades_bd['numero'].index(str(int(row['NÚMERO DE ACTIVIDAD '])))
            cadena_actividad=  "ACTIVIDAD|"+ actividades_bd['id'][aux_indice] +"|INTPROYECTO_ID="+ str (idPOFI) + "|STRDESCRIPCION=" +str(row['ACTIVIDAD']).replace('|','/') + "|STRTIPO=POFI|STROBJETIVO_POFI=" + str(row['OBJETIVO POFI ']) + "|INTNUMERO="+ str(int(row['NÚMERO DE ACTIVIDAD ']))
            #print(cadena_actividad)
            actividades.append(str(int(row['NÚMERO DE ACTIVIDAD '])))
            PARAMS = {'data':cadena_actividad}
            urlF = URL + "/update_One"
            r = requests.get(url = urlF, params = PARAMS)


    #INSERTAR EL INFORME ACTUAL
    cadena_informe = "INFORME|INT" +str (idPOFI) + "|DAT"+ str(datetime.today().strftime('%Y-%m-%d'))
    #print(cadena_informe)
    PARAMS = {'data':cadena_informe}
    urlF = URL + "/add_One"
    r = requests.get(url = urlF, params = PARAMS)

    #Recuperar el ultimo informe POFI agregado para tener su ID
    chain = "INFORME"
    PARAMS = {'data':chain}
    urlF = URL + "/getAll"
    #print (urlF)
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())

    idinforme=None
    for elemento in respuesta:
        if elemento['PROYECTO_ID'] == idPOFI:
            idinforme = elemento['ID']
    #print  (idinforme)


    #Recuperar las actividades otra vez, para las inserciones siguientes
    chain = "ACTIVIDAD|ID|NUMERO|TIPO"
    PARAMS = {'data':chain}
    urlF = URL + "/getAll_Specs"
    #print (urlF)
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json())
    #print(respuesta)

    #Recuperar las instituciones
    chain = "INSTITUCION"
    PARAMS = {'data':chain}
    urlF = URL + "/getAll"
    print (urlF)
    r = requests.get(url = urlF, params = PARAMS)
    respuestaIns = json.loads(r.json())

    instituciones = {'id':[],'nombre':[], 'acronimo' :[] }
    for elementoins in respuestaIns:
        instituciones['id'].append(elementoins['ID'])
        instituciones['nombre'].append(elementoins['NOMBRE'])
        instituciones['acronimo'].append(elementoins['ACRONIMO'])


    #Se insertan Informe_Actividad. Se usa el dataframe de Avances, las actividades en BD  y el ultimo informe POFI
    for i in range(0,len(Avances.index.tolist()),1):
        aux_NUM = (Avances.at[i,'Actividad'])
        aux_avance = str (Avances.at[i,'Porcentaje'])
        for elemento in respuesta: #En respuesta estan los resultados de la consulta sobre las actividades
            id_actividad = elemento['ID']
            numero_actividad = elemento['NUMERO']
            if aux_NUM == numero_actividad : 
                cadena_actv_informe = "INFORME_ACTIVIDAD|INT" +str (id_actividad) + "|INT"+ str(idinforme) +"|FLT" + aux_avance
                print(cadena_actv_informe)
                PARAMS = {'data':cadena_actv_informe}
                urlF = URL + "/add_One"
                r = requests.get(url = urlF, params = PARAMS)

    #print(instituciones) 

    #Se insertan actividades por institucion 
    for i in range(0,len(POFI.index.tolist()),1):
        #print('exterior ')
        aux_institucion = (POFI.at[i,'INSTITUCIÓN'])
        aux_num = (POFI.at[i,'NÚMERO DE ACTIVIDAD '])

        if "|" in  aux_institucion:
            aux0 = aux_institucion.split("|")
            aux_institucion = aux0[0]

        if "Todas" != aux_institucion:
            for elemento in respuesta:
                if(elemento['TIPO'] == 'POFI'):
                    id_actividad = elemento['ID']
                    numero_actividad = elemento['NUMERO']
                    #print(numero_actividad)
                # print('del medio '+ str(numero_actividad)[0:2] + "   " + str(aux_num)[0:2] )
                    if int(aux_num) ==  int(numero_actividad):
                        indice = instituciones['acronimo'].index(aux_institucion)
                        institucion1 = aux_final = str(instituciones['id'][indice]).split("|")
                        #print(institucion1)
                        cadena_inst_actv = "INSTITUCION_ACTIVIDAD|INT" + str(id_actividad) + "|INT"+ str(instituciones['id'][indice]) + "|DAT"+ str(datetime.today().strftime('%Y-%m-%d'))
                        PARAMS = {'data':cadena_inst_actv}
                        urlF = URL + "/add_One"
                        r = requests.get(url = urlF, params = PARAMS)
                        print(cadena_inst_actv)

def split_actividad(row):
    row = row.strip()
    row = row.replace(u'\xa0', u' ')

    actividad_y_descrip = row.split(' ',1)
    print(actividad_y_descrip)
    assert len(actividad_y_descrip) == 2

    numero_y_descrip = actividad_y_descrip[1] .split(':',1)
    print(numero_y_descrip)
    if len(numero_y_descrip) < 2:
        numero_y_descrip = actividad_y_descrip[1].split(' ',1)

    assert len(numero_y_descrip) == 2

    actividad = actividad_y_descrip[0].strip()
    numero = numero_y_descrip[0].strip().replace(',','.')
    print(numero)

    if not all( x.isnumeric() for x in numero.split('.')):
        print(row)
        assert False

    descrip = numero_y_descrip[1].strip()
    print(descrip)

    return numero, descrip

def calcular_avance_actividad(idActividad):  
    print(idActividad)  

    #Obtengo todas las TAREAS por el Id de ACTIVIDAD
    query = "TAREA|PORCENTAJE_AVANCE|ACTIVIDAD_ID"
    PARAMS = {'data':query}
    urlF = URL + "/getAll_Specs"
    r = requests.get(url = urlF, params = PARAMS)
    respuesta = json.loads(r.json(), strict = False)

    tareas = []

    for element in respuesta:
        if element['ACTIVIDAD_ID'] == idActividad :
            tareas.append(element)
        
        avances = 0
        for elemento in tareas:
            avances += float(elemento['PORCENTAJE_AVANCE'])

    avance_act = avances/len(tareas)
    return avance_act

def limpieza_informes(index1, index2):

    #Clean de la tabla
    query_clean = "TAREA"
    PARAMS5 = {'data':query_clean}
    urlF5 = URL + "/Clean_Table"
    requests.get(url = urlF5, params = PARAMS5)

    rutas=[]
    hojas=[]
    proyectos=[]
    informes = []
    meses_corte = ['Marzo', 'Junio', 'Septiembre', 'Diciembre']

    #Establecer mes y año del informe
    if(date.today().month == 4):
        month=meses_corte[0]
        year = date.today().year
    elif(date.today().month == 7):
        month=meses_corte[1]
        year = date.today().year
    #Corregir por 10!!!!!!!!!!!!!!!!!!!!
    elif(date.today().month == 11):
        month=meses_corte[2]
        year = date.today().year
    elif(date.today().month == 1):
        month=meses_corte[3]
        year = date.today().year - 1

    fechacorte = str(year) + "-" + str(date.today().month-1) + "-" + ("30") 

    #Construcción de cadenas de nombrs de archivos
    for i in range (1,11):
        #Construcción de cadenas variables para leer los informes
        informe = 'P' + str(i) + '_Informe tecnico corte ' + str(month) + ' ' + str(year) + '.xlsx'
        informes.append(informe)

    #Bussqueda de rutas de los archivos(informes)
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            for i in informes:
                if i == name:
                    rutas.append(os.path.join(root, name))
                    hoja=name.split('_', 1)
                    p=hoja[0]
                    hojas.append(p)
                    proyecto = "Proyecto " + p[1:len(p)]
                    proyectos.append(proyecto)

    #Insercicón de datos por cada ruta
    for i in range(0, len(rutas)):
        print(i)
        proyecto = proyectos[i]
        hoja = hojas[i]
        #Construcción de cadenas variables para leer los informes
        informe = rutas[i]
        print(informe + "\n")

        #Obtener Id del proyecto
        query2 = "PROYECTO|TAGS|STR" + proyecto
        PARAMS2 = {'data':query2}
        urlF2 = URL + "/getOne"
        r2 = requests.get(url = urlF2, params = PARAMS2)
        respuesta2 = json.loads(r2.json(), strict=False)
        
        idProyecto = None
        for elemento in respuesta2:
            idProyecto = elemento['ID']

        #Creo el INFORME en la BD
        query_inf = "INFORME|INT" + idProyecto + "|STR" + fechacorte
        PARAMS3 = {'data':query_inf}
        urlF3 = URL + "/add_One"
        requests.get(url = urlF3, params = PARAMS3)

        #Obtener Id del INFORME creado
        query_inf2 = "INFORME" #|PROYECTO_ID|" + "INT" + idProyecto
        PARAMS4 = {'data':query_inf2}
        urlF4 = URL + "/getAll"
        r3 = requests.get(url = urlF4, params = PARAMS4)
        respuesta3 = json.loads(r3.json(), strict=False)
                
        idInforme = None
        for elemento in respuesta3:
            if elemento['FECHA_CORTE'] == fechacorte:
                idInforme = elemento['ID']
            print(idInforme)
        
        #Read informes
        df = pd.read_excel(informe, sheet_name= [hoja, 'Productos'])

        #Iteración sobre las hojas
        for key, value in df.items():
            
            #Hoja productos
            if key == 'Productos':
            
            #Control de cantidad de columnas 
                if(len(value.columns) > 13):
                    #Drop columns con porcentajes de avance de informes anteriores
                    idx = np.r_[5:index1,13]
                    productos = value.drop(value.columns[idx], axis=1)
                else:
                    #Drop columns con porcentajes de avance de informes anteriores
                    idx = np.r_[5:index1]
                    productos = value.drop(value.columns[idx], axis=1)

                #Add headers a columnas
                productos.columns =['tipo', 'producto', 'subproducto', 'cantidad', 'descripcion', 'avance', 'verificacion', 'proyeccion']

                #Drop fila 1 con headers pre-determinados
                productos = productos.drop([0])

                #Obtener año sin semestre
                productos['proyeccion'][0:3]

                #Cambio de missing values por valores definidos
                values = {"descripcion": "Por definir", "avance": 0, "proyeccion": "Por definir"}
                productos = productos.fillna(value=values)

                #Drop filas con totales
                total_entregables = productos[productos['subproducto']=='Total de productos'].index.values
                print(total_entregables)
                productos = productos.drop([total_entregables[0], total_entregables[0]+1, total_entregables[0]+2, total_entregables[0]+3])

                #Fill down columnas con missin values
                productos = productos.ffill(axis = 0)

                #Construccion cadena para clase entregable e insert en la BD
                for index, row in productos.iterrows():
                    query_entr = "ENTREGABLE|STR" + str(row['descripcion']) + "|STR" + str(row['subproducto']) + "|STR" + str(row['tipo']) + "|STR" + str(row['producto']) + "|INT" + str(row['proyeccion'])
                    PARAMS10 = {'data':query_entr}
                    urlF10 = URL + "/add_One"
                    requests.get(url = urlF10, params = PARAMS10)

                    query_id_ent = "ENTREGABLE" 
                    PARAMS30 = {'data':query_id_ent}
                    urlF30 = URL + "/getMaxID"
                    r30 = requests.get(url = urlF30, params = PARAMS30)
                    res= json.loads(r30.json(), strict=False)
                    idENT = None
                    for elemento in res:
                        idENT = elemento['ID']

                    ##### INSERTAR INFORME X ENTREGABLE
                    
                    query_inf_entr = "ENTREGABLE_INFORME|INT" + str(idInforme) + "|INT" + str(idENT) + "|FLT" + str(row['avance'])
                    PARAMS11 = {'data':query_inf_entr}
                    urlF11 = URL + "/add_One"
                    requests.get(url = urlF11, params = PARAMS11)

                    print(query_inf_entr)
                
            else:
                #Control de cantidad de columnas             
                if(len(value.columns) > 14):
                    i = len(value.columns)
                    #Drop columns con porcentajes de avance de informes anteriores
                    idx = np.r_[7:index2, 14:i]
                    proyecto = value.drop(value.columns[idx], axis=1)

                else:
                    #Drop columns con porcentajes de avance de informes anteriores
                    idx = np.r_[7:index2]
                    proyecto = value.drop(value.columns[idx], axis=1)

                #Add headers a columnas
                proyecto.columns = ['actividad', 'tarea', 'inicio', 'meses', 'final', 'inicio real', 'final real', 'avance', 'descripcion informe']

                #Drop fila 1,2,3 con headers pre-determinados
                proyecto = proyecto.drop([0, 1, 2])

                #Cambio de missing values por valores definidos
                values = {"tarea": "Por definir", "avance": 0, "descripcion informe": " "}
                proyecto = proyecto.fillna(value=values)

                #Fill down columnas con missing values
                proyecto = proyecto.ffill(axis = 0)

                #Filtrar solo las columnas actividad (descarta los objetivos)
                proyecto = proyecto[proyecto['actividad'].str.contains("Actividad|ACTIVIDAD")]
                proyecto.reset_index(drop=True, inplace=True)

                ###### INSERTAR ACTIVIDADES ########
                print("------------INSERTAR ACTIVIDADES-------------------")

                #Obtengo todas las ACTIVIDADES por en BD
                query = "ACTIVIDAD|ID|NUMERO"
                PARAMS = {'data':query}
                urlF = URL + "/getAll_Specs"
                r = requests.get(url = urlF, params = PARAMS)
                respuesta = json.loads(r.json(), strict = False)

                act_exist=[]
                for element in respuesta:
                    act_exist.append(element['NUMERO'])
                print("Existen")
                print(act_exist)
                
                #Recorrer el dataframe para ACTIVIDADES
                for i in range(0,len(proyecto.index.tolist()),1):
                    act_df = str (proyecto.at[i,'actividad'])
                    n_df, d_df = split_actividad(act_df)
                    numero_df = hoja + "-" + n_df
                    if(numero_df not in act_exist):
                        print("no está" + numero_df)
                        if(i!=0):
                            print("no está>primero")
                            #Obtengo la actividad anterior
                            x = i - 1
                            act_anterior = str(proyecto.at[x, 'actividad'])
                        
                            #Comparo la actividad actual con la anterior, si son diferentes, creo la cadena
                            if(act_anterior != str(proyecto.at[i,'actividad'])):
                                actividad = str(proyecto.at[i,'actividad'])
                                numero, descripcion = split_actividad(actividad)
                                idt_act = hoja + "-" + numero

                                #ACTIVIDAD|PROYECTO_ID|DESCRIPCION|TIPO|OBJETIVO_POFI|NUMERO
                                query_act = "ACTIVIDAD|INT" + idProyecto + "|STR" + descripcion + "|STRTecnico-gestion" + "|NULL" + "|STR" + idt_act
                                print(query_act)
                                PARAMS5 = {'data':query_act}
                                urlF5 = URL + "/add_One"
                                requests.get(url = urlF5, params = PARAMS5)

                        if(i==0):
                            print("no está- primero")
                            actividad = str (proyecto.at[i,'actividad'])
                            numero, descripcion = split_actividad(actividad)
                            idt_act = hoja + "-" + numero

                            #ACTIVIDAD|PROYECTO_ID|DESCRIPCION|TIPO|OBJETIVO_POFI|NUMERO
                            query_act = "ACTIVIDAD|INT" + idProyecto  + "|STR" + descripcion + "|STRTecnico-gestion" + "|NULL" + "|STR" + idt_act
                            print("---------PRIMERA", query_act)
                            PARAMS5 = {'data':query_act}
                            urlF5 = URL + "/add_One"
                            requests.get(url = urlF5, params = PARAMS5)    

                ###### INSERTAR TAREAS ####
                print("------------INSERTAR TAREAS--------------------")

                #Recorrer el dataframe para TAREAS
                for index, row in proyecto.iterrows():

                    actividad2 = str(row['actividad'])
                    numero2, descripcion2 = split_actividad(actividad2)
                    idt_act2= hoja + "-" + numero2

                    #Obtener Id de la actividad
                    query_get_act = "ACTIVIDAD|NUMERO|STR" + idt_act2
                    PARAMS6 = {'data':query_get_act}
                    urlF6 = URL + "/getOne"
                    r4 = requests.get(url = urlF6, params = PARAMS6)
                    respuesta4 = json.loads(r4.json(), strict = False)
                    
                    idActividad = None
                    for elemento in respuesta4:
                        idActividad = elemento['ID']

                    #Obtener solo fechas (descartar horas)
                    inicio = str(row['inicio'])[0:10]
                    final = str(row['final'])[0:10]
                    inicio_real = str(row['inicio real'])[0:10]
                    final_real = str(row['final real'])[0:10]

                    query_tar = "TAREA|INT" + str(idActividad) + "|STR" + str(row['tarea']) +"|STR" + inicio+ "|STR" + final + "|FLT" + str(row['avance']) + "|FLT" + str(row['meses']) + "|STR" + inicio_real + "|STR" + final_real
                    print(query_tar)
                    PARAMS7 = {'data':query_tar}
                    urlF7 = URL + "/add_One"
                    requests.get(url = urlF7, params = PARAMS7)

                ##### INSERTAR INFORME X ACTIVIDAD
                print("------------INSERTAR INFORME X ACTIVIDAD--------------------")

                #Obtengo todas las ACTIVIDADES por en BD
                query = "ACTIVIDAD|ID|NUMERO"
                PARAMS = {'data':query}
                urlF = URL + "/getAll_Specs"
                r = requests.get(url = urlF, params = PARAMS)
                respuesta = json.loads(r.json(), strict = False)

                all_act=[]
                for element in respuesta:
                    all_act.append(element['ID'])

                #Por cada ACTIVIDAD que este en el arreglo de IDs calculo el porcentaje y lo agrego a la tabla de INFORME_ACTIVIDAD
                for elemento in all_act:
                    avance = calcular_avance_actividad(elemento)

                    #INFORME_ACTIVIDAD|ACTIVIDAD_ID|INFORME_ID|PORCENTAJE_AVANCE
                    query_infxact = "INFORME_ACTIVIDAD|INT" + str(elemento) + "|INT" + idInforme + "|FLT" + str(avance)
                    print(query_infxact)
                    PARAMS9 = {'data':query_infxact}
                    urlF9 = URL + "/add_One"
                    requests.get(url = urlF9, params = PARAMS9)


    index = []
    index.append(index1+1)
    index.append(index2+1)
    return index

if __name__ == '__main__':
    # Start process downloading files form osf
    # seconds in 3 months = 7776000
    # seconds in 1 week = 604800
    s = sched.scheduler(time.time, time.sleep)
    index_inicial1 = 10
    index_inicial2 = 12
    esPrimera = True
    s.enter(1, 1, start_process, (s,index_inicial1, datetime.today(), esPrimera,index_inicial2,))
    s.run()
