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
    "mango": [60, "sweet"],
    "pineapple": [50, "sweet"],
    "avocado": [160, "creamy"],
    "orange": [47, "fresh"],
    "watermelon": [30, "fresh"],
    "kiwi": [41, "fresh"],
    "papaya": [43, "fresh"],
    "cherries": [50, "sweet"],

    # Vegetables
    "broccoli": [34, "fresh"],
    "spinach": [23, "fresh"],
    "carrots": [41, "fresh"],
    "mushrooms": [22, "fresh"],
    "cucumber": [16, "fresh"],
    "sweet potato": [86, "filling"],
    "kale": [35, "fresh"],
    "pumpkin": [26, "fresh"],
    "cauliflower": [25, "fresh"],
    "edamame": [121, "protein"],

    # Protein / Meats / Seafood
    "chicken breast": [165, "savoury"],
    "grilled tofu": [144, "savoury"],
    "salmon": [208, "savoury"],
    "tuna": [132, "savoury"],
    "shrimp": [99, "savoury"],
    "beef steak": [250, "savoury"],
    "boiled egg": [155, "protein"],
    "scrambled egg": [148, "protein"],
    "tempeh": [195, "protein"],
    "grilled lamb": [294, "savoury"],
    "roasted duck": [337, "savoury"],
    "chicken nuggets": [296, "savoury"],

    # Grains / Carbs
    "white rice": [130, "filling"],
    "brown rice": [123, "filling"],
    "quinoa": [120, "filling"],
    "whole wheat bread": [247, "filling"],
    "oats": [389, "filling"],
    "noodles": [138, "filling"],
    "pasta": [131, "filling"],
    "roti": [297, "filling"],
    "tortilla": [218, "filling"],
    "bagel": [250, "filling"],
    "croissant": [406, "filling"],

    # Dairy & Alternatives
    "milk": [42, "creamy"],
    "soy milk": [33, "creamy"],
    "yogurt": [59, "creamy"],
    "greek yogurt": [97, "creamy"],
    "cheese": [402, "savoury"],
    "butter": [717, "creamy"],
    "cream cheese": [342, "creamy"],
    "ice cream (dairy-free)": [207, "sweet"],

    # Snacks / Treats
    "cookies": [488, "sweet"],
    "ice cream": [207, "sweet"],
    "cake slice": [350, "sweet"],
    "doughnut": [452, "sweet"],
    "potato chips": [536, "savoury"],
    "nachos": [512, "savoury"],
    "popcorn (buttered)": [375, "savoury"],
    "mochi": [100, "sweet"],
    "gummies": [330, "sweet"],
    "pizza": [300, "savoury"],

    # Nuts / Seeds / Spreads
    "peanut butter": [588, "nutty"],
    "almonds": [579, "nutty"],
    "cashews": [553, "nutty"],
    "walnuts": [654, "nutty"],
    "sunflower seeds": [584, "nutty"],
    "chia seeds": [486, "nutty"],
    "hazelnut spread": [541, "sweet"],

    # Drinks
    "orange juice": [45, "sweet"],
    "apple juice": [46, "sweet"],
    "coffee (black)": [2, "bitter"],
    "latte": [150, "creamy"],
    "bubble tea": [160, "sweet"],
    "green tea": [0, "fresh"],
    "protein shake": [200, "protein"],
    "smoothie": [120, "sweet"],

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

st.markdown(
    "<p style='color:black; font-size:16px;'>Create a daily meal plan based on your goals, calorie intake, cravings, and favourite food.</p>",
    unsafe_allow_html=True
)

goal = st.selectbox("What is your goal?", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
max_calories = st.number_input("Daily calorie limit (min:1500, max:4000)", min_value=1500, max_value=4000, step=50)

cravings = st.selectbox("What are you craving today?", ["sweet", "savoury", "filling", "nutty", "protein", "creamy", "fresh"]).lower()
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
            st.markdown(
    f"<p style='color:black; font-size:16px;'><b>{meal}</b>: {servings} serving(s) of {food.title()} — {cal} kcal</p>",
    unsafe_allow_html=True
)
        st.markdown(
    f"<p style='color:black; font-size:18px; font-weight:bold; text-align:center;'>Total Calories: {total} kcal</p>",
    unsafe_allow_html=True
)

        # Prepare data for pie chart - NOW THIS CODE IS INSIDE THE 'IF PLAN' BLOCK
        # This assumes plan items are (meal_name, food_name, servings, total_food_cal)
        meal_names = [item[0] for item in plan] # Meal name is the first element
        meal_cals = [item[3] for item in plan]  # Calories are the fourth element (total_food_cal)

        # Plot pie chart
        fig, ax = plt.subplots()
        ax.pie(meal_cals, labels=meal_names, autopct='%1.1f%%', startangle=45)
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
 
        <!-- Fruit images placed absolutely -->
        <img class="falling-fruit fruit-1" src="https://cdn-icons-png.flaticon.com/512/590/590685.png" />
        <img class="falling-fruit fruit-2" src="https://cdn-icons-png.flaticon.com/128/25/25345.png" />
        <img class="falling-fruit fruit-3" src="https://cdn-icons-png.flaticon.com/512/590/590707.png" />
        <img class="falling-fruit fruit-4" src="https://cdn-icons-png.flaticon.com/128/765/765608.png" />
        <img class="falling-fruit fruit-5" src="https://cdn-icons-png.flaticon.com/512/590/590692.png" />

    """,
        unsafe_allow_html=True)
set_background()

st.markdown("""
<style>
/* Make labels/questions black */
div.stSelectbox > label, 
div.stTextInput > label, 
div.stNumberInput > label {
    color: black !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)