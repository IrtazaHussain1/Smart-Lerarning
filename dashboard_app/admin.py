from django.contrib import admin
from dashboard_app.models import *
# Register your models here.

admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Student_Enroll)
admin.site.register(Assignment)
admin.site.register(Quiz)
admin.site.register(Enroll_Sessional)
admin.site.register(AssignmentMarks)
admin.site.register(QuizMarks)
admin.site.register(SessionalMarks)
admin.site.register(Final)
admin.site.register(FinalMarks)
admin.site.register(benchmark)
admin.site.register(team)
admin.site.register(intervention)
admin.site.register(predictions)
admin.site.register(total_performance)
admin.site.register(History)
admin.site.register(avg_performance)
admin.site.register(pref_class_count)
admin.site.register(team_history)
admin.site.register(total_perf_hist)
admin.site.register(team_performance_history)
admin.site.register(uploaded_csv)