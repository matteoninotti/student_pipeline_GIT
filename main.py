import os
import json
from sys import argv
from logic.gen_students import Corso
from logic.ETL import ETL
from logic.calc_stats import Stats_calculator
from state import PROJECT_PATH



def install_requirements() -> None:
  """verifica pacchetti installati e -dopo conferma user- installa se non presenti"""
  pass



def create_folders() -> str:
  """crea cartelle di lavoro se non esistenti"""
  os.chdir(PROJECT_PATH)
  f_list = os.listdir()
  if "report" not in f_list:
    os.mkdir("./report")
  if "data" not in f_list:
    os.mkdir("./data")
  
  os.chdir(os.path.join(PROJECT_PATH, "data"))
  f_list = os.listdir()
  if "input" not in f_list:
    os.mkdir("./input")
  if "output" not in f_list:
    os.mkdir("./output")
  if "backup" not in f_list:
    os.mkdir("./backup")
    
  os.chdir(PROJECT_PATH)
  
  return "cartelle di lavoro inizializzate correttamente"



class CLI:
  """
  definisce i comandi da terminale
  """
  # concettualmente no bello che report() chiami validate() ecc..
  # TROVARE ALTRO SISTEMA (instance attributes + file di persistenza)
  def __init__(self) -> None:
    self.studenti_corso = corso.gen_studenti_corso() # creazione random degli studenti
    self.etl = ETL(self.studenti_corso) # creazione istanza ETL
  
  
  def generate(self) -> None:
    print(f"generati {len(self.studenti_corso)} studenti")
    self.etl.create_students_csv()
    self.etl.bkup_csv()
  
  
  def validate(self) -> None:
    self.generate()
    self.validation_errors = self.etl.count_validation_errors()
    
    print("\n\\/------- errori di validazione -------\\/\n")
    print(self.validation_errors)
    self.da_rimuovere = self.etl.clean_scartati()
    
    print("\n\\/------- studenti non validi -------\\/\n")
    print(f"{json.dumps(self.da_rimuovere, indent=2)}")
    
    self.studenti_json = self.etl.create_validi_json()
  
  
  def report(self) -> None:
    self.validate()
    
    print("\n\\/------- statistiche corso -------\\/\n")
    # creaz istanza Stats_calculator passando self.studenti_json (= ret di self.etl.create_validi_json())
    self.calc = Stats_calculator(corso, self.studenti_json)
    self.stats_corso = self.calc.calc_stats_corso()
    print(f"{json.dumps(self.stats_corso, indent=2)}")
    
    print("\n\\/------- statistiche studenti -------\\/\n")
    self.stats_studenti = self.calc.calc_stats_studenti()
    print(f"{json.dumps(self.stats_studenti, indent=2)}")
    self.top5_studenti = self.calc.calc_top5_studenti(self.stats_studenti)
    
    print("\n\\/------- top5 studenti -------\\/\n")
    print(f"{json.dumps(self.top5_studenti, indent=2)}")
    
    self.calc.create_report(self.da_rimuovere,
                            self.validation_errors,
                            self.stats_corso,
                            self.stats_studenti,
                            self.top5_studenti)
  
  
  def all(self) -> None:
    self.generate()
    self.validate()
    self.report()
  
  
  def delete(self) -> None:
    # cancella cartelle di lavoro se esistono
    # + tutto il loro contenuto
    pass



def main() -> None:
  msg = create_folders()
  print(msg)
  global corso
  corso = Corso() # init del corso
  cli = CLI() # creazione istanza CLI
  cmd = argv[1] if len(argv) > 1 else ""
  
  # leggi il comando opzionale da terminale
  if cmd == "generate":
    cli.generate()
  elif cmd == "validate":
    cli.validate()
  elif cmd == "report":
    cli.report()
  elif cmd == "all":
    cli.all()
  else:
    cli.all()



if __name__ == "__main__":
  main()
