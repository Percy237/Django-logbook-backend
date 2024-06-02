from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Backup PostgreSQL database"

    def handle(self, *args, **kwargs):
        # PostgreSQLBackup instance initialization
        database_name = "logbook"
        username = "percy"
        password = "mypassword"
        output_file = "db_backup"
        backup = PostgreSQLBackup(database_name, username, password, output_file)

        # Execute backup
        backup.backup()


class PostgreSQLBackup:
    def __init__(self, database, username, password, output_file):
        self.database = database
        self.username = username
        self.password = password
        self.output_file = output_file

    def backup(self):
        # Set the PGPASSWORD environment variable
        os.environ["PGPASSWORD"] = self.password

        # Construct the command string
        command = (
            f"pg_dump -U {self.username} -d {self.database} "
            f"-Fc -f {self.output_file}"
        )

        # Execute the command using os.system
        os.system(command)
