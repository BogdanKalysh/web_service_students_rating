from models import Session, users, groups

session = Session()

# group0 = groups(id = 1, name = "KN-213")
user0 = users(name = "Ya", email = "bodya_ka2@gmail.com", password = "pass", type_of_user = "teacher")


# session.add(group0)
session.add(user0)

session.commit()

session.close()