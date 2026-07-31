import sqlite3
import os

# In the future, I want to add adding a horse, student, staff, and updating all of them as well, but that's gonna take more time than I have atm

DB_FILE = 'horse_barn.db'
SQL_SETUP_FILE = 'barn_db.sql'

def get_connection():
    """Establish connection and enforce foreign key constraints."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    """Runs the SQL setup script if the database file doesn't exist."""
    if not os.path.exists(DB_FILE):
        print("Database not found. Creating and populating 'horse_barn.db'...")
        conn = get_connection()
        with open(SQL_SETUP_FILE, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully!")


def view_lesson_schedule():
    """Fetch and display master schedule using a multi-table JOIN."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT l.Lesson_ID, s.F_Name || ' ' || s.L_Name, h.Name, 
           st.F_Name || ' ' || st.L_Name, l.Date, l.Length
    FROM Lessons l
    JOIN Student s ON l.Student_ID = s.Student_ID
    JOIN Horse h ON l.Horse_ID = h.Horse_ID
    JOIN Staff st ON l.Staff_ID = st.Staff_ID
    ORDER BY l.Date ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print("\n    LESSON SCHEDULE    ")
    if not rows:
        print("No lessons scheduled.")
        return

    print(f"{'ID':<4} | {'Student':<18} | {'Horse':<12} | {'Instructor':<18} | {'Date & Time':<20} | {'Mins':<5}")
    print("-" * 85)
    for row in rows:
        print(f"{row[0]:<4} | {row[1]:<18} | {row[2]:<12} | {row[3]:<18} | {row[4]:<20} | {row[5]:<5}")

def view_all_students():
    """Display list of students."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Student_ID, F_Name, L_Name, Age, Riding_Level, Phone_Number FROM Student;")
    rows = cursor.fetchall()
    conn.close()

    print("\n    STUDENT DIRECTORY    ")
    for r in rows:
        print(f"ID: {r[0]:<3} | Name: {r[1]} {r[2]:<15} | Age: {r[3]:<2} | Level: {r[4]:<12} | Phone: {r[5]}")

def view_all_horses():
    """Display list of horses."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Horse_ID, Name, Breed, Age, Gender, Activity_Status FROM Horse;")
    rows = cursor.fetchall()
    conn.close()

    print("\n    HORSES    ")
    for r in rows:
        print(f"ID: {r[0]:<3} | Name: {r[1]:<10} | Breed: {r[2]:<15} | Age: {r[3]:<2} | Gender: {r[4]:<8} | Status: {r[5]}")

def view_medical_summary():
    """Display medical visits and total costs per horse."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT m.Record_ID, h.Name, m.Provider, m.Treatment, m.Cost
    FROM MedicalRecord m
    JOIN Horse h ON m.Horse_ID = h.Horse_ID
    ORDER BY m.Record_ID ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print("\n    MEDICAL RECORDS    ")
    for r in rows:
        print(f"ID: {r[0]:<3} | Horse: {r[1]:<10} | Provider: {r[2]:<22} | Treatment: {r[3]:<32} | Cost: ${r[4]:.2f}")

def view_barn_tasks():
    """Display all pending and completed barn tasks."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT bt.Task_ID, bt.Task_Name, bt.Location, 
           st.F_Name || ' ' || st.L_Name AS Assigned_Staff, 
           bt.Completion_Status, bt.Completion_Date
    FROM Barn_Tasks bt
    LEFT JOIN Staff st ON bt.Staff_ID = st.Staff_ID;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print("\n    BARN TASKS    ")
    for r in rows:
        staff = r[3] if r[3] else "Unassigned"
        date = r[5] if r[5] else "N/A"
        print(f"ID: {r[0]:<3} | Task: {r[1]:<32} | Location: {r[2]:<12} | Staff: {staff:<15} | Status: {r[4]:<10} | Done: {date}")


def add_barn_task():
    """Add a new barn maintenance or chore task."""
    print("\n    CREATE NEW BARN TASK    ")
    task_name = input("Task Name (e.g., Fix Fence): ").strip()
    location = input("Location (e.g., Main Arena, Barn): ").strip()
    
    # Show staff for easy reference
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Staff_ID, F_Name, L_Name, Role FROM Staff;")
    staff_members = cursor.fetchall()
    print("\nAvailable Staff Members:")
    for s in staff_members:
        print(f"  #{s[0]}: {s[1]} {s[2]} ({s[3]})")
    
    staff_id = input("Enter Assigned Staff_ID (or leave blank for Unassigned): ").strip()
    status = input("Status (Pending/In Progress/Completed - default Pending): ").strip() or "Pending"

    cursor.execute("""
        INSERT INTO Barn_Tasks (Task_Name, Location, Staff_ID, Completion_Status)
        VALUES (?, ?, ?, ?);
    """, (task_name, location, int(staff_id) if staff_id.isdigit() else None, status))
    
    conn.commit()
    conn.close()
    print("Barn task created successfully!")

def schedule_lesson():
    """Schedule a new lesson linking Student, Horse, and Staff."""
    print("\n    SCHEDULE NEW LESSON    ")
    view_all_students()
    student_id = input("\nEnter Student_ID: ").strip()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Horse_ID, Name, Activity_Status FROM Horse;")
    horses = cursor.fetchall()
    print("\nActive Horses:", [f"#{h[0]} {h[1]}" for h in horses])
    horse_id = input("Enter Horse_ID: ").strip()

    cursor.execute("SELECT Staff_ID, F_Name, L_Name, Role FROM Staff;")
    staff = cursor.fetchall()
    print("Instructors:", [f"#{s[0]} {s[1]} {s[2]}" for s in staff])
    staff_id = input("Enter Staff_ID: ").strip()

    date_str = input("Enter Date & Time (YYYY-MM-DD HH:MM): ").strip()
    length = input("Duration in minutes: ").strip()

    cursor.execute("""
        INSERT INTO Lessons (Student_ID, Horse_ID, Staff_ID, Date, Length)
        VALUES (?, ?, ?, ?, ?);
    """, (student_id, horse_id, staff_id, date_str, int(length)))
    
    conn.commit()
    conn.close()
    print("Lesson successfully scheduled!")



def main():
    initialize_database()
    while True:
        print("\n" + "="*45)
        print("  BARN & LESSON MANAGEMENT SYSTEM")
        print("="*45)
        print("1. View Lesson Schedule")
        print("2. View Student Directory")
        print("3. View Horses")
        print("4. View Medical Records")
        print("5. View Barn Tasks")
        print("-" * 45)
        print("6. Schedule a Riding Lesson")
        print("7. Create New Barn Task")
        print("8. Exit")
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice == '1':
            view_lesson_schedule()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            view_all_horses()
        elif choice == '4':
            view_medical_summary()
        elif choice == '5':
            view_barn_tasks()
        elif choice == '6':
            schedule_lesson()
        elif choice == '7':
            add_barn_task()
        elif choice == '8':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()