import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_diy_project_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Project Basics
    with col1:
        st.subheader("🛠️ Project Basics")
        project_type = st.selectbox(
            "What type of DIY project are you planning?*",
            ["Furniture Building", "Home Decor", "Gardening", "Repairs", "Crafting", "Other"]
        )
        project_description = st.text_input(
            "Briefly describe your project idea*", placeholder="e.g., Build a wooden bookshelf"
        )
        project_location = st.selectbox(
            "Where will this project be used?*",
            ["Indoors", "Outdoors", "Garden", "Kitchen", "Living Room", "Bedroom", "Other"]
        )

    # Column 2: Tools, Materials, Skills
    with col2:
        st.subheader("🔧 Tools, Materials, Skills")
        available_tools = st.multiselect(
            "Which tools do you have access to?*",
            ["Hammer", "Screwdriver", "Drill", "Saw", "Sander", "Glue Gun", "Wrench", "Measuring Tape", "Other"]
        )
        open_to_more_tools = st.radio(
            "Are you open to buying or renting extra tools if needed?",
            ["Yes", "No", "Maybe"], horizontal=True
        )
        material_preference = st.multiselect(
            "Preferred materials (optional)",
            ["Wood", "Metal", "Plastic", "Fabric", "Eco-friendly Materials", "Other"]
        )
        skill_level = st.radio(
            "How would you describe your DIY skill level?",
            ["Beginner", "Intermediate", "Advanced"], horizontal=True
        )

    # Column 3: Budget, Timeline, Safety
    with col3:
        st.subheader("💰 Budget & Timeline")
        budget = st.text_input("Estimated budget for the project*", placeholder="$50, $100, etc.")
        timeline = st.selectbox(
            "When do you want to complete the project?*",
            ["Within 1 day", "Within 1 week", "Flexible timeline"]
        )
        safety_considerations = st.multiselect(
            "Any safety considerations?",
            ["Child-safe", "Pet-safe", "Heavy lifting precautions", "Chemical safety", "No special considerations"]
        )
        preferred_instruction_style = st.selectbox(
            "What style of instructions do you prefer?",
            ["Simple step-by-step", "Detailed with tips", "Concise summary"],
        )

    # Assemble user DIY project profile
    diy_project_preferences = f"""
    **Project Overview:**
    - Project Type: {project_type}
    - Description: {project_description}
    - Location: {project_location}

    **Tools and Skills:**
    - Available Tools: {', '.join(available_tools) if available_tools else 'Not specified'}
    - Open to Extra Tools: {open_to_more_tools}
    - Material Preferences: {', '.join(material_preference) if material_preference else 'Not specified'}
    - Skill Level: {skill_level}

    **Budget and Safety:**
    - Estimated Budget: {budget}
    - Timeline: {timeline}
    - Safety Considerations: {', '.join(safety_considerations) if safety_considerations else 'None specified'}
    - Preferred Instruction Style: {preferred_instruction_style}
    """

    return diy_project_preferences

def generate_diy_project_guide(diy_project_preferences):
    diy_research_agent = Agent(
        name="DIY Project Researcher",
        role="Finds DIY project tutorials, material lists, step-by-step guides, and safety advice based on the user's project preferences.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a DIY project research expert. Given a detailed user profile including project type, available tools, materials, budget, and preferences,
            your job is to suggest project guides and resources that best match the user's DIY goals.
            You will create a focused, real-world search query, search the web, and extract the 10 most relevant links or summaries.
        """),
        instructions=[
            "Carefully read the user's DIY project preferences to understand the project type, available tools, material choices, skill level, budget, timeline, and safety considerations.",
            "Based on this, generate ONE concise and targeted search query (e.g., 'easy DIY wooden bookshelf tutorial under $75 with drill and screwdriver' or 'beginner-friendly home decor DIY projects eco-friendly materials').",
            "Avoid overly broad, general, or unrelated search queries. Be specific about project type, tool availability, and budget if mentioned.",
            "Use search_google with this focused search query.",
            "From the search results, extract the 10 most relevant links or useful summaries that provide clear DIY instructions, material lists, safety tips, or project walk-throughs.",
            "Prioritize resources that are beginner-friendly (if skill level is beginner) or more advanced (if skill level is intermediate/advanced).",
            "Do not fabricate or invent any information. Only use what is found in the search results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = diy_research_agent.run(diy_project_preferences)
    research_results = research_response.content

    diy_planner_agent = Agent(
        name="DIY Project Planner",
        role="Creates a personalized, step-by-step DIY project guide based on user preferences and researched web content.",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a senior DIY project planner responsible for crafting a clear, actionable, and user-friendly project plan.
            You are given:
            1. A structured summary of the user's DIY project preferences
            2. A set of search results pointing to trusted DIY tutorials, materials lists, and safety resources.

            Your job is to carefully study the research results, extract the most relevant and helpful ideas, and organize them into a practical project guide.
        """),
        instructions=[
            "Carefully review the user's project preferences. Pay close attention to:",
            "- **Project Type**: Ensure the guide matches the project goal (e.g., furniture, decor, etc.).",
            "- **Tools Available**: Only suggest techniques using available tools or ones the user is open to acquiring.",
            "- **Materials Preference**: Favor materials aligned with the user's choices if possible.",
            "- **Skill Level**: Match project complexity to user's skill level (e.g., beginner, intermediate, advanced).",
            "- **Budget**: Ensure material and tool suggestions stay within budget where possible.",
            "- **Timeline**: Keep the project steps manageable based on desired completion time.",
            "- **Safety Considerations**: Highlight important safety precautions for tools and materials.",
            "- **Preferred Instruction Style**: Adjust detail level accordingly (simple, detailed, or concise).",
            
            "Now analyze the research results carefully.",
            "Extract only project ideas, techniques, materials, and safety tips that are verifiably found in the research links.",
            "Do not fabricate or invent content. Only use what is sourced from the research results.",
            
            "Create the DIY Project Guide in the following exact Markdown structure:",
            "",
            "## [Project Title]",
            "",
            "### Materials Needed:",
            "- List each material clearly",
            "",
            "### Tools Needed:",
            "- List each tool clearly",
            "",
            "### Step-by-Step Instructions:",
            "1. First clear step",
            "2. Second step",
            "3. Third step",
            "...and so on",
            "",
            "### Safety Tips:",
            "- List important safety considerations clearly",
            "",
            "Embed hyperlinks inside text where needed (Markdown format: [Example](https://example.com)), but do not paste raw URLs.",
            "Write clean, practical, beginner-friendly or advanced level guides based on user profile.",
        ],
        add_datetime_to_instructions=True
    )

    planner_input = f"""
    User DIY Project Preferences:
    {diy_project_preferences}

    Research Results:
    {research_results}

    Use these details to draft a complete DIY Project Guide following the provided Markdown structure.
    """

    response = diy_planner_agent.run(planner_input)
    project_guide = response.content

    return project_guide

def main() -> None:
    # Page config
    st.set_page_config(page_title="DIY Project Planner Bot", page_icon="🛠️", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🛠️ DIY Project Planner Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to DIY Project Planner Bot — your hands-on Streamlit companion that transforms your project ideas, tools, and budget into a clear, actionable DIY Project Guide",
        unsafe_allow_html=True
    )

    render_sidebar()
    diy_project_preferences = render_diy_project_preferences()
    
    st.markdown("---")

    # Button to trigger DIY Project Guide generation
    if st.button("🔨 Generate DIY Project Guide"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("🔎 Researching and drafting your DIY project guide..."):
                diy_project_guide = generate_diy_project_guide(diy_project_preferences)
                st.session_state.diy_project_guide = diy_project_guide

    # Display the DIY Project Guide
    if "diy_project_guide" in st.session_state:
        st.markdown(st.session_state.diy_project_guide, unsafe_allow_html=True)
        st.markdown("---")

        # 5. Download button
        st.download_button(
            label="📥 Download DIY Project Guide",
            data=st.session_state.diy_project_guide,
            file_name="diy_project_guide.txt",
            mime="text/plain"
        )


if __name__ == "__main__": 
    main()