import streamlit as st
import streamlit_survey as ss

survey = ss.StreamlitSurvey("Victim Safe Support Survey")
pages = survey.pages(3, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
with pages:
    if pages.current == 0:
        st.write("How old are you?")
        age = survey.radio(
            "age",
            options=["rather not to say", "younger than 16", "16-25", "older than 25"],
            index=0,
            label_visibility="collapsed",
            horizontal=True,
        )

        if age!="younger than 16" :
            st.experimental_rerun()
        else:
            st.warning("Sorry to hear what you have been through. Unfortunately, we are unable to provide service to you at this point. Please seek medical help immediately.")
            st.stop()
    
    elif pages.current == 1:  
        st.write("How long ago did the event happen? (Best approximation if not sure.)")
        event_ago = st.number_input("Number of Days", min_value=0, value=None)

        # if event_ago:
        #     #st.experimental_rerun()
        # else:
        #     st.stop()
        
        
        if event_ago <= 3:
            st.write("The event happend within three days.")

            uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                st.write(bytes_data)
        elif (event_ago > 3) & (event_ago <= 7 ):
            st.write("The event happend more than three days and within seven days.")
        elif event_ago > 7:
            st.write("The event happend more than seven days.")

    elif pages.current == 2:
        st.write("How satisfied are you with this survey?")
        survey.select_slider(
            "Overall Satisfaction",
            options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            label_visibility="collapsed",
        )