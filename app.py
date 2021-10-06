import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
from PIL import Image
import webbrowser
import matplotlib.pyplot as plt
import os
import base64

#===========  Data Loading & Functions  ==============#
MOOCS_PER_ROW = 5


st.set_page_config(page_title="MOOCs Recommender", layout='wide',page_icon=':book:')
st.title('MOOCs Recomender for System')

# url = 'http://127.0.0.1:8000/'

image = Image.open('Background.png')
excelFile = r'moocs.xlsx'
df = pd.DataFrame(pd.read_excel(excelFile))
df1 = df[['MOOCID','MOOC','URL','Topics','Languages','Time','Level','Rating','Users','Courses','Link']].fillna("UnKnown")

def Search(Topic, Language, Time, Level, data):
    rating = 0
    re = data[data['Topics'].str.contains(Topic)]
    rating = rating + 1
    re['Rating'] =  rating
    re = re[re['Time'] == Time]
    rating = rating + 1
    re['Rating'] =  rating
    re = re[re['Languages'].str.contains(Language) ]
    rating = rating + 1
    re['Rating'] =  rating
    re = re[re['Level'].str.contains(Level)]
    rating = rating + 1
    re['Rating'] =  rating
    re = re[['MOOC','URL','Time','Topics','Rating','Users','Courses']]
    
    return re

map_data = pd.DataFrame(
        np.random.randn(1, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])

page_names = ['Home', 'Making Recommend', 'How to Use and Q & A', 'Rating MOOCs','Contact Us']#,'Forum',]
st.write('<style>div.row-widget.stRadio > div{border: 3px solid #000;padding-left:50px;flex-direction:row;}</style>',unsafe_allow_html=True)
page = st.radio('',page_names,index = 0)

def display_moocs(ids, links, titles, scores, *ratings):
    components = dict()
    prev_id = 0
    if ratings:
        ratings = ratings[0]
    for idx,(m_id, link, title, score) in enumerate(zip(ids, links, titles, scores)):
        components[m_id] = dict()
        components[m_id]["link"] = link
        components[m_id]["title"] = title
        components[m_id]["score"] = score

        row = idx //MOOCS_PER_ROW
        col = idx % MOOCS_PER_ROW

        components[m_id]["row"] = row

        if col == 0:
            components[m_id]["container"] = st.container()
            cols = components[m_id]["container"].columns(5)
        else:
            components[m_id]["container"] = components[prev_id]["container"]

        prev_id = m_id

        components[m_id]["col"] = cols[col]
        components[m_id]["col"].write(f"**{title[0:50] }** ")
        #components[m_id]["col"].write(f"{components[m_id]["title"]} | {components[m_id]["score"]}")
        #components[m_id]["col"].image(components[m_id]["link"], width=180)
        components[m_id]["slider"] = components[m_id]["col"].slider('User rating', 0, 5, key = m_id)
        
        
    return components


def display_moocs_home(ids, links, titles, scores, *ratings):
    components = dict()
    prev_id = 0
    if ratings:
        ratings = ratings[0]
    for idx,(m_id, link, title, score) in enumerate(zip(ids, links, titles, scores)):
        components[m_id] = dict()
        components[m_id]["link"] = link
        components[m_id]["title"] = title
        components[m_id]["score"] = score

        row = idx //MOOCS_PER_ROW
        col = idx % MOOCS_PER_ROW

        components[m_id]["row"] = row

        if col == 0:
            components[m_id]["container"] = st.container()
            cols = components[m_id]["container"].columns(5)
        else:
            components[m_id]["container"] = components[prev_id]["container"]

        prev_id = m_id

        components[m_id]["col"] = cols[col]
        components[m_id]["col"].write(f"**{title[0:50] }**")
        components[m_id]["col"].write(f"Rating: ***{score}***")
        components[m_id]["col"].image(components[m_id]["link"], use_column_width=True)
        #components[m_id]["slider"] = components[m_id]["col"].slider('User rating', 0, 5, key = m_id)
        
        
    return components

#===========  Pages  ==============#


#===========  Making Recommend  ==============#
if page == 'Making Recommend':
    page = 'Making Recommend'
    st.markdown("## How to use")
    st.markdown("This tutorial focuses on how to use Muke recommendation software. Instruction is a relatively detailed description of something or thing in an applied style, which is convenient for people to know and understand something or thing. The instructions should be practical and realistic. One should say one and two should say two. It is not allowed to exaggerate the function and performance of the product in order to achieve a certain purpose.......")

    
    st.sidebar.markdown("## Choose necessary tags to start")

    st.sidebar.markdown("### 1. What's Topic You Want to Learn?")
    select_topic = st.sidebar.selectbox(
        'Topic You Want to Learn',
        ("Languages", "Eduaction", "Art", "Marketing", 'Business Management', 'Communication',' Computer Science', 'Economics', 'Energy and Earth Science', 'Engineering', 'Environment', 'Health', 'Humanities', 'Law', 'Social Science'
))
 
    st.sidebar.markdown("### 2. What's Language You Want to Learn with?")
    select_language = st.sidebar.selectbox(
        'Language',
        ("English", "Chinese", "Japanese",'Spanish', 'French', 'Italian', 'Brazilian', 'Catalan','Portuguese','Polish'))


    st.sidebar.markdown("### 3. Which Duation You Want?")
    select_duation = st.sidebar.selectbox(
        'Duation',
        ('Part-time','Full-Time'))


    st.sidebar.markdown("### 4. Which Eduaction Level You need? ")
    select_level = st.sidebar.selectbox(
        'Eduaction Level',
        ('Bignner','Intermidate','Advance'))


    if st.button('Start Recommend'):
        re = Search(select_topic, select_language, select_duation, select_level, df1)
        latest_iteration = st.empty()
        bar = st.progress(0)
        l = len(re)
        for i in range(l):
            latest_iteration.text(f'Calculating {(i+1)/l*100} %')
            bar.progress((i+1)/l)
            col11, col22, col33 = st.columns(3)
            col11.metric(label="MOOC", value=str(re['MOOC'].iloc[i]), delta=None)
            st.metric(label="URL", value=str(re['URL'].iloc[i]), delta=None)
            x = re['Rating'].iloc[i]#st.slider('choose a number',1,5)
            col33.metric(label="Rating", value=str(re['Rating'].iloc[i]) + "/5", delta=None)
            
            col1, col2, col3=st.columns([2,0.2,2])
            with col1:
                st.empty()
            with col2:
                if x==1:
                    st.markdown(":star:")
                if x==2:
                    st.markdown(":star::star:")
                if x==3:
                    st.markdown(":star::star::star:")
                if x==4:
                    st.markdown(":star::star::star::star:")
                if x==5:
                    st.markdown(":star::star::star::star::star:")
            with col3:
                st.empty()
            #st.metric(label="Topics", value=str(re['Topics'].iloc[i]), delta=None)
            time.sleep(0.05)
          # Update the progress bar with each iteration and show results

        

        
#=========== How to Use  ==============#
        
elif page == 'How to Use and Q & A':
    st.markdown("## How to use")
    st.markdown("### Step 1. Go to 'Making Recommend' page ")
    st.markdown("This tutorial focuses on how to use Muke recommendation software. Instruction is a relatively detailed description of something or thing in an applied style, which is convenient for people to know and understand something or thing. The instructions should be practical and realistic. One should say one and two should say two. It is not allowed to exaggerate the function and performance of the product in order to achieve a certain purpose.......")
    st.markdown("### Step 2. Choosing the necessary tags")
    st.markdown("This tutorial focuses on how to use Muke recommendation software. Instruction is a relatively detailed description of something or thing in an applied style, which is convenient for people to know and understand something or thing. The instructions should be practical and realistic. One should say one and two should say two. It is not allowed to exaggerate the function and performance of the product in order to achieve a certain purpose.......")
    st.markdown("### Step 3. Click 'Start Recommend' to get results")
    st.markdown("This tutorial focuses on how to use Muke recommendation software. Instruction is a relatively detailed description of something or thing in an applied style, which is convenient for people to know and understand something or thing. The instructions should be practical and realistic. One should say one and two should say two. It is not allowed to exaggerate the function and performance of the product in order to achieve a certain purpose.......")
    st.markdown("### Q & A")
    st.markdown("Now that you understand the impact of question and answer technology and you’ve implemented a Q&A solution on your website, read on for five tips for making the most of this solution.")
    st.markdown("If you’re not sure about the volume of questions your team will be equipped to handle, take it slow. Launch Q&A on a few product pages, or on a specific category, to get a sense for the volume and types of questions you’ll be receiving. At PowerReviews, we recommend launching on your most popular products so you get a good baseline expectation and can adjust bandwidth accordingly.")
    st.markdown("Questions asked on your site can go to different question queues based on the type of question. You can keep it simple and route all questions to a general queue, or you can route specific questions to different kinds of people. For example, maybe you want questions about shipping to go to a subject matter expert, but you want any questions having to do with a product and its use to go to a product owner.")
    

    

#=========== Contact Us  ==============#
    
elif page == 'Contact Us':
    left_column1,left_column2 = st.columns(2)
    with left_column1:
        st.map(map_data)
    with left_column2:
        st.markdown("### Team Members: AAAAAA, BBBBBB, CCCCCC")
        st.markdown("### AAAAAA Email Adress: XXXXXXXXXX@XXXXX.com")
        st.markdown("### BBBBBB Email Adress: XXXXXXXXXX@XXXXX.com")
        st.markdown("### CCCCCC Email Adress: XXXXXXXXXX@XXXXX.com")
# #=========== Forum  ==============#        
# elif page == 'Forum':        
#     st.markdown("## Welcome to use our Forum!")
#     st.markdown("This tutorial focuses on how to use Muke recommendation software. Instruction is a relatively detailed description of something or thing in an applied style, which is convenient for people to know and understand something or thing. The instructions should be practical and realistic. One should say one and two should say two. It is not allowed to exaggerate the function and performance of the product in order to achieve a certain purpose.......")  
#     if st.button('Go to the Forum'):
#         webbrowser.open_new_tab(url)
        
#=========== Rating  ==============#   

elif page == 'Rating MOOCs':
    
    
    user_options = ['Choose/Tutorial','New user', 'Log in']
    radio_options = st.sidebar.empty()
    user_option = radio_options.radio('Logged_in', user_options,  0)
    if user_option == user_options[0]:
        title_description = f"## **Are you a new user?**"
        st.markdown(title_description)

        info_description = (f"## **OPTIONS:** \n " + 
            f" 1) New users please creat your account and give us feedbacks \n\n" +  
            f" 2) Create a new-user or log in to input your rating about every MOOCs Platforms")
        st.info(info_description)
    else:
        new_username = st.sidebar.text_input("Introduce your username:", 'username')
        new_password = st.sidebar.text_input("Introduce your password:", 'password', type="password")
        if user_option == user_options[1]:

            new_user_button = st.sidebar.button('Create new user')
            if new_user_button:
                try:
                    #user_id = h.add_new_user(new_username, new_password)	
                    user_name = new_username
                    if user_name:
                        st.success(f"Hello {user_name}! Your account have been successfully created")
                        time.sleep(2)
                        #user_option = radio_options.radio('Logged_in', user_options, 3)
                except:
                    st.warning('This username already exist. Try logging in or chosing a diferent username')

        if user_option == user_options[2]:

            user_id = 1
            if user_id:
                user_name = new_username
                st.success(f"Hello {user_name}! Your are now logged in")
                time.sleep(2)
                st.markdown("## List of all MOOCs Platforms")
                st.markdown("Here, users can score each MOOC platform and evaluate the comprehensive level of the platform through scoring, so as to help us improve the recommended content in the future")

                scores = df1['Rating']
                titles = df1['MOOC']
                ids = df1['MOOCID']
                links = df1['URL']


                components = display_moocs(ids, links, titles, scores)
                #h.testing_collaborative(selected_genre, years, images_per_page, offset, user_id, 'real')
            else:
                st.warning("This username and password combination do not exist in the data base")

    
    
    
#=========== Home  ==============#    
else:
    
    st.markdown("## About this Application")
    left_column1,left_column2 = st.columns(2)
    left_column2.image(image, use_column_width=True)
    left_column1.markdown("Students as well as professionals are increasingly choosing online education to pursue their educational goals and careers. With more than one in three learners taking at least one online course, and one in seven choosing to study exclusively online, it is hardly surprising that we are experiencing a growing number of available online programs.")
    left_column1.markdown("Students as well as professionals are increasingly choosing online education to pursue their educational goals and careers. With more than one in three learners taking at least one online course, and one in seven choosing to study exclusively online, it is hardly surprising that we are experiencing a growing number of available online programs.")
    left_column1.markdown("Students as well as professionals are increasingly choosing online education to pursue their educational goals and careers. With more than one in three learners taking at least one online course, and one in seven choosing to study exclusively online, it is hardly surprising that we are experiencing a growing number of available online programs.")
    left_column1.markdown("Students as well as professionals are increasingly choosing online education to pursue their educational goals and careers. With more than one in three learners taking at least one online course, and one in seven choosing to study exclusively online, it is hardly surprising that we are experiencing a growing number of available online programs.")
    left_column1.markdown("### We’re an education resource supporting online learners to succeed in every aspect of their learning. Our technology and services exist to make your experience easier.")
    
    st.markdown("## List of all MOOCs Platforms")
    scores = df1['Rating']
    titles = df1['MOOC']
    ids = df1['MOOCID']
    links = df1['Link']


    components = display_moocs_home(ids, links, titles, scores)
    
# def click_home():
#     left_column1,left_column2,left_column3, left_column4 = st.columns(4)
#     # You can use a column just like st.sidebar:
#     left_column1.button('Home')
#     #left_column2.button('Making Recommend')
#     left_column3.button('How to Use')
#     left_column4.button('Contact Us')
#     # Or even better, call Streamlit functions inside a "with" block:
#     with left_column2:
#          st.button('Making Recommend', on_click = click_recommend)
# def click_recommend():
    
# def click_howtouse():
#     page = 2
# def click_contactus():
#     page = 3


# left_column1,left_column2,left_column3, left_column4 = st.columns(4)
# # You can use a column just like st.sidebar:
# left_column1.button('Home')
# #left_column2.button('Making Recommend')
# left_column3.button('How to Use')
# left_column4.button('Contact Us')
# # Or even better, call Streamlit functions inside a "with" block:
# with left_column2:
#      st.button('Making Recommend', on_click = click_recommend)

# if page = 'Making Recommend':
    
    #Top page    
    # 1. reporting, 2. piedictive 3.

    
    


