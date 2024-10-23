import sqlite3 as sq

DATABASE = 'database.db'


def connect_db():
    return sq.connect(DATABASE)


def create_db():
    connection = connect_db()
    cursor = connection.cursor()
    scheme_script = ("CREATE TABLE IF NOT EXISTS Wallet ("
                     "uuid INTEGER PRIMARY KEY,"
                     "balance NUMERIC NOT NULL"
                     ");")
    cursor.executescript(scheme_script)
    connection.commit()
    cursor.close()
    connection.close()


def insert_data(items: list):
    with connect_db() as con:
        cursor = con.cursor()
        cursor.executemany("INSERT INTO Wallet VALUES(?, ?)", items)
        con.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


async def get_balance(uuid=None):
    my_list = []
    connection = connect_db()

    sql = f"SELECT * FROM Wallet WHERE uuid = {uuid}"

    try:
        cursor = connection.execute(sql)
        cursor.row_factory = dict_factory
        for row in cursor:
            record = {
                'uuid': row.get('uuid'),
                'balance': row.get('balance')
            }
            my_list.append(record)

    except connection.Error as error:
        print("Error connection to database", error)
    finally:
        if connection:
            connection.close()

    return my_list


async def update_balance(uuid: int, operation: str, amount: int):
    balance = (await get_balance(uuid))[0]["balance"]
    if operation == "WITHDRAW":
        if balance > amount:
            sql = f"UPDATE Wallet SET balance = {balance - amount} WHERE uuid = {uuid}"
            with connect_db() as con:
                con.cursor().execute(sql)
                con.commit()
            return f"Withdraw successful. Now balance = {(await get_balance(uuid))[0]["balance"]}", 200
        return "Insufficient funds", 103
    elif operation == "DEPOSIT":
        sql = f"UPDATE Wallet SET balance = {balance + amount} WHERE uuid = {uuid}"
        with connect_db() as con:
            con.cursor().execute(sql)
            con.commit()
        return f"Deposit successful. Now balance = {(await get_balance(uuid))[0]["balance"]}", 200

