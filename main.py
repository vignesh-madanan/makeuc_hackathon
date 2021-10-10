# Theme ADVANCING CONNECTIVITY
# Crime Reporting Service
# user uploads a audio/image
# run rekognition on image
# use assemblyAI for speech to text

from s3_util_service.upload_to_s3 import upload_to_aws
from rekognition_service.rekognition_image_detection import run_reko_on_s3 #run_reko_on_s3_video
from rekognition_service.rekognition_video_detection import run_reko_on_s3_video
from rekognition_service.rekognition_objects import show_bounding_boxes 
from assemblyai_stt import run_stt
import os
from PIL import Image, ImageDraw, ExifTags, ImageColor
from pydub import AudioSegment
import streamlit as st
from datetime import date
from datetime import datetime
from tinydb import TinyDB, Query
from pydub import AudioSegment
import pandas as pd

db = TinyDB('db.json')


def image_main():
    uploaded_file = st.file_uploader("Choose an image...", type=['png','jpeg', 'jpg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        print('uploaded_file', uploaded_file.name)
        filename = os.path.join('images', str(uploaded_file.name))
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(image, caption='Uploaded Image.', use_column_width=True)
        print('Upload File Name', uploaded_file.name)
        file_name = uploaded_file.name
        st.header('Output: ')
        print(upload_to_aws(filename, bucket='1hackathonbucket', s3_file=file_name))
        data, face_image = run_reko_on_s3(file_name, uploaded_file.getbuffer())
        if data['labels']:
            st.subheader('Image Scenarios')
            for l in data['labels']:
                st.text(f"Image seems to have content of {l.get('parent_name')} ")
                st.text(f"With examples of {l.get('name')}")
                st.text(f"-------------------------------------")               

        st.subheader('Faces and Facial Features')
        if face_image:
            for ix,face_c in enumerate(face_image): 
                f = data['faces'][ix]
                st.image(face_c)
                st.text(f"Gender: {f.get('gender')} age between {f.get('age')}")
                st.text(f"Facial Features {f.get('has')}")
            print('Image ')
            st.text(f"Facial Features: {f.get('has')}")

        return data


def main():
    st.header('AnnonTip-AI👈')
    st.text("Aimed to report crime/incidents that\n may occur in the community. The form is annoymous")
    st.text('We look to you who live in these communities we protect to provide us with information about violence or incidents')

    
    add_selectbox = st.sidebar.selectbox("Select or View..👈👈👈",("Report Incidents", "View Incidents"))
    st.sidebar.text('Made by Vignesh Madanan')
    st.sidebar.text('For MakeUC hackathon')
    
    if add_selectbox == "Report Incidents":
        is_crime = st.radio("What kind of a tip is this", ['Crime', 'Incident'])
        if is_crime == 'Crime':
            st.header('Enter Details of Crime') 
            description = st.text_input('Crime Description: (including..Who, What, Where, When and How Do You Know?) *')
            if not description:
                st.warning("Please fill crime Description")

            address = st.text_input('Location where this crime occurred? *')

        else:
            st.header('Enter Details of Incident') 

            description = st.text_input('Incident Description: (including..Who, What, Where, When and How Do You Know?) *')
            if not description:
                st.warning("Please fill incident Description")
            address = st.text_input('Location where this incident occurred? *')

        zipcode = st.text_input("zipcode")

        if not zipcode:
            st.warning("Please fill Zipcode")

        __date__ = date.today()
        __time__ = datetime.now().time()

        is_image = st.radio("Image/Audio file", ['Image', 'Audio'])

        data = None

        if is_image == 'Image':

            d = image_main()
            data = {'image': d}
            type_ = 'image'

        else:
            audio_file_name = st.file_uploader("Upload file.....",type=['mp3','wav'])
            type_ = 'audio'
            print(audio_file_name)
            if audio_file_name is not None:
                audio_file_name_path = f"./audio/{audio_file_name.name}"
                if os.path.exists(audio_file_name_path):
                    os.remove(audio_file_name_path)
                with open(audio_file_name_path, mode='bx') as f:
                    f.write(audio_file_name.read())
                # audio_file_name_path = audio_file_name.name
                file_name = os.path.basename(audio_file_name_path)
                print('upload_to_aws', upload_to_aws(audio_file_name_path, bucket='1hackathonbucket', s3_file=file_name))
                if st.button('Run Transcription'):
                    url = f"https://1hackathonbucket.s3.us-east-2.amazonaws.com/{file_name}"
                    tx = run_stt(url)
                    st.header('Transcribed Text:', tx)
                    st.text(tx)
                    data = {'audio': {'transcription': tx} }
                else:
                    data = {'audio': None}

        final_data = {'zipcode':zipcode, 'address':address, 'description':description, 'crime_type': is_crime, 'data': data, 'type': type_,'date':str(__date__),'time':str(__time__)}
        
        if st.button('Submit Form'):
            
            db.insert(final_data)
            st.warning('Added to incidents..')
    else:
        df = pd.DataFrame(db.all())
        print(df)
        df.dropna(inplace=True)
        st.dataframe(df)


if __name__ == '__main__':
    main()