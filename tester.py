import io
import math
import pandas as pd

def clean_csv(input_stream):
    """
    :param input_stream: (StringIO) An in-memory stream for text I/O containing CSV data
    :returns: (String) A string containing CSV data
    """
    return pd.read_csv( input_stream )

def dumpAry( ary ) :
    print("-"*(9*3-2))
    for r in range(0,len(ary)):
        for c in range(0,len(ary[r])):
            if (c % 3)==0 :
                print("| ", end="")
            c1 = ary[r][c]
            print( c1, end =" " )
        print("|")
        if ((r+1) % 3)==0 :
            print("-"*(9*3-2))


input_stream = io.StringIO("a,b,c,d,e,f,g,h,i\n0,9,0,2,0,4,0,3,0\n0,0,0,0,1,0,0,0,7\n0,0,2,0,0,0,0,4,0\n0,1,5,0,0,6,4,0,3\n0,8,0,0,0,0,0,7,0\n4,0,7,3,9,0,2,5,0\n0,4,0,0,0,0,8,0,0\n5,0,0,0,8,0,0,0,0\n0,7,0,1,0,2,0,6,0\n")
result_csv = clean_csv(input_stream)
input_stream.close()


ary = result_csv.values 
ary2 = []
for i in range(0,9):
    ary2.append( [1,2,3,4,5,6,7,8,9] )
print(ary)
for r in range(0,9):
    print( r )
    for c in range(0,9):
        c1 = ary[r][c]
        if ( math.isnan(c1)):
            c1 = 0
        else:
            c1 = int(c1)
        ary2[r][c] = str(c1)
dumpAry( ary2 )
# SELECT customers.name, count(transactions.customerId)
# FROM customers
#              left JOIN transactions
#                         ON customers.id = transactions.customerId
# GROUP BY customers.name


# create table menuitems (
#      id integer not null primary key ,
#      title varchar(30) not null, 
#      url varchar(100) not null ,
#      UNIQUE( url )
#      );


# Time to market , mean time to change

