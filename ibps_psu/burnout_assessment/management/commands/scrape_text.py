from django.core.management.base import BaseCommand
from burnout_assessment.models import StudentSurveyQuestion, Student, Assessment
from rake_nltk import Rake
import yake
import numpy as np

class Command(BaseCommand):
    help = 'Scrape text, perform keyword extraction using RAKE and YAKE, generate short phrases, and get the highest score for each question for the 15 most recent StudentSurveyQuestion instances for a specific student'

    def handle(self, *args, **kwargs):
        # Get a sample student instance (replace 1 with the actual student ID)
        sample_student = Student.objects.get(pk=9)

        # Get the 15 most recent instances for the student
        recent_instances = StudentSurveyQuestion.objects.filter(student=sample_student)[:15]

        # Get the assessment for the student
        assessment = Assessment.objects.get(student=sample_student)

        # Initialize RAKE for keyword extraction
        rake_extractor = Rake()

        # Initialize YAKE for keyword extraction
        max_ngram_size = 5
        deduplication_threshold = 0.9
        numOfKeywords = 10
        yake_extractor = yake.KeywordExtractor(lan="en", n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

        # Define a list of indices for which RAKE will be used
        rake_indices = [3, 5, 6]

        # Print the indices for RAKE usage
        print(f"RAKE will be used for instances with indices: {rake_indices}")

        # Define a mapping of statement indices to the desired keyword positions
        statement_mapping = {1: 9, 2: 1, 4: 0, 7: 0, 8: 0, 9: 3, 10: 0, 11: 3, 12: 1, 13: 5, 14: 0, 15: 0}  # Adjust as needed

        # Print the statement mapping
        print("Statement Mapping:")
        for statement_index, keyword_position in statement_mapping.items():
            print(f"Statement {statement_index} -> Keyword Position: {keyword_position}")

        for i, instance in enumerate(recent_instances, start=1):  # Start index from 1
            # Scrape text
            scraped_text = instance.scrape_question_text()
            self.stdout.write(self.style.SUCCESS(f'Scraped text: {scraped_text}'))

            if i in rake_indices:  # Use RAKE for specific instances
                rake_extractor.extract_keywords_from_text(scraped_text)
                keywords = rake_extractor.get_ranked_phrases()
            else:  # Use YAKE for other instances
                keywords_with_scores = yake_extractor.extract_keywords(scraped_text)
                keywords = [keyword[0] for keyword in keywords_with_scores]  # Extract only the string part

            # Filter out non-string keywords (including numpy.float64)
            keywords = [str(keyword) for keyword in keywords if isinstance(keyword, (str, np.str_)) and not any(char.isdigit() for char in str(keyword))]

            # Choose a representative keyword based on the defined mapping
            representative_keyword_position = statement_mapping.get(i, 0)  # Default to the first keyword
            if i in rake_indices:
                representative_keyword_position = 0  # Use the first keyword for RAKE

            representative_keyword = keywords[representative_keyword_position] if keywords else "N/A"

            # Find the corresponding score in the assessment for the question
            question_code = instance.question.code.lower()
            question_score = getattr(assessment, f'{question_code}_score', None)

            # Generate a short statement with the representative keyword and question score
            short_statement = f"{i}. Regarding '{instance.question.question}': Representative Keyword: {representative_keyword}. Score: {question_score}"

            self.stdout.write(self.style.SUCCESS(f'Short Statement: {short_statement}'))
