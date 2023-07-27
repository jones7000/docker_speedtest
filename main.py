import re
import subprocess
import time
import mysql.connector

# interval in MIN
interval = 15*60

# database host:
host = "server_laptop"

# database
sqlHost = "192.168.1.199"
sqlUser = "user"
sqlPass = "jonas123"
sqlPort = "6033"




# speedtest, returns array with [ping, download, upload]
def speedtest():
    # open speedtest-cli
    print("speedtest")
    try:
        response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
    except:
        data = 3
        return data

    response = response.decode("utf-8")
    ping = re.findall(r'Ping:\s(.*?)\s', response, re.MULTILINE)
    download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
    upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

    # new array to return as: ping(0),down(1),up(2)
    if ping and download and upload:
        data = ['','','']
        data[0] = ping[0].replace(',', '.')
        data[1] = download[0].replace(',', '.')
        data[2] = upload[0].replace(',', '.')
    else:
        data = 0

    return data

# Insert DATA to SQL database
def sqlInsert(speedData):
    print("sqlInsert")
    try:
        mydb = mysql.connector.connect(
            host=sqlHost,
            user=sqlUser,
            password=sqlPass,
            port=sqlPort,
        )
    except:
        return 0

    if mydb:
        mycursor = mydb.cursor()
        sql = "INSERT INTO home.speedtest (host, ping, download, upload) VALUES (%s, %s, %s, %s)"
        val = (host, speedData[0], speedData[1], speedData[2])

        # Executing the SQL command
        mycursor.execute(sql, val)
        mydb.commit()
        # Commit your changes in the database
        print(mycursor.rowcount, "record inserted.")
        # Closing the connection
        mycursor.close()

def main():
    while True:
        starttime = time.time()
        data = speedtest()
        sqlInsert(data)
        time.sleep(interval - ((time.time() - starttime) % interval))


if __name__ == "__main__":
    main()