import mysql.connector


def phishing(url):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="arulkumaran",
            password='6170',
            database='arulkumaran'
        )
        cursor = db.cursor()
        cursor.execute(f"insert into phishingurls values('{url}');")
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(e)


def getPhishURLS():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="arulkumaran",
            password='6170',
            database='arulkumaran'
        )
        cursor = db.cursor()
        cursor.execute("select * from phishingurls;")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        return data
    except Exception as e:
        print(e)