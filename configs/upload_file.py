import os

class upload_file:

  dir="upload"

  def define_dir(self):
    if not os.path.isfile(f"public/{self.dir}"):
      os.makedirs("public/upload")

  def run(self):
    self.define_dir()