import base64, os, random
from pathlib import Path
from src.summary.summary import Summary
from src.classify import classify
from dash_app.summary_card import summary_card
from dash_app.utils import generate_name
import logging
logging.basicConfig(
    filename="./logs.txt",
    level=logging.INFO, 
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%d/%m/%Y-%H:%M:%S'
 )
import schedule #pip install schedule
import time
import shutil


path = "./results/doc_type/a_ranger/"

# function that lists all files
def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file



# same function as app.py without probability in the front but addition in the log
def upload_pdf(filecontent, file):
    logging.info("Start Run_docs")
    print(f"nom du fichier ds fonction: {file}")
    saving_name     = generate_name(filecontent)
    pdf_path        = os.path.join("data",   saving_name, file) # file a la place de temp.pdf
    os.makedirs(os.path.join("data",    saving_name), exist_ok=True)
    # content_path    = os.path.join("results", saving_name, file+".txt")
    content_path    = os.path.join("temp", saving_name, "contents.txt")
    print(f"nom du path ds fonction: {content_path}")
    os.makedirs(os.path.join("temp", saving_name), exist_ok=True)
    pathEncoded=os.path.join("temp", saving_name)
    print(pathEncoded)
    
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(filecontent))
    logging.info(f"Saved {saving_name}")
    
    try:
        classification, proba_res = classify(pathEncoded, pdf_path, content_path, clean=True)
        
        logging.info("Classified")

        with open(content_path, encoding="utf-8") as f:
            data = f.read()
        s = random.randint(0, max([len(data)- 500, 0]))

        pages = list()
        for contents in [str(e) for e in Path(os.path.dirname(content_path)).rglob("*.txt")]:
            # print(contents)
            with open(contents, "r", encoding="utf-8") as f:
                pages.append(f.read())

        summary = Summary(classification)

        logging.info("extract")
        summary.extract(data, pages=pages[1:])

        logging.info("name")
        name = summary.naming()
        # print(summary.content)

        logging.info("Summarize")
        card = summary_card(summary)

        logging.info("Summarized")
    except Exception as e:
        logging.critical(str(e))
        classification, proba_res, name, card, data, s  = "nsp", dict(nsp=1), "inconnu", "aucune synthèse", "", 0

    proba = int(proba_res[classification]* 100)
    logging.info(f"Probability {proba}")

    return [classification, name, data[s: s+500], card]



# function that opens, reads binary files and converts them to string
# after, list all the directories and files in path to delete them
def run_batch():
    for file in get_files(path):
        
        with open(path+file, "rb") as pdf_file:
            filecontent = base64.b64encode(pdf_file.read())
            filecontent=str(filecontent, "utf-8")
            upload_pdf(filecontent, file) # j'ai mis le 2eme argument pour recuperer le nom du fichier dans la fonction upload_pdf()

            shutil.rmtree("./temp/") # apres avoir appeler upload_pdf() , je supprime le dossier temporaire


    for file_object in os.listdir(path): 
        file_object_path = os.path.join(path, file_object) 
        if os.path.isfile(file_object_path): 
            os.unlink(file_object_path) 
        else: 
            shutil.rmtree(file_object_path)
    logging.info("Clear a_ranger")


# if folder not empty execute run_batch else go to schedule
if os.path.isdir(path) and os.path.exists(path):
    if len(os.listdir(path)) != 0:
        run_batch()
else:
    os.makedirs(os.path.join("./", path), exist_ok=True)
    logging.info("Création dossier a_ranger")



run_batch()





