import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the database engine
engine = create_engine('sqlite:///example.db')
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data if table is empty
if not session.query(User).first():
    sample_users = [
        User(name='Alice', age=30),
        User(name='Bob', age=25)
    ]
    session.add_all(sample_users)
    session.commit()

# Add input fields for new user data
st.header("Add New User")
new_name = st.text_input("Name")
new_age = st.number_input("Age", min_value=0, max_value=150, value=25)

if st.button("Add User"):
    new_user = User(name=new_name, age=new_age)
    session.add(new_user)
    session.commit()
    st.success(f"Added new user: {new_name}")

# Query all users
users = session.query(User).all()

# Display the data in Streamlit
st.header("Users in the database:")
for user in users:
    st.write(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

# Close the session
session.close()

# okokok