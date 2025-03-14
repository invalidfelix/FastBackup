import os
import time
from sys import platform

import config
from logger import logger

date = time.strftime(config.date_format)
logger = logger("backup.log")

def os_check():
    """Check if script is running on a unix based operation system"""
    if platform.startswith("linux") or platform.startswith("darwin"):
        return True
    else:
        return False
    
def mysql_backup():
    logger.log("INFO", "Starting backup for MySQL database...")
    tmp_check = os.system(f"cd {config.backup_location}")
    if tmp_check == 0:
        mysql_backup_file_name = f"{get_file_name('mysql_backup')}.sql"
        create_backup = os.system(
            f"cd {config.backup_location} && mysqldump -u {config.mysql_user} -p '{config.mysql_password}'"
            f" --all-databases > {mysql_backup_file_name}"
        )
        if create_backup == 0:
            logger.log("SUCCESS", "MySQL database backup created successfully")
        else:
            logger.log("ERROR", "MySQL database backup failed")
            os.system(f"cd {config.backup_location} && rm {mysql_backup_file_name}")
    else:
        logger.log("ERROR", "Mount not exits")

def backup():
    logger.log("INFO", f"Starting backup for {len(config.backup_dirs)} directories...")
    if len(config.backup_dirs) == 0:
        logger.log("ERROR", "No directories to backup")
    else:
        exclude_str = ""
        for file in config.exclude:
            exclude_str += f"--exclude '{file}' "
        
        for index, folder in enumerate(config.backup_dirs):
            backup_file_name = get_file_name(f"backup{index + 1}.tar.gz")
            logger.log("INFO", f"Starting backup for {folder}...")
            status = os.system(
                f"cd {config.backup_location} && tar {exclude_str}-czf {backup_file_name} {folder}"
            )
            if status == 0:
                logger.log("SUCCESS", f"Backup for {folder} created successfully")
            else:
                logger.log("ERROR", f"Backup for {folder} failed")

def clear_backups():
    logger.log("INFO", "Cleaning backup dirs...")
    for file in os.listdir(config.backup_location):
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            os.rmdir(file)
        else:
            logger.log("ERROR", f"Failed to delete {file}")
        
    logger.log("SUCCESS", "Backup dirs cleaned successfully")
    
def get_file_name(name):
    file_name = config.backup_name_format
    file_name = file_name.replace("%date%", date)
    file_name = file_name.replace("%backup_name%", name)
    logger.log("INFO", f"File name created: {file_name}")
    return file_name

if os_check():
    if os.path.exists(config.backup_location):
        if config.clear_backups:
            clear_backups()
        if config.mysql_backup:
            mysql_backup()
        backup()
    else:
        logger.log("ERROR", "Failed to create backup")
        logger.log("ERROR", f"{config.backup_location} does not exist")
else:
    logger.log("ERROR", "This script is only for Linux or MacOS")
    
logger.close_file()