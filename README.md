# Rubric-Based Exam Mark Generator

## Overview

This Streamlit app allows users to upload an Excel sheet containing student details (name, registration number, and marks scored) and automatically generates random marks for each question in an exam. The app ensures that the randomly generated marks are within a defined range (e.g., 0 to 10) and the sum of the generated marks equals the total marks scored by the student.

The output is an updated Excel file that contains the original student details along with the randomly generated marks for each question.

## Features

- Upload an Excel file with student data.
- Define the number of questions and the maximum mark per question.
- Automatically generate random marks for each question, ensuring they sum to the total score.
- Download the updated Excel file with the marks breakdown.

## How to Use Locally

### 1. Clone the repository

```bash
git clone https://github.com/RushikX/Random_marks_generator/
```
### 2.Install Dependecies
```bash
pip install -r requirements.txt
```
