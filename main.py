#Importing the libraries that I will use for this program
import pandas as pd
import numpy as np
import csv
from scipy.constants import elementary_charge

#CSC 3400: Artificial Intelligence
#Assignment 1: College Admissions
#Created by: Jayden Cruz

#Resources Used
#https://docs.python.org/3/library/csv.html
#https://docs.python.org/3/howto/sorting.html
#https://stackoverflow.com/questions/18952716/valueerror-i-o-operation-on-closed-file


#read in the df
students_df = pd.read_csv('Admissions Test 1.csv')
students_df2 = pd.read_csv('Admissions Test 2.csv')
#students_df.info()
#students_df2.info()
#print(students_df.head())
#print(students_df2.head())

#converting each element to the appropriate type
#problem 1 and 2: convert the data types to the appropriate type
def convert_row_type(row):
    return [
        float(row[1]), #SAT[1]
        float(row[2]), #GPA[2]
        float(row[3]), #Interest
        float(row[4]), #High School Quality
        float(row[5]), #Semester 1
        float(row[6]), #Semester 2
        float(row[7]), #Semester 3
        float(row[8]), #Semester 4
        0 if row[9] == 'in' else 1 #convert text to number 0=instate 1=out-state
    ]
#Problem 1: College Admissions v1.0
#the compute_score function uses the students stats as parameters and normalizes them
#by making them 0-10
def compute_score(SAT, GPA, Interest, HighSchoolQuality, is_out, sem1,sme2,sem3,sem4):
    SAT_normalized = SAT * 2
    GPA_normalized = GPA / 160
    score = (GPA_normalized * 0.4) + (SAT_normalized * 0.6) + (Interest * 0.05) + (HighSchoolQuality * 0.2) + (is_out * 0.05)
    return round(score,2) #python round function ,2 to the nearest hundreth

#is the student an outlier based on intested and gpa vs sat score
#Problem 2: check for outliers
def is_outlier(SAT, GPA, Interest, HighSchoolQuality, is_out, sem1,sme2,sem3,sem4):
    GPA_normalized = GPA * 2
    SAT_normalized = SAT / 160

    condition1 = Interest == 0
    condition2 = GPA_normalized > SAT_normalized + 2

    return condition1 & condition2

#Problem 4: check for sig. outlier in grades
def grade_outlier(grades):
    grades = sorted(grades)
    return grades[1] - grades[0] > 20

#problem 4: chekcs if studnet grades are improving each sem.
def grade_improvement(grades):
    return grades == sorted(grades)

#Problem 1: read og csv and computes scores and puts students with scores >= 6 to a new file(output)
def process_data(input_csv, output_file):
    with open(input_csv, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)

        results = []
        for row in reader:
            try:
                name = row[0]
                data = convert_row_type(row)
                score = compute_score(*data)
                if score >= 6.0:
                    results.append((name, score))
            except ValueError as e:
                print("skipping row due to invalid value", e)

        results.sort(key=lambda x: x[1], reverse=True) # sorts the results into a list, greatest to least.
        for name, score in results:
            writer.writerow([name, score])

#Problem 2: find outliers with score >= 5.0 and makes a file
def find_outliers(input_csv, output_csv):
    outlier = []
    with open(input_csv, "r", newline="") as infile, open(output_csv, "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            try:
                name = row[0]
                data = convert_row_type(row)
                score = compute_score(*data)

                if score >= 5.0 and is_outlier(*data):
                    outlier.append((name, score))

            except ValueError as e:
                print("skipping row due to invalid value", e)

        for name, score in outlier:
            writer.writerow([name, score])

#Problem 2/4: combine scores and outliers into one file
#combines lists based on scores and outliers
def combine_list(scores_list, outlier_file, output_file):
    with open(scores_list, "r") as f1, open(output_file, "r") as f2, open(output_file,"w") as outfile:
        scores = {row[0]: float(row[1]) for row in csv.reader(f1)}
        outliers = {row[0]: float(row[1]) for row in csv.reader(f2)}
        combined = {**scores, **outliers}

        for name, score in combined.items():
            outfile.write(f"{name}\n")


#Problem4:
def enhanced_admissions(input_file, output_file):

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)

        results = []
        for row in reader:
            name = row[0]
            data = convert_row_type(row)
            score = compute_score(*data)
            grades = data[4:8]

            if score >= 6.0 or (
                    score >= 5.0 and (is_outlier(*data) or grade_outlier(grades) or grade_improvement(grades))):
                results.append((name, score))

        results.sort(key=lambda x: x[1], reverse=True)
        for name, score in results:
            writer.writerow([name, score])

#runs all the guts
#to test your csv replace it in process_data, find_outliers, and enhanced admissions
#DONOT change combine_list
def main():
    process_data('Admissions Test 1.csv', 'chosen_improved.txt')
    find_outliers('Admissions Test 1.csv', 'outliers.txt')
    combine_list('chosen_improved.txt', 'outliers.txt', 'chosen_improved.txt')
    enhanced_admissions('Admissions Test 1.csv', 'extra_improved_chosen.txt')

if __name__ == "__main__":
    main()



