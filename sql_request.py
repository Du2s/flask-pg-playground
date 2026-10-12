import psycopg2

class ReqHandler():
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def modify_table(self):
        pass

    def query(self, user_query:str):
        res = []
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
                )       
            with conn.cursor() as cursor:
                cursor.execute(user_query)
                header = [desc[0] for desc in cursor.description]
                res.append(header)
                for line in cursor:
                    res.append(line)
        except Exception as error:
            print(f"Error {error}")

        finally:
            if conn:
                conn.close()
            return res


