import os
import shutil
try:
	os.remove('Django/db.sqlite3')
except OSError:
	pass
shutil.rmtree('Django/przyciski/migrations', ignore_errors=True)
