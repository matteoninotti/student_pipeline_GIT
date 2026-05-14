import os
import json
from statistics import mean, median, stdev
from logic.ETL import now_time
from logic.gen_students import Corso
from state import PROJECT_PATH



class Stats_calculator:
  def __init__(self, corso: Corso, studenti_json: list) -> None:
    self.subjects = corso.MATERIE
    self.classe = corso.CLASSE
    self.n_studenti = corso.N_STUDENTI
    self.studenti_json = studenti_json
    self.txt_file_name = os.path.join(PROJECT_PATH, "report", f"report_{now_time}.txt")
    # crea una lista di liste contenente i voti per ogni studente
    self.voti_studenti = [] 
    for studente in self.studenti_json:
      voti_studente = [studente[subj] for subj in self.subjects]
      self.voti_studenti.append([int(v) for v in voti_studente]) # cast da str ad int


  def calc_stats_corso(self) -> dict:
    # raggruppa i voti in una lista di tuple, una per ogni materia
    voti = list(zip(*self.voti_studenti))
    
    # calcola stats per ogni materia
    stats = {}
    for voti_subj in voti:
      stats_subj = {
        "media": mean(voti_subj),
        "mediana": median(voti_subj),
        "dev. standard": stdev(voti_subj),
        "voto minimo": min(voti_subj),
        "voto massimo": max(voti_subj)
      }
      stats.update({
        self.subjects[voti.index(voti_subj)]:stats_subj
      })
    
    return stats
  
  
  def calc_stats_studenti(self) -> list:
    stats = []
    #associa ai voti l'id corrispondente dello studente
    for studente, self.voti_studente in zip(self.studenti_json, self.voti_studenti): 
      stats_studente = {
        "id": studente["id"],
        "nome": studente["nome"],
        "cognome": studente["cognome"],
        "media": mean(self.voti_studente)
      }
      stats.append(stats_studente)
      
    return stats
  
  
  def calc_top5_studenti(self, stats_studenti: list) -> list:
    medie_top5 = sorted(stats_studenti, key = lambda stats: stats["media"], reverse=True)[:5]
    
    return medie_top5
  
  
  def create_report(self, da_rimuovere: list,
                    validation_errors: str,
                    stats_corso: dict,
                    stats_studenti: list,
                    top5_studenti: list) -> None:
    report = f"""report della classe: {self.classe}
generato in data e ora: {now_time}
studenti totali: {self.n_studenti}
record validi: {self.n_studenti - len(da_rimuovere)}

\\/------- errori di validazione -------\\/

{validation_errors}

\\/------- studenti non validi -------\\/

{json.dumps(da_rimuovere, indent=2)}

\\/------- statistiche corso -------\\/

{json.dumps(stats_corso, indent=2)}

\\/------- statistiche studenti -------\\/

{json.dumps(stats_studenti, indent=2)}

\\/------- top5 studenti -------\\/

{json.dumps(top5_studenti, indent=2)}
    """
    
    with open(self.txt_file_name, "w", encoding="utf-8") as f:
      f.write(report)

