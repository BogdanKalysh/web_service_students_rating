from models import Session, users, groups

session = Session()

group0 = groups(id = 1, name = "KN-213")
user0 = users(id = 3, name = "Ya", email = "bodyaka@gmail.com", password = "pass", type_of_user = "teacher", group_id = 1)


session.add(group0)
session.add(user0)

session.commit()

session.close()