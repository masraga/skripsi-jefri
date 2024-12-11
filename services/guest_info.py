from repositories.guest_repo import guest_repo
from datetime import datetime
from dateutil import rrule

class guest_info:

  db=None

  def __init__(self,db):
    self.db = db

  def get_list_guest(self, params={}):
    new_guest_repo = guest_repo(self.db)
    guests = new_guest_repo.get_list(params)
    return guests
  
  def get_list_face(self, params={}):
    new_guest_repo=guest_repo(self.db)
    faces=new_guest_repo.get_list_face(params)
    return faces
  
  def get_yearly_user_total(self, params={}):
    new_guest_repo=guest_repo(self.db)
    overview=new_guest_repo.get_yearly_user_total()
    year=datetime.today().replace(month=1).strftime("%Y")
    month=12 
    i=1
    overview_dict={}
    while i <= month:
      overview_dict[f"{year}-{i}"]=0
      i += 1
    
    for o in overview:
      overview_dict[o["month_year"]]=o["total"]
    
    return {"label": list(overview_dict.keys()), "value": list(map(str, list(overview_dict.values())))}
  
  def add_log(self, params={}):
    new_guest_repo=guest_repo(self.db)
    return new_guest_repo.add_log(params)