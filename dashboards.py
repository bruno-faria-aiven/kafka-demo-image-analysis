import streamlit as st

# Streamlit app
def dashboard(dashboard_type: str):
    # Default settings
    st.set_page_config(
        page_title="Real-Time Image Analysis",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        # stBaseButton-header
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        [data-testid="stBaseButton-header"] {
    visibility: hidden;
}

    </style>
""", unsafe_allow_html=True)

    # Run the Streamlit app
    st.title(f"Kafka Image Analysis - {str.upper(dashboard_type)}")

    # Add Logo
    # st.sidebar.image("images-tmp/aiven-logo_vert_RGB-wht.png", width=250)
    st.sidebar.image("images-tmp/aiven-logo_vert_RGB.svg", width=250)

    # Sidebar with user instructions
    st.sidebar.markdown(
        """
        This app shows how to perform real-time image analysis with Kafka. 
        This produces images to Kafka, consumes those messages, and then 
        passes the images to the OpenAI API for analysis. The image and description 
        of it is then returned to the user.
        """
    )

    # Display image analysis in the main section
    st.header("Real-Time Image Analysis with Aiven for Apache Kafka")
