import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
load_dotenv()
import io
import os

# Page config
st.set_page_config(page_title="Text to Speech Converter", layout="wide")

# Title
st.title("Text to Speech Converter")

# Initialize ElevenLabs client
api_key = st.secrets("ELEVENLABS_API_KEY")  # Store your API key in Streamlit secrets


client =ElevenLabs(api_key=api_key)

VOICES = {
    "Voice 1": "7fbQ7yJuEo56rYjrYaEh",
    "Voice 2": "XB0fDUnXU5powFXDhCwa",
    "Voice 6": "nPczCjzI2devNBz1zQrb",
    "Voice 7": "Xb7hH8MSUJpSbSDYk0k2",
    "Voice 8": "9BWtsMINqrJLrRacOk9x",
    "Voice 9": "pqHfZKP75CvOlQylNhV4",
    "Voice 10": "N2lVS1w4EtoT3dr4eOWO",
    "Voice 11": "onwK4e9ZLuTAKqWW03F9",
    "Voice 12": "Z3R5wn05IrDiVCyEkUrK",
    "Voice 13": "cgSgspJ2msm6clMCkdW9",
    "Voice 14": "FGY2WhTYpPnrIDTdsKH5",
    "Voice 15": "TX3LPaxmHKxFdv7VOQHJ"
}

# Sidebar for input controls
with st.sidebar:
    st.header("Settings")
    
    # Voice selection
    selected_voice = st.selectbox(
        "Select Voice",
        options=list(VOICES.keys())
    )
    
    # Audio format selection - simplified to MP3 formats that work better with Streamlit
    output_format = st.selectbox(
        "Select Audio Quality",
        options=[
   # Medium quality
            "mp3_22050_32"    # Low quality
        ],
        format_func=lambda x: {
            "mp3_22050_32": "Low Quality (32kbps)"
        }[x]
    )

# Main content
text_input = st.text_area("Enter text to convert to speech", height=150)

# Function to convert generator to bytes
def generator_to_bytes(generator):
    return b"".join(list(generator))

# Generate button
if st.button("Generate Speech"):
    if text_input:
        with st.spinner("Generating audio..."):
            try:
                # Generate audio
                audio_stream = client.text_to_speech.convert(
                    text=text_input,
                    voice_id=VOICES[selected_voice],
                    model_id="eleven_turbo_v2_5",
                    output_format=output_format
                )
                
                # Convert generator to bytes
                audio_data = generator_to_bytes(audio_stream)
                
                # Save to temporary file for Streamlit audio player
                with open("temp_audio.mp3", "wb") as f:
                    f.write(audio_data)
                
                # Display audio player
                st.audio("temp_audio.mp3")
                
                # Download button
                st.download_button(
                    label="Download Audio",
                    data=audio_data,
                    file_name="generated_speech.mp3",
                    mime="audio/mpeg"
                )
                
            except Exception as e:
                st.error(f"Error generating audio: {str(e)}")
    else:
        st.warning("Please enter some text to convert to speech.")

# Add instructions
st.markdown("""
### Instructions:
1. Enter your text in the text area above
2. Select your preferred voice from the sidebar
3. Choose your desired audio quality:
   - High Quality: Best for music and professional use
   - Medium Quality: Good for most speech
   - Low Quality: Smaller file size, suitable for basic speech
4. Click 'Generate Speech' to create the audio
5. Use the audio player to listen to the generated speech
6. Click 'Download Audio' to save the file
""")

# Cleanup temporary file on session end
if 'temp_audio.mp3' in globals():
    import os
    try:
        os.remove("temp_audio.mp3")
    except:
        pass
