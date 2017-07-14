import pymysql.cursors
# infuser={"method":"", "param":{"idT":0, "idv":0, "score":100}}
# sock = socket.socket()

# sock.connect(('127.0.0.1', 8080))


def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection