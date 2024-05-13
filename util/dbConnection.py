import mysql.connector as sql


class DBConnection:
    @staticmethod
    def getconnection():
        host='localhost'
        database='ECOM'
        user='root'
        password='Harini2002'
        return host,database,user,password


class PropertyUtil:
    @staticmethod
    def getpropertystring():
        l=DBConnection.getconnection()
        conn=sql.connect(host=l[0],database=l[1],user=l[2],password=l[3])
        if conn.is_connected:
            print('DB is Connected')
        return conn


PropertyUtil.getpropertystring()



