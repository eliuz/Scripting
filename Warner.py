import os
import shutil
import pandas as pd
from datetime import  datetime 

#Copia Pega y organiza en estructura de carpetas los assets de Warner para cargarlos a Aspera,
#posteriormente genera log de encontrados para comparar con su lista de entrega

def organiza():
   
    path_origen ="D:/WARNER/descarga"   
    path_video="D:/WARNER/carga/Media"
    path_metadata="D:/WARNER/carga/Metadata/WarnerChannel"
    path_art="D:/WARNER/carga/Art/WarnerChannel"
    data={
          
        }
    
    
    raiz= os.listdir(path_origen)
    for directorio1 in raiz:
        # directorio1 carpeta raiz de descarga
        if "WBD" in directorio1 :
            
            name = directorio1
            path_art= os.path.join(path_art,name)
            os.mkdir(path_art) if os.path.exists(path_art) == False else print("ya existe carpeta de imágenes")
            data['ID']= name            
            carpeta= os.path.join(path_origen,directorio1)            
            directorio2= os.listdir(carpeta)
            # directorio2 carpeta con assets
            for archivo in directorio2:
                    
                if ".XML" in archivo:
                    data['XML'] =["ENCONTRADO"]
                    print("XML encontrado"+name)                    
                    origen= os.path.join(carpeta,archivo)                                  
                    xml= os.path.join(path_metadata,archivo)
                    shutil.copy(origen,xml) if os.path.isfile(xml) == False else print("ya existe la metadata "+name)
                    
                if "_highlight" in archivo:
                    data['highlight'] =["ENCONTRADO"]
                    ("highlight encontrado"+name)  
                    origen= os.path.join(carpeta,archivo)
                    img=os.path.join(path_art,archivo)
                    shutil.copy(origen,img)  if os.path.isfile(img) == False else print("ya existe highlight "+name)
                                        
                if "_highlight1" in archivo:
                    data['highlight1'] =["ENCONTRADO"]
                    ("highlight1 encontrado"+name) 
                    origen= os.path.join(carpeta,archivo)
                    img=os.path.join(path_art,archivo)
                    shutil.copy(origen,img) if os.path.isfile(img) == False else print("ya existe highlight1 "+name)
                    
                if "_main" in archivo:
                    data['main'] =["ENCONTRADO"]
                    ("main encontrado"+name) 
                    origen= os.path.join(carpeta,archivo)
                    img=os.path.join(path_art,archivo)
                    shutil.copy(origen,img) if os.path.isfile(img) == False else print("ya existe main "+name)   
                                                   
                if ".mp4" in archivo:
                    data['MP4']=["ENCONTRADO"]
                    print("mp4 encontrado"+name)
                    origen= os.path.join(carpeta,archivo)
                    video= os.path.join(path_video,archivo)
                    shutil.copy(origen,video) if os.path.isfile(video) == False else print("ya existe el video "+name)
    
    #Genera checklist de elementos encontrados
    now= datetime.now().time() 
    now = now.strftime("%H%M%S")  
    print(data)
    df = pd.DataFrame(data)
    df.to_csv(f"D:/WARNER/log{now}.csv", index=False)
    print("fin")                
 
 

organiza()