# CSC 3400: Artificial Intelligence
# Assignment 1: College Admissions
# Created by: Jayden Cruz


# Resources Used
# https://docs.python.org/3/library/csv.html
# https://docs.python.org/3/howto/sorting.html
# https://stackoverflow.com/questions/18952716/valueerror-i-o-operation-on-closed-file
# https://www.w3schools.com/python/ref_string_split.asp
# https://www.geeksforgeeks.org/rename-column-by-index-in-pandas/


# Importing the libraries that I will use for this program
import pandas as pd
import numpy as np




# read in the df
# students_df = pd.read_csv('Admissions Test 1.csv')
# students_df2 = pd.read_csv('Admissions Test 2.csv')
# students_df.info()
# students_df2.info()
# print(students_df.head())
# print(students_df2.head())

# Converts the rows into doubles/floats
def convert_row_type(row):
    row["SAT"] = float(row["SAT"])
    row["GPA"] = float(row["GPA"])
    row["Interest"] = float(row["Interest"])
    row["High School Quality"] = float(row["High School Quality"])
    row["Semester 1"] = float(row["Semester 1"])
    row["Semester 2"] = float(row["Semester 2"])
    row["Semester 3"] = float(row["Semester 3"])
    row["Semester 4"] = float(row["Semester 4"])

    if row["in_out"] == "in":
        row['in_out'] = 0
    else:
        row["in_out"] = 1
    # print(row)

    # Convert to a list
    row_list = [
        row["SAT"], row["GPA"], row["Interest"], row["High School Quality"], row["in_out"],
        row["Semester 1"], row["Semester 2"], row["Semester 3"], row["Semester 4"]
    ]
    # print("Original List:",row_list)

    # Separate into two lists using slicing
    first_list = row_list[:5]  # First 5 elements Problem 1-2
    second_list = row_list[5:]  # Last 4 elements (semester grades) Problem 2-4
    # print("First List:", first_list)
    # print("Second List:", second_list)

    return first_list, second_list


# function uses the students stats to compute their score
def compute_student_scores(first_list):
    # getting the values from the first list
    SAT = first_list[0]
    GPA = first_list[1]
    Interest = first_list[2]
    High_School_Quality = first_list[3]
    in_out = first_list[4]

    # Normalizing GPA and SAT
    GPA = GPA * 2
    SAT = SAT / 160

    # Calculate the student's weighted score using list one
    score = (
            GPA * 0.4 +
            SAT * 0.3 +
            High_School_Quality * 0.2 +
            Interest * 0.05 +
            in_out * 0.05
    )
    return round(score, 2)


# Problem 2- check for outliers
def is_outlier(first_list):
    SAT = first_list[0]
    GPA = first_list[1]
    Interest = first_list[2]

    # Normalize GPA and SAT
    normalized_GPA = GPA * 2
    normalized_SAT = SAT / 160

    has_zero_intrest = (Interest == 0)

    # check if the student GPA is 2 points higher than SAT(both normalize)
    high_gpa_relative_to_sat = (normalized_GPA > normalized_SAT + 2)

    if has_zero_intrest or high_gpa_relative_to_sat:
        return True

    return False


# Problem 3 check for outlier __ > 20
def has_grade_outlier(second_list):
    sorted_grades = sorted(second_list, reverse=True)

    # check if lowest grade is more than 20 points lower than the next
    if sorted_grades[1] - sorted_grades[0] > 20:
        return True
    return False


# Problem 3 check for improvement
def grade_improvement(second_list):
    # compares each sem grade with the previous one
    for i in range(1, len(second_list)):
        if second_list[i] <= second_list[i - 1]:
            return False
    return True


# runs all the guts
# to test your csv replace it in process_data, find_outliers, and enhanced admissions
# DONOT change combine_list
def main():
    df = pd.read_csv("Admissions Test 2.csv", delimiter=",")

    # Deals with "in_out" being named differently
    df.columns.values[9] = "in_out"
    # Deals with the annoying spaces in strings in Test 2
    df['Student'] = df['Student'].apply(lambda x: x.strip())
    # print(df.head())

    # Read in the data
    results = []
    # Problem 2: store the outliers
    outliers = []
    # problem 3: store the extra improved
    improved = []

    for index, row in df.iterrows():  # .iterrows iterates through the rows

        first_list, second_list = convert_row_type(row)

        score = compute_student_scores(first_list)
        # Problem 1 conditional for chosen_students
        if score >= 6.0:
            results.append((row["Student"], score))
        # Problem 2 conditional for outliers
        if is_outlier(first_list) and score >= 5.0:
            outliers.append((row["Student"], score))

        if has_grade_outlier(second_list):
            print(f"Student {row['Student']} has a grade outlier.")

        if grade_improvement(second_list):
            print(f"Student {row['Student']} has improving grades.")

        # sort students greatest to lowest score
        results.sort(key=lambda x: x[1], reverse=True)
        # writes the chosen_students.txt
        with open("chosen_students.txt", "w") as file:
            for student, score in results:
                file.write(f"{student} {score}\n")
        # print(index, row)

        # writes the outliers
        with open("outliers.txt", "w") as file:
            for student, score in outliers:
                file.write(f"{student} {score}\n")

        # Problem 2: combine the lists from problems 1 and 2 to create an improved list of students
        with open("chosen_improved.txt", "w") as file:
            for student, score in results:
                file.write(f"{student}\n")
            for student, score in outliers:
                file.write(f"{student}\n")

        # Problem 4: Create the final list by combining all the previous lists.
        combined_set = combined_set = set(results) | set(improved)  # results union improved
        sorted_list = sorted(combined_set, key=lambda x: x[1], reverse=True)
        final_list = sorted_list

        with open("extra_improved_chosen.txt", "w") as file:
            for student, score in final_list:
                file.write(f"{student}\n")


if __name__ == "__main__":
    main()
