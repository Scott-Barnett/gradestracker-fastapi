from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

from local_config import local_config

if local_config["DATABASE"]["TYPE"] == "sqlite":
    engine = create_engine(f"sqlite:///{local_config['DATABASE']['PATH']}", connect_args={"check_same_thread": False})
else:
    print("That database configuration is not supported. Please edit the local_config.json and restart")
    exit(1)

LocalSession = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    full_name = Column(String(50))
    email_address = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(60))


Base.metadata.create_all(bind=engine)
