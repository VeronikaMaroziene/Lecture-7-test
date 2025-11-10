# Weekly Exercise Advisor 💪

A Streamlit-based web application that provides personalized weekly exercise plans using AI (Ollama gemma3:4b model).

## Features

- **Age-based recommendations**: Select your date of birth and get age-appropriate exercises
- **Custom time allocation**: Specify how many minutes you can exercise daily
- **Fitness goals**: Choose between losing weight or gaining muscles
- **AI-powered plans**: Uses Ollama's gemma3:4b model for personalized recommendations
- **7-day workout schedule**: Complete weekly plan with specific exercises for each day
- **Download capability**: Save your exercise plan for offline reference

## Requirements

- Python 3.8 or higher
- Ollama installed and running locally
- Google AI Studio API Key

## Installation

1. **Install Ollama** (if not already installed):
   - Visit https://ollama.ai and download for your operating system
   - Follow installation instructions for your platform

2. **Pull the gemma3:4b model**:
   ```bash
   ollama pull gemma3:4b
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements_packages.txt
   ```

## Running the Application

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser**:
   - The app should automatically open at http://localhost:8503
   - If not, navigate to the URL shown in your terminal

## How to Use

1. **Enter API Key**: In the sidebar, enter your Google AI Studio API Key
2. **Select Date of Birth**: Choose your birth date from the date picker
3. **Enter Exercise Time**: Specify how many minutes you can dedicate daily (1-300 minutes)
4. **Choose Fitness Goal**: Select either "lose weight" or "gain muscles"
5. **Generate Plan**: Click the "Generate My Exercise Plan" button
6. **Review & Download**: View your personalized 7-day plan and download it if needed

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Verify the gemma3:4b model is installed: `ollama list`
- If model is missing, pull it: `ollama pull gemma3:4b`

### API Key Issues
- Make sure you've entered a valid Google AI Studio API Key
- The key should be kept confidential and not shared

### Port Already in Use
- If port 8501 is busy, run with a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements_packages.txt   # Python dependencies
├── requirements.txt           # Program requirements document
├── README.md                  # This file
├── docs/
│   ├── program_instructions.txt  # Technical specifications
│   └── Streamlit.md             # Streamlit documentation
└── ollama.md                  # Ollama documentation
```

## Technical Details

- **Frontend**: Streamlit (Python web framework)
- **AI Model**: Ollama gemma3:4b (local LLM)
- **Architecture**: Client-server model with local AI inference
- **Data**: No user data is stored; all processing is done in-memory

## Disclaimer

This application provides AI-generated exercise advice for informational purposes only. Always consult with healthcare professionals, certified personal trainers, or physicians before starting any new exercise program, especially if you have pre-existing health conditions.

## License

This project is for educational purposes.
