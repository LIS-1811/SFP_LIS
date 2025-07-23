import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAbAsNYSboAyKF3FlwKZ3n49Rme2D45rW4")

# Set up falling fruit background and theme
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(-23deg, #ff512a, #5bffa6, #ffc67e, #ffa989);
            background-size: 500% 500%;
            animation: gradientBG 10s ease infinite;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        @keyframes fall {
            0% {
                top: -50px;
                opacity: 1;
                transform: translateX(0) rotate(0deg);
            }
            100% {
                top: 110vh;
                opacity: 0.6;
                transform: translateX(100px) rotate(360deg);
            }
        }

        .falling-fruit {
            position: absolute;
            width: 40px;
            top: -50px;
            z-index: 0;
            animation-name: fall;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        }

        .fruit-1 { left: 10%; animation-duration: 6s; animation-delay: 0s; }
        .fruit-2 { left: 30%; animation-duration: 8s; animation-delay: 1s; }
        .fruit-3 { left: 50%; animation-duration: 5s; animation-delay: 2s; }
        .fruit-4 { left: 70%; animation-duration: 7s; animation-delay: 3s; }
        .fruit-5 { left: 90%; animation-duration: 9s; animation-delay: 4s; }
        </style>

        <img class="falling-fruit fruit-1" src="https://cdn-icons-png.flaticon.com/512/590/590685.png" />
        <img class="falling-fruit fruit-2" src="https://cdn-icons-png.flaticon.com/128/25/25345.png" />
        <img class="falling-fruit fruit-3" src="https://cdn-icons-png.flaticon.com/512/590/590707.png" />
        <img class="falling-fruit fruit-4" src="https://cdn-icons-png.flaticon.com/128/765/765608.png" />
        <img class="falling-fruit fruit-5" src="https://cdn-icons-png.flaticon.com/512/590/590692.png" />
        """,
        unsafe_allow_html=True
    )

# Gemini-powered meal plan generator
def create_meal_plan_with_gemini(goal, calories, cravings, fav_foods):
    prompt = f"""
You are a helpful and qualified dietitian. Create a healthy and realistic 1-day meal plan for someone whose goal is to "{goal.lower()}". 
Their daily calorie target is {calories} kcal. They are craving something "{cravings}". Their favourite foods are: {', '.join(fav_foods) if fav_foods else 'none'}.

The meal plan should include:
- Breakfast
- Lunch
- Snack
- Dinner

Each meal must include:
- Food name
- Short description
- Estimated calories

Also provide:
- Total daily calories
- Ensure the calorie target is NOT exceeded

Use this format:

Breakfast:
- Food: ...
- Description: ...
- Calories: ...

...

Total Calories: ...

Avoid unrealistic items. Focus on healthy, enjoyable, and balanced options.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
set_background()

st.title("🥗 AI Diet Timetable Generator")

st.markdown(
    "<p style='color:black; font-size:16px;'>Create a daily meal plan based on your goals, calorie intake, cravings, and favourite food.</p>",
    unsafe_allow_html=True
)

goal = st.selectbox("What is your goal?", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
max_calories = st.number_input("Daily calorie limit (min: 1500, max: 4000)", min_value=1500, max_value=4000, step=50)

cravings = st.selectbox("What are you craving today?", ["sweet", "savoury", "filling", "nutty", "protein", "creamy", "fresh"]).lower()
favourites_input = st.text_input("Your favourite foods? (comma separated)").lower()
favourite_foods = [f.strip() for f in favourites_input.split(",") if f]

if st.button("Generate Diet Plan"):
    with st.spinner("Asking Gemini to generate your meal plan..."):
        result = create_meal_plan_with_gemini(goal, max_calories, cravings, favourite_foods)
    st.subheader("🍴 Your AI-Generated Meal Plan")
    st.markdown(f"<div style='color:black; font-size:16px;'>{result}</div>", unsafe_allow_html=True)

# Make labels/questions black
st.markdown("""
<style>
div.stSelectbox > label, 
div.stTextInput > label, 
div.stNumberInput > label {
    color: black !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
