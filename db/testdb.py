from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from models import User, Profile
from database import Base


load_dotenv('.env.development')
dbpassword = os.getenv('DBPASSWORD')
DATABASE_URL = f"postgresql://maxhgeaz:{dbpassword}@trumpet.db.elephantsql.com/maxhgeaz"
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a session maker
Session = sessionmaker(bind=engine)

# Create a new user
session = Session()

user = User(email="user1@example.com", name="John Doe", is_active=True)

# Create a new profile for the user
profile = Profile(user_id=user.id, photo_url="https://example.com/profile-photo.jpg", description="I am a great user!")
user.items.append(profile)

# Save the user and profile to the database
session.add(user)
session.commit()

# Print the user's ID
print(user.id)

