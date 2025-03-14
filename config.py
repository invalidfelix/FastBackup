# Locations to back up
backup_dirs = ["/home"]

# Exclude files or directories from backup
exclude = ["__pycache__", "venv"]

# location to final backup
backup_location = "/media/backup"

# File name for final backup
backup_name_format = "%date%_%backup_name%"

# Date format for file name
date_format = "%d-%m-%Y_%H-%M-%S"

# clear old backups
clear_backups = True

# MySQL backup
mysql_backup = False
mysql_user = "root"
mysql_password = ""