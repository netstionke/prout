import mysql.connector

class dbJdr:
    connection = None

    def connect(self):
        if self.is_connected() == None:
            return self.get_connection()
        host = 'localhost'
        user = 'jdr'
        passwd = '18122001Bd-'

        for i in range(3):
            try:
                self.connection = mysql.connector.connect(host=host, user=user, password=passwd, database="jdr")
                return (self.connection)
            except:
                pass
        print("Connection to database failded !")
        return None

    def is_connected(self):
        if self.get_connection() == None:
            return False
        return True

    def get_connection(self):
        return self.connection

    def execute(self, command, dictionary=True, raw=False):
        if not self.is_connected():
            if self.connect() == None:
                print("execution db error")
                return None
        cursor = self.connection.cursor(dictionary=dictionary, raw=raw)
        #cursor.execute("USE odium;")
        cursor.execute(command)
        liste = []
        for i in cursor:
            liste.append(i)
            print(i)
        cursor.close()
        self.connection.commit()
        return liste
