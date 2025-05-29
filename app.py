import streamlit as st
import base64
from together import Together
from io import BytesIO
from PIL import Image

# Set up the page
st.set_page_config(page_title="Image Generation Chatbot", page_icon="🖼️")

# Sidebar for API key and settings
with st.sidebar:
    st.title("🖼️ Image Generation Chatbot")
    st.write("This chatbot generates images based on your descriptions using AI.")
    
    if 'TOGETHER_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        together_api = st.secrets['TOGETHER_API_KEY']
    else:
        together_api = st.text_input('Enter Together API token:', type='password')
        if not together_api.startswith(''):
            st.warning('Please enter your Together API token!', icon='⚠️')
        else:
            st.success('API key entered!', icon='✅')
    
    st.subheader("Image Settings")
    num_images = st.slider("Number of images", 1, 8, 4)
    steps = st.slider("Generation steps", 5, 50, 10)
    model = st.selectbox(
        "Model",
        [
            "black-forest-labs/FLUX.1-dev",
            "stability-ai/sdxl",
            "runwayml/stable-diffusion-v1-5"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("Built with Together AI")

# Store generated images
if 'generated_images' not in st.session_state:
    st.session_state['generated_images'] = []

# Main chat interface
st.title("Image Generation Chatbot")
st.caption("Describe the image you want to generate and I'll create it for you!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("images"):
            cols = st.columns(len(message["images"]))
            for idx, img_data in enumerate(message["images"]):
                with cols[idx]:
                    st.image(img_data, use_column_width=True)

# Accept user input
if prompt := st.chat_input("Describe the image you want to create..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating your images...")
        
        try:
            if not together_api:
                st.error("Please enter a valid Together API token in the sidebar!")
                st.stop()
            
            # Initialize Together client
            client = Together(api_key=together_api)
            
            # Generate images
            response = client.images.generate(
                prompt=prompt,
                model=model,
                steps=steps,
                n=num_images
            )
            
            generated_images = []
            cols = st.columns(num_images)
            
            for idx, img_data in enumerate(response.data[:num_images]):
                if hasattr(img_data, 'b64_json'):
                    # Decode base64 image
                    image_bytes = base64.b64decode(img_data.b64_json)
                    image = Image.open(BytesIO(image_bytes))
                    generated_images.append(image)
                    
                    # Display in column
                    with cols[idx]:
                        st.image(image, use_column_width=True)
            
            st.session_state.generated_images.extend(generated_images)
            
            message_placeholder.empty()
            st.markdown(f"Here are your generated images based on: '{prompt}'")
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Here are your generated images based on: '{prompt}'",
                "images": generated_images
            })
            
        except Exception as e:
            message_placeholder.error(f"Error generating images: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Sorry, I couldn't generate the images. Error: {str(e)}"
            })

# Display generated images in sidebar
if st.session_state.generated_images:
    with st.sidebar.expander("Generated Images"):
        for i, image in enumerate(st.session_state.generated_images):
            st.write(f"Image {i+1}")
            st.image(image, use_column_width=True)
