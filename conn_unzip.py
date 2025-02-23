import os, re, zipfile, shutil
from colorama import init, Fore

def find_file (file):
    # get folder content
    folder = os.listdir(".")

    # find file
    pattern = re.compile(file)
    for archivo in folder:
        if pattern.search(archivo):
            return(archivo)
        
def unzip (file):
    # unzip file
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(".") 


def get_new_connections ():
    # get zip file
    zip_file = find_file("instagram.*zip")

    if zip_file is None:
        # raise Error
        raise ValueError("Can't find zip file")

    else:
        # get connections folder from last run
        conn = find_file("connections")

        # delete old connections
        if conn is not None:
          shutil.rmtree(conn)

        # unzip instragram-zip
        try: 
            unzip(zip_file)
            init(autoreset=True)
            print(Fore.GREEN + f"Succesfuly unziped {zip_file}")
        
        except:
            print(f"Can't unzip {zip_file}")


    

    


