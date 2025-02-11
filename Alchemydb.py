from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Database setup
Base = declarative_base()
engine = create_engine("sqlite:///applications.db", echo=True)  # 'echo=True' for debugging
SessionLocal = sessionmaker(bind=engine)

class Applicants(Base):
    __tablename__ = "Applicants"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    caste = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    university = Column(String, nullable=False)
    gpa = Column(Integer, nullable=False)


def search_applicant(name):
    
    session = SessionLocal()
    try:
        # Perform the query with case-insensitive search
        results = session.query(Applicants).filter(Applicants.first_name.ilike(f"%{name}%")).all()
        return results
    except SQLAlchemyError as e:
        # Catch specific SQLAlchemy errors
        print(f"SQLAlchemyError occurred: {str(e)}")
        session.rollback()  # Rollback the transaction on error
    except Exception as e:
        # Catch other exceptions
        print(f"An error occurred: {str(e)}")
        session.rollback()
    finally:
        session.close()  # Ensure the session is always closed


def clear_applicant_table():
    session = SessionLocal()

    try:
        session.query(Applicants).delete()
        session.commit()
        print("All records from Applicants table deleted successfully.")
    except Exception as e:
        print(f"Error deleting records: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    
    Base.metadata.create_all(engine)


