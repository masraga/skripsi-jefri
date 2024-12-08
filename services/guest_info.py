from repositories.guest_repo import guest_repo

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