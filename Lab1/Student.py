class Student:
    courseMarks = {}

    def __init__(self, courseName):
        self.courseMarks[courseName] = 0
    
    def addCourseMark(self, course, mark):
        self.courseMarks[course] = mark
    
    def average(self):
        number = 0
        total = 0

        for course in self.courseMarks:
            number += 1
            total += self.courseMarks[course]

        return total/number

#Creates two courses, and the average is 75
myStudent = Student("Math")
myStudent.addCourseMark("Math", 100)
myStudent.addCourseMark("History", 50)
print myStudent.average()
