import pymysql.cursors

def connect_shluz():
    try:
        sock = socket.socket()
        return sock.connect(("194.67.217.180", 8080))
    except:
        sock = socket.socket()
        return sock.connect(("194.67.217.180", 9090))

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection