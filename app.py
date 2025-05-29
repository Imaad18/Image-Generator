import streamlit as st
import base64
from together import Together
from io import BytesIO
from PIL import Image
import time

# Set up the page
st.set_page_config(page_title="Image Generation Chatbot", page_icon="🖼️")

# Serverless-compatible models with recommended settings
SERVERLESS_MODELS = {
    "FLUX-1 (Best Quality)": {
        "model": "black-forest-labs/FLUX.1-dev",
        "max_steps": 50,
        "default_steps": 30
    },
    "SDXL 1.0 (Balanced)": {
        "model": "stability-ai/sdxl",
        "max_steps": 50,
        "default_steps": 25
    },
    "Playground v2 (Aesthetic)": {
        "model": "playgroundai/playground-v2-1024px-aesthetic",
        "max_steps": 50,
        "default_steps": 20
    }
}

# Sidebar for API key and settings
with st.sidebar:
    st.title("🖼️ Image Generation Chatbot")
    st.write("Generate AI images from text prompts using Together AI")
    
    # API Key Section
    if 'TOGETHER_API_KEY' in st.secrets:
        st.success('API key loaded from secrets!', icon='✅')
        together_api = st.secrets['TOGETHER_API_KEY']
    else:
        together_api = st.text_input('Enter Together API token:', type='password')
        if not together_api:
            st.warning('Please enter your API token', icon='⚠️')
        else:
            st.success('API key entered!', icon='✅')
    
    # Model Settings
    st.subheader("Generation Settings")
    model_name = st.selectbox(
        "Select Model",
        list(SERVERLESS_MODELS.keys()),
        index=0
    )
    
    selected_model = SERVERLESS_MODELS[model_name]
    steps = st.slider(
        "Quality Steps", 
        10, 
        selected_model["max_steps"], 
        selected_model["default_steps"],
        help="More steps = better quality but slower generation"
    )
    
    num_images = st.slider(
        "Number of Images", 
        1, 
        4, 
        1,
        help="Some models may limit the number of images"
    )
    
    st.markdown("---")
    st.markdown("💡 Tip: Use descriptive prompts for best results")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("images"):
            cols = st.columns(len(message["images"]))
            for idx, img_data in enumerate(message["images"]):
                with cols[idx]:
                    st.image(img_data, use_column_width=True)

# Main chat function
def generate_images(prompt, model_info, num_images=1, steps=20):
    try:
        client = Together(api_key=together_api)
        response = client.images.generate(
            prompt=prompt,
            model=model_info["model"],
            steps=steps,
            n=num_images
        )
        
        generated_images = []
        for img_data in response.data[:num_images]:
            if not hasattr(img_data, 'b64_json') or not img_data.b64_json:
                raise ValueError("Invalid image data received from API")
            
            try:
                image_bytes = base64.b64decode(img_data.b64_json)
                image = Image.open(BytesIO(image_bytes))
                generated_images.append(image)
            except Exception as e:
                raise ValueError(f"Failed to decode image: {str(e)}")
        
        return generated_images
    
    except Exception as e:
        raise RuntimeError(f"API Error: {str(e)}")

# Handle user input
if prompt := st.chat_input("Describe the image you want to create..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        status_message = st.empty()
        status_message.markdown("🔄 Generating your images...")
        
        try:
            if not together_api:
                raise ValueError("Please enter your API key in the sidebar")
            
            start_time = time.time()
            images = generate_images(
                prompt=prompt,
                model_info=SERVERLESS_MODELS[model_name],
                num_images=num_images,
                steps=steps
            )
            generation_time = time.time() - start_time
            
            status_message.empty()
            
            if images:
                cols = st.columns(len(images))
                for idx, image in enumerate(images):
                    with cols[idx]:
                        st.image(image, use_column_width=True)
                
                st.success(f"Generated {len(images)} image(s) in {generation_time:.1f}s")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Generated {len(images)} image(s) based on: '{prompt}'",
                    "images": images
                })
            else:
                st.error("No images were generated")
        
        except Exception as e:
            status_message.error(f"❌ Error: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Failed to generate images: {str(e)}"
            })

# Add help section
with st.sidebar.expander("Prompt Guide"):
    st.write("""
    **Better Prompt Examples:**
    - "A majestic lion in the savanna at sunset, photorealistic, 8K"
    - "Cyberpunk city street at night, neon lights, rain puddles"
    - "Cute anime-style cat wearing a wizard hat, fantasy background"
    
    **Advanced Tips:**
    - Include style references (photo, painting, digital art)
    - Specify lighting (sunset, studio lighting, neon)
    - Add details (4K, ultra-detailed, intricate)
    """)
