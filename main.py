import streamlit as st
import random
from datetime import datetime
from fpdf import FPDF
from streamlit_extras.let_it_rain import rain

# Set page config
st.set_page_config(
    page_title="✨ Enchanted Story Weaver",
    page_icon="🧙‍♂️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'display_story' not in st.session_state:
    st.session_state.display_story = None
if 'pdf_story' not in st.session_state:
    st.session_state.pdf_story = None
if 'show_story' not in st.session_state:
    st.session_state.show_story = False
if 'current_genre' not in st.session_state:
    st.session_state.current_genre = "Adventure"

# Custom CSS for magical UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .title {
        color: #6a3093;
        text-align: center;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .story-box {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #6a3093;
    }
    .stButton>button {
        background: linear-gradient(to right, #6a3093, #a044ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(106, 48, 147, 0.3);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Story templates with different genres (without emojis in the PDF version)
STORY_TEMPLATES = {
    "Adventure": [
        "The Quest for the {object}\n\nIn the land of {place}, {name} and their loyal {animal} embarked on a daring journey. Feeling {emotion}, they used their {superpower} to overcome {number} treacherous challenges. At last, they found the legendary {object} and became heroes!",
    ],
    "Mystery": [
        "The Case of the Missing {object}\n\nWhen the {object} vanished from {place}, {name} and their clever {animal} sprang into action. Using their {superpower}, they uncovered {number} shocking clues. The truth? It was hidden in plain sight all along!",
    ],
    "Comedy": [
        "The Great {object} Fiasco\n\nNobody believed {name} when they said their {animal} could use a {object}. But when they arrived in {place}, chaos erupted! With {superpower}, they caused {number} hilarious mishaps.",
    ],
    "Fantasy": [
        "The {object} of Destiny\n\nIn the magical kingdom of {place}, {name} discovered they were the chosen one. Guided by a mystical {animal}, they wielded {superpower} to defeat {number} dark forces. The {object} held the key to saving the realm!",
    ],
    "Sci-Fi": [
        "The {object} Protocol\n\nOn planet {place}, {name} and their robotic {animal} uncovered a sinister plot. Using {superpower}, they hacked into {number} alien systems. The secret? The {object} was actually a cosmic key!",
    ]
}

# Display versions with emojis
DISPLAY_TEMPLATES = {
    "Adventure": [
        "🌄 **The Quest for the {object}**\n\nIn the land of {place}, {name} and their loyal {animal} embarked on a daring journey. Feeling {emotion}, they used their {superpower} to overcome {number} treacherous challenges. At last, they found the legendary {object} and became heroes!",
    ],
    "Mystery": [
        "🔍 **The Case of the Missing {object}**\n\nWhen the {object} vanished from {place}, {name} and their clever {animal} sprang into action. Using their {superpower}, they uncovered {number} shocking clues. The truth? It was hidden in plain sight all along!",
    ],
    "Comedy": [
        "🤣 **The Great {object} Fiasco**\n\nNobody believed {name} when they said their {animal} could use a {object}. But when they arrived in {place}, chaos erupted! With {superpower}, they caused {number} hilarious mishaps.",
    ],
    "Fantasy": [
        "🏰 **The {object} of Destiny**\n\nIn the magical kingdom of {place}, {name} discovered they were the chosen one. Guided by a mystical {animal}, they wielded {superpower} to defeat {number} dark forces. The {object} held the key to saving the realm!",
    ],
    "Sci-Fi": [
        "🚀 **The {object} Protocol**\n\nOn planet {place}, {name} and their robotic {animal} uncovered a sinister plot. Using {superpower}, they hacked into {number} alien systems. The secret? The {object} was actually a cosmic key!",
    ]
}

# Character icons for fun
CHARACTER_ICONS = {
    "Adventure": "🌄",
    "Mystery": "🔍",
    "Comedy": "🤣",
    "Fantasy": "🏰",
    "Sci-Fi": "🚀"
}

def generate_story(genre, inputs, for_pdf=False):
    """Select a random template from the chosen genre and fill in inputs."""
    templates = STORY_TEMPLATES if for_pdf else DISPLAY_TEMPLATES
    template = random.choice(templates[genre])
    return template.format(**inputs)

def create_pdf(story_content):
    """Generate a PDF version of the story without emojis."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Remove markdown formatting and emojis for PDF
    clean_content = story_content.replace("**", "").replace("__", "")
    for line in clean_content.split('\n'):
        # Encode each line separately to handle special characters
        try:
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        except:
            pdf.multi_cell(0, 10, line.encode('ascii', 'replace').decode('ascii'))
    
    return pdf.output(dest="S").encode("latin-1")

def main():
    # Title with emoji
    st.markdown("<h1 class='title'>✨ Enchanted Story Weaver</h1>", unsafe_allow_html=True)
    st.caption("Turn your ideas into magical tales!")

    # Sidebar with genre selection
    with st.sidebar:
        st.subheader("🎭 Choose Your Story Genre")
        genre = st.selectbox(
            "Pick a genre:",
            list(STORY_TEMPLATES.keys()),
            index=0,
            help="Different genres = different story styles!",
            key="genre_selector"
        )
        st.session_state.current_genre = genre

        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit")

    # Input form with visual feedback
    with st.form("story_inputs"):
        st.subheader(f"{CHARACTER_ICONS[genre]} Create Your Characters")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Hero's Name", "Alex", help="The protagonist of your story")
            animal = st.text_input("Animal Companion", "dragon", help="A loyal sidekick")
            place = st.text_input("Magical Place", "Avalon", help="Where the adventure happens")
        
        with col2:
            object_ = st.text_input("Mystical Object", "crystal orb", help="A key item in the story")
            emotion = st.text_input("Dominant Emotion", "excitement", help="How the hero feels")
            superpower = st.text_input("Unique Power", "shapeshifting", help="The hero's special ability")
            number = st.number_input("Magic Number", 1, 100, 7, help="A significant number in the tale")

        submitted = st.form_submit_button("✨ Generate My Story!")

    # Generate and display story
    if submitted or st.session_state.show_story:
        if not all([name, animal, place, object_, emotion, superpower]) and not st.session_state.display_story:
            st.warning("Please fill in all fields to weave your tale!")
        else:
            if submitted:
                inputs = {
                    "name": name,
                    "animal": animal,
                    "place": place,
                    "object": object_,
                    "emotion": emotion,
                    "superpower": superpower,
                    "number": number
                }

                with st.spinner(f"🧙‍♂️ Brewing your {genre.lower()} story..."):
                    st.session_state.display_story = generate_story(genre, inputs, for_pdf=False)
                    st.session_state.pdf_story = generate_story(genre, inputs, for_pdf=True)
                    st.session_state.show_story = True
                    rain(emoji="✨", font_size=20, falling_speed=5)

            if st.session_state.show_story:
                # Display story in a beautiful box
                st.markdown(
                    f"""
                    <div class='story-box'>
                        <h3>📖 Your {st.session_state.current_genre} Story</h3>
                        <hr>
                        <p style='font-size: 18px; line-height: 1.6;'>{st.session_state.display_story}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Download options
                st.subheader("📥 Save Your Story")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📝 Download as TXT",
                        data=st.session_state.display_story,
                        file_name=f"{st.session_state.current_genre}_story_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    pdf = create_pdf(st.session_state.pdf_story)
                    st.download_button(
                        label="📄 Download as PDF",
                        data=pdf,
                        file_name=f"{st.session_state.current_genre}_story_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )

                # Story rating
                st.markdown("---")
                st.subheader("💬 Rate Your Story")
                rating = st.slider("How much did you like it?", 1, 5, 3)
                if rating >= 4:
                    st.success("🎉 We're glad you loved it! Try another genre!")
                elif rating <= 2:
                    st.info("🔄 Want to try again? Adjust your inputs!")

if __name__ == "__main__":
    main()