#importing librarieis
import tqdm
import os
import psycopg2 as db
from faker import Faker
import socket




#Generating fake data for the data base
fake = Faker()
data1 = []
for r in range(5000):
    data1.append((fake.name(),fake.ssn(),fake.pricetag(),fake.bban(),fake.iban(),fake.credit_card_number(),fake.credit_card_security_code(),fake.credit_card_expire(),fake.random_int(0,1)))

data_for_db=tuple(data1)
print(data_for_db)


#Making database connection
conn = db.connect(host="localhost", dbname='postgres' , user="postgres",password="user",port=5432)
cur=conn.cursor()
query = "insert into users (client_name, ssn,monthly_salary, bban, iban, credit_card_number, credit_card_sc, credit_card_expiry_date, in_dept) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cur.executemany(query,data_for_db)
conn.commit()
with open('DataBase.csv', 'w') as file:
    cur.copy_to(file,'users', sep = ',')
conn.close()




#Raspberry PI connection
SEPARATOR = "<SEPERATOR>"
BUFFER_SIZE = 2404404
#host = '172,18,3,176'
host = '192.168.1.159'
port = 5001

filename = "DataBase.csv"
filesize = os.path.getsize(filename)

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")


s.send(f"{filename}{SEPARATOR}{filesize}".encode())



progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filename, "rb") as f:
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break


    
    s.sendall(bytes_read)

    progress.update(len(bytes_read))


s.close




