import matplotlib.pyplot as plt
import streamlit as st

# Step 1: Set up a small food database (food: [calories, tag])
FOODS = {
    # Fruits
    "apple": [52, "sweet"],
    "banana": [89, "sweet"],
    "grapes": [69, "sweet"],
    "strawberries": [32, "sweet"],
    "blueberries": [57, "sweet"],
    "avocado": [160, "creamy"],
    "orange": [47, "fresh"],
    "watermelon": [30, "fresh"],

    # Vegetables
    "broccoli": [34, "fresh"],
    "spinach": [23, "fresh"],
    "carrots": [41, "fresh"],
    "mushrooms": [22, "fresh"],
    "cucumber": [16, "fresh"],
    "sweet potato": [86, "filling"],

    # Protein / Meats / Seafood
    "chicken breast": [165, "savoury"],
    "grilled tofu": [144, "savoury"],
    "salmon": [208, "savoury"],
    "tuna": [132, "savoury"],
    "shrimp": [99, "savoury"],
    "beef steak": [250, "savoury"],
    "boiled egg": [155, "protein"],
    "scrambled egg": [148, "protein"],

    # Grains / Carbs
    "white rice": [130, "filling"],
    "brown rice": [123, "filling"],
    "quinoa": [120, "filling"],
    "whole wheat bread": [247, "filling"],
    "oats": [389, "filling"],
    "noodles": [138, "filling"],
    "pasta": [131, "filling"],
    "roti": [297, "filling"],

    # Dairy & Alternatives
    "milk": [42, "creamy"],
    "soy milk": [33, "creamy"],
    "yogurt": [59, "creamy"],
    "greek yogurt": [97, "creamy"],
    "cheese": [402, "savoury"],

    # Snacks / Treats
    "dark chocolate": [598, "chocolate"],
    "milk chocolate": [535, "chocolate"],
    "cookies": [488, "sweet"],
    "ice cream": [207, "sweet"],
    "peanut butter": [588, "nutty"],
    "almonds": [579, "nutty"],
    "cashews": [553, "nutty"],
    "granola": [471, "filling"],
    "protein bar": [350, "protein"]
}

# Step 2: Meal plan generator
def create_meal_plan(goal, max_calories, cravings, fav_foods):
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meal_plan = []
    total_cals = 0
    used_foods = set()

    calories_per_meal = max_calories // len(meals)

    for meal in meals:
        # Filter food choices
        options = [food_name for food_name in FOODS if (cravings in FOODS[food_name][1] or food_name in fav_foods) and food_name not in used_foods]
        if not options:
            options = [food_name for food_name in FOODS if food_name not in used_foods]
        if not options:
            options = list(FOODS.keys())

        selected_food = None
        for food_name in options:
            cal_per_serving = FOODS[food_name][0]
            if cal_per_serving > 0:
                servings = calories_per_meal // cal_per_serving
                if servings >= 1:
                    total_food_cal = servings * cal_per_serving
                    meal_plan.append((meal, food_name, servings, total_food_cal))
                    total_cals += total_food_cal
                    used_foods.add(food_name)
                    selected_food = food_name
                    break # Move to the next meal after selecting one food

        # If no food was selected for a meal, you might want to handle it (e.g., skip it or add a placeholder)
        if not selected_food:
            meal_plan.append((meal, "No food selected", 0, 0)) # Placeholder
            
    return meal_plan, total_cals


# Step 3: Build the Streamlit app
st.title("🥗 Diet Timetable Generator")

st.write("Create a daily meal plan based on your goals, calorie intake, cravings, and favourite food.")

goal = st.selectbox("What is your goal?", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
max_calories = st.number_input("Daily calorie limit (min:1500, max:4000)", min_value=1500, max_value=4000, step=50)

cravings = st.text_input("What are you craving today? (choose from: sweet, savoury, chocolate, filling, nutty, protein, creamy, fresh)").lower()
favourites_input = st.text_input("Your favourite foods? (comma separated)").lower()
favourite_foods = [f.strip() for f in favourites_input.split(",") if f]

# Initialize plan and total outside the button's scope
plan = [] # Initialize plan as an empty list
total = 0 # Initialize total calories

if st.button("Generate Diet Plan"):
    plan, total = create_meal_plan(goal, max_calories, cravings, favourite_foods)

    if plan:
        st.subheader("🍴 Your Meal Plan")
        for meal, food, servings, cal in plan: # Assuming your create_meal_plan returns (meal, food, servings, total_food_cal)
            st.write(f"**{meal}**: {servings} serving(s) of {food.title()} — {cal} kcal")
        st.success(f"Total Calories: {total} kcal")

        # Prepare data for pie chart - NOW THIS CODE IS INSIDE THE 'IF PLAN' BLOCK
        # This assumes plan items are (meal_name, food_name, servings, total_food_cal)
        meal_names = [item[0] for item in plan] # Meal name is the first element
        meal_cals = [item[3] for item in plan]  # Calories are the fourth element (total_food_cal)

        # Plot pie chart
        fig, ax = plt.subplots()
        ax.pie(meal_cals, labels=meal_names, autopct='%1.1f%%', startangle=90)
        ax.set_title("Calories per Meal")
        st.pyplot(fig)

    else:
        st.error("Could not create a plan with your inputs. Try changing your cravings or foods.")

def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(-23deg, #ff512a, #5bffa6, #ffc67e, #ffa989);
            background-size: 200% 200%;
            animation: gradientBG 20s ease infinite;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }  
        
        /* Specific overrides if needed (e.g., if you wanted some parts black) */
        /* For example, if you wanted the pie chart labels black, you'd add: */
        /*
        .st-emotion-cache-1f810n4.e1tzin5v2 {
            fill: black !important;
            color: white !important;
        }
        */

        /* Ensures Streamlit's text components are white */
        .stMarkdown, .stText, .stSuccess, .stError {
            color: black !important;
        }

        /* Labels for input fields */
        .stSelectbox label, .stNumberInput label, .stTextInput label {
            color: black !important;
        }

        /* Text inside the input fields (what the user types or sees selected) */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            color: white !important;
        }

        /* Selected value text in the selectbox */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="button"] {
             color: white !important;
        }

        /* Button text */
        .stButton > button {
            color: white !important;
        }

        /* Ensure options in dropdown (when opened) are readable. */
        /* This targets the actual text of the options in the dropdown list */
        .stSelectbox div[role="listbox"] div[role="option"] {
            color: black !important; /* Set dropdown options to black for contrast */
            background-color: white !important; /* Give them a white background */
        }
        /* If dropdown options are still white or hard to read, you might need to adjust this */


        /* Text in the sidebar (if you add one later) */
        .stSidebar * {
            color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
 
set_background()