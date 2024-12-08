class guest_repo:

  guest_table="guests"

  face_table="guest_faces"

  username=""

  faces=[]
  
  db=None

  def __init__(self, db):
    self.db = db
  
  def create(self, username, faces, face_id):
    cursor = self.db.cursor()
    
    guest_sql = "INSERT INTO guests (name, is_active, face_id) VALUES ( %s, %s, %s )"
    guest_val = (username, "1", face_id)
    cursor.execute(guest_sql, guest_val)
    self.db.commit()
    guest_id = cursor.lastrowid

    for face in faces:
      face_sql = "INSERT INTO guest_faces SET guest_id=%s, face=%s, is_active=%s"
      face_val = (guest_id, face, 1)
      cursor.execute(face_sql, face_val)
      self.db.commit()

    return True
    