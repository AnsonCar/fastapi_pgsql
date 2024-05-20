from sqlmodel import Session, SQLModel, create_engine
from setting import get_url


# sqlite_file_name = "database.db"
# db_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(
#     db_url,
#     echo=True,
#     connect_args=connect_args,
# )

engine = create_engine(get_url())  # , echo=True


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
