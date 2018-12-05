import ftplib
import time

while True:
    ftp = ftplib.FTP("10.31.31.1")
    ftp.login("vkbot", "vkbot13042000")
    ftp.retrbinary("RETR Users19.xml", open('Users19.xml', 'wb').write)
    ftp.retrbinary("RETR Users19.xml", open('Users10.xml', 'wb').write)
    ftp.retrbinary("RETR Users19.xml", open('Users61.xml', 'wb').write)
    time.sleep(20)
