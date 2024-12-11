from datetime import date
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
    query ="SELECT * FROM guests"
    if len(params) > 0:
      query += " WHERE "
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
      GROUP BY month_year
      ORDER BY created_at ASC
    """
    cursor.execute(query)
    result=cursor.fetchall()
    return result