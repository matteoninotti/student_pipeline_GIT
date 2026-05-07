from statistics import mean, median, stdev
import json
from logic.ETL import now_time
from state import PROJECT_PATH


class Stats_calculator:
  def __init__(self, corso, etl):
    self.subjects = corso.MATERIE
    self.studenti_json = etl.create_validi_json()
    # crea una lista di liste contenente i voti per ogni studente
    voti_studenti = [] 
    for studente in self.studenti_json:
      voti_studente = [studente[subj] for subj in self.subjects]
      voti_studenti.append([int(v) for v in voti_studente]) # cast da str ad int
    print(voti_studenti)





  # def calc_stats_corso(self, voti_studenti: list) -> dict:
  #  # raggruppa i voti in una lista di tuple, una per ogni materia
  #  voti = list(zip(*voti_studenti))
  #  
  #  # calcola stats per ogni materia
  #  stats = {}
  #  for voti_subj in voti:
  #    stats_subj = {
  #      "media": mean(voti_subj),
  #      "mediana": median(voti_subj),
  #      "dev. standard": stdev(voti_subj),
  #      "voto minimo": min(voti_subj),
  #      "voto massimo": max(voti_subj)
  #    }
  #    stats.update({
  #      subjects[voti.index(voti_subj)]:stats_subj
  #    })
#
  #  return stats
#
#
  ##print(calc_stats_corso(voti_studenti))
#
#
#
  # def calc_stats_studenti(voti_studenti: list) -> list:
  #  stats = []
  #  #associa ai voti l'id corrispondente dello studente
  #  for studente, voti_studente in zip(studenti_json, voti_studenti): 
  #    stats_studente = {
  #      "id": studente["id"],
  #      "nome": studente["nome"],
  #      "cognome": studente["cognome"],
  #      "media": mean(voti_studente)
  #    }
  #    stats.append(stats_studente)
  #    
  #  return stats
#
#
  ##print(calc_stats_studenti(voti_studenti))
#
#
#
  #def calc_top5_studenti() -> list:
  #  stats = calc_stats_studenti(voti_studenti)
  #  medie_top5 = sorted(stats, key = lambda stats: stats["media"], reverse=True)[:5]
  #  
  #  return medie_top5
#
#
#
  #txt_file_name = PROJECT_PATH + "report/report_" + now_time + ".txt"
#
  #def create_report():
  #  report = f"""report della classe: {Corso_studenti.CLASSE}
  #generato in data e ora: {now_time}
  #studenti totali: {Corso_studenti.N_STUDENTI}
  #record validi: {Corso_studenti.N_STUDENTI - len(da_rimuovere)}
  #{count_validation_errors(validati)}
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
  #**statistiche classe**
#
  #{json.dumps(calc_stats_corso(voti_studenti), indent=2)}
#
#
  #**statistiche per studente**
#
  #{json.dumps(calc_stats_studenti(voti_studenti), indent=2)}
#
#
  #**top 5 studenti**
#
  #{json.dumps(calc_top5_studenti(), indent=2)}
  #  """
  #  
  #  with open(txt_file_name, "w", encoding="utf-8") as f:
  #    f.write(report)
#
#
#create_report()