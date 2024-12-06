import matplotlib.pyplot as plt
import glob
import math

students_file = r'./data/students.txt'
assignments_file = r'./data/assignments.txt'
submissions_folder = r'./data/submissions'

def load_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            student_id = line[:3]
            name = line[3:]
            students[int(student_id)] = name
    return students

def load_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[assignment_id] = {"name": name, "points": points}
    return assignments

def load_submissions(directory_path):
    submissions = {}
    for file_path in glob.glob(f"{directory_path}/*.txt"):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    student_id, assignment_id, percentage = map(str.strip, line.split('|'))
                    student_id = int(student_id)
                    assignment_id = int(assignment_id)
                    percentage = float(percentage)
                    if assignment_id not in submissions:
                        submissions[assignment_id] = {}
                    submissions[assignment_id][student_id] = percentage
                except ValueError:
                    continue
    return submissions

def get_student_grade(students, assignments, submissions):
    student_name = input("What is the student's name: ")
    student_id = next((id for id, name in students.items() if name == student_name), None)
    if student_id is None:
        print("Student not found")
        return

    total_points = 0
    earned_points = 0
    for assignment_id, submission in submissions.items():
        if student_id in submission:
            percentage = submission[student_id]
            points = assignments[assignment_id]["points"]
            earned_points += (percentage / 100) * points
            total_points += points

    grade = (earned_points / total_points) * 100 if total_points > 0 else 0
    print(f"{round(grade)}%")

def get_assignment_statistics(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    assignment_id = next((id for id, data in assignments.items() if data["name"] == assignment_name), None)
    if assignment_id is None:
        print("Assignment not found")
        return

    percentages = submissions.get(assignment_id, {}).values()
    if not percentages:
        print("No submissions for this assignment")
        return

    min_score = min(percentages)
    avg_score = sum(percentages) / len(percentages)
    max_score = max(percentages)

    print(f"Min: {math.floor(min_score)}%")  # Floor to ensure integer
    print(f"Avg: {math.floor(avg_score)}%")  # Floor to always round down
    print(f"Max: {math.floor(max_score)}%")  # Floor to ensure integer

def plot_assignment_histogram(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    assignment_id = next((id for id, data in assignments.items() if data["name"] == assignment_name), None)
    if assignment_id is None:
        print("Assignment not found")
        return

    percentages = submissions.get(assignment_id, {}).values()
    if not percentages:
        print("No submissions for this assignment")
        return

    plt.hist(percentages, bins=[0, 25, 50, 75, 100])
    plt.show()

def main_menu():
    students = load_students(students_file)
    assignments = load_assignments(assignments_file)
    submissions = load_submissions(submissions_folder)

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print("Enter your selection: ", end="")
    choice = input().strip()

    if choice == "1":
        get_student_grade(students, assignments, submissions)
    elif choice == "2":
        get_assignment_statistics(assignments, submissions)
    elif choice == "3":
        plot_assignment_histogram(assignments, submissions)
    else:
        print("Invalid option selected")

if __name__ == "__main__":
    main_menu()
