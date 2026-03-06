import streamlit as st
import base64

def generate_svg(text, text_color, bg_color, shape, font_family, icon_emoji):
    """Generates an SVG string based on user input."""
    
    # Shape definitions
    shape_element = ""
    if shape == "Circle":
        shape_element = f'<circle cx="250" cy="250" r="200" fill="{bg_color}" />'
    elif shape == "Square":
        shape_element = f'<rect x="50" y="50" width="400" height="400" rx="20" fill="{bg_color}" />'
    elif shape == "Hexagon":
        shape_element = f'<polygon points="250,50 423,150 423,350 250,450 77,350 77,150" fill="{bg_color}" />'

    # SVG Template
    svg_code = f"""
    <svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        {shape_element}
        <text x="50%" y="45%" font-size="80" text-anchor="middle" fill="{text_color}" 
              font-family="{font_family}" font-weight="bold">
            {icon_emoji}
        </text>
        <text x="50%" y="65%" font-size="40" text-anchor="middle" fill="{text_color}" 
              font-family="{font_family}" font-weight="bold" letter-spacing="2">
            {text.upper()}
        </text>
    </svg>
    """
    return svg_code

def main():
    st.set_page_config(page_title="Vector Logo Designer", layout="wide")
    
    st.title("🎨 Vector Logo Designer")
    st.markdown("Create high-quality SVG logos instantly.")

    # Sidebar Controls
    with st.sidebar:
        st.header("Settings")
        logo_text = st.text_input("Brand Name", "ALCHEMIST")
        icon_emoji = st.text_input("Icon (Emoji)", "🚀")
        
        shape = st.selectbox("Background Shape", ["Circle", "Square", "Hexagon"])
        font = st.selectbox("Font Style", ["sans-serif", "serif", "monospace", "cursive"])
        
        col1, col2 = st.columns(2)
        bg_color = col1.color_picker("Background", "#6366F1")
        text_color = col2.color_picker("Text/Icon", "#FFFFFF")

    # Logic to Generate
    svg_data = generate_svg(logo_text, text_color, bg_color, shape, font, icon_emoji)

    # Display Preview
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Preview")
        # Display SVG via base64 encoding
        b64 = base64.b64encode(svg_data.encode('utf-8')).decode("utf-8")
        st.image(f"data:image/svg+xml;base64,{b64}", width=400)

    with col_right:
        st.subheader("Export")
        st.download_button(
            label="Download SVG",
            data=svg_data,
            file_name="my_logo.svg",
            mime="image/svg+xml"
        )
        
        st.info("💡 SVG files can be opened in any browser or scaled to any size for printing.")

if __name__ == "__main__":
    main()
