import streamlit as st
from datetime import datetime, date
import os
from ollama import chat
import traceback

# Page configuration
st.set_page_config(
    page_title="UAB Sveikata - Exercise Advisor",
    page_icon="💪",
    layout="wide"
)

# Title and description with agent introduction
st.title("💪 UAB Sveikata - Exercise Advisor")
st.info("👋 **Hello! I am UAB Sveikata agent.** I'm here to help you create a personalized weekly exercise plan based on your goals and availability.")
st.markdown("Get personalized exercise recommendations for your fitness goals!")
st.warning("⚠️ **Important Notice:** The advice is AI based and is not a professional doctor's opinion.")

# Sidebar for API Key input
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Google AI Studio API Key",
        type="password",
        help="Enter your Google AI Studio API key to use the AI model"
    )
    
    if api_key:
        os.environ['GOOGLE_API_KEY'] = api_key
        st.success("✅ API Key configured")
    else:
        st.warning("⚠️ Please enter your API Key to use the app")
    
    st.markdown("---")
    st.header("🔧 System Status")
    
    # Check Ollama connection
    if st.button("🔍 Test Ollama Connection"):
        try:
            from ollama import list as ollama_list
            models = ollama_list()
            st.success("✅ Ollama is running!")
            
            # Check for gemma3:4b model
            model_names = [m.model for m in models.models]
            if any('gemma3:4b' in name or 'gemma3' in name for name in model_names):
                st.success("✅ gemma3 model found!")
            else:
                st.warning("⚠️ gemma3:4b model not found")
                st.info("Run in terminal: `ollama pull gemma3:4b`")
            
            with st.expander("📋 Available models"):
                for model in models.models:
                    st.text(f"• {model.model}")
        except Exception as e:
            st.error("❌ Cannot connect to Ollama")
            st.error(f"Error: {str(e)}")
            st.info("""
            **To start Ollama:**
            1. Open PowerShell
            2. Run: `ollama serve`
            3. Keep the terminal open
            """)

# Main form section
st.header("📋 Your Information")

col1, col2 = st.columns(2)

with col1:
    # Date of birth selection
    st.subheader("Date of Birth")
    birth_date = st.date_input(
        "Select your date of birth",
        value=date(2000, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        help="We'll use this to calculate your age"
    )
    
    # Calculate age
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    st.info(f"Your age: {age} years old")

with col2:
    # Exercise duration input
    st.subheader("Daily Exercise Time")
    exercise_minutes = st.number_input(
        "How many minutes can you exercise per day?",
        min_value=1,
        max_value=300,
        value=30,
        step=5,
        help="Enter the number of minutes you can dedicate to exercise daily"
    )
    st.info(f"Daily commitment: {exercise_minutes} minutes")

# Fitness goal selection
st.subheader("Fitness Goal")
fitness_goal = st.selectbox(
    "What is your primary fitness goal?",
    options=["lose weight", "gain muscles"],
    help="Select the goal you want to achieve"
)

# User additional input/notes
st.subheader("Additional Information")
user_notes = st.text_area(
    "Any additional information or specific requirements?",
    placeholder="e.g., I have knee problems, I prefer home workouts, I enjoy swimming, etc.",
    help="Share any relevant information that should be considered in your exercise plan",
    height=100
)

# Display current selections
st.markdown("---")
st.subheader("📊 Your Profile Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Age", f"{age} years")
with col2:
    st.metric("Daily Time", f"{exercise_minutes} min")
with col3:
    st.metric("Goal", fitness_goal.title())

if user_notes:
    st.info(f"**Additional notes:** {user_notes}")

# Generate exercise plan button
st.markdown("---")
if st.button("🎯 Generate My Exercise Plan", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Please enter your Google AI Studio API Key in the sidebar first!")
    else:
        with st.spinner("🤖 Creating your personalized exercise plan..."):
            try:
                # Prepare the prompt for the AI model
                additional_context = f"\n\nAdditional user information: {user_notes}" if user_notes else ""
                
                prompt = f"""You are a professional fitness trainer working for UAB Sveikata. Create a detailed 7-day exercise plan for a person with the following profile:

Age: {age} years old
Available time per day: {exercise_minutes} minutes
Fitness goal: {fitness_goal}{additional_context}

IMPORTANT: Start your response with a reminder that "The advice is AI based and is not a professional doctor's opinion."

Please provide:
1. A weekly exercise plan with specific exercises for each day (Monday to Sunday)
2. Each day should have exercises that fit within {exercise_minutes} minutes
3. Exercises should be appropriate for someone who wants to {fitness_goal}
4. Include warm-up and cool-down activities
5. Consider the age of the person when recommending exercises
6. Provide brief instructions for each exercise
7. Include rest days if appropriate
8. Consider any additional information provided by the user

IMPORTANT: End your response with a reminder that "The advice is AI based and is not a professional doctor's opinion."

Format the response in a clear, day-by-day structure that is easy to follow."""

                # Call the Ollama model (gemma3:4b)
                response = chat(
                    model='gemma3:4b',
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are a professional fitness trainer working for UAB Sveikata who creates personalized, safe, and effective exercise plans. Always remind users that your advice is AI-based and not a professional doctor\'s opinion at the beginning and end of your recommendations. Provide detailed, actionable advice.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    options={
                        'temperature': 0.7,
                        'num_predict': 1500
                    }
                )
                
                # Display the exercise plan
                st.success("✅ Your personalized exercise plan is ready!")
                st.warning("⚠️ **Reminder:** The advice is AI based and is not a professional doctor's opinion.")
                st.markdown("---")
                st.subheader("📅 Your 7-Day Exercise Plan")
                
                # Display the AI response
                st.markdown(response.message.content)
                
                st.markdown("---")
                st.warning("⚠️ **Important:** The advice is AI based and is not a professional doctor's opinion.")
                
                # Additional tips section
                st.markdown("---")
                st.subheader("💡 Additional Tips")
                st.info("""
                **Remember:**
                - Stay hydrated throughout your workout
                - Listen to your body and rest if needed
                - Maintain proper form to prevent injuries
                - Consistency is key to achieving your goals
                - Consider consulting a healthcare professional before starting any new exercise program
                """)
                
                # Download button for the plan
                st.download_button(
                    label="📥 Download Exercise Plan",
                    data=response.message.content,
                    file_name=f"exercise_plan_{fitness_goal.replace(' ', '_')}_{age}yrs.txt",
                    mime="text/plain"
                )
                
            except ConnectionError as e:
                st.error(f"❌ Connection Error: Cannot connect to Ollama")
                st.error(f"Details: {str(e)}")
                st.info("""
                **Ollama is not running!**
                
                Please follow these steps:
                1. Open a new PowerShell terminal
                2. Run: `ollama serve`
                3. Wait for it to start (you'll see "Ollama is running")
                4. Come back to this app and try again
                """)
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error(f"Error type: {type(e).__name__}")
                st.info("""
                **Troubleshooting:**
                - Make sure Ollama is running: Open PowerShell and run `ollama serve`
                - Verify that the gemma3:4b model is installed: `ollama list`
                - If model is missing, install it: `ollama pull gemma3:4b`
                - Try refreshing the page and generating again
                """)
                
                # Show expanded error details
                with st.expander("🔍 View detailed error information"):
                    st.code(str(e))
                    import traceback
                    st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>💪 UAB Sveikata - Exercise Advisor | Powered by Ollama & Streamlit</p>
    <p style='font-size: 0.8em;'>Disclaimer: The advice is AI based and is not a professional doctor's opinion. Consult with healthcare professionals before starting any exercise program.</p>
</div>
""", unsafe_allow_html=True)
