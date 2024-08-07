
import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import filedialog as fd
import os
from datetime import date, datetime, timedelta
from xml.dom import minidom
import shutil

#Conversion a XML, generación de ID por nombre y organizacion por carpetas para metadata Champions League


class Especiales:

    def __init__(self):
        self.champions()


    def champions(self):
        archivo = fd.askopenfilename(title="Selecciona csv de Metadata",filetypes=[("CSV Files","*.csv")])
        print('primero carpeta para exportar datos')
        exporta = fd.askdirectory(title="Carpeta para datos exportados de Comecast")
        print('despues carpeta de imagenes')
        carpeta= fd.askdirectory(title="selecciona carpeta de imgs")
        archivopd = pd.read_csv(archivo,header=3)
        path0 = os.path.join(exporta,"Champions")
        os.mkdir(path0)

        Title= archivopd['title']
        time=archivopd['time']
        summary=archivopd['summary']
        runtime=archivopd['runtime']
        deeplink= archivopd['deeplink']
        year= archivopd['publishYear']
        startDate= archivopd['startDate']       
        endDate=archivopd['endDate']
        


        for i in range(len(Title)):
            #Genera ID
            title= (Title[i]).rstrip()
            IDs= 'CHMP'+'0000000000'+(title[-3:]).upper()+(title[:1]).upper()+'0'
            type(time)   

            if 'hs' in time :                
                time= time.replace('hs','')
                
            if 'h' in runtime:                
                runtime= runtime.replace('h','')
           
            path1 = os.path.join(path0,self.acentos(IDs)+'1')
            os.mkdir(path1)
            try:                
                self.xmlHBO(self.acentos(IDs),str(deeplink[i]),path1,title,str(year[i]),str(startDate[i]),
                            str(endDate[i]),str(time[i]),summary[i],str(runtime[i]))
                self.Imgs(self.acentos(IDs),str(title),carpeta,path1)
                
            except Exception as e:
                print(e)
            
            
    def acentos(self,data):
        #Sustituye acentos
        ac={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U'}
        for letra in ac:
            if letra in data:
                data= data.replace(letra, ac[letra])
                
        return data
        
    def Imgs(self,IDs,name,carpeta,path1):
        #Búsqueda por coincidencia, detecta a que ID pertenece, funciona con títulos incompletos
        name=name.upper()
        name=name.split()
        IDs=IDs+str(1)        
        contenido=os.listdir(carpeta)
        arr=[]

        for folder in contenido:

            if os.path.isfile(folder) == False and '.DS_Store'not in folder:
                archivos=os.listdir(carpeta+'/'+folder)
                
                for archivo in archivos:
                    arr.append(archivo)

        cc={}
        for im in arr :   
            c=0

            for p in name:
                p=p[:3]        
                if p in im:
                    c=c+1
                    
            cc[im]=c    

        resultado=max(cc,key= cc.get)
        print(resultado)

        #Organizacion de imágenes por folder
        for folder in contenido:
            if 'HORIZONTAL' in folder:
                if '_ver' in resultado:
                    resultado=resultado.replace('_ver','_hor')
                    print(resultado)
                pathr=os.path.join(carpeta,folder,resultado)
                destino=os.path.join(path1,IDs+'_1.jpg')
                shutil.copy(pathr,destino)
                
                                
            if 'VERTICAL' in folder:
                if '_hor' in resultado:
                    resultado=resultado.replace('_hor','_ver')
                    print(resultado)
                pathr=os.path.join(carpeta,folder,resultado)
                destino=os.path.join(path1,IDs+'.jpg')                
                shutil.copy(pathr,destino)

                
    def xmlHBO(self,ID,deeplink,path1,title,year,startDate,endDate,time,summary,runtime):
        
        #Creación de XML
        nameProveedor="HBMX"
        webProveedor="hbomax.com"
        i = 1
        today = date.today()
        hoy = today.strftime("%Y-%m-%d")
        startDate= datetime.strptime(startDate,'%m/%d/%Y')
        startDate2= startDate - timedelta(3)
        startDate2=startDate2.strftime("%Y-%m-%d")
        startDate=startDate.strftime("%Y-%m-%d")        
        endDate= datetime.strptime(endDate,'%m/%d/%Y')
        endDate2= endDate + timedelta(2)  
        endDate2=endDate2.strftime("%Y-%m-%d")     
        endDate=endDate.strftime("%Y-%m-%d")
       


        root = ET.Element('ADI')
        tag1 = ET.SubElement(root,"Metadata")
        ET.SubElement(tag1,"AMS",  Asset_Class="package", Asset_ID= ID+str(i), Asset_Name=title +" -PACKAGE", Creation_Date=str(hoy),
                    Description= title+" PACKAGE ASSET", Product="SVOD",  Provider=nameProveedor, Provider_ID=webProveedor, Version_Minor="0", Version_Major="1" )
        ET.SubElement(tag1,"App_Data", App="MOD", Name="Metadata_Spec_Version", Value="CableLabsVOD1.1")
        tag2 = ET.SubElement(root,"Asset")
        tag3CH = ET.SubElement(tag2,"Metadata")
        ET.SubElement(tag3CH,"AMS", Version_Minor="0", Version_Major="1", Provider_ID=webProveedor, Provider=nameProveedor,Product="SVOD",
                    Description= title+" TITLE",Creation_Date=str(hoy), Asset_Name=title +" -TITLE",  Asset_ID= ID+str(i+1), Asset_Class="title")
        ET.SubElement(tag3CH,"App_Data",App="MOD", Value="title", Name="Type" )
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value=title+' '+startDate+' '+time[:-3], Name="Title")
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value=title[:19], Name="Title_Brief")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=runtime, Name="Run_Time")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value =runtime[:-3], Name="Display_Run_Time")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=str(year), Name="Year" )
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=startDate2+'T00:00:00', Name="Licensing_Window_Start" )
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=endDate2+'T23:59:00', Name="Licensing_Window_End" )
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value="Y", Name="Platform_MOD") 
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value="Y", Name="Platform_Streaming")
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value="Movies", Name="Show_Type")       
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value="99021", Name="Billing_ID")  
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value="02:00:00", Name="Maximum_Viewing_Length")          
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value=summary[:128], Name="Summary_Short")
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value=summary, Name="Summary_Long")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=".", Name="Actors" )
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value=".", Name="Actors_Display" ) 
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='sports', Name="Genre")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='deportes', Name="Genre")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='películas de deportes', Name="Genre")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='sports', Name="Category")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='deportes', Name="Category")
        ET.SubElement(tag3CH, "App_Data", App="MOD", Value='películas de deportes', Name="Category")
        ET.SubElement(tag3CH,"App_Data", App="MOD", Value='G', Name="Rating")
        tag4CH = ET.SubElement(tag2,"Asset")
        tag4Children = ET.SubElement(tag4CH,"Metadata")
        ET.SubElement(tag4Children,"AMS", Version_Minor="0", Version_Major="1",   Provider_ID=webProveedor, Provider=nameProveedor,Product="SVOD",
                       Description= title+" MOVIE",Creation_Date=str(hoy), Asset_Name= title+"-MOVIE",  Asset_ID= ID+str(i+2), Asset_Class="movie")
        ET.SubElement(tag4Children, "App_Data", App="MOD", Value="movie", Name="Type")
        ET.SubElement(tag4Children, "App_Data",App="MOD", Value="Y", Name="HDContent" ) 
        ET.SubElement(tag4Children, "App_Data",App="MOD", Value="APP", Name="Protocol_Info" ) 
        ET.SubElement(tag4Children, "App_Data",App="MOD", Value="None", Name="Encryption_Type" ) 
        ET.SubElement(tag4Children, "App_Data",App="MOD", Value="N", Name="Encryption" ) 
        ET.SubElement(tag4Children, "App_Data", App="MOD", Value="DUMY_DEMO-DEEPL-LINK_MOD_DASH_Widevine", Name="Conax_Product_ID" )                
        ET.SubElement(tag4CH,"Content",Value = deeplink)
        tag5CH = ET.SubElement(tag2,"Asset")
        tag5Children = ET.SubElement(tag5CH,"Metadata")
        ET.SubElement(tag5Children,"AMS", Version_Minor="0", Version_Major="1", Provider_ID=webProveedor, Provider=nameProveedor,Product="SVOD",
                       Description= title+" POSTER", Creation_Date=str(hoy), Asset_Name= title+" -POSTER",  Asset_ID= ID+str(i+3), Asset_Class="poster") 
        ET.SubElement(tag5Children, "App_Data", App="MOD", Value="image", Name="Type")
        ET.SubElement(tag5Children, "App_Data", App="MOD", Value= '71108c262a57eba1cce1edafa91412a5', Name="Content_CheckSum")
        ET.SubElement(tag5Children, "App_Data", App="MOD", Value='2341715',Name="Content_FileSize" )
        ET.SubElement(tag5Children, "App_Data", App="MOD", Value="poster", Name="Type")
        ET.SubElement(tag5Children, "App_Data", App="MOD", Value="1920x1080", Name="Image_Aspect_Ratio")
        ET.SubElement(tag5CH,"Content",Value = ID+str(i)+"_1.jpg")
        tag6CH = ET.SubElement(tag2,"Asset")
        tag6Children = ET.SubElement(tag6CH,"Metadata")
        ET.SubElement(tag6Children,"AMS", Version_Minor="0", Version_Major="1", Provider_ID=webProveedor, Provider=nameProveedor,Product="SVOD", 
                      Description= title+" IMAGE", Creation_Date=str(hoy), Asset_Name=title+" -IMAGE",  Asset_ID= ID+str(i+4), Asset_Class="image")
        ET.SubElement(tag6Children, "App_Data", App="MOD", Value="image", Name="Type")
        ET.SubElement(tag6Children, "App_Data", App="MOD", Value= '71108c262a57eba1cce1edafa91412a5', Name="Content_CheckSum")
        ET.SubElement(tag6Children, "App_Data", App="MOD", Value='2341715',Name="Content_FileSize" )
        ET.SubElement(tag6Children, "App_Data", App="MOD", Value='POSTER|VERTICAL|TEXT',Name="Tag" )
        ET.SubElement(tag6Children, "App_Data", App="MOD", Value="527x858", Name="Image_Aspect_Ratio")
        ET.SubElement(tag6CH,"Content",Value = ID+str(i)+".jpg")

        #PRETTY xml ADI
        pretty = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        rot = ET.fromstring(pretty)
        doc2 = ET.ElementTree(rot)

        #wb se usa para string y bytes
        with open (path1+'/ADI.XML', 'wb' ) as f:
            #linea adicional
            f.write ('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE ADI SYSTEM "ADI.DTD">'.encode('utf8'))
            doc2.write(f,'utf-8')
        
        






Especiales()