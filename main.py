import streamlit as st
from dotenv import load_dotenv
from src.guardrails_openai import openai_gradrails_text, openai_gradrails_image, openai_gradrails_audio, openai_gradrails_video
from src.guardrails_anthropic import graudrails_anthropic
from src.guardrails_gemini import moderate_and_respond, image_with_gemini, video_with_gemini
from src.utilities import save_all_frames
# from src.NVIDIA.guardrails_Nvidia import Nvidia_gradrails_text
from src.guardrails_ai import guardrails_ai
import pandas as pd

# Load environment variables
load_dotenv()


def main():
    col1, col2, col3, col4 = st.columns((2, 5, 5, 2))
    m1, m2, m3 = st.columns((3, 3, 3))
    m11, m22,m33 = st.columns((1, 8, 1))
    
    # Model selection
    with col2:
        st.markdown("<p style='text-align: left; line-height:6.2rem; color: black; font-size:20px;'><span style='font-weight: bold'>Select Model</span></p>", unsafe_allow_html=True)

    with col3:
        vAR_model = st.selectbox("", ["Select", "ALL", "Openai(omni-moderation-latest)", "Google (Gemini-1.5-pro)", "Anthropic (claude-3-haiku)", "NVIDIA Nemo","Graudrails AI"])

    if vAR_model == "Openai(omni-moderation-latest)":
        # Input type selection
        with col2:
            st.markdown("<p style='text-align: left; color: black; line-height:2rem; font-size:20px;'><span style='font-weight: bold'>Select Input Type</span></p>", unsafe_allow_html=True)

        with col3:
            vAR_input_type = st.selectbox("", ["Select", "Text", "Image", "Audio", "Video"])

        if vAR_input_type == "Text":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Give Input Text</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_input = st.text_area("", height=100)
            if vAR_input:
                response = openai_gradrails_text(vAR_input)
                with col3:
                    st.success(response)
        elif vAR_input_type == "Image":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Image</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_img_input = st.file_uploader("", type=["jpg", "jpeg", "png"])
            if vAR_img_input:
                with m2:
                    st.image(vAR_img_input, width=300)
                response = openai_gradrails_image(vAR_img_input)
                with col3:
                    st.success(response)
        elif vAR_input_type == "Audio":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Audio</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_Audio_input = st.file_uploader("", type=["mp3", "wav"])
            if vAR_Audio_input:
                response = openai_gradrails_audio(vAR_Audio_input)
                with col3:
                    st.success(response)
        elif vAR_input_type == "Video":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Video</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_video_input = st.file_uploader("", type=["mp4"])
            if vAR_video_input:
                response = openai_gradrails_video(vAR_video_input)
                st.json(response)

    elif vAR_model == "Google (Gemini-1.5-pro)":
        # Input type selection
        with col2:
            st.markdown("<p style='text-align: left; line-height:2rem; color: black; font-size:20px;'><span style='font-weight: bold'>Enter Input Text</span></p>", unsafe_allow_html=True)

        with col3:
            vAR_input_type = st.text_input("",)
            if vAR_input_type:
                response = moderate_and_respond(vAR_input_type)
                st.write("# ")
                st.success(response)
    
    elif vAR_model == "Anthropic (claude-3-haiku)":
        # Input type selection
        with col2:
            st.markdown("<p style='text-align: left; line-height:2rem; color: black; font-size:20px;'><span style='font-weight: bold'>Enter Input Text</span></p>", unsafe_allow_html=True)

        with col3:
            vAR_input_type = st.text_input("",)
            if vAR_input_type:
                response = graudrails_anthropic(vAR_input_type)
                st.write("# ")
                st.success(response)
    
    elif vAR_model == "ALL":
        with col2:
            st.markdown("<p style='text-align: left; color: black; line-height:2rem; font-size:20px;'><span style='font-weight: bold'>Select Input Type</span></p>", unsafe_allow_html=True)

        with col3:
            vAR_input_type = st.selectbox("", ["Select", "Text", "Image", "Audio", "Video"])
        
        if vAR_input_type == "Text":
            with m22:
                # Initialize chat history and feedback state
                if "messages" not in st.session_state:
                    st.session_state.messages = [
                        {"role": "user", "content": "We are delighted to have you here in the Live Agent Chat room!"},
                        {"role": "assistant", "content": "Hello! How can I assist you today?"}
                    ]
                    
                # Add custom CSS for styling chat
                st.markdown(
                    """
                    <style>
                    .chat-container { display: flex; align-items: center; margin: 10px 0; }
                    .chat-container.user { justify-content: flex-end; }
                    .chat-container.assistant { justify-content: flex-start; }
                    .chat-container img { width: 40px; height: 40px; border-radius: 50%; margin: 0 10px; }
                    .chat-bubble { max-width: 70%; padding: 10px; border-radius: 10px; margin: 5px 0; }
                    .chat-bubble.user { background-color: #e0e0e0; text-align: right; }
                    .chat-bubble.assistant { background-color: #ffffff; text-align: left; }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )    
                
                user_image_url = "https://storage.googleapis.com/macrovector-acl-eu/previews/118720/thumb_118720.webp"
                assistant_image_url = "https://cdn-icons-png.flaticon.com/512/6014/6014401.png"                    
                
                # Display chat history
                for i, message in enumerate(st.session_state.messages):
                    if message["role"] == "user":
                        st.markdown(
                            f'''
                            <div class="chat-container user">
                                <div class="chat-bubble user">{message["content"]}</div>
                                <img src="{user_image_url}" alt="User">
                            </div>
                            ''',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'''
                            <div class="chat-container assistant">
                                <img src="{assistant_image_url}" alt="Assistant">
                                <div class="chat-bubble assistant">{message["content"]}</div>
                            </div>
                            ''',
                            unsafe_allow_html=True,
                        )
                
                if "table_heading" in message:
                    st.write(f"### {message['table_heading']}")
                if "table" in message:
                    st.table(message["table"])
            with m22:
                prompt = st.chat_input("What else can I do to help?")
            if prompt:
                # Append user message
                st.session_state.messages.append({"role": "user", "content": prompt})   
                
                response_gcp = moderate_and_respond(prompt)
                response_openai = openai_gradrails_text(prompt)
                response_anthropic = graudrails_anthropic(prompt)
                response_guradrails_ai = guardrails_ai(prompt)
                # response_NVIDIA = Nvidia_gradrails_text(prompt)
                
                # Create a DataFrame with the JSON strings
                data = {
                    "Openai(omni-moderation-latest)": [response_openai],
                    "Google (Gemini-1.5-pro)": [response_gcp],
                    "Anthropic (claude-3-haiku)": [response_anthropic],
                    "Guardrails AI": [response_guradrails_ai],
                    # "NVIDIA Nemo": [response_NVIDIA]
                }
                df = pd.DataFrame(data)
                st.session_state.messages.append({"role": "assistant", "content": "", "table_heading": "Model Response Comparison:","table": df})
                st.rerun()
        
        elif vAR_input_type == "Image":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Image</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_img_input = st.file_uploader("", type=["jpg", "jpeg", "png"])
            if vAR_img_input:
                with m2:
                    st.image(vAR_img_input, width=300)
                response = openai_gradrails_image(vAR_img_input)
                gemini_img = image_with_gemini(vAR_img_input)
                with m2:
                    st.markdown(f"""
                                | Openai(GPT)   |Google(Gemini)|
                                |---------------|--------------|
                                |{response}     |{gemini_img}  |
                                """)
        elif vAR_input_type == "Audio":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Audio</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_Audio_input = st.file_uploader("", type=["mp3", "wav"])
            
            if vAR_Audio_input:
                response, text = openai_gradrails_audio(vAR_Audio_input)
                gemini_res = moderate_and_respond(text)
                response_graudrails_ai = guardrails_ai(text)
                
                # Create a DataFrame with the JSON strings
                data = {
                    "Openai(omni-moderation-latest)": [response],
                    "Google (Gemini-1.5-pro)": [gemini_res],
                    "Graudrails AI": [response_graudrails_ai]
                } 
                with m2:
                    df = pd.DataFrame(data)
                    st.table(df)
                    
        elif vAR_input_type == "Video":
            with col2:
                st.markdown("<p style='text-align: left; line-height:10rem; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Input Audio</span></p>", unsafe_allow_html=True)
            with col3:
                vAR_video_input = st.file_uploader("", type=["mp4"])
            if vAR_video_input:
                temp_video_path = "uploaded_video.mp4"
                with open(temp_video_path, "wb") as f:
                    f.write(vAR_video_input.getbuffer())
                # Output directory for frames
                output_dir = "frames_output"
                save_all_frames(temp_video_path, output_dir)
                vAR_img_input = "frames_output/middle_frame.jpg"
                response = openai_gradrails_video(vAR_img_input)
                # response = openai_gradrails_video(output_dir)
                gemini_video = video_with_gemini(vAR_video_input)
                # gemini_img = "Need to implement"
                with m2:
                    # Create a DataFrame with the JSON strings
                    data = {
                        "Openai(omni-moderation-latest)": [response],
                        "Google (Gemini-1.5-pro)": [gemini_video]
                    }
                    # Apply custom styling to make headers bold
                    def style_dataframe(df):
                        return df.style.set_table_styles(
                            [{'selector': 'th', 'props': [('font-weight', 'bold')]}]
                        )
                    with m2:
                        df = pd.DataFrame(data)
                        df = style_dataframe(df)
                        st.markdown(df.to_html(), unsafe_allow_html=True)
