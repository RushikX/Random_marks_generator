import streamlit as st
import pandas as pd
import random


# Function to generate random marks ensuring they sum up to the total and are within the range
def generate_random_marks(total, num_questions, max_mark_per_question):
    # Start with an empty list of marks
    marks = [0] * num_questions

    # Step 1: Generate random points to partition the total score
    partitions = sorted(random.sample(range(1, total), num_questions - 1))

    # Step 2: Break the total into parts based on the partitions
    partitions = [0] + partitions + [total]
    for i in range(num_questions):
        marks[i] = partitions[i + 1] - partitions[i]

    # Step 3: Adjust marks to ensure none exceed the max per question
    for i in range(num_questions):
        if marks[i] > max_mark_per_question:
            excess = marks[i] - max_mark_per_question
            marks[i] = max_mark_per_question

            # Distribute the excess to other questions within range
            remaining_excess = excess
            for j in range(num_questions):
                if marks[j] < max_mark_per_question and remaining_excess > 0:
                    space_available = max_mark_per_question - marks[j]
                    addition = min(space_available, remaining_excess)
                    marks[j] += addition
                    remaining_excess -= addition

    return marks


# Function to process the Excel file and add random marks for each question
def process_excel(file, num_questions, max_mark_per_question):
    df = pd.read_excel(file)

    # Ensure the required columns are present
    required_columns = {"name", "reg no", "marks"}
    if not required_columns.issubset(df.columns.str.lower()):
        st.error(
            "Excel sheet must contain the following columns: 'name', 'reg no', 'marks'."
        )
        return None

    # Add columns for each question's marks
    for q in range(1, num_questions + 1):
        df[f"Q{q}_marks"] = None

    # Generate random marks for each student
    for index, row in df.iterrows():
        total_marks = row["marks"]
        random_marks = generate_random_marks(
            total_marks, num_questions, max_mark_per_question
        )

        # Update the DataFrame with random marks for each question
        for q in range(1, num_questions + 1):
            df.at[index, f"Q{q}_marks"] = random_marks[q - 1]

    return df


# Streamlit App Interface
st.title("Rubric-Based Exam Mark Generator")

st.markdown(
    """
### Instructions

1. **Upload an Excel File**: The Excel file have the following columns(check spelling of column names):
   - `name`: The student's name.
   - `reg no`: The student's registration number.
   - `marks`: The total marks scored by the student.

   **Example:**
   | name     | reg no | marks |
   |----------|--------|-------|
   | John Doe | 101    | 37    |
   | Jane Doe | 102    | 45    |

2. **Define Parameters**:
   - Enter the number of questions in the exam.
   - Enter the maximum mark that can be assigned to each question.
"""
)

# File uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# User inputs
num_questions = st.number_input("Enter number of questions", min_value=1, value=5)
max_mark_per_question = st.number_input(
    "Enter max mark per question", min_value=1, value=10
)

if uploaded_file is not None:
    st.write("Processing file...")

    # Process the Excel file
    df_with_marks = process_excel(uploaded_file, num_questions, max_mark_per_question)

    if df_with_marks is not None:
        # Display the updated DataFrame
        st.dataframe(df_with_marks)

        # Save the updated file
        output_filename = "processed_marks.xlsx"
        df_with_marks.to_excel(output_filename, index=False)

        # Download link
        st.download_button(
            label="Download Updated Excel File",
            data=open(output_filename, "rb").read(),
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
