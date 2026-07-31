import streamlit as st
import tempfile
from extractor import extract_text_from_pdf, get_results_back

class App:
    def __init__(self):
        def render_template():
            
            #Page configuration
            st.set_page_config(layout='centered')
            
            with st.container(border=False, horizontal=True, horizontal_alignment='distribute'):
                st.subheader('Resume Matcher')
                st.badge('v1.0 AI Engine', color='green')
                
            
            st.text('Match your resume against any job description in seconds.')
            
            #Upload
            with st.container(border=False):
                pdf_upload = st.file_uploader(accept_multiple_files=False, max_upload_size=20, label='Upload PDF', label_visibility='hidden',
                                              type=['.pdf'])            
                job_description = st.text_area('Job Description', placeholder='Place  the full job description here...')   
                
                #Analyze button  
                if st.button('Analyze Match', type='secondary', icon_position='right', icon=':material/arrow_forward:', width=200):
                    if len(job_description) > 10 and pdf_upload is not None:
                        
                        #Using temp file to remember the path of the uploaded document
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(pdf_upload.getbuffer())
                            temp_path = tmp.name
                            
                        
                        #Loading Animation   
                        with st.spinner('Getting Matches...'):
                            text_extract = extract_text_from_pdf(temp_path)
                            result = get_results_back(text_extract, job_description)
                            
                            if result:
                                matched, missing, recommendation, scores, status, skill_breakdown = result
                                
                                if status == "VALID":
                                    
                                    with st.container(border=False, horizontal=True, horizontal_alignment='distribute'):
                                        st.metric('Overall match score', value=scores.get("overall_match", 0))
                                        st.metric('Matched Skills Count', value=skill_breakdown.get("matched_skills_count", 0))
                                        st.metric('Missing Skills Count', value=skill_breakdown.get("missing_skills_count", 0))
                                                      
                                    tab1, tab2 = st.tabs(['🎯Keywords', '💡Recommendation'])
                                    
                                    #Tabs
                                    with tab1:
                                        st.subheader('Matched keywords')
                                        with st.container(border=False, horizontal=True):
                                            for item in matched:
                                                st.badge(item, color='green', icon=':material/check:', width='stretch')
                                        
                                        st.subheader('Missing keywords')
                                        with st.container(border=False, horizontal=True):
                                            for item in missing:
                                                st.badge(item, color='red', icon=':material/close:', width='stretch')
                                                
                                    #Tabs          
                                    with tab2:
                                        for item in recommendation:
                                            with st.container(border=True):
                                                st.text(item)                      
                                
                                                    
                                else:
                                    st.error('The provided information does not contain enough information to identify a target position!')
                                                    
                    else:
                        st.error('Job Description is too short')
                          
        render_template()
              
app = App()