#!/usr/bin/env Python
'''
Refactoring the class: Writing the helper class
'''

## Bad example: nested dictionaries
class SimpleGradebook(object):
    def __init__(self):
        self._grades={}

    def add_student(self,name):
        self._grades[name] = {}

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_lst = by_subject.setdefault(subject, [])
        grade_lst.append((score, weight))

    def avg_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight
            if total_weight != 1:
                raise Exception("The sum of weights for a subject should be 1")
            score_sum += subject_avg
            score_count += 1
        return score_sum / float(score_count)

## Good example: refactoring the class

# namedtuple lets you define tiny, immutable data classes
# import collections
# Grade = collections.namedtuple('Grade', ('score', 'weight'))

# Another solution is defining own Grade class
class Grade(object):
    def __init__(self, score, weight):
        self.score = score
        self.weight = weight

class Subject(object):
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def avg_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        if total_weight != 1:
            raise Exception("The sum of weights for a subject should be 1")
        return total / total_weight

class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def avg_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.avg_grade()
            count += 1
        return total/count

class Gradebook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]

if __name__=="__main__":
    # 1. nested dictionaries can be quickly complicated
    print ("==Bad example: nested dictionaries==")
    sgb = SimpleGradebook()
    sgb.add_student(name = "DJ")
    sgb.report_grade(name = "DJ",subject = "math",score = 100, weight = 0.9)
    sgb.report_grade(name = "DJ",subject = "math",score = 10, weight = 0.1)
    sgb.report_grade(name = "DJ",subject = "english",score = 80, weight = 0.9)
    sgb.report_grade(name = "DJ",subject = "english",score = 20, weight = 0.1)
    print("DJ's average score is {}".format(sgb.avg_grade("DJ")))

    sgb.add_student(name = "SK")
    sgb.report_grade(name = "SK",subject = "math",score = 100, weight = 0.9)
    sgb.report_grade(name = "SK",subject = "math",score = 100, weight = 0.1)
    print("SK's average score is {}".format(sgb.avg_grade("SK")))
    print ''

    # 2. In that case, define small classes
    print ("==Good example: refactoring the class==")
    book = Gradebook()
    dj = book.student(name = "Doosan Jung")
    math = dj.subject(name = "math")
    math.report_grade(score = 100, weight = 0.9)
    math.report_grade(score = 10, weight = 0.1)
    english = dj.subject("english")
    english.report_grade(score = 80, weight = 0.9)
    english.report_grade(score = 20, weight = 0.1)
    print("DJ's average score is {}".format(dj.avg_grade()))
    sk = book.student(name = "SK")
    math = sk.subject(name = "math")
    math.report_grade(score = 100, weight = 0.9)
    math.report_grade(score = 100, weight = 0.1)
    print("SK's average score is {}".format(sk.avg_grade()))
