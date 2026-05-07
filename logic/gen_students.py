import json
from faker import Faker
from datetime import datetime, date
from random import randint
from state import DATA_PATH


fake = Faker("it_IT")

class Studente:
  """
  studente di cui genereremo i dati con faker
  """
  def __init__(self, id:int, nome:str, cognome:str,
              data_nascita:datetime | date, email:str, voti:dict):
    self.id = id
    self.nome = nome
    self.cognome = cognome
    self.data_nascita = data_nascita
    self.email = email
    self.voti = voti

  def to_dict(self) -> dict:
    """
    converte l'istanza di Studente in un dict
    """
    return {
      "id": self.id,
      "nome": self.nome,
      "cognome": self.cognome,
      "data_nascita": self.data_nascita.isoformat(),
      "email": self.email,
      "voti": self.voti
    }

  @staticmethod
  def gen_random_student(id:int, materie:list,
                        voto_min:int, voto_max:int) -> dict:
    """
    genera studenti random con Faker e li ritorna come dict.
    genera alcuni degli studenti con valori non validi x test
    """
    if id == randint(1, Corso.N_STUDENTI): # genera studenti con valori non validi
      nome = fake.first_name()
      cognome = fake.last_name()
      data_nascita = datetime.now()
      email = f"{nome.lower()}.{cognome.lower()}@scuola"
      voti = {materia: randint(1,40) for materia in materie}
    
    else: # genera studenti VALIDI
      nome = fake.first_name()
      cognome = fake.last_name()
      data_nascita = fake.date_of_birth(minimum_age=18, maximum_age=38)
      email = f"{nome.lower()}.{cognome.lower()}@scuola.it"
      voti = {materia: randint(voto_min, voto_max) for materia in materie}
    
    return Studente(
      id=id,
      nome=nome,
      cognome=cognome,
      data_nascita=data_nascita,
      email=email,
      voti=voti
    ).to_dict()



with open(DATA_PATH, "r", encoding="utf-8") as f:
  corso = json.load(f)

class Corso:
  """
  config iniziale del corso.
  modificare config.json per cambiare gli attributi del corso
  """
  N_STUDENTI = corso["numero_studenti"]
  VOTO_MIN = corso["voto_min"]
  VOTO_MAX = corso["voto_max"]
  MATERIE = corso["materie"]
  CLASSE = corso["classe"]
  
  def gen_studenti_corso(self):
  # genera studenti tenendo in considerazione le specifiche di config.json
    return [
      Studente.gen_random_student(
        i+1, self.MATERIE,
        self.VOTO_MIN, self.VOTO_MAX
      )
      for i in range(self.N_STUDENTI)
    ]
