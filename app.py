import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import requests
from together import Together

# Custom CSS injection for modern styling
def inject_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
        }
        
        /* Header styling */
        .stMarkdown h1 {
            color: #00d4ff;
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0, 212, 255, 0.3);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(15, 32, 39, 0.9) !important;
            border-right: 1px solid #00d4ff33;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #00d4ff, #0077ff);
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
        }
        
        /* Text input styling */
        .stTextArea textarea, .stTextInput input {
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid #00d4ff33 !important;
            border-radius: 8px !important;
        }
        
        /* Select box styling */
        .stSelectbox select {
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid #00d4ff33 !important;
        }
        
        /* Slider styling */
        .stSlider .thumb {
            background: #00d4ff !important;
        }
        
        .stSlider .track {
            background: #0077ff !important;
        }
        
        /* Card styling for generated images */
        .generated-image-card {
            background: rgba(15, 32, 39, 0.7);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #00d4ff33;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 32, 39, 0.7);
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00d4ff, #0077ff) !important;
        }
        
        /* Footer styling */
        .footer {
            margin-top: 50px;
            text-align: center;
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9em;
        }
        
        /* Tooltip styling */
        .stTooltip {
            background: #0f2027 !important;
            border: 1px solid #00d4ff !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="NexusAI Image Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
inject_css()

# Title and description with modern layout
st.markdown("""
<div style="padding: 20px 0 30px 0; border-bottom: 1px solid rgba(0, 212, 255, 0.2);">
    <h1 style="margin-bottom: 0;">✨ NexusAI Image Generator</h1>
    <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.1em;">
        Create stunning AI-generated artwork with Together AI's advanced FLUX models
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar for API key and settings with improved organization
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 20px; border-bottom: 1px solid rgba(0, 212, 255, 0.2); margin-bottom: 20px;">
        <h2 style="color: #00d4ff; margin-bottom: 5px;">⚙️ Configuration</h2>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9em;">
            Set up your API key and generation parameters
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key input with enhanced security
    api_key = st.text_input(
        "🔑 Together AI API Key",
        type="password",
        help="Get your API key from https://api.together.xyz/",
        placeholder="Enter your API key here..."
    )
    
    # Model selection with descriptions
    with st.expander("🧠 Model Selection", expanded=True):
        model_options = {
            "black-forest-labs/FLUX.1-dev": "High-quality image generation with detailed results (recommended)",
            "black-forest-labs/FLUX.1-schnell": "Faster generation with slightly reduced quality"
        }
        selected_model = st.selectbox(
            "Select Model",
            list(model_options.keys()),
            index=0,
            help=model_options[selected_model] if api_key else "Select a model for image generation"
        )
        
        st.markdown(f"""
        <div style="background: rgba(0, 212, 255, 0.1); padding: 12px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; color: rgba(255, 255, 255, 0.8); font-size: 0.85em;">
                <strong>Model Info:</strong> {model_options[selected_model]}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generation parameters with better organization
    with st.expander("🎛️ Generation Settings", expanded=True):
        steps = st.slider(
            "🔢 Steps",
            min_value=1,
            max_value=50,
            value=20,
            help="More steps = higher quality but slower generation (20-30 recommended)"
        )
        
        num_images = st.slider(
            "🖼️ Number of Images",
            min_value=1,
            max_value=4,
            value=2,
            help="How many variations to generate"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox(
                "↔️ Width",
                [512, 768, 1024],
                index=2,
                help="Image width in pixels"
            )
        with col2:
            height = st.selectbox(
                "↕️ Height", 
                [512, 768, 1024],
                index=2,
                help="Image height in pixels"
            )
    
    # Quick tips section
    st.markdown("""
    <div style="margin-top: 30px; padding: 15px; background: rgba(0, 212, 255, 0.1); border-radius: 8px;">
        <h4 style="color: #00d4ff; margin-bottom: 10px;">💡 Quick Tips</h4>
        <ul style="color: rgba(255, 255, 255, 0.7); font-size: 0.85em; padding-left: 20px; margin: 0;">
            <li>Use descriptive prompts for best results</li>
            <li>Try adding style references (e.g., "4K photorealistic")</li>
            <li>20-30 steps usually provides good quality</li>
            <li>1024x1024 works best for detailed images</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area with improved layout
tab1, tab2, tab3 = st.tabs(["🎨 Generate", "📚 Guide", "⚙️ Settings"])

with tab1:
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="color: #00d4ff; margin-bottom: 5px;">🎯 Prompt Crafting</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em;">
                Describe your vision in detail for best results
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prompt input with examples
        prompt = st.text_area(
            "**Describe your image**",
            height=150,
            placeholder="Example: 'A futuristic cityscape at sunset, cyberpunk style, neon lights reflecting on wet streets, 4K hyper-detailed'",
            value="A majestic lion with a glowing mane, digital art, highly detailed, cinematic lighting"
        )
        
        # Negative prompt with examples
        negative_prompt = st.text_area(
            "**Exclusion terms (optional)**",
            height=100,
            placeholder="Example: 'blurry, low quality, distorted faces'",
            help="Specify elements you want to exclude from the generated images"
        )
        
        # Advanced options
        with st.expander("⚡ Advanced Options"):
            seed = st.number_input(
                "Random seed",
                min_value=-1,
                max_value=2147483647,
                value=-1,
                help="Use -1 for random seed or specify a value for reproducible results"
            )
        
        # Generate button with improved UX
        generate_btn = st.button(
            "🚀 Generate Images",
            type="primary",
            use_container_width=True,
            disabled=not api_key
        )
        
        if not api_key:
            st.warning("Please enter your API key to enable generation")
    
    with col2:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="color: #00d4ff; margin-bottom: 5px;">🖼️ Gallery</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em;">
                Your generated images will appear here
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if generate_btn:
            if not prompt.strip():
                st.error("Please enter a prompt to generate images")
            else:
                try:
                    # Initialize Together client
                    client = Together(api_key=api_key)
                    
                    # Show loading animation
                    with st.spinner("✨ Weaving your imagination into reality... This may take a moment"):
                        
                        # Prepare parameters
                        generation_params = {
                            "prompt": prompt,
                            "model": selected_model,
                            "steps": steps,
                            "n": num_images,
                            "width": width,
                            "height": height,
                            "seed": seed if seed != -1 else None
                        }
                        
                        # Add negative prompt if provided
                        if negative_prompt.strip():
                            generation_params["negative_prompt"] = negative_prompt
                        
                        # Generate images
                        response = client.images.generate(**generation_params)
                        
                        # Display generated images
                        if response.data:
                            st.success(f"🎉 Successfully generated {len(response.data)} image(s)!")
                            
                            # Create responsive grid for images
                            if len(response.data) <= 2:
                                cols = st.columns(len(response.data))
                            else:
                                cols = st.columns(2)
                                for i in range(2, len(response.data)):
                                    cols += st.columns(2)
                            
                            for i, image_data in enumerate(response.data):
                                col_idx = i % len(cols)
                                
                                with cols[col_idx]:
                                    st.markdown(f'<div class="generated-image-card">', unsafe_allow_html=True)
                                    
                                    try:
                                        # Try different possible attributes for the image data
                                        b64_data = None
                                        if hasattr(image_data, 'b64_json') and image_data.b64_json:
                                            b64_data = image_data.b64_json
                                        elif hasattr(image_data, 'base64') and image_data.base64:
                                            b64_data = image_data.base64
                                        elif hasattr(image_data, 'data') and image_data.data:
                                            b64_data = image_data.data
                                        elif hasattr(image_data, 'url') and image_data.url:
                                            # If it's a URL instead of base64
                                            st.image(image_data.url, caption=f"Generated Image {i+1}")
                                        
                                        if b64_data:
                                            # Decode base64 image
                                            image_bytes = base64.b64decode(b64_data)
                                            image = Image.open(BytesIO(image_bytes))
                                            
                                            # Display image with enhanced styling
                                            st.image(
                                                image,
                                                caption=f"✨ Variation {i+1}",
                                                use_container_width=True
                                            )
                                            
                                            # Download button with icon
                                            img_buffer = BytesIO()
                                            image.save(img_buffer, format='PNG')
                                            img_bytes = img_buffer.getvalue()
                                            
                                            st.download_button(
                                                label=f"📥 Download Image {i+1}",
                                                data=img_bytes,
                                                file_name=f"nexus_ai_image_{i+1}.png",
                                                mime="image/png",
                                                use_container_width=True,
                                                key=f"download_{i}"
                                            )
                                        else:
                                            st.error("Unable to process image data")
                                    
                                    except Exception as img_error:
                                        st.error(f"Error processing image: {str(img_error)}")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error("No images were generated. Please try adjusting your prompt or settings.")
                            
                except Exception as e:
                    st.error(f"🚨 Generation failed: {str(e)}")
                    
                    # Show specific error guidance
                    if "api_key" in str(e).lower():
                        st.info("Please verify your API key is correct and has sufficient credits.")
                    elif "rate limit" in str(e).lower():
                        st.info("You've hit the rate limit. Please wait a moment before trying again.")
                    elif "invalid prompt" in str(e).lower():
                        st.info("Your prompt may contain blocked terms. Try rephrasing.")

with tab2:
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: #00d4ff; border-bottom: 1px solid rgba(0, 212, 255, 0.3); padding-bottom: 10px;">📚 User Guide</h2>
        
        <div style="margin-top: 30px;">
            <h3 style="color: #00d4ff;">🔑 Getting Started</h3>
            <ol style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <li><strong>Obtain an API Key:</strong> Sign up at <a href="https://api.together.xyz/" target="_blank" style="color: #00d4ff;">Together AI</a> to get your API key</li>
                <li><strong>Enter Your Key:</strong> Paste your API key in the sidebar configuration</li>
                <li><strong>Describe Your Vision:</strong> Write a detailed prompt in the "Describe your image" box</li>
                <li><strong>Generate:</strong> Click the "Generate Images" button to create your artwork</li>
            </ol>
        </div>
        
        <div style="margin-top: 40px;">
            <h3 style="color: #00d4ff;">✍️ Prompt Crafting Guide</h3>
            <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <h4 style="margin-top: 0; color: #00d4ff;">Elements of a Great Prompt</h4>
                <ul style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                    <li><strong>Subject:</strong> Clearly describe the main focus (e.g., "a cyberpunk samurai")</li>
                    <li><strong>Style:</strong> Specify artistic style (e.g., "digital art, hyper-detailed, 8K")</li>
                    <li><strong>Lighting:</strong> Describe lighting conditions (e.g., "cinematic lighting, neon glow")</li>
                    <li><strong>Composition:</strong> Add framing details (e.g., "close-up portrait, shallow depth of field")</li>
                    <li><strong>Mood:</strong> Convey the atmosphere (e.g., "mysterious, futuristic, vibrant")</li>
                </ul>
            </div>
            
            <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h4 style="margin-top: 0; color: #00d4ff;">Example Prompts</h4>
                <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                    <p><strong>Portrait:</strong> "A wise old wizard with glowing runes on his skin, intricate detailed facial features, surrounded by magical energy, digital painting by Greg Rutkowski and Artgerm, 8K resolution"</p>
                    <p><strong>Landscape:</strong> "A futuristic city floating in the clouds at golden hour, massive skyscrapers with neon signs, art deco architecture, cinematic lighting, ultra-detailed 4K"</p>
                    <p><strong>Concept Art:</strong> "Steampunk airship with intricate brass details flying through a canyon at dawn, Jules Verne style, highly detailed matte painting"</p>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h3 style="color: #00d4ff;">⚙️ Advanced Techniques</h3>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <p><strong>Negative Prompts:</strong> Use the exclusion box to remove unwanted elements like "blurry, distorted, extra limbs"</p>
                <p><strong>Seeds:</strong> Set a specific seed value to recreate similar images later</p>
                <p><strong>Steps:</strong> Higher values (30-50) produce more refined results but take longer</p>
                <p><strong>Dimensions:</strong> 1024x1024 works well for most purposes, but experiment with different aspect ratios</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: #00d4ff; border-bottom: 1px solid rgba(0, 212, 255, 0.3); padding-bottom: 10px;">⚙️ Current Settings</h2>
        
        <div style="margin-top: 30px; background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px;">
            <h3 style="margin-top: 0; color: #00d4ff;">Generation Configuration</h3>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <p><strong>Selected Model:</strong> {model}</p>
                <p><strong>Steps:</strong> {steps}</p>
                <p><strong>Image Count:</strong> {num_images}</p>
                <p><strong>Resolution:</strong> {width} × {height} px</p>
                <p><strong>Seed:</strong> {seed if seed != -1 else "Random"}</p>
                <p><strong>API Key:</strong> {"Provided" if api_key else "Not provided"}</p>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <h3 style="color: #00d4ff;">Performance Tips</h3>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <ul>
                    <li>Start with 20-30 steps for quick iterations</li>
                    <li>Generate 1-2 images initially to test prompts</li>
                    <li>Use 512px for faster concept testing</li>
                    <li>Higher resolutions consume more credits</li>
                </ul>
            </div>
        </div>
    </div>
    """.format(
        model=selected_model,
        steps=steps,
        num_images=num_images,
        width=width,
        height=height,
        seed=seed,
        api_key=api_key
    ), unsafe_allow_html=True)

# Footer with copyright and version
st.markdown("""
<div class="footer">
    <p>✨ NexusAI Image Generator v2.0 | © 2023 | Powered by Together AI</p>
</div>
""", unsafe_allow_html=True)
