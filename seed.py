from models import User, Post, db
from app import app

# Drop existing tables (if any)
db.drop_all()

# Create tables based on the models
db.create_all()

# Sample data
danielle = User(id=1, first_name="Danielle", last_name="Gomez")
joel = User(id=2, first_name="Joel", last_name="Osteen")

p1 = Post(id=1, title="First Post", content="This is just a test!", user_id=1)
p2 = Post(id=2, title="Second Post", content="This is just another test!", user_id=2)

# Add data to the session
db.session.add(danielle)
db.session.add(joel)
db.session.add(p1)
db.session.add(p2)

# Commit the changes to the database
db.session.commit()

