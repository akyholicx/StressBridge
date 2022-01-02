import sqlite3

con = sqlite3.connect("data.db",check_same_thread=False) #connect to database if exists, otherwise create "data.db"
c = con.cursor() # cursor object


def create(table_name,**kwargs):   # creates a new table in game.db, kwargs is a dictionary that contains key=<column name> value=<SQL data type>
    '''
        examples:
            create("playerdata",name="TEXT",hp="INTEGER")
        or
            columns = {"name":"TEXT", "hp":"INTEGER"}
            create("playerdata",**columns)
    '''
        
    c.execute(f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ") #checking for table

    
    if c.fetchone()[0]== 0: # if number of tables is 0 (table does not exist), create table
        if len(kwargs) > 0:
            msg = f"CREATE TABLE {table_name} " 
            cols = ""
            for k,v in kwargs.items():
                cols += f"{k} {v}, "
            cols = f"({cols[:-2]})"
            print(f"{msg}{cols}")
            c.execute(f"{msg}{cols};")
        else:
            print(f"Table {table_name} cannot be created (no columns specified)")

    else:
        print(f"Table {table_name} already exists")
    
    con.commit()

def drop(table_name):   # delete table of name "table_name" from game.db
    
    c.execute(f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ") #checking for table
    if c.fetchone()[0]:
        c.execute(f"DROP TABLE {table_name}")
        con.commit()
        print(f"Table {table_name} suceessfully dropped")

    else:
        print(f"Table {table_name} not found")

    con.commit()


def fetch(table_name, count=0, delete=False): # returns UP TO count rows from table_name as a list of dictionaries, if count == 0 it returns all rows, delete=True will delete those rows from table_name

    lst = []
    limit_query = "" if not count else f"LIMIT {count}"
    query = f"SELECT * FROM {table_name} {limit_query}"
    query2 = f"DELETE FROM {table_name} {limit_query}"
    #print(query)
    #print(query2)

    rows = c.execute(query)

    for row in rows:
        d = {}
        for i in range(len(rows.description)):
            k,v = rows.description[i][0], row[i]
            d[k] = v
        lst.append(d)

    c.execute(query2) if delete else None
    con.commit()
    return lst


def insert(table_name,**kwargs): # inserts new row into table_name, with kwargs being a dictionary (key=<column name>, value=<cell data>)

    '''
        examples:
            insert("playerdata",name="jon",hp=6)
        or
            columns = {"name":"jon", "hp":6}
            insert("playerdata",**columns)
    '''

    cols = ""
    vals = ""
    for k,v in kwargs.items():
        cols += k + ", "
        vals += f"'{v}'" + ", "
    cols = f"({cols[:-2]})"
    vals = f"({vals[:-2]})"
    c.execute(f"INSERT INTO {table_name} {cols} VALUES {vals}")
    con.commit()

def update(table_name, column, where_clause, **kwargs): # updates all rows in table_name, whenever cell value of specified column matches where_clause (SEARCHING ONLY WORKS FOR TEXT TYPE)

    '''
        examples:
            update("playerdata","name","jon",hp=5)
        or
            columns = {"hp":5}
            update("playerdata","name","jon",**columns)
    '''

    set_query = ""
    where_query = f"WHERE {column}='{where_clause}'"

    for k,v in kwargs.items():
        set_query += f"{k}='{v}', "
    set_query = f"{set_query[:-2]}"
    query = f"UPDATE {table_name} SET {set_query} {where_query}"
    print(query)
    c.execute(query)
    con.commit()



def deleteall(table_name): # deletes ALL rows from the table

    query = f"DELETE FROM {table_name}"
    print(query)
    c.execute(query)
    con.commit()

'''
params = {"pname":"TEXT", "password":"TEXT", "points":"INTEGER"}
drop("players")
create("players",**params)
insert("game", **{"pname":"jon", "hp":6})
insert("game", **{"pname":"jon2", "hp":5})
insert("game", **{"pname":"jon3", "hp":4})
insert("game", **{"pname":"jon4", "hp":3})
insert("game", **{"pname":"jon5", "hp":2})
#update("game","pname","jon", **{"hp":5})
#deleteall("game")
con.commit()
l = fetch("game",1,True)
print(l)
l = fetch("game")
print(l)
'''
