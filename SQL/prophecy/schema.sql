CREATE TABLE new_students (
    id INTEGER,
    student_name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE houses (
    id INTEGER,
    House TEXT,
    Head TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE relationships (
    id INTEGER,
    student_name TEXT,
    house TEXT,
    PRIMARY KEY(id)
);

