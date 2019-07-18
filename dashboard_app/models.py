from django.db import models
from django.contrib.auth.models import User
from Login_app.choices import *
from Login_app.models import Teacher
from smart_selects.db_fields import ChainedForeignKey,GroupedForeignKey



class uploaded_csv(models.Model):
    title = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

class Class(models.Model):
    c_name=models.CharField(max_length=256, primary_key=True)

    def __str__(self):
        return self.c_name

class Subject(models.Model):
    sub_teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    sub_id=models.CharField(max_length=20, primary_key=True)
    sub_name=models.CharField(max_length=100)
    # sub_class=models.ForeignKey(Class, on_delete=models.CASCADE, null=True,blank=True, default=Class.objects.all()[0])
    def __str__(self):
        return  self.sub_id+" "+self.sub_name + " "

class Student(models.Model):
    # s_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    s_roll_number=models.CharField(max_length=15, primary_key=True)
    s_first_name=models.CharField(max_length=256)
    s_last_name=models.CharField(max_length=256)
    s_gender=models.CharField(max_length=1, choices=gender_list)
    s_department=models.CharField(max_length=3, choices=department_list)
    def __str__(self):
        return self.s_roll_number
class Student_Enroll(models.Model):
    s_class=models.ForeignKey(Class, on_delete=models.CASCADE )
    s_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    s_student= models.ForeignKey(Student, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('s_subject', 's_student','s_class'),)
    def __str__(self):
        return str(self.s_student)

class Assignment(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    ass_teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ass_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    ass_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    ass_number=models.IntegerField()
    ass_title=models.CharField(max_length=256)
    ass_total_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('ass_subject', 'ass_title'),)
    def __str__(self):
        return self.ass_title

class AssignmentMarks(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    assm_student=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE)       
    assm_assignment=models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assm_obtained_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('assm_student', 'assm_assignment'),)
    def __str__(self):
        return str(self.assm_student) +" " + str(self.assm_assignment)


class Quiz(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    quiz_teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    quiz_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    quiz_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    quiz_number=models.IntegerField()
    quiz_title=models.CharField(max_length=256)
    quiz_total_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('quiz_subject', 'quiz_title'),)
    def __str__(self):
        return self.quiz_title

class QuizMarks(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    quizm_student=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE)
    quizm_quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quizm_obtained_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('quizm_student', 'quizm_quiz'),)
    def __str__(self):
        return str(self.quizm_quiz) +" " + str(self.quizm_student) + " "+ str(self.quizm_obtained_marks)

class Enroll_Sessional(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    ses_teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ses_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    ses_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    ses_number=models.IntegerField()
    ses_title=models.CharField(max_length=256)
    ses_total_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('ses_subject', 'ses_title'),)
    def __str__(self):
        return self.ses_title

class SessionalMarks(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    sesm_student=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE)
    sesm_sessional=models.ForeignKey(Enroll_Sessional, on_delete=models.CASCADE)
    sesm_obtained_marks=models.FloatField(max_length=4)
    class Meta:
        unique_together = (('sesm_student', 'sesm_sessional'),)
    def __str__(self):
        return str(self.sesm_student)+" "+ str(self.sesm_sessional) + " " + str(self.sesm_obtained_marks)

class Final(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    fnl_teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    fnl_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    fnl_class=models.ForeignKey(Class,on_delete=models.CASCADE)
    fnl_total_marks=models.FloatField(max_length=4)

    def __str__(self):
        return str(self.fnl_subject)
    class Meta:
        unique_together = (('fnl_subject'),)

class FinalMarks(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add= True)
    fnlm_student=models.ForeignKey(Student_Enroll,on_delete=models.CASCADE)
    fnlm_final=models.ForeignKey(Final,on_delete=models.CASCADE)
    fnlm_obtained_marks=models.FloatField(max_length=4)

    def __str__(self):
        return str(self.fnlm_student)+ "=>"+ str(self.fnlm_final)+ '=>'+ str(self.fnlm_obtained_marks)
    class Meta:
        unique_together = (('fnlm_student', 'fnlm_final'),)

class benchmark(models.Model):
    b_id=models.AutoField(primary_key=True)
    TimeStamp=models.DateTimeField(auto_now_add=True)
    benchmark_name=models.CharField(max_length=256)
    end_date=models.DateTimeField()
    benchmark_value=models.IntegerField()

    def __str__(self):
        return str(self.TimeStamp) + " " + self.benchmark_name + " " + str(self.end_date)

class team(models.Model):
    team_subj=models.ForeignKey(Subject, on_delete=models.CASCADE)
    team_id=models.AutoField(primary_key=True)
    position1=GroupedForeignKey(Student_Enroll,"s_subject", related_name='m1')
    position2=GroupedForeignKey(Student_Enroll,"s_subject", related_name='m2', null=True, blank=True)
    position3=GroupedForeignKey(Student_Enroll,"s_subject", related_name='m3', null=True, blank=True)
    class Meta:
        unique_together = (('position1', 'position2', 'position3'),('position1', 'position3', 'position2'),('position2', 'position1', 'position3'),('position2', 'position3', 'position1'),('position3', 'position1', 'position2'),('position3', 'position2', 'position1'),)
    # position1=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE, related_name='Member1')
    # position2=models.ForeignKey(Student_Enroll, null=True, blank=True, on_delete=models.CASCADE, related_name='Member2')
    # position3=models.ForeignKey(Student_Enroll, null=True, blank=True, on_delete=models.CASCADE, related_name='Member3')

    def __str__(self):
        return str(self.team_id)


    
class team_history(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    team_id=models.IntegerField()
    member_1=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE, related_name='member_1')
    member_2=models.ForeignKey(Student_Enroll, on_delete= models.CASCADE, related_name='member_2', null=True, blank=True)
    member_3=models.ForeignKey(Student_Enroll, on_delete= models.CASCADE, related_name='member_3', null=True, blank=True)
    def __str__(self):
        return str(self.TimeStamp) + " " + str(self.team_id)

class team_performance_history(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    team_p_id=models.ForeignKey(team, on_delete=models.CASCADE)
    total_perf=models.FloatField(max_length=4)

    def __Str__(self):
        return str(self.TimeStamp) + "=>" + str(self.team_p_id) + " =>" + str(self.total_perf)

class intervention(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    intervention_id=models.AutoField(primary_key=True)
    inter_student=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE)
    inter_team=models.ForeignKey(team, on_delete=models.CASCADE)
    inter_postion=models.IntegerField()

    def __str__(self):
        return str(self.intervention_id) + " " + str(self.inter_student)

class predictions(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    Student_Prediction=models.OneToOneField(Student_Enroll, on_delete=models.CASCADE)
    prediction_class=models.CharField(max_length=5 ,choices=prediction_list)

    def __str__(self):
        return str(self.Student_Prediction)+ "==>" + self.prediction_class

class total_performance(models.Model):
    TimeStamp= models.DateTimeField(auto_now_add=True)
    Student_perf=models.OneToOneField(Student_Enroll, on_delete=models.CASCADE)
    total=models.FloatField(max_length=4)
    purpose=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.Student_perf) + "===" + str(self.total)

class total_perf_hist(models.Model):
    TimeStamp=models.DateTimeField(auto_now_add=True)
    stud_pref_hist=models.ForeignKey(Student_Enroll,on_delete=models.CASCADE)
    total_val=models.FloatField(max_length=4)
    purpose=models.CharField(max_length=100, null=True, blank=True)

    def __Str__(self):
        return str(self.stud_pref_hist)+ "=>"+ str(self.total_val)

class History(models.Model):
    TimeStamp= models.DateTimeField(auto_now_add=True)
    student_history=models.ForeignKey(Student_Enroll, on_delete=models.CASCADE)
    student_team=models.ForeignKey(team, on_delete=models.CASCADE)
    student_position=models.IntegerField()

    def __str__(self):
        return str(self.TimeStamp) + "->" + str(self.student_history) + "<-" + str(self.student_team)

class avg_performance(models.Model):
    TimeStamp= models.DateTimeField(auto_now_add= True)
    Subject_pref=models.ForeignKey(Subject, on_delete=models.CASCADE)
    avg_perf= models.FloatField(max_length=4)

    def __str__(self):
        return str(self.TimeStamp) + "==>" + str(self.Subject_pref) + "==" + str(self.avg_perf)
class pref_class_count(models.Model):
    TimeStamp= models.DateTimeField(auto_now_add=True)
    subj_of_count=models.ForeignKey(Subject, on_delete=models.CASCADE)
    A_count= models.IntegerField()
    B_count=models.IntegerField()
    G_count= models.IntegerField()

    def __str__(self):
        return str(self.TimeStamp) + " " + str(self.subj_of_count)