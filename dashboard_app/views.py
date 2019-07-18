from django.shortcuts import render,redirect, render_to_response
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.views.generic import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import datetime
from dashboard_app.forms import *
from .models import *
from django.db.models import Q
from Login_app.models import *
import pandas as pd
import numpy as np


#                                       import for Machine Learning
#import matplotlib.pyplot as plt
#import seaborn as sns
#from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.model_selection import cross_val_predict
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import KFold
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import classification_report
#from sklearn.metrics import accuracy_score
#from sklearn.metrics import confusion_matrix      
#from sklearn.metrics import *
##from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
##from sklearn.tree import DecisionTreeClassifier
#from sklearn.multiclass import OneVsRestClassifier
#from sklearn.preprocessing import label_binarize
#from sklearn.metrics import roc_curve
#from sklearn.metrics import auc
from sklearn.externals import joblib

#Loading OneHotEncoders
ohe_9 = joblib.load('statics/encodes/ohe9.save')
ohe_10 = joblib.load('statics/encodes/ohe10.save')
ohe_11 = joblib.load('statics/encodes/ohe11.save')
ohe_12 = joblib.load('statics/encodes/ohe12.save')
ohe_14 = joblib.load('statics/encodes/ohe14.save')
ohe_19 = joblib.load('statics/encodes/ohe19.save')
ohe_25 = joblib.load('statics/encodes/ohe25.save')
ohe_32 = joblib.load('statics/encodes/ohe32.save')
ohe_35 = joblib.load('statics/encodes/ohe35.save')

#Loading Label Encoders
labelencoder_X4 = joblib.load('statics/encodes/le_4.save')
labelencoder_X6 = joblib.load('statics/encodes/le_6.save')
labelencoder_X24 = joblib.load('statics/encodes/le_24.save')
labelencoder_X28 = joblib.load('statics/encodes/le_28.save')
labelencoder_X29 = joblib.load('statics/encodes/le_29.save')
labelencoder_X30 = joblib.load('statics/encodes/le_30.save')
labelencoder_X31 = joblib.load('statics/encodes/le_31.save')
labelencoder_X34 = joblib.load('statics/encodes/le_34.save')

# Loading Scalers
scaler = joblib.load('statics/encodes/scaler.save')


#                                           end of Encoders
pre_class=['A','B','G']

pre_dic={0:'A',1:'G',2:'B'}


gender_dic={'Male':'M','Female':'F'}


# Create your views here.

class Profile_View(DetailView):
        model = Teacher
        template_name= 'dashboard_app/user_profile.html'

def Dashboard_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            json_dict=dict()
            if request.method== "GET" and request.is_ajax():
                json_dict['student']=list(Student.objects.all().values('s_roll_number','s_first_name','s_last_name'))
                json_dict['Stud_data']=list(Student_Enroll.objects.all().values())
                json_dict['pre_data']=list(predictions.objects.all().values('Student_Prediction', 'prediction_class'))
                json_dict['tp']=list(total_performance.objects.all().values())
                return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder))
            elif request.method == 'POST' and request.is_ajax():   
                value=request.POST['sub_team_val']
                json_dict['Stud_data']=list(Student_Enroll.objects.all().values())
                json_dict['pre_data']=list(predictions.objects.all().values())
                return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder))
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            Sub_view=Subject.objects.filter(sub_teacher=c_user)
            stud_view=Student_Enroll.objects.filter(s_subject=Sub_view)  
            pre_st=predictions.objects.all()
            top_s=total_performance.objects.all().order_by('-total')[:5]
            bad_s=total_performance.objects.all().order_by('total')[:3]
            ass_sum=Assignment.objects.all().order_by('-TimeStamp')[:3]
            quiz_sum=Quiz.objects.all().order_by('-TimeStamp')[:3]
            ses_sum=Enroll_Sessional.objects.all().order_by('-TimeStamp')[:3]
            if len(Sub_view) != 0: 
                return render(request, "dashboard_app/index.html",{'name':name, 'sub_view':Sub_view,'stud_view':stud_view, 'pre_st':pre_st,'top_s':top_s,'bad_s':bad_s , 'ass_sum':ass_sum,'quiz_sum':quiz_sum, 'ses_sum':ses_sum})
            else:
                return render(request, "dashboard_app/welcome.html")
        else:
            return redirect('/')
    return redirect('/')


def Student_detail(request, stud_id):
    st=Student.objects.get(s_roll_number=stud_id)
    se=Student_Enroll.objects.filter(s_student=st)[0]
    current_teams=team.objects.filter( Q(position1=se) | Q(position2=se)  | Q(position3=se))
    prev_teams=History.objects.filter(student_history=se).order_by('-TimeStamp')[1:]
    total_performance_ver=total_performance.objects.filter(Student_perf=se)
    pred=predictions.objects.filter(Student_Prediction=se)[0]
    assignments=AssignmentMarks.objects.filter(assm_student=se)
    quizs=QuizMarks.objects.filter(quizm_student= se)
    sessionals=SessionalMarks.objects.filter(sesm_student= se)
    return render(request,'dashboard_app/Student_detail.html',{'team':current_teams, 'pred':pred, 'total_performance':total_performance_ver,'assignments':assignments, 'quizs':quizs, 'sessionals':sessionals,'se':se, 'stud_id':stud_id ,'prev_teams':prev_teams})

def Analysis_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            return render(request, "dashboard_app/analysis.html",{'name':name})
        else:
            return redirect('/')
    else:
        return redirect('/')

def Analysis_View_Quiz(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            return render(request, "dashboard_app/analysis_quiz.html",{'name':name})
        else:
            return redirect('/')
    else:
        return redirect('/')
def Analysis_View_Sessional(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            return render(request, "dashboard_app/analysis_sessional.html",{'name':name})
        else:
            return redirect('/')
    else:
        return redirect('/')
def Group_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form=form_team_add()
            data=team.objects.all()
            inter=intervention.objects.all()
            hist= History.objects.all()
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            sub_data=Subject.objects.filter(sub_teacher=c_user)            
            students_data=Student_Enroll.objects.all()
            context={'name':name, 'data':data ,'sub_data':sub_data,'s_data':students_data,'hist':hist,  'inter':inter , 'form':form}
            data_dict= dict()
            # form=form_team_add()
            # on POST request from AJAX
            if request.method== "POST" and request.is_ajax():
                value=request.POST['sub_team_val']
                data_dict['data']=list(team.objects.all().values())
                data_dict['students']=list(Student.objects.all().values())
                return HttpResponse(json.dumps(data_dict, cls=DjangoJSONEncoder))
            # On POST request
            elif request.method == "POST":
                try:
                    form=form_team_add(request.POST)
                    if form.is_valid():
                        data=form.save(commit=False)
                        data.save()
                        data.refresh_from_db()
                        if data.position2 is not None and data.position3 is not None:
                            pos1_val=total_performance.objects.get(Student_perf=data.position1)
                            pos2_val=total_performance.objects.get(Student_perf=data.position2)
                            pos3_val=total_performance.objects.get(Student_perf=data.position3)
                            t_a=(pos1_val.total+pos2_val.total+pos3_val.total)/3
                        elif data.position2 is None and data.position3 is not None:
                            pos1_val=total_performance.objects.get(Student_perf=data.position1)
                            pos3_val=total_performance.objects.get(Student_perf=data.position3)
                            t_a=(pos1_val.total+pos3_val.total)/2
                        elif data.position3 is None and data.position2 is not None:
                            pos1_val=total_performance.objects.get(Student_perf=data.position1)
                            pos2_val=total_performance.objects.get(Student_perf=data.position2)
                            t_a=(pos1_val.total+pos2_val.total)/2
                        else:
                            pos1_val=total_performance.objects.get(Student_perf=data.position1)
                            t_a=pos1_val.total
                        team_performance_history.objects.create(team_p_id=data,total_perf=t_a)
                        History.objects.create(student_history=data.position1, student_team= data, student_position=1)
                        if data.position2 is not None:
                            History.objects.create(student_history=data.position2, student_team= data, student_position=2)
                        if data.position3 is not None:
                            History.objects.create(student_history=data.position3, student_team= data, student_position=3)
                        return redirect('/dashboard/groups/')
                    else:
                        context['form']=form_team_add()
                        context.update({'message':'Invalid Type Data Added'})
                        return render(request, "dashboard_app/group.html",context)
                except Exception as e:
                    context['form']=form_team_add()
                    context.update({'message':str(e)})
                    return render(request, "dashboard_app/group.html",context)

            # on GET request From AJAX
            elif request.method == 'GET' and request.is_ajax():
                json_list=dict()
                json_list['student']=list(Student_Enroll.objects.all().values())
                json_list['team_hist']=list(History.objects.all().values())
                json_list['team']=list(team.objects.all().values())
                json_list['predictions']=list(predictions.objects.all().values())
                json_list['tp']=list(total_performance.objects.all().values())
                return HttpResponse(json.dumps(json_list, cls=DjangoJSONEncoder))
            else:
                return render(request, "dashboard_app/group.html",context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def Seating_Plan_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            data=intervention.objects.all()
            team_val=team.objects.all()
            subject_val= Subject.objects.all()
            return render(request, "dashboard_app/seating_plan.html",{'name':name,'data':data, 'team_val':team_val, 'subj':subject_val})
        else:
            return redirect('/')
    else:
        return redirect('/')

def BenchMark_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            if request.method == "GET" and request.is_ajax():
                valu=request.GET.get('valu')
                bench=benchmark.objects.get(pk=valu)
                bench_min=bench.benchmark_val
                data=total_performance.objects.filter(total<= bench_min)
                data_json=list(Student_Enroll.objects.filter(pk=data.Student_pref))
                return HttpResponse(json.dumps(data_json, cls=DjangoJSONEncoder))
            elif request.method == 'POST':
                val=request.POST['benchmark_val']
                n_bench=request.POST['name_benchmark']
                ed=request.POST['end_date']
                save_bench=benchmark.objects.create(benchmark_name=n_bench,end_date=ed,benchmark_value=val)
                data=benchmark.objects.all()
                return redirect('/dashboard/benchmark/',{ 'name':name, 'data':data})

            st_data=Student_Enroll.objects.all()
            tp=total_performance.objects.all()
            data=benchmark.objects.all()
            return render(request, "dashboard_app/Benchmark.html",{'name':name, 'data':data, 'st':st_data, 'tp':tp})
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Class_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            if request.method == 'POST':
                form = form_class(request.POST)
                if form.is_valid():
                    try:
                        data=form.save()
                        data.save()
                        s=Student_Enroll.objects.all()
                        if len(s) == 0:
                            return redirect('/dashboard/enroll_student_class/')
                        return redirect('/dashboard/enroll_class/')
                    except IntegrityError as e:
                        if 'UNIQUE constraint':
                            form=form_class()
                            class_d=Class.objects.all()
                            return render(request, "dashboard_app/enroll_class.html",{'form':form, 'name':name, 'class_d':class_d,'message':'Already Existed Data'})
                return redirect('/dashboard/enroll_class/')
            elif request.method== 'GET' and request.is_ajax():
                c_pk=request.GET.get('val')
                c=Class.objects.get(c_name=c_pk)
                stud_list=list(Student_Enroll.objects.filter(s_class=c).values())
                return HttpResponse(json.dumps(stud_list))
            form=form_class()
            class_d=Class.objects.all()
            return render(request, "dashboard_app/enroll_class.html",{'form':form, 'name':name, 'class_d':class_d})
        else:
            return redirect('/')
    else:
        return redirect('/')
def Enroll_Subject_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form= form_subject()
            if request.method == 'POST':
                form = form_subject(request.POST)
                if form.is_valid():
                    data=form.save()
                    data.save()
                    d=Class.objects.all()
                    if len(d) == 0:
                        return redirect('/dashboard/enroll_class/')
                    return redirect('/dashboard/enroll_subject/')
                data=Subject.objects.all()
                return render(request, "dashboard_app/enroll_subject.html",{'form':form, 'name':name, 'data':data,'message':'Already Existed ID'})    
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            data=Subject.objects.filter(sub_teacher=c_user)
            return render(request, "dashboard_app/enroll_subject.html",{'form':form, 'name':name, 'data':data})
        else:
            return redirect('/')
    else:
        return redirect('/')
def Enroll_Student_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form= form_student()
            if request.method == 'POST':
                form = form_student(request.POST)
                try:
                    if form.is_valid():
                        data=form.save()
                        data.save()
                        return redirect('/dashboard/enroll_student/')
                    else:
                        form=form_enrole_student()
                        up_form=file_upload_form()
                        sub_list=Subject.objects.all()
                        data=Student_Enroll.objects.filter(s_subject= sub_list[0])
                        return render(request, 'dashboard_app/student_marks.html',{'form':form,'up_form':up_form, 'name':name,'data':data ,'sub_list':sub_list,'message':'Invalid Data or Already Exist'})

                except IntegrityError as e:
                    if 'UNIQUE constraint':
                        pass

                data=Student.objects.all()
                return render(request, 'dashboard_app/enroll_student.html',{'form':form, 'name':name, 'data':data})
            else:
                data= Student.objects.all()
                return render(request, "dashboard_app/enroll_student.html",{'form':form, 'name':name, 'data':data})
        else:
            return redirect('/')
    else:
        return redirect('/')
def Enroll_Student_class_view(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form=form_enrole_student()
            up_form=file_upload_form()
            if request.method=='POST':
                val= request.POST.get('sub')
                c_val=request.POST.get('class')
                print(val)
                form=form_enrole_student(request.POST)
                up_form=file_upload_form(request.POST, request.FILES)
                if form.is_valid() or up_form.is_valid() and up_form.is_bound:
                    if form.is_valid():
                        data=form.save()
                        data.save()
                        data.refresh_from_db()
                        pre_s=data.s_student
                        pre_s_u=Student_Enroll.objects.filter(s_student=pre_s)
                        c_pre=np.random.choice(pre_class)
                        predictions.objects.create(Student_Prediction=pre_s_u[0],prediction_class=c_pre)
                        if c_pre == 'G':
                            t_val=int(np.random.randint(85,100, size=1))
                        elif c_pre == 'A':
                            t_val=int(np.random.randint(60,84, size=1))
                        else:
                            t_val=int(np.random.randint(0,59, size=1))
                        total_performance.objects.create(Student_perf=pre_s_u[0], total=t_val)
                        return redirect('/dashboard/enroll_student_class')
                    elif up_form.is_valid():
                        
                        up=up_form.save(commit=False)
                        if up.file_upload == None:
                            return redirect('/dashboard/')
                        up.title='Questionierfile'+ up.file_upload.name
                        up.save()
                        path='media/'+up.file_upload.name

                        # making Prediction start here
                        dataset = pd.read_csv(path,encoding='ISO-8859-1')

                        # dataset=dataset.head(30)

                        # Handling missing values in dataset
                        dataset.fillna(0, inplace=True)

                        # Converting dataset into X
                        X = dataset.iloc[:, :38].values
                        df_X = pd.DataFrame(X)

                        #Applying Label Encoders
                        X[:, 4] = labelencoder_X4.transform(X[:, 4])
                        X[:, 6] = labelencoder_X6.transform(X[:, 6])
                        X[:, 24] = labelencoder_X24.transform(X[:, 24])
                        X[:, 28] = labelencoder_X28.transform(X[:, 28])
                        X[:, 29] = labelencoder_X29.transform(X[:, 29])
                        X[:, 30] = labelencoder_X30.transform(X[:, 30])
                        X[:, 31] = labelencoder_X31.transform(X[:, 31])
                        X[:, 34] = labelencoder_X34.transform(X[:, 34])

                        #Applying One Hot Encoders
                        df_9 = df_X.iloc[:, 9].values
                        df_9 = ohe_9.transform(df_9.reshape(-1, 1))
                        df_9 = pd.DataFrame(df_9, columns=["Both", "Only Father", "Only Mother"])

                        df_10 = df_X.iloc[:, 10].values
                        df_10 = ohe_10.transform(df_10.reshape(-1, 1))
                        df_10 = pd.DataFrame(df_10, columns=["Both Educated", "Both Uneducated", "Father Educated", "Mother Educated"])

                        df_11 = df_X.iloc[:, 11].values
                        df_11 = ohe_11.transform(df_11.reshape(-1, 1))
                        df_11 = pd.DataFrame(df_11, columns=["Business Man", "Dead", "Non-Services", "Services"])

                        df_12 = df_X.iloc[:, 12].values
                        df_12 = ohe_12.transform(df_12.reshape(-1, 1))
                        df_12 = pd.DataFrame(df_12, columns=["Business Woman", "Mother_Dead", "Housewife", "Job"])

                        df_14 = df_X.iloc[:, 14].values
                        df_14 = ohe_14.transform(df_14.reshape(-1, 1))
                        df_14 = pd.DataFrame(df_14, columns=["Medium", "Strong", "Weak"])
                        #
                        df_19 = df_X.iloc[:, 19].values
                        df_19 = ohe_19.transform(df_19.reshape(-1, 1))
                        df_19 = pd.DataFrame(df_19, columns=["A-Level", "FSC Pre-Engneering", "FSC Pre-Medical", "ICS"])
                        # df_19=pd.DataFrame(df_19, columns=ohe_19.get_feature_names())

                        df_25 = df_X.iloc[:, 25].values
                        df_25 = ohe_25.transform(df_25.reshape(-1, 1))
                        df_25 = pd.DataFrame(df_25, columns=["Co-Education", "Only Boys", "Only Girls"])

                        df_32 = df_X.iloc[:, 32].values
                        df_32 = ohe_32.transform(df_32.reshape(-1, 1))
                        df_32 = pd.DataFrame(df_32, columns=["By Walk", "Car", "Motorcycle", "Public Transport", "University Transport"])

                        df_35 = df_X.iloc[:, 35].values
                        df_35 = ohe_35.transform(df_35.reshape(-1, 1))
                        df_35 = pd.DataFrame(df_35, columns=["Computer Science Related", "Indoor", "Indoor Outdoor", "None", "Outdoor"])

                        #Joining in dataframe to avoid index problem
                        df_X = df_X.join(df_9)
                        df_X = df_X.join(df_10)
                        df_X = df_X.join(df_11)
                        df_X = df_X.join(df_12)
                        df_X = df_X.join(df_14)
                        df_X = df_X.join(df_19)
                        df_X = df_X.join(df_25)
                        df_X = df_X.join(df_32)
                        df_X = df_X.join(df_35)


                        sc_X7 = StandardScaler()
                        X_sc7=sc_X7.fit_transform(df_X.iloc[:,7].values.reshape(-1,1))
                        df_X[7]=pd.DataFrame(X_sc7)

                        sc_X8 = StandardScaler()
                        X_sc8=sc_X8.fit_transform(df_X.iloc[:,8].values.reshape(-1,1))
                        df_X[8]=pd.DataFrame(X_sc8)

                        sc_X13 = StandardScaler()
                        X_sc13=sc_X13.fit_transform(df_X.iloc[:,13].values.reshape(-1,1))
                        df_X[13]=pd.DataFrame(X_sc13)

                        sc_X15 = StandardScaler()
                        X_sc15=sc_X15.fit_transform(df_X.iloc[:,15].values.reshape(-1,1))
                        df_X[15]=pd.DataFrame(X_sc15)

                        sc_X16 = StandardScaler()
                        X_sc16=sc_X16.fit_transform(df_X.iloc[:,16].values.reshape(-1,1))
                        df_X[16]=pd.DataFrame(X_sc16)

                        sc_X17 = StandardScaler()
                        X_sc17=sc_X17.fit_transform(df_X.iloc[:,17].values.reshape(-1,1))
                        df_X[17]=pd.DataFrame(X_sc17)

                        sc_X18 = StandardScaler()
                        X_sc18=sc_X18.fit_transform(df_X.iloc[:,18].values.reshape(-1,1))
                        df_X[18]=pd.DataFrame(X_sc18)

                        sc_X20 = StandardScaler()
                        X_sc20=sc_X20.fit_transform(df_X.iloc[:,20].values.reshape(-1,1))
                        df_X[20]=pd.DataFrame(X_sc20)

                        sc_X21 = StandardScaler()
                        X_sc21=sc_X21.fit_transform(df_X.iloc[:,21].values.reshape(-1,1))
                        df_X[21]=pd.DataFrame(X_sc21)

                        sc_X22 = StandardScaler()
                        X_sc22=sc_X22.fit_transform(df_X.iloc[:,22].values.reshape(-1,1))
                        df_X[22]=pd.DataFrame(X_sc22)

                        sc_X23 = StandardScaler()
                        X_sc23=sc_X23.fit_transform(df_X.iloc[:,23].values.reshape(-1,1))
                        df_X[23]=pd.DataFrame(X_sc23)

                        sc_X26 = StandardScaler()
                        X_sc26=sc_X26.fit_transform(df_X.iloc[:,26].values.reshape(-1,1))
                        df_X[26]=pd.DataFrame(X_sc26)


                        sc_X33 = StandardScaler()
                        X_sc33=sc_X33.fit_transform(df_X.iloc[:,33].values.reshape(-1,1))
                        df_X[33]=pd.DataFrame(X_sc33)

                        sc_X36 = StandardScaler()
                        X_sc36=sc_X36.fit_transform(df_X.iloc[:,36].values.reshape(-1,1))
                        df_X[36]=pd.DataFrame(X_sc36)


                        #   Droping non predictable indexes
                        df_X=df_X.drop(0,axis=1)
                        df_X=df_X.drop(1,axis=1)
                        df_X=df_X.drop(2,axis=1)
                        df_X=df_X.drop(3,axis=1)
                        df_X=df_X.drop(5,axis=1)
                        df_X=df_X.drop(9,axis=1)
                        df_X=df_X.drop(10,axis=1)
                        df_X=df_X.drop(11,axis=1)
                        df_X=df_X.drop(12,axis=1)
                        df_X=df_X.drop(14,axis=1)
                        df_X=df_X.drop(19,axis=1)
                        df_X=df_X.drop(25,axis=1)
                        df_X=df_X.drop(27,axis=1)
                        df_X=df_X.drop(32,axis=1)
                        df_X=df_X.drop(35,axis=1)
                        df_X=df_X.drop(37,axis=1)


                        #Loading Classifier and Taking Prediction
                        DTC_load = joblib.load('statics/encodes/DTCsaved1.pkl')
                        load_pred = DTC_load.predict(df_X)

                        for i in range(0,len(dataset)):
                            s_name=dataset['1- Name'][i]
                            sp_name=s_name.split(" ",1)
                            Student.objects.get_or_create(s_roll_number=dataset['2- Registration Number'][i],s_first_name=sp_name[0],s_last_name=sp_name[1],s_gender=gender_dic[dataset['4- Gender'][i]], s_department='CS')
                            st=Student.objects.get(s_roll_number=dataset['2- Registration Number'][i])
                            sub=Subject.objects.get(sub_id=val)
                            c=Class.objects.get(c_name=c_val)
                            Student_Enroll.objects.get_or_create(s_student=st,s_subject=sub,s_class=c)
                            ss=Student_Enroll.objects.get(s_student=st,s_subject=sub)
                            predictions.objects.get_or_create(Student_Prediction=ss,prediction_class=pre_dic[load_pred[i]])
                            if pre_dic[load_pred[i]] == 'G':
                                t_val=int(np.random.randint(71,100, size=1))
                            elif pre_dic[load_pred[i]] == 'A':
                                t_val=int(np.random.randint(50,70, size=1))
                            elif pre_dic[load_pred[i]] == 'B':
                                t_val=int(np.random.randint(30,49, size=1))
                            # t=total_performance.objects.get(Student_perf=ss)
                            # if len(t) == 0:
                            total_performance.objects.get_or_create(Student_perf=ss, total=t_val,purpose='Predicted')
                        p=predictions.objects.all()
                        ac=0
                        bc=0
                        gc=0
                        sub=Subject.objects.get(sub_id=val)
                        for i in p:
                            if i.Student_Prediction.s_subject == sub:
                                if i.prediction_class == 'A':
                                    ac = ac+1
                                elif i.prediction_class == 'B':
                                    bc= bc+1
                                else:
                                    gc=gc+1
                        pref_class_count.objects.get_or_create(subj_of_count=sub,A_count=ac,B_count=bc, G_count=gc)
                        t_v=0
                        s=Student_Enroll.objects.filter(s_subject=sub)
                        for i in s:
                            t=total_performance.objects.get(Student_perf=i)
                            t_v=t_v+t.total
                        t_v=t_v/len(s)
                        avg_performance.objects.get_or_create(Subject_pref=sub, avg_perf=t_v)
                        return redirect('/dashboard/enroll_student_class/')
                        # except Exception as e:
                        #     sub_list=Subject.objects.all()
                        #     data=Student_Enroll.objects.filter(s_subject= sub_list[0])
                        #     return render(request, 'dashboard_app/student_marks.html',{'form':form,'up_form':up_form, 'name':name,'data':data ,'sub_list':sub_list,'message':str(e)})
                        
            
            elif request.method == 'GET' and request.is_ajax():
                su=request.GET.get('subj_s')
                cu=request.GET.get('cl_s')
                json_l=dict()
                sub=Subject.objects.get(sub_id=su)
                cla=Class.objects.get(c_name=cu)
                json_l['sub']=list(Subject.objects.filter(sub_id=su).values())
                json_l['stud_enroll']=list(Student_Enroll.objects.filter(s_subject=sub,s_class=cla).values())
                return HttpResponse(json.dumps(json_l, cls=DjangoJSONEncoder))

            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            sub_list=Subject.objects.filter(sub_teacher=c_user)
            class_list=Class.objects.all()
            data=Student_Enroll.objects.filter(s_subject= sub_list[0], s_class=class_list[0])
            return render(request, 'dashboard_app/student_marks.html',{'form':form,'up_form':up_form, 'name':name,'data':data ,'sub_list':sub_list,'class_list':class_list})
        else:
            return redirect('/')    
    else:
        return redirect('/')

def Enroll_Assignment_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form= form_assignment()
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            sub_list=Subject.objects.filter(sub_teacher=c_user)
            ass=Assignment.objects.filter(ass_subject = sub_list[0])
            context={'form':form, 'name':name, 'sub_list':sub_list, 'ass':ass}
            json_dict= dict()
            if request.method == 'GET' and request.is_ajax():
                json_dict['assignments']=list(Assignment.objects.all().values())
                return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder))
            elif request.method == 'POST':
                form = form_assignment(request.POST)
                if form.is_valid():
                    try:
                        data=form.save()
                        data.save()
                    except IntegrityError as e:
                        if 'UNIQUE constraint':
                            context.update({'message':'Cannot Add Already Exist'})
                            return render(request,'dashboard_app/enroll_assignment.html', context)        
                    return redirect('/dashboard/enroll_assignment/')
                else:
                    context['form']=form_assignment()
                    context.update({'message':'Invalid Data Enterd or Already Added'})
                    return render(request,'dashboard_app/enroll_assignment.html',context)
            return render(request, "dashboard_app/enroll_assignment.html", context)
        else:
            return redirect('/')
    else:
        return redirect('/')


def Enroll_Assignment_Marks_View(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            # form= form_assignment_marks()
            if request.method== 'POST' :
                name=request.session['username']
                form_ass= form_assignment()
                sub_list=Subject.objects.all()
                ass=Assignment.objects.filter(ass_subject = sub_list[0])
                context={'form':form_ass, 'name':name, 'sub_list':sub_list, 'ass':ass}
                form = file_upload_form(request.POST, request.FILES)
                if form.is_bound and form.is_valid():
                    d=form.save()
                    if d.file_upload != None:
                        ass=Assignment.objects.get(pk=pk)
                        ss=AssignmentMarks.objects.filter(assm_assignment=ass)
                        if len(ss) ==0:
                            d.title= ass.ass_subject.sub_id + ass.ass_title + d.file_upload.name
                            d.save()
                            print(d.file_upload)
                            path='media/'+d.file_upload.name
                            df=pd.read_csv(path,encoding='ISO-8859-1')
                            s_a= None
                            for row in range(0,len(df)):
                                try:
                                    st=Student.objects.get(s_roll_number=df['Reg.No.'][row])
                                    s_a=Student_Enroll.objects.get(s_subject=ass.ass_subject, s_student=st)
                                    AssignmentMarks.objects.get_or_create(assm_student=s_a, assm_assignment=ass, assm_obtained_marks=df[ass.ass_title][row])
                                    csv_total(ass.ass_subject,s_a)
                                except Exception as e:
                                    form=file_upload_form()
                                    ass=Assignment.objects.get(pk=pk)
                                    t_mark=ass.ass_total_marks
                                    st=Student_Enroll.objects.filter(s_subject=ass.ass_subject)
                                    return render(request, "dashboard_app/enroll_assignment_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            #  calculating avarage
                            if s_a is not None:
                                cal_avg(s_a)
                            return redirect('/dashboard/enroll_assignment/')
                        else:
                            context.update({'message':'Already Exist Data'})
                            return render(request, 'dashboard_app/enroll_assignment.html', context)
                    else:
                        ass=Assignment.objects.get(pk=pk)
                        t_mark=ass.ass_total_marks
                        ex=AssignmentMarks.objects.filter(assm_assignment=ass)
                        st=None
                        if len(ex) == 0:  
                            for key, value in request.POST.items():
                                if(key != 'csrfmiddlewaretoken'):
                                    try:
                                        s=Student.objects.get(s_roll_number=str(key))
                                        st=Student_Enroll.objects.filter(s_student=s, s_subject=ass.ass_subject)[0]
                                        AssignmentMarks.objects.get_or_create(assm_student=st,assm_assignment= ass, assm_obtained_marks=value)
                                        csv_total(ass.ass_subject,st)
                                    except Exception as e:
                                        form=file_upload_form()
                                        ass=Assignment.objects.get(pk=pk)
                                        t_mark=ass.ass_total_marks
                                        st=Student_Enroll.objects.filter(s_subject=ass.ass_subject)
                                        return render(request, "dashboard_app/enroll_assignment_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            if st is not None:
                                # calaultaing avarage
                                cal_avg(st) 
                            return redirect('/dashboard/enroll_assignment/')
                        else:
                            context.update({'message':'Already Exist Data'})
                            return render(request, 'dashboard_app/enroll_assignment.html', context)
                          
            if request.method == 'POST' and request.is_ajax():
                return redirect('/dashboard/enroll_assignment/')
            form=file_upload_form()
            ass=Assignment.objects.get(pk=pk)
            t_mark=ass.ass_total_marks
            st=Student_Enroll.objects.filter(s_subject=ass.ass_subject)
            contextz={'form':form, 'name':name,'st':st,'t_mark':t_mark,'pk':pk}
            return render(request,"dashboard_app/enroll_assignment_marks.html",contextz)
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Quiz_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            form= form_quiz()
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            sub_list=Subject.objects.filter(sub_teacher=c_user)
            ass=Quiz.objects.filter(quiz_subject = sub_list[0])
            context={'form':form, 'name':name, 'sub_list':sub_list, 'ass':ass}
            json_dict= dict()
            if request.method == 'GET' and request.is_ajax():
                json_dict['quiz']=list(Quiz.objects.all().values())
                return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder))
            elif request.method == 'POST':
                form = form_quiz(request.POST)
                if form.is_valid():
                    data=form.save()
                    data.save()
                    return redirect('/dashboard/enroll_quiz/')
                else:
                    context['form']=form_quiz()
                    context.update({'message':'Invalid Inputs or Already Added'})
                    return render(request,'dashboard_app/enroll_quiz.html',context)
            return render(request, "dashboard_app/enroll_quiz.html",context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Quiz_Marks_View(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            if request.method == 'POST':
                form_qu=form_quiz()
                sub_list=Subject.objects.all()
                ass=Quiz.objects.filter(quiz_subject = sub_list[0])
                context={'form':form_qu, 'name':name, 'sub_list':sub_list, 'ass':ass}
                form = file_upload_form(request.POST, request.FILES)
                if form.is_bound and form.is_valid():
                    d=form.save()
                    if d.file_upload != None:
                        ass=Quiz.objects.get(pk=pk)
                        ex=QuizMarks.objects.filter(quizm_quiz=ass)
                        if len(ex) == 0:
                            d.title= ass.quiz_subject.sub_id + ass.quiz_title + d.file_upload.name
                            d.save()
                            path='media/'+d.file_upload.name
                            df=pd.read_csv(path,encoding='ISO-8859-1')
                            s_a=None
                            for row in range(0,len(df)):
                                try:
                                    st=Student.objects.get(s_roll_number=df['Reg.No.'][row])
                                    s_a=Student_Enroll.objects.filter(s_subject=ass.quiz_subject, s_student=st)[0]
                                    QuizMarks.objects.get_or_create(quizm_student=s_a, quizm_quiz=ass, quizm_obtained_marks=df[ass.quiz_title][row])
                                    csv_total(ass.quiz_subject,s_a)
                                except Exception as e:
                                    form=file_upload_form()
                                    ass=Quiz.objects.get(pk=pk)
                                    t_mark=ass.quiz_total_marks
                                    st=Student_Enroll.objects.filter(s_subject=ass.quiz_subject)
                                    return render(request, "dashboard_app/enroll_quiz_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                                    
                            if s_a is not None:
                                #  calculating avarage
                                cal_avg(s_a)
                            return redirect('/dashboard/enroll_quiz/')
                        else:
                            context['form']=form_quiz()
                            context.update({'message':'Already Added'})
                            return render(request, 'dashboard_app/enroll_quiz.html',context)

                    else:
                        ass=Quiz.objects.get(pk=pk)
                        ex=QuizMarks.objects.filter(quizm_quiz=ass)
                        st= None
                        if len(ex) == 0:
                            t_mark=ass.quiz_total_marks  
                            for key, value in request.POST.items():
                                if(key != 'csrfmiddlewaretoken'):
                                    try:
                                        s=Student.objects.get(s_roll_number=key)
                                        st=Student_Enroll.objects.filter(s_student=s, s_subject=ass.quiz_subject)[0]
                                        QuizMarks.objects.get_or_create(quizm_student=st,quizm_quiz= ass, quizm_obtained_marks=value)
                                        csv_total(ass.quiz_subject,st)
                                    except Exception as e:
                                        form=file_upload_form()
                                        ass=Quiz.objects.get(pk=pk)
                                        t_mark=ass.quiz_total_marks
                                        st=Student_Enroll.objects.filter(s_subject=ass.quiz_subject)
                                        return render(request, "dashboard_app/enroll_quiz_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            
                            if st is not None:
                                cal_avg(st)
                            return redirect('/dashboard/enroll_quiz/')
                        else:
                            context['form']=form_quiz()
                            context.update({'message':'Already Added'})
                            return render(request, 'dashboard_app/enroll_quiz.html', context)
            
            form=file_upload_form()
            ass=Quiz.objects.get(pk=pk)
            t_mark=ass.quiz_total_marks
            st=Student_Enroll.objects.filter(s_subject=ass.quiz_subject)
            return render(request, "dashboard_app/enroll_quiz_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark})
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Sessional_View(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name = request.session['username']
            form = form_sessional()
            ca_user=User.objects.get(username=request.user)
            c_user=Teacher.objects.get(t_teacher=ca_user)
            sub_list=Subject.objects.filter(sub_teacher=c_user)
            ass=Enroll_Sessional.objects.filter(ses_subject = sub_list[0])
            context={'form':form, 'name':name, 'sub_list':sub_list, 'ass':ass}
            json_dict= dict()
            if request.method == 'GET' and request.is_ajax():
                json_dict['sessional']=list(Enroll_Sessional.objects.all().values())
                return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder))
            elif request.method == 'POST':
                form = form_sessional(request.POST)
                if form.is_valid():
                    data = form.save()
                    data.save()
                    return redirect('/dashboard/enroll_sessional/')
                else:
                    context['form']=form_sessional()
                    context.update({'message':'Invalid Form or Already Added Data'})
                    return render(request,'dashboard_app/enroll_sessional.html',context)
            
            return render(request, "dashboard_app/enroll_sessional.html",context)
        else:
            return redirect('/')
    else:
        return redirect('/')


def Enroll_Sessional_Marks_View(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            if request.method == 'POST':
                form_sess = form_sessional()
                sub_list=Subject.objects.all()
                ass=Enroll_Sessional.objects.filter(ses_subject = sub_list[0])
                context={'form':form_sess, 'name':name, 'sub_list':sub_list, 'ass':ass}
                form = file_upload_form(request.POST, request.FILES)
                if form.is_bound and form.is_valid():
                    d=form.save()
                    if d.file_upload != None:
                        ass=Enroll_Sessional.objects.get(pk=pk)
                        ex=SessionalMarks.objects.filter(sesm_sessional=ass)
                        if len(ex) == 0:
                            d.title= ass.ses_subject.sub_id + ass.ses_title + d.file_upload.name
                            d.save()
                            path='media/'+d.file_upload.name
                            df=pd.read_csv(path,encoding='ISO-8859-1')
                            s_a=None
                            for row in range(0,len(df)):
                                try:
                                    st=Student.objects.get(s_roll_number=df['Reg.No.'][row])
                                    s_a=Student_Enroll.objects.filter(s_subject=ass.ses_subject, s_student=st)[0]
                                    SessionalMarks.objects.get_or_create(sesm_student=s_a, sesm_sessional=ass, sesm_obtained_marks=df[ass.ses_title][row])
                                    csv_total(ass.ses_subject,s_a)
                                except Exception as e:
                                    form=file_upload_form()
                                    ass=Enroll_Sessional.objects.get(pk=pk)
                                    t_mark=ass.ses_total_marks
                                    st=Student_Enroll.objects.filter(s_subject=ass.ses_subject)
                                    return render(request, "dashboard_app/enroll_quiz_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            if s_a is not None:
                                #  calculating avarage
                                cal_avg(s_a)
                            return redirect('/dashboard/enroll_sessional/')
                        else:
                            context['form']=form_sessional()
                            context.update({'message':'Already Added'})
                            return render(request,'dashboard_app/enroll_sessional.html',context)
                    else:

                        ass=Enroll_Sessional.objects.get(pk=pk)
                        ex=SessionalMarks.objects.filter(sesm_sessional=ass)
                        t_mark=ass.ses_total_marks 
                        st=None
                        if len(ex) == 0:
                            for key, value in request.POST.items():
                                if(key != 'csrfmiddlewaretoken'):
                                    try:
                                        s=Student.objects.get(s_roll_number=str(key))
                                        st=Student_Enroll.objects.filter(s_student=s, s_subject=ass.ses_subject)[0]
                                        SessionalMarks.objects.get_or_create(sesm_student=st,sesm_sessional= ass, sesm_obtained_marks=value)
                                        csv_total(ass.ses_subject,st)
                                    except Exception as e:
                                        form=file_upload_form()
                                        ass=Enroll_Sessional.objects.get(pk=pk)
                                        t_mark=ass.ses_total_marks
                                        st=Student_Enroll.objects.filter(s_subject=ass.ses_subject)
                                        return render(request, "dashboard_app/enroll_sessional_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            if st is not None:
                                cal_avg(st)
                            return redirect('/dashboard/enroll_sessional/')
                        else:
                            context['form']=form_sessional()
                            context.update({'message':'Already Added'})
                            return render(request,'dashboard_app/enroll_sessional.html', context)

            form=file_upload_form()
            ass=Enroll_Sessional.objects.get(pk=pk)
            t_mark=ass.ses_total_marks
            st=Student_Enroll.objects.filter(s_subject=ass.ses_subject)
            return render(request, "dashboard_app/enroll_sessional_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark})
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Final(request):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name = request.session['username']
            form = form_final()
            ass=Final.objects.all()
            context={'form':form, 'name':name,  'ass':ass}
            if request.method == 'POST':
                form = form_final(request.POST)
                if form.is_valid():
                    data = form.save()
                    data.save()
                    return redirect('/dashboard/enroll_final/')
                else:
                    context['form']=form_final()
                    context.update({'message':'Invalid Form or Already Added Data'})
                    return render(request,'dashboard_app/enroll_final.html',context)
            
            return render(request, "dashboard_app/enroll_final.html",context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def Enroll_Final_Marks(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            if request.method == 'POST':
                form_fnl = form_final()
                ass=Final.objects.filter(ses_subject = sub_list[0])
                context={'form':form_fnl, 'name':name, 'sub_list':sub_list, 'ass':ass}
                form = file_upload_form(request.POST, request.FILES)
                if form.is_bound and form.is_valid():
                    d=form.save()
                    if d.file_upload != None:
                        ass=Final.objects.get(pk=pk)
                        ex=FinalMarks.objects.filter(fnlm_final=ass)
                        if len(ex) == 0:
                            d.title= ass.fnl_subject.sub_id + d.file_upload.name
                            d.save()
                            path='media/'+d.file_upload.name
                            df=pd.read_csv(path,encoding='ISO-8859-1')
                            s_a=None
                            for row in range(0,len(df)):
                                try:
                                    st=Student.objects.get(s_roll_number=df['Reg.No.'][row])
                                    s_a=Student_Enroll.objects.get(s_subject=ass.fnl_subject, s_student=st)
                                    FinalMarks.objects.get_or_create(fnlm_student=s_a, fnlm_final=ass, fnlm_obtained_marks=df['Final'][row])
                                    csv_total(ass.fnl_subject,s_a)
                                except Exception as e:
                                    form=file_upload_form()
                                    ass=Final.objects.get(pk=pk)
                                    t_mark=ass.fnl_total_marks
                                    st=Student_Enroll.objects.filter(s_subject=ass.fnl_subject)
                                    return render(request, "dashboard_app/enroll_final_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            if s_a is not None:
                                #  calculating avarage
                                cal_avg(s_a)
                            return redirect('/dashboard/enroll_sessional/')
                        else:
                            context['form']=form_final()
                            context.update({'message':'Already Added'})
                            return render(request,'dashboard_app/enroll_final.html',context)
                    else:
                        ass=Final.objects.get(pk=pk)
                        ex=FinalMarks.objects.filter(fnlm_final=ass)
                        t_mark=ass.fnl_total_marks 
                        st=None 
                        if len(ex) == 0:
                            for key, value in request.POST.items():
                                if(key != 'csrfmiddlewaretoken'):
                                    try:
                                        s=Student.objects.get(s_roll_number=str(key))
                                        st=Student_Enroll.objects.get(s_student=s, s_subject=ass.fnl_subject)
                                        SessionalMarks.objects.get_or_create(fnlm_student=st,fnlm_final= ass, fnlm_obtained_marks=value)
                                        csv_total(ass.fnl_subject,st)
                                    except Exception as e:
                                        form=file_upload_form()
                                        ass=Final.objects.get(pk=pk)
                                        t_mark=ass.fnl_total_marks
                                        st=Student_Enroll.objects.filter(s_subject=ass.fnl_subject)
                                        return render(request, "dashboard_app/enroll_final_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark,'message':'Error Fields Missings:'+str(e)})
                            if st is not None:
                                cal_avg(st)                            
                            return redirect('/dashboard/enroll_final/')
                        else:
                            context['form']=form_final()
                            context.update({'message':'Already Added'})
                            return render(request,'dashboard_app/enroll_final.html', context)

            form=file_upload_form()
            ass=Final.objects.get(pk=pk)
            t_mark=ass.fnl_total_marks
            st=Student_Enroll.objects.filter(s_subject=ass.fnl_subject)
            return render(request, "dashboard_app/enroll_final_marks.html",{'form':form, 'name':name,'st':st,'t_mark':t_mark})
        else:
            return redirect('/')
    else:
        return redirect('/')

def Assign_marks_view(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            ass=Assignment.objects.get(pk=pk)
            t_mark=ass.ass_total_marks
            try:
                st=AssignmentMarks.objects.filter(assm_assignment=ass)
            except Exception as e:
                print(e)
                return redirect('/dashboard/enroll_assignment/')

            return render(request, "dashboard_app/marks_view.html",{'name':name,'st':st,'t_mark':t_mark})
        else:
            return redirect('/')
    else:
        return redirect('/')

def quiz_marks_view(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            ass=Quiz.objects.get(pk=pk)
            t_mark=ass.quiz_total_marks
            try:
                st=QuizMarks.objects.filter(quizm_quiz=ass)
                return render(request, "dashboard_app/quiz_mark_view.html",{'name':name,'st':st,'t_mark':t_mark})
            except Exception:
                return redirect('/dashboard/enroll_quiz/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def sessional_marks_view(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            ass=Enroll_Sessional.objects.get(pk=pk)
            t_mark=ass.ses_total_marks
            try:
                st=SessionalMarks.objects.filter(sesm_sessional=ass)
                return render(request, "dashboard_app/sess_marks_view.html",{'name':name,'st':st,'t_mark':t_mark})
            except Exception:
                return redirect('/dashboard/enroll_sessional/')
        else:
            return redirect('/')
    else:
        return redirect('/')

def final_marks_view(request,pk):
    if request.user.is_authenticated:
        if request.session.has_key('username'):
            name=request.session['username']
            ass=Final.objects.get(pk=pk)
            t_mark=ass.fnl_total_marks
            try:
                st=FinalMarks.objects.filter(fnlm_final=ass)
                return render(request, "dashboard_app/final_marks_view.html",{'name':name,'st':st,'t_mark':t_mark})
            except Exception:
                return redirect('/dashboard/enroll_final/')
        else:
            return redirect('/')
    else:
        return redirect('/')


class History_view(TemplateView):
    template_name= 'dashboard_app/History.html'

class Team_Delete(DeleteView):
    model= team
    success_url = reverse_lazy('dashboard_app:group_page')
class Team_Update(UpdateView):
    model= team
    fields=['position1','position2','position3']
    template='dashboard_app/detail_page.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team']= team.objects.all()
        context['pk']=self.kwargs['pk']
        # s=Student_Enroll.objects.filter(s_student=)
        context['tp']= total_performance.objects.all().order_by('Student_perf').distinct()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        pre_check=team.objects.get(pk=post.team_id)
        if post.position1 != pre_check.position1 or post.position2 != pre_check.position2 or post.position3 != pre_check.position3:
            if post.position1 != pre_check.position1:
                prev_team=team.objects.get(Q(position1=post.position1) | Q(position2=post.position1) | Q(position3=post.position1))
                if prev_team.position1 == post.position1:
                    prev_team.position1=pre_check.position1
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position1, inter_team=prev_team, inter_postion=1)
                    History.objects.create(student_history= prev_team.position1, student_team=prev_team, student_position= 1 )
                elif prev_team.position2 == post.position1:
                    prev_team.position2=pre_check.position1
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position2, inter_team=prev_team, inter_postion=2)
                    History.objects.create(student_history= prev_team.position2, student_team=prev_team, student_position= 2 )
                else:
                    prev_team.position3=pre_check.position1
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position3, inter_team=prev_team, inter_postion=3)
                    History.objects.create(student_history= prev_team.position3, student_team=prev_team, student_position= 3 )                
                data=intervention.objects.create(inter_student=post.position1, inter_team=pre_check,inter_postion=1)
                data.save()
                History.objects.create(student_history= post.position1, student_team=pre_check, student_position= 1 )
                post.save()
                post.refresh_from_db()
                # # craete avarage performance of team
                # if post.position2 is not None and post.position3 is not None:
                #         pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #         pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #         pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #         t_a=(pos1_val.total+pos2_val.total+pos3_val.total)/3
                # elif post.position2 is None and post.position3 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #     t_a=(pos1_val.total+pos3_val.total)/2
                # elif post.position3 is None and post.position2 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #     t_a=(pos1_val.total+pos2_val.total)/2
                # else:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     t_a=pos1_val.total
                # team_performance_history.objects.create(team_p_id=pre_check,total_perf=t_a)
                # su=Subject.objects.get(sub_id=post.position1.s_subject)
                # t_v=0
                # s=Student_Enroll.objects.filter(s_subject=su)
                # for i in s:
                #     t=total_performance.objects.get(Student_perf=s)
                #     t_v=t_v+t.total
                # t_v=t_v/len(s)
                # avg_performance.objects.create(Subject_pref=su, avg_perf=t_v)
            elif post.position2 != pre_check.position2:
                try:
                    prev_team=team.objects.get(Q(position1=post.position2) | Q(position2=post.position2) | Q(position3=post.position2))
                except team.DoesNotExist:
                    prev_team= None
                if prev_team == None:
                    pass
                elif prev_team.position1 == post.position2:
                    prev_team.position1=pre_check.position2
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position1, inter_team=prev_team, inter_postion=1)
                    History.objects.create(student_history= prev_team.position1, student_team=prev_team, student_position= 1 )
                elif prev_team.position2 == post.position2:
                    prev_team.position2=pre_check.position2
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position2, inter_team=prev_team, inter_postion=2)
                    History.objects.create(student_history= prev_team.position2, student_team=prev_team, student_position= 2 )
                else:
                    prev_team.position3=pre_check.position2
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position3, inter_team=prev_team, inter_postion=3)
                    History.objects.create(student_history= prev_team.position3, student_team=prev_team, student_position= 3 )
                data=intervention.objects.create(inter_student=post.position2, inter_team=pre_check,inter_postion=2)
                data.save()
                History.objects.create(student_history= post.position2, student_team=pre_check, student_position= 2 )
                post.save()
                post.refresh_from_db()
                # # craete avarage performance of team
                # if post.position2 is not None and post.position3 is not None:
                #         pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #         pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #         pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #         t_a=(pos1_val.total+pos2_val.total+pos3_val.total)/3
                # elif post.position2 is None and post.position3 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #     t_a=(pos1_val.total+pos3_val.total)/2
                # elif post.position3 is None and post.position2 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #     t_a=(pos1_val.total+pos2_val.total)/2
                # else:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     t_a=pos1_val.total
                # team_performance_history.objects.create(team_p_id=pre_check,total_perf=t_a)
                # su=Subject.objects.get(sub_id=post.position1.s_subject)
                # t_v=0
                # s=Student_Enroll.objects.filter(s_subject=su)
                # for i in s:
                #     t=total_performance.objects.get(Student_perf=s)
                #     t_v=t_v+t.total
                # t_v=t_v/len(s)
                # avg_performance.objects.create(Subject_pref=su, avg_perf=t_v)
            else:
                prev_team=team.objects.get(Q(position1=post.position3) | Q(position2=post.position3) | Q(position3=post.position3))
                if prev_team.position1 == post.position3:
                    prev_team.position1=pre_check.position3
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position1, inter_team=prev_team, inter_postion=1)
                    History.objects.create(student_history= prev_team.position1, student_team=prev_team, student_position= 1 )
                elif prev_team.position2 == post.position3:
                    prev_team.position2=pre_check.position3
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position2, inter_team=prev_team, inter_postion=2)
                    History.objects.create(student_history= prev_team.position2, student_team=prev_team, student_position= 2 )
                else:
                    prev_team.position3=pre_check.position3
                    prev_team.save()
                    prev_team.refresh_from_db()
                    intervention.objects.create(inter_student=prev_team.position3, inter_team=prev_team, inter_postion=3)
                    History.objects.create(student_history= prev_team.position3, student_team=prev_team, student_position= 3 )
                data=intervention.objects.create(inter_student=post.position3, inter_team=pre_check,inter_postion=3)
                data.save()
                History.objects.create(student_history= post.position3, student_team=pre_check, student_position= 3 )
                post.save()
                post.refresh_from_db()
                # create avarage performance of team
                # if post.position2 is not None and post.position3 is not None:
                #         pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #         pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #         pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #         t_a=(pos1_val.total+pos2_val.total+pos3_val.total)/3
                # elif post.position2 is None and post.position3 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos3_val=total_performance.objects.get(Student_perf=post.position3)
                #     t_a=(pos1_val.total+pos3_val.total)/2
                # elif post.position3 is None and post.position2 is not None:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     pos2_val=total_performance.objects.get(Student_perf=post.position2)
                #     t_a=(pos1_val.total+pos2_val.total)/2
                # else:
                #     pos1_val=total_performance.objects.get(Student_perf=post.position1)
                #     t_a=pos1_val.total
                # team_performance_history.objects.create(team_p_id=pre_check,total_perf=t_a)
                # su=Subject.objects.get(sub_id=post.position1.s_subject)
                # t_v=0
                # s=Student_Enroll.objects.filter(s_subject=su)
                # for i in s:
                #     t=total_performance.objects.get(Student_perf=s)
                #     t_v=t_v+t.total
                # t_v=t_v/len(s)
                # avg_performance.objects.create(Subject_pref=su, avg_perf=t_v)
    
        return redirect('/dashboard/groups/')

def inter_graph(request):
    json_dict= dict()
    ca_user=User.objects.get(username=request.user)
    c_user=Teacher.objects.get(t_teacher=ca_user)
    # json_dict['c_user']=c_user.pk
    json_dict['subject']= list(Subject.objects.filter(sub_teacher=c_user).values())
    json_dict['class']=list(Class.objects.all().values())
    json_dict['prediction']=list(predictions.objects.all().order_by('-TimeStamp').values())
    json_dict['Student']= list(Student.objects.all().values())
    json_dict['History']= list(History.objects.all().values())
    json_dict['team']= list(team.objects.all().values())
    json_dict['Student_Enroll']= list(Student_Enroll.objects.all().values())
    json_dict['intervention']= list(intervention.objects.all().order_by('-TimeStamp').values())
    json_dict['total_performance']= list(total_performance.objects.all().order_by('-TimeStamp').values())
    json_dict['avg_performance']= list(avg_performance.objects.all().order_by('-TimeStamp').values())
    json_dict['pref_class_count']= list(pref_class_count.objects.all().values())
    json_dict['Assignment']=list(Assignment.objects.all().values())
    json_dict['AssignmentMarks']=list(AssignmentMarks.objects.all().values())
    json_dict['Quiz']= list(Quiz.objects.all().values())
    json_dict['QuizMarks']=list(QuizMarks.objects.all().values())
    json_dict['Sessional']=list(Enroll_Sessional.objects.all().values())
    json_dict['SessionalMarks']=list(SessionalMarks.objects.all().values())
    json_dict['team_performance_history']=list(team_performance_history.objects.all().order_by('-TimeStamp').values())
    json_dict['total_perf_hist']=list(total_perf_hist.objects.all().order_by('-TimeStamp').values())
    json_dict['th']=list(total_perf_hist.objects.all().values())
    json_dict['tp']=list(total_performance.objects.all().values())
    return JsonResponse(json_dict,  safe=False)

def pie_chart_data(request):
    data=dict()
    data['predictions'] = list(predictions.objects.all().values())
    data['Student_Enroll']=list(Student_Enroll.objects.all().values())
    return JsonResponse(data, safe=False)

def csv_total(ass,s_a):
    ass_t=0
    quiz_t=0
    sessional_t=0
    ass_gain=0
    quiz_gain=0
    sessional_gain=0
    final_total=0
    final_gain=0
    total_p=0
    f=dict()
    # assignment
    try:
        ass_res=Assignment.objects.filter(ass_subject= ass)
        for i in range(0,len(ass_res)):
            ass_t=ass_t + int(ass_res[i].ass_total_marks)
            t_asm=AssignmentMarks.objects.filter(assm_assignment=ass_res[i], assm_student=s_a )[0]
            # for j in range(0,len(t_asm)):
            ass_gain= ass_gain + float(t_asm.assm_obtained_marks)
            ass_weight=ass_gain/ass_t
    except Exception:
        pass
    #  Quiz
    try:
        quiz_res=Quiz.objects.filter(quiz_subject= ass)
        for i in range(0,len(quiz_res)):
            quiz_t=quiz_t + int(quiz_res[i].quiz_total_marks)
            t_asm=QuizMarks.objects.filter(quizm_quiz=quiz_res[i], quizm_student=s_a )
            for j in range(0,len(t_asm)):
                quiz_gain= quiz_gain + float(t_asm[j].quizm_obtained_marks)
                quiz_weight=quiz_gain/quiz_t
    except Exception:
        pass
    #  Sessionals
    try:
        sess_res=Enroll_Sessional.objects.filter(ses_subject= ass)
        for i in range(0,len(sess_res)):
            sessional_t=sessional_t + int(sess_res[i].ses_total_marks)
            t_asm=SessionalMarks.objects.filter(sesm_sessional=sess_res[i],sesm_student=s_a)
            for j in range(0,len(t_asm)):
                sessional_gain= sessional_gain + float(t_asm[j].sesm_obtained_marks)
                sessional_weight=sessional_gain/sessional_t
    except Exception:
        pass
    # final result
    try:
        final_res=Final.objects.get(fnl_subject=ass)
        final_total=final_res.fnl_total_marks
        t_asm=FinalMarks.objects.get(fnlm_final=final_res, fnlm_student=s_a)
        final_gain=t_asm.fnlm_obtained_marks
        final_weight=final_gain/final_total
    except Exception:
        pass

    #  total preformance
    if ass_t != 0 and quiz_t != 0 and sessional_t != 0 and final_total !=0:
        total_p=(ass_weight*10) + (quiz_weight*15) + (sessional_weight*25) + (final_weight*50)
        total_p=round(total_p,2)
    else:
        if ass_t == 0 and quiz_t !=0 and sessional_t !=0 and final_total ==0:
            gg=(quiz_weight*15) + (sessional_weight*25)
            total_p=round((gg/40)*100,2)
        elif ass_t !=0 and quiz_t==0  and sessional_t !=0 and final_total == 0:
            gg=(ass_weight*10)+ (sessional_weight*25)
            total_p=round((gg/35)*100,2)
        elif ass_t !=0 and quiz_t !=0 and sessional_t== 0 and final_total == 0:
            gg= (ass_weight*10) + (quiz_weight*15)
            print(ass_weight, quiz_weight)
            total_p=round((gg/25)*100,2)
        elif ass_t==0 and quiz_t==0 and sessional_t!=0 and final_total == 0:
            total_p=round((sessional_weight*100),2)
        elif ass_t == 0 and quiz_t !=0 and sessional_t==0 and final_total == 0:
            total_p=round(quiz_weight*100,2)
        elif ass_t !=0 and quiz_t==0 and sessional_t ==0 and final_total == 0:
            total_p=round(ass_weight*100,2)
        elif ass_t == 0 and quiz_t == 0 and sessional_t == 0 and final_total !=0:
            total_p=round((final_weight*100),2)
        elif ass_t==0  and quiz_t == 0 and sessional_t !=0 and final_total !=0:
            total_p= sessional_weight*25 + final_weight*50
            total_p= round(((total_p/75)*100),2)
        elif ass_t ==0  and quiz_t !=0 and sessional_t !=0 and final_total !=0:
            total_p= quiz_weight*15 + sessional_weight*25 + final_weight*50
            total_p= round(((total_p/90)*100),2)
        elif ass_t != 0 and quiz_t == 0 and  sessional_t !=0 and final_total!=0:
            total_p= ass_weight*10 + sessional_weight*25 + final_weight*50
            total_p= round(((total_p/85)*100),2)
        elif ass_t !=0 and quiz_t !=0 and sessional_t==0 and final_total !=0:
            total_p= ass_weight*10 + quiz_weight*15 + final_weight * 50
            total_p= round(((total_p/70)*100),2)
        elif ass_t !=0 and quiz_t ==0 and sessional_t==0 and final_total !=0:
            total_p= ass_weight*10 + final_weight * 50
            total_p= round(((total_p/60)*100),2)
        elif ass_t ==0 and quiz_t !=0 and sessional_t==0 and final_total !=0:
            total_p= quiz_weight*15 + final_weight * 50
            total_p= round(((total_p/65)*100),2)
        elif ass_t !=0 and quiz_t !=0 and sessional_t!=0 and final_total ==0:
            total_p= ass_weight*10 + quiz_weight*15 + sessional_weight * 25
            total_p= round(((total_p/50)*100),2)
    # total_p=ass_weight + quiz_weight + sessional_weight
    tg=total_performance.objects.get(Student_perf=s_a)
    total_perf_hist.objects.create(stud_pref_hist=s_a,total_val=tg.total,purpose=tg.purpose)
    tg.total=total_p
    tg.purpose='Assesment'
    tg.save()

def cal_avg(s_a):
    avg=0
    se_t=Student_Enroll.objects.filter(s_subject=s_a.s_subject)
    for s in se_t:
        t_s=total_performance.objects.filter(Student_perf=s)
        for v in t_s:
            avg=avg+v.total
    avg=avg/len(se_t) 
    avg_performance.objects.create(Subject_pref=s_a.s_subject, avg_perf=avg)
    # calcutaing team avarage
    te_av=team.objects.filter(team_subj=s_a.s_subject)
    for ta in te_av:
        pos1=total_performance.objects.get(Student_perf=ta.position1)
        pos2=total_performance.objects.get(Student_perf=ta.position2)
        pos3=total_performance.objects.get(Student_perf=ta.position3)
        tem_av_val=(pos1.total+pos2.total+pos3.total)/3
        team_performance_history.objects.get_or_create(team_p_id=ta, total_perf=tem_av_val)