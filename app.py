import streamlit as st
import base64
from together import Together
from io import BytesIO
from PIL import Image

# Set up the page
st.set_page_config(page_title="Image Generation Chatbot", page_icon="🖼️")

# Serverless-compatible models
SERVERLESS_MODELS = {
    "FLUX-1 (Recommended)": "black-forest-labs/FLUX.1-dev",
    "SDXL 1.0": "stability-ai/sdxl",
    "Playground v2": "playgroundai/playground-v2-1024px-aesthetic",
    "Kandinsky 2.2": "kandinsky-community/kandinsky-2-2-decoder",
    "Realistic Vision": "SG161222/Realistic_Vision_V5.1_noVAE"
}

# Sidebar for API key and settings
with st.sidebar:
    st.title("🖼️ Image Generation Chatbot")
    st.write("This chatbot generates images based on your descriptions using AI.")
    
    if 'TOGETHER_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        together_api = st.secrets['TOGETHER_API_KEY']
    else:
        together_api = st.text_input('Enter Together API token:', type='password')
        if not together_api:
            st.warning('Please enter your Together API token!', icon='⚠️')
        else:
            st.success('API key entered!', icon='✅')
    
    st.subheader("Image Settings")
    num_images = st.slider("Number of images", 1, 4, 1)
    steps = st.slider("Generation steps", 10, 50, 20)
    model_name = st.selectbox(
        "Model",
        list(SERVERLESS_MODELS.keys()),
        index=0
    )
    
    st.markdown("---")
    st.markdown("Built with Together AI")

# Main chat interface
st.title("Image Generation Chatbot")
st.caption("Describe the image you want to generate and I'll create it for you!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
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
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating your images...")
        
        try:
            if not together_api:
                raise ValueError("API token not provided")
            
            client = Together(api_key=together_api)
            
            response = client.images.generate(
                prompt=prompt,
                model=SERVERLESS_MODELS[model_name],
                steps=steps,
                n=num_images
            )
            
            generated_images = []
            cols = st.columns(num_images)
            
            for idx, img_data in enumerate(response.data[:num_images]):
                if hasattr(img_data, 'b64_json'):
                    image_bytes = base64.b64decode(img_data.b64_json)
                    image = Image.open(BytesIO(image_bytes))
                    generated_images.append(image)
                    
                    with cols[idx]:
                        st.image(image, use_column_width=True)
            
            message_placeholder.empty()
            st.markdown(f"Generated {len(generated_images)} image(s) based on: '{prompt}'")
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Generated {len(generated_images)} image(s) based on: '{prompt}'",
                "images": generated_images
            })
            
        except Exception as e:
            message_placeholder.error(f"Error generating images: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Sorry, I couldn't generate the images. Error: {str(e)}"
            })

# Display help in sidebar
with st.sidebar.expander("Help"):
    st.write("""
    **Tips for better results:**
    - Be specific in your descriptions
    - Include style references (e.g., "photorealistic", "anime style")
    - For multiple concepts, separate with commas
    - Try different models for different styles
    """)
