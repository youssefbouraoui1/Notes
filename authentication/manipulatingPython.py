class Person:
    
    @classmethod
    def iam(cls):
        print(f"it is me {cls.__name__}")
        
class Teacher(Person):
    def __init__(self,age):
        self.age = age
    
    def __gt__(self, other):
        return self.age>other.age
    

t = Teacher(34)
t.iam()
t2 = Teacher(23)

print(t>t2)