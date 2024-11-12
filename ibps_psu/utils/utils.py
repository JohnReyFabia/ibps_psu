# 0 - Never
# 1 - A few times a year or less
# 2 - Once a month or less
# 3 - A few times a month
# 4 - Once a week
# 5 - A few times a week
# 6 - Everyday

import csv
import json


def read_csv_to_dict(file_path):
    data_list = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for n, row in enumerate(csv_reader):
                date_key = list(row.keys())[0]
                date_key_Should = "Date"
                # replace date_key with date_key_Should
                row[date_key_Should] = row.pop(date_key)
                data_list.append(dict(row))

    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")

    return data_list


# Provide the path to your CSV file here
file_path = r"c:\Users\Ramon Rodriguez\Downloads\MBI-CALCULATION-DG13.csv"
d = read_csv_to_dict(file_path)

json_text = json.dumps(d, indent=4)
# print(json_text)
output_file_path = "out.json"

# Save the JSON data to a file
with open(output_file_path, "w") as json_file:
    json_file.write(json_text)


def insert_row(d):
    from burnout_assessment.models import (
        SurveyQuestionChoice,
    )
    from landingpage.forms import StudentForm
    from django.contrib.auth.models import User

    possible_answers = {
        0: SurveyQuestionChoice.objects.get(value=0),
        1: SurveyQuestionChoice.objects.get(value=1),
        2: SurveyQuestionChoice.objects.get(value=2),
        3: SurveyQuestionChoice.objects.get(value=3),
        4: SurveyQuestionChoice.objects.get(value=4),
        5: SurveyQuestionChoice.objects.get(value=5),
        6: SurveyQuestionChoice.objects.get(value=6),
    }
    if User.objects.filter(email=d["Email Address"]).exists():
        user = User.objects.get(email=d["Email Address"])
    else:
        form = StudentForm(
            {
                "email": d["Email Address"],
                "student_id": d["Student ID (0000-00-0000)"],
                "program": d["Program"],
                "password": "1234",
                "confirm_password": "1234",
            }
        )
        if form.is_valid():
            user = form.save()
        else:
            raise Exception(f"Error creating user: {form.errors}")

    print("user created successfully")

    # student = Student.objects.get(account=user)

    # survey_form = StudentSurveyForm(
    #     {
    #         "question_15": possible_answers.get(d["CY4_SCORE"]),
    #         "question_14": possible_answers.get(d["CY3_SCORE"]),
    #         "question_13": possible_answers.get(d["CY2_SCORE"]),
    #         "question_12": possible_answers.get(d["CY1_SCORE"]),
    #         "question_11": possible_answers.get(d["EX5_SCORE"]),
    #         "question_10": possible_answers.get(d["EX4_SCORE"]),
    #         "question_9": possible_answers.get(d["EX3_SCORE"]),
    #         "question_8": possible_answers.get(d["EX2_SCORE"]),
    #         "question_7": possible_answers.get(d["EX1_SCORE"]),
    #         "question_6": possible_answers.get(d["EF5_SCORE"]),
    #         "question_5": possible_answers.get(d["EF4_SCORE"]),
    #         "question_4": possible_answers.get(d["EF3_SCORE"]),
    #         "question_3": possible_answers.get(d["EF2_SCORE"]),
    #         "question_2": possible_answers.get(d["EF1_SCORE"]),
    #         "question_1": possible_answers.get(d["EF6_SCORE"]),
    #     }
    # )

    # if survey_form.is_valid():
    #     survey = survey_form.save_to_assessment(student)
    # else:
    #     raise Exception(f"Error saving survey: {survey_form.errors}")

    # print(f"Survery successfully saved survey: {survey_form.errors}")


insert_row(d[0])
