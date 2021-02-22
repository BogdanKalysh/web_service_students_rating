CREATE TABLE groups(
    id INT NOT NULL,
    name VARCHAR NOT NULL,

    PRIMARY KEY(id)
);

CREATE TABLE users(
    id INT NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    type_of_user VARCHAR NOT NULL,
    group_id INT REFERENCES groups(id),

    PRIMARY KEY(id)
);

CREATE TABLE teacher_group(
    teacher_id INT REFERENCES users(id),
    group_id INT REFERENCES groups(id)
);

CREATE TABLE rating(
    id INT NOT NULL,
    student_id INT REFERENCES users(id) NOT NULL UNIQUE,
    student_name VARCHAR NOT NULL,
    group_name VARCHAR NOT NULL,
    mark DOUBLE(6,3) NOT NULL
);

CREATE TABLE subjects(
    id INT NOT NULL,
    name VARCHAR NOT NULL,

    PRIMARY KEY(id)
);

CREATE TABLE user_subject(
    user_id INT REFERENCES users(id),
    subject_id INT REFERENCES subjects(id)
);

CREATE TABLE marks(
    id INT NOT NULL,
    date DATE NOT NULL,
    subject_id INT REFERENCES subjects(id),
    student_id INT REFERENCES users(id),

    PRIMARY KEY(id)
);




-- psql -h localhost -d rating -U postgres -p 5432 -a -q -f create_table.sql
-- python add_models.py 

-- env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2

-- alembic init alembic
-- alembic revision --autogenerate
-- alembic upgrade head