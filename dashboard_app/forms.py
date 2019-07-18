from django import forms
from Login_app.choices import *
from dashboard_app.models import *


def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")

class file_upload_form(forms.ModelForm):
    class Meta:
        model=uploaded_csv
        fields= ('file_upload',)
        widgets={
        'file_upload':forms.FileInput(attrs={'class':'form-control','accept': ".csv"})
        }


class benchmark_form(forms.ModelForm):
    class Meta:
        model= benchmark
        fields='__all__'

class form_class(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        # labels={'c_name':'Class Name'}
        widgets={
        'c_name': forms.TextInput(
        attrs={
                'class': 'form-control',
                'placeholder': 'Class Name (E.g. FA15-BCS-A)',
            }),
      

        }

class form_team(forms.ModelForm):
    class Meta:
        model= team
        exclude=['team_subj']

        widgets={
            'team_id':forms.TextInput(attrs={
                'readonly':'readonly',
                'class':'form-control',
                }),
            'position1':forms.Select(attrs={
                'class':'form-control',
                }),
            'position2':forms.Select(attrs={
                'class':'form-control',
                }),
            'position3':forms.Select(attrs={
                'class':'form-control',
                })
        }
class form_team_add(forms.ModelForm):
    class Meta:
        model= team
        fields='__all__'

        widgets={
            'team_subj':forms.Select(attrs={
                'class':'form-control',
                }),
            'position1':forms.Select(attrs={
                'class':'form-control',
                }),
            'position2':forms.Select(attrs={
                'class':'form-control',
                }),
            'position3':forms.Select(attrs={
                'class':'form-control',
                })
        }


class form_subject(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets={
        'sub_id': forms.TextInput(
        attrs= {
        'class': 'form-control',
        'placeholder': 'Subject Code/id',
        }),

        'sub_name': forms.TextInput(
        attrs = {
        'class': 'form-control',
        'placeholder': 'Subject Name',
        }),
        'sub_teacher': forms.Select(attrs={
            'class':'form-control',
        }),

        }

class form_student(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets={
        's_class':forms.Select(attrs={
            'class':'form-control'
        }),
        's_first_name':forms.TextInput(
        attrs={
        'class': 'form-control',
        'placeholder' : 'First Name'
        }),
        's_last_name':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
        's_roll_number':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Roll Number',
            }),
        's_gender': forms.Select(
        choices=gender_list,
        attrs={
            'class': 'form-control',
        }),
        's_department': forms.Select(
        choices=department_list,
        attrs={
            'class': 'form-control',
        })
        }

class form_enrole_student(forms.ModelForm):
    class Meta:
        model= Student_Enroll
        fields='__all__'
        widgets={
            's_class': forms.Select(attrs={
                'class': 'form-control'
            }),
            's_subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            's_student': forms.Select(attrs={
                'class':'form-control'
            })
        }
        labels={'s_class':'Class','s_subject':'Subject','s_student':'Students'}

class form_assignment(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        widgets={
        'ass_teacher':forms.Select(attrs={
        'class':'form-control'
        }),
        'ass_subject':forms.Select(attrs={
        'class':'form-control'
        }),
        'ass_number':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Assignment Number',
            }),
        'ass_title':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Assignment Title',
            }),
        'ass_total_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Total Marks',
            }),
        'ass_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),
        'ass_class':forms.Select(attrs={
            'class':'form-control'
            }),

        }

class form_assignment_marks(forms.ModelForm):
    class Meta:
        model = AssignmentMarks
        fields = '__all__'
        widgets={
            'assm_student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'assm_assignment': forms.Select(attrs={
                'class': 'form-control'
            }),
        'assm_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),

        }


class form_quiz(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        widgets={
            'quiz_teacher': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quiz_subject': forms.Select(attrs={
                'class': 'form-control'
            }),
        'quiz_number':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Quiz Number',
            }),
        'quiz_title':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Quiz Title',
            }),
        'quiz_total_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Total Marks',
            }),
        'quiz_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),
        'quiz_class':forms.Select(attrs={
            'class':'form-control'
            }),

        }

class form_quiz_marks(forms.ModelForm):
    class Meta:
        model = QuizMarks
        fields = '__all__'
        widgets={
            'quizm_student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quizm_quiz': forms.Select(attrs={
                'class': 'form-control'
            }),
        'quizm_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),

        }

class form_sessional(forms.ModelForm):
    class Meta:
        model = Enroll_Sessional
        fields = '__all__'
        widgets={
            'ses_teacher':forms.Select(attrs={
                'class':'form-control'
            }),
            'ses_subject': forms.Select(attrs={
                'class': 'form-control'
            }),

        'ses_number':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Sessional Number',
            }),
        'ses_title':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Sessional Title (E.g. Sessional 1 or S1)',
            }),
        'ses_total_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Total Marks',
            }),
        'ses_class':forms.Select(attrs={
            'class':'form-control'
            }),
        }

class form_sessional_marks(forms.ModelForm):
    class Meta:
        model = SessionalMarks
        fields = '__all__'
        widgets={
        'sesm_student':forms.Select(attrs={
            'class':'form-control'
        }),
        'sesm_sessional':forms.Select(attrs={
            'class':'form-control'
        }),
        'sesm_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),
        }
class form_final(forms.ModelForm):
    class Meta:
        model = Final
        fields = '__all__'
        labels={'fnl_teacher':'Teacher','fnl_subject':'Subject','fnl_total_marks':'Total Marks'}
        widgets={
            'fnl_teacher':forms.Select(attrs={
                'class':'form-control'
            }),
            'fnl_subject': forms.Select(attrs={
                'class': 'form-control'
            }),

        'fnl_total_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Total Marks',
            }),
        }
class form_final_marks(forms.ModelForm):
    class Meta:
        model =FinalMarks
        fields = '__all__'
        widgets={
        'fnlm_student':forms.Select(attrs={
            'class':'form-control'
        }),
        'fnlm_final':forms.Select(attrs={
            'class':'form-control'
        }),
        'fnlm_obtained_marks':forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Obtained Marks',
            }),
        }
