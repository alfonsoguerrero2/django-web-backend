from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Student( models.Model):
    id = models.AutoField(primary_key=True) 
    username = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 128)


    def __str__(self):
        return self.username



class Professor(models.Model):
    id = models.AutoField(primary_key=True) 
    professor_id = models.CharField(max_length = 5, unique=True) ## initials and number 
    name = models.CharField(max_length = 30)
#   ratings = list with all his rating // might be unnesecary to add here
    def __str__(self):
        return self.professor_id

    def get_professor_list(self):
        """ Returns a list of professor names teaching this module """
        return ", ".join([prof.name for prof in self.professors.all()])



# many- to - many relationship 
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    module_code = models.CharField(max_length=10) 
    name = models.CharField(max_length = 30)
    year = models.IntegerField()
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    professor = models.ManyToManyField(Professor)
    # use of module.professors.add(prof1, prof2)
    def __str__(self):
        return self.name
    



class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    rating = models.IntegerField()  # Rating value (e.g., 1-5)
    
    professor = models.ForeignKey("Professor", on_delete=models.CASCADE)  # Rated professor
    module = models.ForeignKey("Module", on_delete=models.CASCADE)  # Module being rated

    def __str__(self):
        return f" {self.professor.name} in {self.module.name}: {self.rating}/5"
