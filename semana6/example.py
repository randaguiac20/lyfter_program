def get_average_score(scores):
  return (scores["spanish_score"] + scores["science_score"] + scores["history_score"]) / 3


def is_student_exempted(scores):
  return scores["average_score"] > 70


# Scores
students = [
  {
    "name": "Juan",
    "spanish_score": 75,
    "science_score": 95,
    "history_score": 54,
	},
  {
    "name": "Sofia",
    "spanish_score": 64,
    "science_score": 56,
    "history_score": 98,
	},
  {
    "name": "Paul",
    "spanish_score": 72,
    "science_score": 75,
    "history_score": 79,
	}
]

# Averages
for student in students:
  student["average_score"] = get_average_score(student)
  student["is_exempted"] = is_student_exempted(student)
  print(student["name"], " is_exempted is ", student["is_exempted"])