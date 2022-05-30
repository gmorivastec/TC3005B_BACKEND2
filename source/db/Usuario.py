from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

# instala con pip sqlalchemy
# también ibm_db_sa
Base = declarative_base()

# intención de ORM 
# mappear renglones de una DB a objetos
class Usuario(Base):
    # agregamos los campos donde se mapearan las columnas de la db
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(150))
    password = Column(String(100))
    token = Column(String(100))
    last_date = Column(Integer)