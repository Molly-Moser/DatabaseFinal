PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Barn_Tasks;
DROP TABLE IF EXISTS Lessons;
DROP TABLE IF EXISTS MedicalRecord;
DROP TABLE IF EXISTS EmergencyContact;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Horse;

-- HORSE
CREATE TABLE Horse (
    Horse_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Breed TEXT,
    Age INTEGER,
    Gender TEXT,
    Activity_Status TEXT DEFAULT 'Active'
);

-- STUDENT
CREATE TABLE Student (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    F_Name TEXT NOT NULL,
    L_Name TEXT NOT NULL,
    Age INTEGER,
    Riding_Level TEXT DEFAULT 'Beginner',
    Phone_Number TEXT
);

-- EMERGENCY CONTACT
CREATE TABLE EmergencyContact (
    Contact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    F_Name TEXT NOT NULL,
    L_Name TEXT NOT NULL,
    Phone_Number TEXT NOT NULL,
    Relation TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- MEDICAL RECORD
CREATE TABLE MedicalRecord (
    Record_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Horse_ID INTEGER NOT NULL,
    Provider TEXT NOT NULL,
    Treatment TEXT NOT NULL,
    Cost REAL NOT NULL DEFAULT 0.00,
    FOREIGN KEY (Horse_ID) REFERENCES Horse(Horse_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- STAFF
CREATE TABLE Staff (
    Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    F_Name TEXT NOT NULL,
    L_Name TEXT NOT NULL,
    Role TEXT NOT NULL,
    Phone_Number TEXT,
    Salary REAL
);

-- LESSONS
CREATE TABLE Lessons (
    Lesson_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Horse_ID INTEGER NOT NULL,
    Staff_ID INTEGER NOT NULL,
    Date TEXT NOT NULL, -- Stored as YYYY-MM-DD HH:MM:SS in SQLite
    Length INTEGER NOT NULL DEFAULT 60,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON UPDATE CASCADE,
    FOREIGN KEY (Horse_ID) REFERENCES Horse(Horse_ID) ON UPDATE CASCADE,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON UPDATE CASCADE
);

-- BARN TASKS
CREATE TABLE Barn_Tasks (
    Task_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Task_Name TEXT NOT NULL,
    Location TEXT,
    Staff_ID INTEGER,
    Completion_Status TEXT DEFAULT 'Pending',
    Completion_Date TEXT,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

--  DATA INSERTIONS
INSERT INTO Horse (Name, Breed, Age, Gender, Activity_Status) VALUES
('Flash', 'Quarter Horse', 32, 'Mare', 'Retired'),
('Beauty', 'Quarter Horse', 27, 'Mare', 'Active'),
('Lightnin', 'Tenesee Walker', 23, 'Gelding', 'Active'),
('Otis', 'Quarab', 17, 'Gelding', 'Active');
  

INSERT INTO Student (F_Name, L_Name, Age, Riding_Level, Phone_Number) VALUES
('Mo', 'Dawn', 17, 'Advanced', '555-0101'),
('Sam', 'Tilford', 23, 'Beginner', '555-0103'),
('Jane', 'Hamm', 28, 'Intermediate', '555-0105'),
('Lucas', 'Jones', 9, 'Beginner', '555-0107');

INSERT INTO EmergencyContact (Student_ID, F_Name, L_Name, Phone_Number, Relation) VALUES
(1, 'Sarah', 'Dawn', '555-0102', 'Grandma'),
(2, 'Cathy', 'Tilford', '555-0104', 'Mother'),
(3, 'Joe', 'Hamm', '555-0106', 'Brother'),
(4, 'Amanda', 'Jones', '555-0108', 'Mother');

INSERT INTO MedicalRecord (Horse_ID, Provider, Treatment, Cost) VALUES
(1, 'Barbra Schmidt (Vet)', 'Bloodwork and Wellness Assesment', 250.00),
(1, 'Jeremy (Farrier)', 'Front shoes', 140.00),
(4, 'Dan (Farrier)', 'Front shoes', 80.00),
(3, 'Barbra Schmidt (Vet)', 'Weight and cough check', 175.50);

INSERT INTO Staff (F_Name, L_Name, Role, Phone_Number, Salary) VALUES
('Jenn', 'Alice', 'Barn Director', '555-0201', 48000.00),
('Carlee', 'Jo', 'Head Instructor', '555-0202', 35000.00),
('Molly', 'Moser', 'Instructor', '555-0203', 30000.00);

INSERT INTO Lessons (Student_ID, Horse_ID, Staff_ID, Date, Length) VALUES
(1, 4, 1, '2026-08-10 10:00:00', 60),
(2, 3, 3, '2026-08-10 11:30:00', 45),
(3, 3, 2, '2026-08-11 14:00:00', 60),
(4, 2, 3, '2026-08-12 09:00:00', 45);

INSERT INTO Barn_Tasks (Task_Name, Location, Staff_ID, Completion_Status, Completion_Date) VALUES
('Hay Delivery', 'Barn', 1, 'Completed', '2026-07-01'),
('New Main Gate for B Triangle Field', 'B Triangle', 3 , 'Pending', NULL),
('Replace Old Feed Buckets', 'Barn', 2, 'Pending', NULL);
