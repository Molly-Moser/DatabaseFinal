-- QUERY 1) DISPLAY SCHEDUALED LESSONS
SELECT 
    l.Lesson_ID,
    s.F_Name || ' ' || s.L_Name AS Student_Name,
    h.Name AS Horse_Name,
    st.F_Name || ' ' || st.L_Name AS Instructor_Name,
    l.Date AS Lesson_Time,
    l.Length AS Duration_Mins
FROM Lessons l
JOIN Student s ON l.Student_ID = s.Student_ID
JOIN Horse h ON l.Horse_ID = h.Horse_ID
JOIN Staff st ON l.Staff_ID = st.Staff_ID
ORDER BY l.Date ASC;

-- QUERY 2) DISPLAY MEDICAL COSTS
SELECT 
    h.Horse_ID,
    h.Name AS Horse_Name,
    h.Breed,
    COUNT(m.Record_ID) AS Total_Visits,
    COALESCE(SUM(m.Cost), 0.00) AS Total_Medical_Cost
FROM Horse h
LEFT JOIN MedicalRecord m ON h.Horse_ID = m.Horse_ID
GROUP BY h.Horse_ID, h.Name;

-- QUERY 3) DISPLAY NON-COMPLETED BARN TASKS
SELECT 
    bt.Task_ID,
    bt.Task_Name,
    bt.Location,
    st.F_Name || ' ' || st.L_Name AS Assigned_Staff,
    bt.Completion_Status,
    bt.Completion_Date
FROM Barn_Tasks bt
LEFT JOIN Staff st ON bt.Staff_ID = st.Staff_ID
WHERE bt.Completion_Status != 'Completed' 
   OR bt.Completion_Status IS NULL;