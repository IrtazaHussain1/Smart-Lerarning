import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','SEPPS.settings')

import django
django.setup()

#faker script
import random
from dashboard_app.models import Student
# from faker import Faker
import pandas as pd

df= pd.read_csv('F:/django projects/SEPPS/statics/Data/PF_SP18-BCS-A.csv')

# fakegen=Faker()

# anime_type_fake_list=['Ninja','High School','Hentai','Action','Adventure','Darama','Comedy','Magic','Supernatural']

# def Add_Anime_Type():
#     t=AnimeType.objects.get_or_create(anime_type=random.choice(anime_type_fake_list))[0]
#     t.save()
#     return t

def Populate(N):
    st_name=df['Name']
    st__reg=df['Register_no']
    st_gender='M'
    st_department='CS'
    sp_name=st_name.str.split(n=1)
    for i in range(N):
        student_data=Student.objects.create(s_roll_number=st__reg[i],s_first_name=sp_name[i][0],s_last_name=sp_name[i][1],s_gender=st_gender,s_department=st_department)

# main
if __name__=='__main__':
    print("Starting Populating program")
    Populate(df.count().max())
    print("population crated successfully")
