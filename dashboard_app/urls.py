from django.urls import path
from dashboard_app import views
from django.conf.urls.static import static
from SEPPS import settings

app_name='dashboard_app'

urlpatterns = [
    path('', views.Dashboard_View, name='dashboard_page'),
    path('analysis/',views.Analysis_View,name='analysis_page'),
    path('analysis_quiz/',views.Analysis_View_Quiz,name='analysis_quiz_page'),
    path('analysis_sessional/',views.Analysis_View_Sessional,name='analysis_sessional_page'),
    path('intervention/',views.Seating_Plan_View,name='seating_plan_page'),
    path('benchmark/',views.BenchMark_View,name='benchmark_page'),
    path('enroll_class/',views.Enroll_Class_View ,name='enroll_class_page'),
    path('enroll_subject/',views.Enroll_Subject_View,name='enroll_subject_page'),
    path('enroll_student/',views.Enroll_Student_View,name='enroll_student_page'),
    path('enroll_student_class/',views.Enroll_Student_class_view, name='enroll_student_class_page'),
    path('enroll_assignment/',views.Enroll_Assignment_View,name='enroll_assignment_page'),
    path('enroll_assignment_marks/<int:pk>/',views.Enroll_Assignment_Marks_View,name='enroll_assignment_marks_page'),
    path('enroll_quiz/',views.Enroll_Quiz_View,name='enroll_quiz_page'),
    path('enroll_quiz_marks/<int:pk>',views.Enroll_Quiz_Marks_View,name='enroll_quiz_marks_page'),
    path('enroll_sessional/',views.Enroll_Sessional_View,name='enroll_sessional_page'),
    path('enroll_sessional_marks/<int:pk>',views.Enroll_Sessional_Marks_View,name='enroll_sessional_marks_page'),
    path('enroll_final/',views.Enroll_Final,name='enroll_final_page'),
    path('enroll_final_marks/<int:pk>',views.Enroll_Final_Marks, name='enroll_final_marks_page'),
    path('Profile/',views.Profile_View.as_view(),name='profile_page'),
    path('groups/', views.Group_View, name='group_page'),
    path('deatils/<int:pk>/',views.Team_Update.as_view(), name='team_update'),
    path('delete/<int:pk>/',views.Team_Delete.as_view(), name='team_delete'),
    path('history/',views.History_view.as_view(), name='history_page'),
    path('pie_chart_data/', views.pie_chart_data, name='pie_chart_data'),
    path('inter_graph/', views.inter_graph, name='inter_graph'),
    path('student_detail/<stud_id>',views.Student_detail, name='student_detail_page'),
    path('assign_marks_view/<int:pk>',views.Assign_marks_view, name="assign_marks_view"),
    path('quiz_marks_view/<int:pk>',views.quiz_marks_view, name="quiz_marks_view"),
    path('sessional_marks_view/<int:pk>',views.sessional_marks_view, name="sessional_marks_view"),
    path('final_marks_view/<int:pk>',views.final_marks_view, name="final_marks_view")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


