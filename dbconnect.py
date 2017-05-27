import MySQLdb


def connection():
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='ypsilon17',
        db='middlezation'
    )
    c = conn.cursor()
    return c, conn
