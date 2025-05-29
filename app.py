import streamlit as st
import replicate
import os
import time

# Set up the page
st.set_page_config(page_title="Video Generation Chatbot", page_icon="🎥")

# Sidebar for API key and settings
with st.sidebar:
    st.title("🎥 Video Generation Chatbot")
    st.write("This chatbot generates videos based on your descriptions using AI.")
    
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not replicate_api.startswith('r8_'):
            st.warning('Please enter your Replicate API token!', icon='⚠️')
        else:
            st.success('API key entered!', icon='✅')
    
    st.subheader("Video Settings")
    size = st.selectbox("Video size", ["1280*720", "1920*1080", "1024*576"])
    frame_num = st.slider("Number of frames", 24, 120, 81)
    speed_mode = st.selectbox("Speed mode", 
                             ["Standard", "Fast 🚀", "Extra Juiced 🚀 (even more speed)"], 
                             index=2)
    
    st.markdown("---")
    st.markdown("Built by [Your Name]")

# Store generated videos
if 'generated_videos' not in st.session_state:
    st.session_state['generated_videos'] = []

# Main chat interface
st.title("Video Generation Chatbot")
st.caption("Describe the video you want to generate and I'll create it for you!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("video"):
            st.video(message["video"])

# Accept user input
if prompt := st.chat_input("Describe the video you want to create..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating your video...")
        
        try:
            if not replicate_api.startswith('r8_'):
                st.error("Please enter a valid Replicate API token in the sidebar!")
                st.stop()
            
            os.environ['REPLICATE_API_TOKEN'] = replicate_api
            
            # Generate video
            output = replicate.run(
                "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273",
                input={
                    "seed": -1,
                    "size": size,
                    "prompt": prompt,
                    "src_mask": "https://replicate.delivery/pbxt/N323tegI7AuoZmg0U5CuTKa7VBFC4gymhe0kT8Jk3o2sjUUj/src_mask.mp4",
                    "frame_num": frame_num,
                    "src_video": "https://replicate.delivery/pbxt/N323u1ljtNYyyaLrgw0ZLmXgepvWlBvxbJWi3sAa2VDPuNus/src_video.mp4",
                    "speed_mode": speed_mode,
                    "sample_shift": 16,
                    "sample_steps": 50,
                    "sample_solver": "unipc",
                    "src_ref_images": ["https://replicate.delivery/pbxt/N323t5X69JB1MPD4w4cDIxK4rm0BG0W2JOWBrDrR4O9HTcyp/src_ref_image_1.png"],
                    "sample_guide_scale": 5
                }
            )
            
            video_url = output
            st.session_state.generated_videos.append(video_url)
            
            message_placeholder.empty()
            st.markdown(f"Here's your generated video based on: '{prompt}'")
            st.video(video_url)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Here's your generated video based on: '{prompt}'",
                "video": video_url
            })
            
        except Exception as e:
            message_placeholder.error(f"Error generating video: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Sorry, I couldn't generate the video. Error: {str(e)}"
            })

# Display generated videos in sidebar
if st.session_state.generated_videos:
    with st.sidebar.expander("Generated Videos"):
        for i, video_url in enumerate(st.session_state.generated_videos):
            st.write(f"Video {i+1}")
            st.video(video_url)
