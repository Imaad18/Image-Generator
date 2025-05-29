import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import requests
from together import Together

# Custom CSS injection for modern, futuristic styling
def inject_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Header styling */
        .stMarkdown h1 {
            color: #00f5d4;
            font-weight: 800;
            text-shadow: 0 2px 15px rgba(0, 245, 212, 0.4);
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.85) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid #00f5d433;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #00f5d4, #00bbf9);
            border: none;
            color: #0f0c29;
            font-weight: 600;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 245, 212, 0.3);
            transition: all 0.3s ease;
            padding: 10px 24px;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 245, 212, 0.5);
        }
        
        /* Text input styling */
        .stTextArea textarea, .stTextInput input {
            background: rgba(255, 255, 255, 0.08) !important;
            color: white !important;
            border: 1px solid #00f5d433 !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }
        
        /* Select box styling */
        .stSelectbox select {
            background: rgba(255, 255, 255, 0.08) !important;
            color: white !important;
            border: 1px solid #00f5d433 !important;
            border-radius: 12px;
            padding: 8px;
        }
        
        /* Slider styling */
        .stSlider .thumb {
            background: #00f5d4 !important;
            border: none !important;
            box-shadow: 0 0 10px rgba(0, 245, 212, 0.5);
        }
        
        .stSlider .track {
            background: #00bbf9 !important;
            height: 6px;
            border-radius: 3px;
        }
        
        /* Card styling for generated content */
        .generated-card {
            background: rgba(15, 12, 41, 0.7);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid #00f5d433;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }
        
        .generated-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 245, 212, 0.2);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            padding: 0 20px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 12, 41, 0.7);
            border-radius: 12px !important;
            padding: 12px 24px;
            transition: all 0.3s ease;
            margin: 0 5px;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00f5d4, #00bbf9) !important;
            color: #0f0c29 !important;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 245, 212, 0.3);
        }
        
        /* Tooltip styling */
        .stTooltip {
            background: #0f0c29 !important;
            border: 1px solid #00f5d4 !important;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Spinner styling */
        .stSpinner > div {
            border: 3px solid rgba(0, 245, 212, 0.3);
            border-radius: 50%;
            border-top: 3px solid #00f5d4;
            width: 30px;
            height: 30px;
        }
        
        /* Footer styling */
        .footer {
            margin-top: 50px;
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9em;
            padding: 20px 0;
            border-top: 1px solid rgba(0, 245, 212, 0.2);
        }
        
        /* Custom glowing effect for important elements */
        .glow-effect {
            box-shadow: 0 0 15px rgba(0, 245, 212, 0.5);
            animation: glow-pulse 2s infinite alternate;
        }
        
        @keyframes glow-pulse {
            0% { box-shadow: 0 0 10px rgba(0, 245, 212, 0.3); }
            100% { box-shadow: 0 0 20px rgba(0, 245, 212, 0.7); }
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

# Sidebar for API key and settings
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 20px; border-bottom: 1px solid rgba(0, 245, 212, 0.2); margin-bottom: 20px;">
        <h2 style="color: #00f5d4; margin-bottom: 5px;">⚙️ Configuration</h2>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9em;">
            Configure your API keys and settings
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key input
    api_key = st.text_input(
        "🔑 Together AI API Key",
        type="password",
        help="Get your API key from https://api.together.xyz/",
        placeholder="Enter your API key here..."
    )
    
    # Model selection tabs
    tab_model_text, tab_model_image = st.tabs(["📝 Text", "🖼️ Image"])
    
    with tab_model_text:
        text_model = st.selectbox(
            "Text Model",
            ["deepseek-ai/DeepSeek-V3", "meta-llama/Llama-3-70b-chat-hf"],
            index=0,
            help="Select model for text generation"
        )
        
        st.markdown("""
        <div style="background: rgba(0, 245, 212, 0.1); padding: 12px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; color: rgba(255, 255, 255, 0.8); font-size: 0.85em;">
                <strong>Current:</strong> {model}<br>
                <strong>Best for:</strong> General text generation and prompt crafting
            </p>
        </div>
        """.format(model=text_model), unsafe_allow_html=True)
    
    with tab_model_image:
        image_model = st.selectbox(
            "Image Model",
            ["black-forest-labs/FLUX.1-dev", "black-forest-labs/FLUX.1-schnell"],
            index=0,
            help="Select model for image generation"
        )
        
        st.markdown("""
        <div style="background: rgba(0, 245, 212, 0.1); padding: 12px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; color: rgba(255, 255, 255, 0.8); font-size: 0.85em;">
                <strong>Current:</strong> {model}<br>
                <strong>Best for:</strong> {purpose}
            </p>
        </div>
        """.format(
            model=image_model,
            purpose="High-quality images" if image_model == "black-forest-labs/FLUX.1-dev" else "Fast generation"
        ), unsafe_allow_html=True)
    
    # Generation parameters
    with st.expander("🎛️ Image Settings", expanded=True):
        steps = st.slider(
            "🔢 Steps",
            min_value=1,
            max_value=50,
            value=20,
            help="More steps = higher quality but slower generation"
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
    <div style="margin-top: 30px; padding: 15px; background: rgba(0, 245, 212, 0.1); border-radius: 8px;">
        <h4 style="color: #00f5d4; margin-bottom: 10px;">💡 Pro Tips</h4>
        <ul style="color: rgba(255, 255, 255, 0.7); font-size: 0.85em; padding-left: 20px; margin: 0;">
            <li>Generate a text prompt first if you're unsure</li>
            <li>Use 20-30 steps for best quality/speed balance</li>
            <li>1024x1024 works best for detailed images</li>
            <li>Try different models for varied results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2 = st.tabs(["🎨 Generate", "📚 Guide"])

with tab1:
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="color: #00f5d4; margin-bottom: 5px;">🧠 Creative Studio</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em;">
                Craft your prompt or let AI help you generate one
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prompt generation section
        with st.expander("✨ Generate AI-Powered Prompt", expanded=True):
            prompt_idea = st.text_area(
                "**Describe your idea**",
                height=100,
                placeholder="Example: 'I want an image of a futuristic city'",
                help="Let AI help you craft a professional prompt"
            )
            
            generate_prompt_btn = st.button(
                "🪄 Generate Professional Prompt",
                disabled=not api_key,
                use_container_width=True
            )
        
        # Main prompt input
        prompt = st.text_area(
            "**Your Final Prompt**",
            height=150,
            placeholder="Example: 'A futuristic cyberpunk cityscape at night, neon lights reflecting on wet streets, 4K hyper-detailed'",
            help="This will be used for image generation"
        )
        
        # Negative prompt
        negative_prompt = st.text_area(
            "**Exclusion Terms**",
            height=80,
            placeholder="What you don't want in the image (optional)",
            help="Specify elements to exclude from generated images"
        )
        
        # Generate buttons
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            generate_text_btn = st.button(
                "📝 Generate Text",
                disabled=not api_key,
                use_container_width=True
            )
        with col1_2:
            generate_image_btn = st.button(
                "🚀 Generate Images",
                type="primary",
                disabled=not api_key or not prompt.strip(),
                use_container_width=True
            )
        
        if not api_key:
            st.warning("Please enter your API key to enable generation")
    
    with col2:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="color: #00f5d4; margin-bottom: 5px;">🎭 Output</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9em;">
                Your generated content will appear here
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle prompt generation
        if generate_prompt_btn and prompt_idea.strip():
            if not api_key:
                st.error("Please enter your API key")
            else:
                try:
                    with st.spinner("🧠 Crafting the perfect prompt for you..."):
                        client = Together(api_key=api_key)
                        response = client.chat.completions.create(
                            model=text_model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a professional prompt engineer for AI image generation. Create a detailed, creative prompt based on the user's simple idea. Include style, composition, lighting, and artistic details. Respond with just the prompt text, no additional commentary."
                                },
                                {
                                    "role": "user",
                                    "content": f"Create a professional AI image generation prompt for: {prompt_idea}"
                                }
                            ]
                        )
                        generated_prompt = response.choices[0].message.content
                        prompt = generated_prompt  # Auto-fill the main prompt
                        st.session_state.generated_prompt = generated_prompt
                    
                    st.success("✨ Here's your AI-crafted prompt:")
                    st.markdown(f'<div class="generated-card" style="padding: 15px; margin-bottom: 20px;">{generated_prompt}</div>', unsafe_allow_html=True)
                    
                    # Copy button for the prompt
                    st.download_button(
                        label="📋 Copy Prompt",
                        data=generated_prompt,
                        file_name="ai_generated_prompt.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                except Exception as e:
                    st.error(f"Failed to generate prompt: {str(e)}")
        
        # Handle text generation
        if generate_text_btn and prompt.strip():
            try:
                with st.spinner("💡 Generating creative text..."):
                    client = Together(api_key=api_key)
                    response = client.chat.completions.create(
                        model=text_model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1024
                    )
                    generated_text = response.choices[0].message.content
                    st.session_state.generated_text = generated_text
                
                st.success("📚 Generated Text:")
                st.markdown(f'<div class="generated-card">{generated_text}</div>', unsafe_allow_html=True)
                
                # Download button for the text
                st.download_button(
                    label="📥 Download Text",
                    data=generated_text,
                    file_name="ai_generated_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            except Exception as e:
                st.error(f"Failed to generate text: {str(e)}")
        
        # Handle image generation
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
                                        
                                        st.image(
                                            image,
                                            caption=f"🎨 Variation {i+1}",
                                            use_container_width=True
                                        )
                                        
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
                        st.error("No images were generated. Please try adjusting your prompt.")
            
            except Exception as e:
                st.error(f"🚨 Image generation failed: {str(e)}")
                if "api_key" in str(e).lower():
                    st.info("Please verify your API key is correct")
                elif "rate limit" in str(e).lower():
                    st.info("You've hit the rate limit. Please wait before trying again.")

with tab2:
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto;">
        <h2 style="color: #00f5d4; border-bottom: 1px solid rgba(0, 245, 212, 0.3); padding-bottom: 10px;">📚 User Guide</h2>
        
        <div style="margin-top: 30px;">
            <h3 style="color: #00f5d4;">🔮 Two-Step Generation Process</h3>
            <ol style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <li><strong>Generate a Professional Prompt:</strong> Describe your basic idea in the "Generate AI-Powered Prompt" section and let the AI craft a detailed prompt for you</li>
                <li><strong>Create Your Artwork:</strong> Use the generated prompt (or your own) to produce stunning images with the image generation models</li>
            </ol>
            
            <div style="background: rgba(0, 245, 212, 0.1); padding: 20px; border-radius: 12px; margin: 20px 0;">
                <h4 style="color: #00f5d4; margin-top: 0;">💎 Pro Tip</h4>
                <p style="color: rgba(255, 255, 255, 0.8);">
                    The AI can help you refine vague ideas into professional-grade prompts. Start with a simple concept like "a cat in space" and let the system expand it into a detailed description.
                </p>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h3 style="color: #00f5d4;">🖼️ Image Generation Tips</h3>
            <div style="background: rgba(0, 245, 212, 0.1); padding: 20px; border-radius: 12px; margin-top: 15px;">
                <h4 style="margin-top: 0; color: #00f5d4;">Prompt Structure</h4>
                <ul style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                    <li><strong>Subject:</strong> Clear main focus (e.g., "cyberpunk samurai warrior")</li>
                    <li><strong>Style:</strong> Artistic style (e.g., "digital art, hyper-detailed, Unreal Engine 5")</li>
                    <li><strong>Lighting:</strong> "cinematic lighting, neon glow, volumetric fog"</li>
                    <li><strong>Details:</strong> "intricate armor, reflective surfaces, dynamic pose"</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h3 style="color: #00f5d4;">⚙️ Technical Settings</h3>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <p><strong>Steps (20-30):</strong> Balances quality and generation time</p>
                <p><strong>Resolution (1024x1024):</strong> Higher values produce more detail but use more credits</p>
                <p><strong>Negative Prompts:</strong> Remove unwanted elements like "blurry, distorted, extra limbs"</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🚀 NexusAI Studio v2.1 | © 2023 | Powered by Together AI</p>
</div>
""", unsafe_allow_html=True)
