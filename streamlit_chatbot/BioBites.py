import streamlit as st

# Step 1: Set up a small food database (food: [calories, tag])
FOODS = {
    "apple": [95, "sweet"],
    "banana": [105, "sweet"],
    "orange": [62, "fresh"],
    "grapes": [70, "sweet"],
    "watermelon": [46, "fresh"],
    "strawberries": [50, "sweet"],
    "blueberries": [85, "sweet"],

    "chicken breast": [165, "savory"],
    "grilled tofu": [144, "savory"],
    "salmon": [208, "savory"],
    "tuna": [179, "savory"],
    "scrambled egg": [91, "protein"],
    "boiled egg": [78, "protein"],
    "shrimp": [99, "savory"],

    "broccoli": [55, "fresh"],
    "spinach": [23, "fresh"],
    "carrots": [41, "fresh"],
    "sweet potato": [103, "filling"],
    "mushrooms": [22, "fresh"],
    "avocado": [160, "creamy"],

    "rice": [206, "filling"],
    "quinoa": [222, "filling"],
    "whole wheat bread": [110, "filling"],
    "oats": [150, "filling"],
    "noodles": [220, "filling"],
    "pasta": [210, "filling"],
    "roti": [150, "filling"],

    "dark chocolate": [170, "chocolate"],
    "milk chocolate": [235, "chocolate"],
    "cookies": [160, "sweet"],
    "ice cream": [207, "sweet"],
    "peanut butter": [190, "nutty"],
    "almonds": [164, "nutty"],
    "cashews": [157, "nutty"],

    "protein bar": [210, "protein"],
    "yogurt": [100, "creamy"],
    "cheese": [113, "savory"],
    "milk": [103, "creamy"],
    "soy milk": [80, "creamy"],
    "granola": [190, "filling"]
}

# Step 2: Meal plan generator
def create_meal_plan(goal, max_calories, cravings, fav_foods):
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meal_plan = []
    total_cals = 0
    used_foods = set()  # Track already used foods

    for meal in meals:
        # Try to get foods that match cravings or favourites
        options = [food for food in FOODS if (cravings in food or food in fav_foods) and food not in used_foods]

        # If no new foods match cravings/favourites, use any unused food
        if not options:
            options = [food for food in FOODS if food not in used_foods]

        # If all foods are used, reset (optional)
        if not options:
            options = list(FOODS.keys())

        # Pick the first food that fits calorie limit
        for food in options:
            calories = FOODS[food][0]
            if total_cals + calories <= max_calories:
                meal_plan.append((meal, food, calories))
                total_cals += calories
                used_foods.add(food)
                break

    return meal_plan, total_cals


# Step 3: Build the Streamlit app
st.title("🥗 Diet Timetable Generator")

st.write("Create a daily meal plan based on your goals, calorie intake, cravings, and favourite food.")

goal = st.selectbox("What is your goal?", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
max_calories = st.number_input("Daily calorie limit", min_value=800, max_value=4000, step=50)

cravings = st.text_input("What are you craving today? (e.g. sweet, savory, chocolate)").lower()
favourites_input = st.text_input("Your favourite foods? (comma separated)").lower()
favourite_foods = [f.strip() for f in favourites_input.split(",") if f]

if st.button("Generate Diet Plan"):
    plan, total = create_meal_plan(goal, max_calories, cravings, favourite_foods)

    if plan:
        st.subheader("🍴 Your Meal Plan")
        for meal, food, cal in plan:
            st.write(f"**{meal}**: {food.title()} — {cal} kcal")
        st.success(f"Total Calories: {total} kcal")
    else:
        st.error("Could not create a plan with your inputs. Try changing your cravings or foods.")
