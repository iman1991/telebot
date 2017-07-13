import pymysql.cursors
import connection



def add_user(uid, uname):
    connect = connection.connect()
    cursor = connect.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connect.close()
    if results is None or str(results['idT']) != str(uid):
        connect = connection.connect()
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users (idT, name, score) values ( %i, '%s', %i)" % (uid, uname, 0))
        connect.commit()   
        cursor.close()
        connect.close()
        return True

def score(uid):
    connect = connection.connect()
    cursor = connect.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connect.close()
    res = results["score"]
    return res