from media_db import init_db, DB_PATH
import os

print("Expecting DB to be created at:", os.path.abspath(DB_PATH))
init_db()

# Check if it actually exists after calling init_db
if os.path.isfile(DB_PATH):
    print("Success: Database file created.")
else:
    print("❌ Database file was NOT created.")
