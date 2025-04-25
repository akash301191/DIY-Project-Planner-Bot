# DIY Project Planner Bot

DIY Project Planner Bot is a creative Streamlit application that helps you transform your project ideas, available tools, and budget into a clear, actionable DIY Project Guide. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot searches the web for relevant tutorials, materials, and safety tips, and generates a personalized, step-by-step DIY guide just for you.

## Folder Structure

```
DIY-Project-Planner-Bot/
├── diy-project-planner-bot.py
├── README.md
└── requirements.txt
```

- **diy-project-planner-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **DIY Project Preferences Input**  
  Fill out your project type, available tools, material choices, skill level, budget, timeline, and safety considerations.

- **AI-Powered DIY Research**  
  The DIY Researcher agent generates a focused Google search using SerpAPI based on your project preferences and extracts the best tutorials and resources.

- **Personalized DIY Project Guide**  
  The DIY Planner agent analyzes the research results and crafts a complete step-by-step guide, including materials list, tools required, detailed instructions, and safety tips.

- **Structured Markdown Output**  
  Your DIY guide is presented in a clean Markdown format with section headers, bullet points, numbered steps, and embedded hyperlinks where relevant.

- **Download Option**  
  Download the generated DIY Project Guide as a `.txt` file for offline reference or sharing.

- **Clean Streamlit UI**  
  Built with Streamlit to ensure an intuitive, user-friendly, and responsive experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/DIY-Project-Planner-Bot.git
   cd DIY-Project-Planner-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run diy-project-planner-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys in the sidebar.
   - Fill out your DIY project requirements and preferences.
   - Click **🔨 Generate DIY Project Guide**.
   - View and download your personalized, AI-generated DIY guide.

3. **Download Option**  
   Use the **📥 Download DIY Project Guide** button to save your project plan as a `.txt` file.

---

## Code Overview

- **`render_diy_project_preferences()`**: Captures user inputs such as project type, tools, materials, budget, and safety preferences.
- **`render_sidebar()`**: Stores and manages OpenAI and SerpAPI keys in Streamlit session state.
- **`generate_diy_project_guide()`**:  
  - Uses the `DIY Project Researcher` agent to find DIY tutorials and resources via SerpAPI.  
  - Sends results to the `DIY Project Planner` agent to generate a complete project guide.
- **`main()`**: Handles layout, collects inputs, manages the full end-to-end flow from user input to guide generation and download.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your changes are clean, well-tested, and aligned with the app’s purpose.