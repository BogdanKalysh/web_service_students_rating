from models import Session, users, groups

session = Session()


admin1 = users(name = "admin1", email = "admin1@gmail.com", password = "pass", type_of_user = "admin")

session.add(admin1)

session.commit()

session.close()