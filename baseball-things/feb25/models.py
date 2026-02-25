from sqlmodel import SQLModel, create_engine, Field

#make the table and database

#setup the structure of the table
class Faculty(SQLModel, table=True):
    id: int | None = Field(default = None, primary_key = True)
    first_name: str
    last_name: str
    age: int | None = None

#make the actual database
engine = create_engine('sqlite:///department.db')

#access all the metadata and create the specified database
SQLModel.metadata.create_all(engine) 