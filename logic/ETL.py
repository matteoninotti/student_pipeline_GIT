import csv
import re
import json
from collections import Counter
from datetime import datetime
from logic.gen_students import Corso
from state import PROJECT_PATH


now_time = datetime.now().strftime("%Y%m%d_%H%M%S") 



class ETL:
  def __init__(self, studenti_corso):
    self.subjects = Corso.MATERIE
    self.studenti = studenti_corso
    # definisce i nomi dei campi usati dal csv
    self.fieldnames = ["id", "nome", "cognome", "data_nascita", "email", *self.subjects]
    self.csv_file_name = PROJECT_PATH + "data/input/studenti_" + now_time + ".csv"
    # crea il nome del file JSON degli studenti validi, appendendo data e ora attuale
    self.json_file_name = PROJECT_PATH + "data/output/studenti_validi_" + now_time + ".json"
  
  
  def reformat_studenti(self) -> list:
    """
    riformatta la lista studenti "spacchettando" le materie
    per ogni studente. questo per preparare la lista al
    formato richiesto dal csv (-> una colonna per ogni materia)
    """
    studenti_reformated = []
    for s in self.studenti:
      studente_reformated = {
        "id": s["id"],
        "nome": s["nome"],
        "cognome": s["cognome"],
        "data_nascita": s["data_nascita"],
        "email": s["email"],
      }
      for subj in self.subjects:
        studente_reformated[subj] = s["voti"][subj]
      
      studenti_reformated.append(studente_reformated)
    
    return studenti_reformated
  

  def create_students_csv(self) -> None:
    """
    scrive studenti_reformated in formato csv in "student_pipeline/data/input/" 
    """
    studenti_reformated = self.reformat_studenti()
    with open(self.csv_file_name, "w", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=self.fieldnames)
      writer.writeheader()
      writer.writerows(studenti_reformated)
    
    return None
  
  
  def validate_csv(self) -> list:
    """
    valida che il formato di ogni studente sia corretto.
    ritorna lista di dizionari
    """
    validati = []
    
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    DATA_REGEX = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

    with open(self.csv_file_name, "r", encoding="utf-8") as f:
      studenti_reader = csv.DictReader(f)
      
      for studente in studenti_reader:
        valido = {"id": studente["id"]} #inizializzo dict per validazione studenti
        valido["email_valida"] = bool(re.match(EMAIL_REGEX, studente["email"]))
        valido["data_valida"] = bool(re.match(DATA_REGEX, studente["data_nascita"]))
        voti = [studente[subj] for subj in self.subjects]
        valido["voti_in_range"] = all(Corso.VOTO_MIN <= int(voto) <= Corso.VOTO_MAX for voto in voti)
        
        validati.append(valido)
    
    return validati
  
  
  def count_validation_errors(self) -> str:
    """
    conta quante mail, date e voti contengono errori di formato
    """
    validati = self.validate_csv()
    c = Counter
    email_counter = c(v.get("email_valida") for v in validati)
    date_counter = c(v.get("data_valida") for v in validati)
    voti_counter = c(v.get("voti_in_range") for v in validati)

    return f"""
  email non valide: {email_counter[False]}
  date non valide: {date_counter[False]}
  voti fuori range: {voti_counter[False]}
    """
  
  
  def clean_scartati(self) -> list:
    """
    rimuove dal csv i record di studenti contenenti errori e li appende a lista "scartati"
    """
    validati = self.validate_csv()
    with open(self.csv_file_name, "r", encoding="utf-8") as f:
      righe = list(csv.DictReader(f))
    
    da_rimuovere = [s["id"] for s in validati if not all(v for v in s.values())]
    
    righe_filtrate = [r for r in righe if r["id"] not in da_rimuovere]
    
    with open(self.csv_file_name, "w", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=righe[0].keys())
      writer.writeheader()
      writer.writerows(righe_filtrate)
    
    return da_rimuovere
  
  
  def create_validi_json(self) -> list:
    """
    converti csv in json e salva come file .json in /data/output.
    inoltre ritorna studenti_json da passare a calc_stats.py
    """
    with open(self.csv_file_name, "r", encoding="utf-8") as f:
      da_convertire = csv.DictReader(f)
      studenti_json = [s for s in da_convertire]
    
    with open(self.json_file_name, "w", encoding="utf-8") as f:
      json.dump(studenti_json, f, indent=2)
    
    return studenti_json

