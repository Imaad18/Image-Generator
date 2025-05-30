import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from together import Together

# Custom CSS injection for modern, futuristic styling
def inject_css():
    st.markdown("""
    <style>
        /* (Keep all your existing CSS styles here) */
        
        /* Add this new style for download buttons */
        .download-btn {
            margin-top: 10px;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="NexusAI Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
inject_css()

# Title and description with modern layout
st.markdown("""
<div style="padding: 20px 0 30px 0; border-bottom: 1px solid rgba(0, 245, 212, 0.2);">
    <h1 style="margin-bottom: 0.2rem;">🚀 NexusAI Studio</h1>
    <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.1em;">
        Your all-in-one AI creative suite for text and image generation
    </p>
</div>
""", unsafe_allow_html=True)

# (Keep all your existing sidebar and configuration code here)

# Main content area with tabs
tab1, tab2 = st.tabs(["🎨 Generate", "📚 Guide"])

with tab1:
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        # (Keep all your existing left column code here)
    
    with col2:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="color: #00f5d4; margin-bottom: 5px;">🎭 Output</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em;">
                Your generated content will appear here
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle prompt generation (keep existing code)
        
        # Handle text generation (keep existing code)
        
        # Handle image generation - MODIFIED SECTION
        if generate_image_btn and prompt.strip():
            try:
                client = Together(api_key=api_key)
                
                with st.spinner("🎨 Painting your vision... This may take a moment"):
                    generation_params = {
                        "prompt": prompt,
                        "model": image_model,
                        "steps": steps,
                        "n": num_images,
                        "width": width,
                        "height": height
                    }
                    
                    if negative_prompt.strip():
                        generation_params["negative_prompt"] = negative_prompt
                    
                    response = client.images.generate(**generation_params)
                    
                    if response.data:
                        st.success(f"🎉 Generated {len(response.data)} image(s)!")
                        
                        # Create responsive grid
                        if len(response.data) <= 2:
                            cols = st.columns(len(response.data))
                        else:
                            cols = st.columns(2)
                            for i in range(2, len(response.data)):
                                cols += st.columns(2)
                        
                        for i, image_data in enumerate(response.data):
                            col_idx = i % len(cols)
                            
                            with cols[col_idx]:
                                st.markdown('<div class="generated-card">', unsafe_allow_html=True)
                                
                                try:
                                    b64_data = None
                                    if hasattr(image_data, 'b64_json') and image_data.b64_json:
                                        b64_data = image_data.b64_json
                                    elif hasattr(image_data, 'base64') and image_data.base64:
                                        b64_data = image_data.base64
                                    elif hasattr(image_data, 'data') and image_data.data:
                                        b64_data = image_data.data
                                    elif hasattr(image_data, 'url') and image_data.url:
                                        st.image(image_data.url, caption=f"Generated Image {i+1}")
                                    
                                    if b64_data:
                                        image_bytes = base64.b64decode(b64_data)
                                        image = Image.open(BytesIO(image_bytes))
                                        
                                        # Display the image
                                        st.image(
                                            image,
                                            caption=f"🎨 Variation {i+1}",
                                            use_column_width=True
                                        )
                                        
                                        # Convert image to bytes for download
                                        img_buffer = BytesIO()
                                        image.save(img_buffer, format="PNG")
                                        img_bytes = img_buffer.getvalue()
                                        
                                        # Download button for this image
                                        st.download_button(
                                            label=f"📥 Download Image {i+1}",
                                            data=img_bytes,
                                            file_name=f"nexus_ai_image_{i+1}.png",
                                            mime="image/png",
                                            key=f"download_{i}",
                                            use_container_width=True,
                                            help=f"Download this generated image as PNG"
                                        )
                                    else:
                                        st.error("Unable to process image data")
                                
                                except Exception as img_error:
                                    st.error(f"Error processing image: {str(img_error)}")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("No images were generated. Please try adjusting your prompt.")
            
            except Exception as e:
                st.error(f"🚨 Image generation failed: {str(e)}")
                if "api_key" in str(e).lower():
                    st.info("Please verify your API key is correct")
                elif "rate limit" in str(e).lower():
                    st.info("You've hit the rate limit. Please wait before trying again.")

# (Keep all your existing Guide tab and footer code here)
