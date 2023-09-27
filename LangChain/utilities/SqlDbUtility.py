import os
from langchain.sql_database import SQLDatabase

class SqlDbUtility:
    def __init__(self):
        SQL_DB_USER = os.environ["SQL_DB_USER"]
        SQL_DB_PASSWORD = os.environ["SQL_DB_PASSWORD"]
        SQL_DB_SERVER_NAME = os.environ["SQL_DB_SERVER_NAME"]
        SQL_DB_NAME = os.environ["SQL_DB_NAME"]
        SQL_CONNECTIONSTRING_FORMAT = os.environ["SQL_CONNECTIONSTRING_FORMAT"]

        # Initialize
        connection_string = SQL_CONNECTIONSTRING_FORMAT.format(
            database_user=SQL_DB_USER,
            database_password=SQL_DB_PASSWORD,
            database_server=SQL_DB_SERVER_NAME,
            database_db=SQL_DB_NAME)

        self.db = SQLDatabase.from_uri(connection_string)

    # Functions
    def ExecDBStoredProcedure(self, stored_procedure_name, *args, schema='dbo'):
        sql_string = "exec [{schema}].[{stored_procedure_name}] ".format(schema=schema, stored_procedure_name=stored_procedure_name)
        for i in range(0, len(args), 2):
            param_name = args[i]
            param_value = args[i+1]
            sql_string += "@{param_name}='{param_value}', ".format(param_name=param_name, param_value=param_value)
        sql_string = sql_string[:-2]

        return self.db._execute(sql_string)

    def ExecDBStoredProcedureStrResult(self, stored_procedure_name, *args, schema='dbo'):
        result = self.ExecDBStoredProcedure(stored_procedure_name, *args, schema=schema)
        return str(result)

    def ExecDBScalar(self, stored_procedure_name, *args, schema='dbo'):
        result = self.ExecDBStoredProcedure(stored_procedure_name, *args, schema=schema)
        return str(result[0][0])