import csv

def read():
    with open('restore-real-coffee.csv') as local_csv:
        local_reader = csv.reader(local_csv)
        next(local_reader)
        with open('restore-coffee-server-production.csv') as server_csv:
            server_reader = csv.reader(server_csv)
            next(server_reader)

            with open('repair-data.sql', 'w') as sql_file:

                for local_row in local_reader:
                    print(local_row)
                    server_row = next(server_reader)
                    print(server_row)

                    new_row = transform(local_row, server_row)
                    if new_row[5] == "2":
                        # skip unchanged
                        print("\n")
                        continue
                    sql = "UPDATE coffee.protokoll SET Value = {}, Kommentar = '{}', ActionID = {} WHERE id = {};".format(
                        new_row[3], new_row[4], new_row[5], new_row[0]
                    )
                    print(sql)
                    sql_file.write(sql + "\n")
                    print("\n")



def transform(local_row, server_row):
    if local_row[3] == "1" and local_row[4] == "0":
        # coffee without milk
        server_row[3] = "-20"
        server_row[4] = "Buy (rfid) Black Coffee"
        server_row[5] = "1"
    elif local_row[3] == "0":
        # hot water
        server_row[3] = "-1"
        server_row[4] = "Buy (rfid) Hot Water"
        server_row[5] = "3"
    return server_row

if __name__ == "__main__":
    read()