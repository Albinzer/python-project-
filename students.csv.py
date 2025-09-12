        dataset using list of lists


students =[["rafi",20,"A"],
           ["Munni",20,"B"],
           ["Sumi",23,"A+"]]

print("Students dataset(list of list):" )
for row in students:
    print(row)


        dataset using dictionary

books = {
    "Title" : ["machine learning","Artificial intelligence","deep learning"],
    "Author" : ["Rafi","Sumi","Abs"],
    "year" : [2020,2021,2022]
}
print("books dataset using dictionary:")
print(books)

        # dataset using pandas dataframe
import pandas as pd
import statistics as st
import numpy as np

# Original data: each sublist is a column
students = [
    ["Sumi","Soniya","Munni"],   # names
    [19,21,20],                  # ages
    ["A+","B","A"]               # grades
]

# Transpose data so each sublist becomes a row
students_transposed = list(zip(*students))

# Create DataFrame
df = pd.DataFrame(students_transposed, columns=["Name", "Age", "Grade"])
df.index = df.index + 1  # start index from 1

print("\nStudent Details:")
print(df)

# Convert 'Age' column to int
ages = df['Age'].astype(int)

# Compute statistics using statistics module
print("\nStep by Step Statistics for 'Age':")
print("Mean:", st.mean(ages))
print("Median:", st.median(ages))
print("Mode:", st.mode(ages))
print("Variance:", st.variance(ages))
print("Standard Deviation:", st.stdev(ages))




