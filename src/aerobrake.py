# References:
# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
import sqlite3
sqlite_file = 'aerobrake.sqlite'

def add_one(data):
    return data + 1

def duplicate(data):
    return [data]*2

def pick_first(data):
    return data[0]

def interpolate(data):
    return [(data[i]+data[i+1])/2. for i in range(len(data))[:-1]]

def add_column(db,table,column):
    # Adds `column` to `table`. Creates `table` if necessary.
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE {tn} ({nf} {ft})'.format(
                        tn=table, nf=column, ft='INTEGER'))
    except:
        print 'Table {f} already exists. Adding column.'.format(f=table)
        try:
            c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(
                                    tn=table, cn='output', ct='INTEGER'))
        except:
            print 'Column {c} already exists.'.format(c=column)
    conn.commit()
    conn.close()
    return

def add_columns(db,table,columns):
    # Add several `columns` to `table`. Creates `table` if necessary.
    for column in columns:
        add_column(db,table,column)
    return

def add_data(db,table,columns,data):
    add_columns(db,table,columns)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO {tn} ({c}) VALUES ({d})".format(tn=table,c="'"+"','".join(columns)+"'",d=str(data)[1:-1]))
    conn.commit()
    conn.close()
    return

def aerobrake(f,data,db):
    # Save the input
    # Save the output
    out = f(data)
    print '{f}:{d}->{o}'.format(f=f.__name__,d=data,o=out)
    add_data(db,f.__name__,['input','output'],[data,out])
    return

aerobrake(add_one,1,sqlite_file)

#aerobrake(duplicate,1,sqlite_file)

#aerobrake(pick_first,[1,1],sqlite_file)

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute('SELECT * FROM {tn}'.format(tn='add_one'))
all_rows = c.fetchall()
print all_rows
conn.close()
