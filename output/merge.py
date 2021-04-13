import json
from tqdm import tqdm

with open("output/coursera_data_complete.json", "r", encoding="utf-8") as c:
    course = json.load(c)

with open("output/coursera_syllabus_data.json", "r", encoding="utf-8") as s:
    syllabus = json.load(s)

courses = list(course.keys())
syllabuses = list(syllabus.keys())
for i in tqdm(range(0, len(courses))):
    c = courses[i]
    course[c]["syllabus"] = syllabus[c] if c in syllabuses else "None"

print("Export Merged...")

with open("output/coursera_data_merged.json", "w", encoding="utf-8") as json_file:
    json.dump(course, json_file)
