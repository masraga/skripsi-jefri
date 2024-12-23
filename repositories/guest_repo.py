import os
from datetime import date, datetime
class guest_repo:

  guest_table="guests"

  face_table="guest_faces"

  username=""

  faces=[]
  
  db=None

  def __init__(self, db):
    self.db = db
  
  def create(self, username, faces, face_id, gender):
    cursor = self.db.cursor()
    
    guest_sql = "INSERT INTO guests (name, is_active, face_id, created_at, gender) VALUES ( %s, %s, %s, %s, %s )"
    guest_val = (username, "1", face_id, date.today(),gender)
    cursor.execute(guest_sql, guest_val)
    self.db.commit()
    guest_id = cursor.lastrowid

    for face in faces:
      face_sql = "INSERT INTO guest_faces SET guest_id=%s, face=%s, is_active=%s"
      face_val = (guest_id, face, 1)
      cursor.execute(face_sql, face_val)
      self.db.commit()

    return True

  def get_list(self, params={}):
    cursor = self.db.cursor(dictionary=True)
    query ="SELECT * FROM guests WHERE is_active=1"
    if len(params) > 0:
      query += " AND "
      if 'id' in params:
        query += f"id={params['id']}"
      if 'face_id' in params:
        query += f"face_id='{params['face_id']}'"
    
    cursor.execute(query)
    result = cursor.fetchall()
    self.db.commit()
    # self.db.close()
    return result
  
  def get_list_face(self, params={}):
    cursor=self.db.cursor(dictionary=True)
    query="SELECT * FROM guest_faces"
    if len(params) > 0:
      query += " WHERE "
      if 'guest_id' in params:
        query += f"guest_id={params['guest_id']}"
    cursor.execute(query)
    result=cursor.fetchall()
    return result
  
  def get_yearly_user_total(self):
    cursor=self.db.cursor(dictionary=True)
    query="""
      SELECT 
        concat(year(created_at),"-",month(created_at)) as month_year, 
        sum(1) as total
      FROM 
        guests 
      WHERE
        is_active=1
      GROUP BY month_year
      ORDER BY created_at ASC
    """
    cursor.execute(query)
    result=cursor.fetchall()
    return result
  
  def add_log(self, params={}):
    cursor=self.db.cursor()
    query="INSERT INTO guest_log_history (guest_id, log, created_at, is_active, accuracy) VALUES (%s, %s, %s, %s, %s)"
    query_value=(params["guest_id"], params["log"], datetime.now() , 1, params["accuracy"])
    cursor.execute(query, query_value)
    self.db.commit()

  def get_log(self, params={}):
    cursor=self.db.cursor(dictionary=True)
    query="SELECT * FROM guest_log_history"
    if len(params) > 0:
      query += " WHERE "
      if 'guest_id' in params:
        query += f"guest_id={params['guest_id']}"
    cursor.execute(query)
    result=cursor.fetchall()
    return result

  def delete_user(self, params={}):
    cursor=self.db.cursor()
    id=params['id']
    faces=self.get_list_face(params={"guest_id":id})
    for face in faces:
      print('[log] delete file', face['face'])
      os.remove(os.path.join("public/upload/", face['face']))
    query="UPDATE guests SET is_active=%s WHERE id=%s"
    val=("0",id)
    cursor.execute(query, val)
    self.db.commit()