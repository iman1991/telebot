import pymysql.cursors
import connection

connect = connection.connect()

def add_user(uid, uname):
    cursor = connect.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connect.close()
    if results is None or str(results['idT']) != str(uid):
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users (idT, name, score) values ( %i, '%s', %i)" % (uid, uname, 0))
        connect.commit()   
        cursor.close()
        connect.close()
        return True

def score(uid):
    cursor = connect.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connect.close()
    res = results["score"]
    return res