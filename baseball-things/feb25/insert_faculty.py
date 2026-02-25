from sqlmodel import Session
from models import Faculty, engine

#prep entries to be added to the Faculty table
#(using the faculty table as the template to set up the entry)
f1 = Faculty(first_name = 'Christopher', last_name = 'Mansour')
f2 = Faculty(first_name = 'Mahesh', last_name = 'Maddumala')
f3 = Faculty(first_name = 'Chad', last_name = 'Redmond', age = 60)

#connect to the "engine" database
with Session(engine) as session:
    session.add(f1)
    session.add(f2)
    session.add(f3)
    session.commit()

