import nltk
import os
from django.core.cache import cache

# Get the current working directory
current_directory = os.getcwd()

# Create the NLTK data path dynamically
nltk_data_path = os.path.join(current_directory, 'nltk_data')

nltk.data.path.append(nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)
# print(nltk.data.path)

# For queries
from collections import Counter
from django.db.models import Count
from concurrent.futures import ThreadPoolExecutor

# Keyword Extraction
from rake_nltk import Rake
import yake
import numpy as np

#  Burnout assessment forms and models import
from burnout_assessment.models import Student, Assessment, StudentSurveyQuestion, BurnoutProfile

# For updating the cached data
def check_for_new_assessment():
    latest_assessment = Assessment.objects.order_by('-created_date').first()

    if latest_assessment:
        latest_assessment_timestamp = latest_assessment.created_date

        last_cached_assessment_timestamp = cache.get('last_assessment_timestamp')

        cache.set('last_assessment_timestamp', latest_assessment_timestamp)

        if last_cached_assessment_timestamp and latest_assessment_timestamp > last_cached_assessment_timestamp:
            return True 
        else:
            return False 
    else:
        return False
    
# Admin burnout factors chart
def get_keywords_and_counts_for_students(students):
    max_ngram_size_yake = 5
    deduplication_threshold_yake = 0.9
    numOfKeywords_yake = 10

    custom_kw_extractor_yake = yake.KeywordExtractor(
        lan="en",
        n=max_ngram_size_yake,
        dedupLim=deduplication_threshold_yake,
        top=numOfKeywords_yake,
        features=None,
    )
    rake_extractor = Rake()

    rake_indices = [3, 5, 6]
    rake_statement_mapping = {3: 0, 5: 0, 6: 0}
    yake_statement_mapping = {
        1: 9,
        2: 1,
        4: 0,
        7: 0,
        8: 0,
        9: 1,
        10: 0,
        11: 1,
        12: 1,
        13: 3,
        14: 0,
        15: 0,
    }

    extracted_keywords_and_scores = []

    def process_student(student):
        recent_instances = StudentSurveyQuestion.objects.filter(student=student)[:15]
        burnout_assessment = Assessment.objects.filter(student=student).first()

        for i, instance in enumerate(recent_instances, start=1):
            scraped_text = instance.scrape_question_text()

            if i in rake_indices:
                rake_extractor.extract_keywords_from_text(scraped_text)
                keywords = rake_extractor.get_ranked_phrases()
                representative_keyword_position = rake_statement_mapping.get(i, 0)
            else:
                keywords_with_scores = custom_kw_extractor_yake.extract_keywords(scraped_text)
                keywords = [keyword[0] for keyword in keywords_with_scores]
                representative_keyword_position = yake_statement_mapping.get(i, 0)

            keywords = [
                str(keyword)
                for keyword in keywords
                if isinstance(keyword, (str, np.str_))
                and not any(char.isdigit() for char in str(keyword))
            ]
            representative_keyword = (
                keywords[representative_keyword_position]
                if keywords and 0 <= representative_keyword_position < len(keywords)
                else "N/A"
            )

            question_code = instance.question.code.lower()
            question_score = getattr(burnout_assessment, f"{question_code}_score", None)

            # Skip instances where question_score is None
            if question_score is not None:
                extracted_keywords_and_scores.append(
                    {"keywords": representative_keyword, "score": question_score}
                )

    with ThreadPoolExecutor() as executor:
        executor.map(process_student, students)

    highest_score_keywords = [entry["keywords"] for entry in extracted_keywords_and_scores if entry["score"] in {5, 6}]
    keyword_counts = dict(Counter(highest_score_keywords))
    top_keywords = dict(sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)[:15])

    print("Keyword count:", keyword_counts)
    print("Extracted keywords:", extracted_keywords_and_scores)
    print("Top Keywords:", top_keywords)

    return top_keywords



def calculate_age_range_distribution(students, burnout_profiles):
    age_data_per_profile = {}
    age_ranges = ["16-20", "21-25", "26-30", "31+"]

    for profile in burnout_profiles:
        profile_students = students.filter(assessment__profile=profile)
        age_data_per_profile[profile.profile] = [
            profile_students.filter(age__range=(16, 20)).count(),
            profile_students.filter(age__range=(21, 25)).count(),
            profile_students.filter(age__range=(26, 30)).count(),
            profile_students.filter(age__gte=31).count(),
        ]

    return age_data_per_profile



# def get_overall_burnout_counts(selected_college=None):
#     queryset = Assessment.objects.all()

#     if selected_college:
#         queryset = queryset.filter(
#             student__program__college__college_name=selected_college
#         )

#     overall_burnout_counts = (
#         queryset.values("profile__profile", "student__gender")
#         .annotate(profile_count=Count("profile"))
#         .values("profile__profile", "student__gender", "profile_count")
#     )

#     return overall_burnout_counts

def get_overall_burnout_counts(selected_college=None):
    assessments = Assessment.objects.all()

    if selected_college:
        assessments = assessments.filter(student__program__college__college_name=selected_college)

    burnout_profiles = {
        "Engaged": BurnoutProfile.objects.get(profile="Engaged"),
        "Disengaged_and_Ineffective": BurnoutProfile.objects.get(profile="Disengaged and Ineffective"),
        "Overextended_and_Ineffective": BurnoutProfile.objects.get(profile="Overextended and Ineffective"),
        "Overextended_and_Disengaged": BurnoutProfile.objects.get(profile="Overextended and Disengaged"),
        "Ineffective": BurnoutProfile.objects.get(profile="Ineffective"),
        "Disengaged": BurnoutProfile.objects.get(profile="Disengaged"),
        "Overextended": BurnoutProfile.objects.get(profile="Overextended"),
        "Burned_out": BurnoutProfile.objects.get(profile="Burned Out"),

    }

    overall_burnout_counts = {}

    for profile_name, profile_obj in burnout_profiles.items():
        # Overall profile count
        overall_count = assessments.filter(profile=profile_obj).count()
        overall_burnout_counts[profile_name] = {'overall_count': overall_count}

        # Gender-wise profile count
        gender_counts = assessments.filter(profile=profile_obj).values("student__gender").annotate(profile_count=Count("profile"))
        gender_counts_list = list(gender_counts)  # Convert the queryset to a list of dictionaries
        overall_burnout_counts[profile_name]['gender_counts'] = gender_counts_list

    return overall_burnout_counts




def get_program_info(all_programs):
    program_info = []

    for program in all_programs:
        program_students = Student.objects.filter(program=program)
        program_burnout_counts = (
            Assessment.objects.filter(student__in=program_students)
            .values("profile__profile")
            .annotate(profile_count=Count("profile"))
            .values("profile__profile", "profile_count")
        )

        d = {
            "program": program,
            "burnout_counts": {},
        }

        for entry in program_burnout_counts:
            if entry["profile__profile"]:
                d["burnout_counts"][
                    entry["profile__profile"].replace(" ", "_")
                ] = entry["profile_count"]

        program_info.append(d)

    return program_info


def get_profile_gender_counts(overall_burnout_counts):
    profile_gender_counts = {}

    for profile_name, counts_dict in overall_burnout_counts.items():
        gender_counts_list = counts_dict.get('gender_counts', [])  
        profile_gender_counts[profile_name] = {"Male": 0, "Female": 0}

        for gender_counts in gender_counts_list:
            gender = gender_counts.get("student__gender")
            count = gender_counts.get("profile_count", 0)
            if gender:
                profile_gender_counts[profile_name][gender] += count

    return profile_gender_counts


