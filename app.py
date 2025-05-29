import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import requests
from together import Together

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Title and description
st.title("🎨 AI Image Generator")
st.markdown("Generate stunning images using Together AI's FLUX.1-dev model")

# Sidebar for API key and settings
st.sidebar.header("⚙️ Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "Together AI API Key",
    type="password",
    help="Enter your Together AI API key"
)

# Model selection
model_options = [
    "black-forest-labs/FLUX.1-dev",
    "black-forest-labs/FLUX.1-schnell"
]
selected_model = st.sidebar.selectbox(
    "Select Model",
    model_options,
    index=0
)

# Generation parameters
st.sidebar.subheader("Generation Settings")

steps = st.sidebar.slider(
    "Steps",
    min_value=1,
    max_value=50,
    value=10,
    help="Number of inference steps"
)

num_images = st.sidebar.slider(
    "Number of Images",
    min_value=1,
    max_value=4,
    value=2,
    help="Number of images to generate"
)

# Image dimensions (if supported by the model)
width = st.sidebar.selectbox(
    "Width",
    [512, 768, 1024],
    index=2
)

height = st.sidebar.selectbox(
    "Height", 
    [512, 768, 1024],
    index=2
)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎯 Prompt")
    
    # Prompt input
    prompt = st.text_area(
        "Enter your image prompt",
        height=100,
        placeholder="Describe the image you want to generate...",
        value="Cats eating popcorn"
    )
    
    # Negative prompt (optional)
    negative_prompt = st.text_area(
        "Negative prompt (optional)",
        height=80,
        placeholder="What you don't want in the image..."
    )
    
    # Generate button
    generate_btn = st.button(
        "🚀 Generate Images",
        type="primary",
        use_container_width=True
    )

with col2:
    st.subheader("🖼️ Generated Images")
    
    if generate_btn:
        if not api_key:
            st.error("Please enter your Together AI API key in the sidebar.")
        elif not prompt.strip():
            st.error("Please enter a prompt to generate images.")
        else:
            try:
                # Initialize Together client
                client = Together(api_key=api_key)
                
                # Show loading spinner
                with st.spinner("Generating images... This may take a few moments."):
                    
                    # Prepare parameters
                    generation_params = {
                        "prompt": prompt,
                        "model": selected_model,
                        "steps": steps,
                        "n": num_images,
                        "width": width,
                        "height": height
                    }
                    
                    # Add negative prompt if provided
                    if negative_prompt.strip():
                        generation_params["negative_prompt"] = negative_prompt
                    
                    # Generate images
                    response = client.images.generate(**generation_params)
                    
                    # Display generated images
                    if response.data:
                        st.success(f"Generated {len(response.data)} image(s)!")
                        
                        # Create columns for images
                        if len(response.data) == 1:
                            cols = [st.container()]
                        elif len(response.data) == 2:
                            cols = st.columns(2)
                        else:
                            cols = st.columns(2)
                        
                        for i, image_data in enumerate(response.data):
                            col_idx = i % len(cols)
                            
                            with cols[col_idx]:
                                try:
                                    # Decode base64 image
                                    image_bytes = base64.b64decode(image_data.b64_json)
                                    image = Image.open(BytesIO(image_bytes))
                                    
                                    # Display image
                                    st.image(
                                        image,
                                        caption=f"Generated Image {i+1}",
                                        use_container_width=True
                                    )
                                    
                                    # Download button
                                    img_buffer = BytesIO()
                                    image.save(img_buffer, format='PNG')
                                    img_bytes = img_buffer.getvalue()
                                    
                                    st.download_button(
                                        label=f"📥 Download Image {i+1}",
                                        data=img_bytes,
                                        file_name=f"generated_image_{i+1}.png",
                                        mime="image/png",
                                        use_container_width=True
                                    )
                                    
                                except Exception as img_error:
                                    st.error(f"Error processing image {i+1}: {str(img_error)}")
                    else:
                        st.error("No images were generated. Please try again.")
                        
            except Exception as e:
                st.error(f"Error generating images: {str(e)}")
                
                # Show more specific error messages
                if "api_key" in str(e).lower():
                    st.info("Please check if your API key is valid and has sufficient credits.")
                elif "rate limit" in str(e).lower():
                    st.info("Rate limit exceeded. Please wait a moment before trying again.")

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📝 Instructions:
1. **Get API Key**: Sign up at [Together AI](https://api.together.xyz/) and get your API key
2. **Enter API Key**: Paste your API key in the sidebar
3. **Write Prompt**: Describe the image you want to generate
4. **Adjust Settings**: Modify steps, number of images, and dimensions as needed
5. **Generate**: Click the generate button and wait for your images!

### 💡 Prompt Tips:
- Be specific and descriptive
- Include style information (e.g., "photorealistic", "cartoon", "oil painting")
- Mention lighting, colors, and composition
- Use negative prompts to exclude unwanted elements
""")

# Display current settings
with st.expander("Current Settings"):
    st.json({
        "model": selected_model,
        "steps": steps,
        "num_images": num_images,
        "dimensions": f"{width}x{height}",
        "api_key_provided": bool(api_key)
    })
