
import pyodbc
import os
from src.logger_ga import writeLog
from dotenv import load_dotenv

load_dotenv()

DRIVER = os.environ.get('DRIVER')
SERVER = os.environ.get('SERVER')
DATABASE = os.environ.get('DATABASE')
UID = os.environ.get('UID')
PSWD = os.environ.get('PSWD')

class Connect():

    def __init__(self):
        self.driver = DRIVER
        self.server = SERVER
        self.database = DATABASE
        self.uid = UID
        self.pwd = PSWD

    def connection(self):
        try: 
            return pyodbc.connect(
                driver = self.driver,
                server = self.server,
                database = self.database,
                uid = self.uid,
                pwd = self.pwd
            )
        except Exception as e:
            writeLog(e).write_log()

    def orderParamsToExecProc(self, paramsToBeProcessed):
        array = []

        for chaveExterna, valoresE in paramsToBeProcessed['urls'].items():
            for chave, valor in valoresE.items():
                array.append([chaveExterna, chave, valor])

        return array

    def executeProc(self, procName, procParams):

        params = self.orderParamsToExecProc(procParams)

        try:
            con = self.connection()
            cursorTest = con.cursor()
            cursorTest.execute("EXEC "+ procName +" ?", [params])
            con.commit()
            
        except Exception as e:
            writeLog(e).write_log()
            print(e)

        finally:
            con.close()
