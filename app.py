import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "page": 1,
    "age_group": "",
    "suggested_goal": 2250,
    "goal": 2250,
    "total_water": 0,
    "reminders": True,
    "reminder_time": "Every 2 hours",
    "last_logged": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def navigate(page):
    st.session_state.page = page
    st.rerun()


# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #F1F8FC;
}

.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: #183D55;
}

p, label {
    color: #58788A;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 18px rgba(20, 100, 140, 0.06);
}

.hero {
    background: linear-gradient(135deg, #D7F2FF, #E5FAF6);
    padding: 35px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #164767;
}

.hero-subtitle {
    font-size: 17px;
    color: #52758A;
}

.mascot {
    font-size: 85px;
    text-align: center;
}

.big-number {
    font-size: 35px;
    font-weight: 800;
    color: #0786B9;
}

.small-label {
    font-size: 14px;
    color: #7894A4;
}

.bottle {
    height: 230px;
    width: 100px;
    border: 5px solid #69BFE1;
    border-radius: 18px 18px 30px 30px;
    margin: 20px auto;
    position: relative;
    overflow: hidden;
    background: #E8F8FF;
}

.water {
    position: absolute;
    bottom: 0;
    width: 100%;
    background: linear-gradient(180deg, #72D8F5, #159CD1);
}

.screen-number {
    font-size: 13px;
    color: #86A5B6;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

div.stButton > button {
    border-radius: 13px;
    min-height: 45px;
    font-weight: 600;
    border: 1px solid #B9DFEF;
    background: #E2F5FD;
    color: #087DAA;
}

div.stButton > button:hover {
    background: #C8EDFC;
    border-color: #69BFE1;
    color: #075A7C;
}

hr {
    border-color: #DCECF3;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# COMMON FUNCTIONS
# =====================================================

def header(number, title, subtitle=""):

    st.markdown(
        f'<div class="screen-number">SCREEN {number} / 13</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()


def mascot_message():

    progress = st.session_state.total_water / st.session_state.goal

    if progress >= 1:
        return "🐢🎉", "You did it! Daily goal completed!"

    elif progress >= 0.75:
        return "🐢💪", "Almost there! Keep going!"

    elif progress >= 0.50:
        return "🐢😊", "Great progress! You're halfway there!"

    elif progress > 0:
        return "🐢💧", "Nice start! Keep drinking water."

    return "🐢", "Ready to get started?"


def show_progress():

    total = st.session_state.total_water
    goal = st.session_state.goal

    remaining = max(goal - total, 0)
    percentage = min(total / goal, 1)

    st.markdown(
        f"""
        <div class="card">
            <p class="small-label">WATER CONSUMED</p>
            <div class="big-number">{total:,} ml</div>
            <p class="small-label">Daily goal: {goal:,} ml</p>
            <p class="small-label">Remaining: {remaining:,} ml</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(percentage)

    st.caption(f"{percentage * 100:.1f}% completed")

    return percentage


def navigation_buttons(back_page, next_page, next_text="Continue"):

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", use_container_width=True):
            navigate(back_page)

    with col2:
        if st.button(next_text + " →", use_container_width=True):
            navigate(next_page)


# =====================================================
# SCREEN 1: WELCOME
# =====================================================

def screen_1():

    st.markdown("""
    <div class="hero">
        <div style="font-size:75px;">💧</div>
        <div class="hero-title">WaterBuddy</div>
        <div class="hero-subtitle">
            Your Daily Hydration Companion
        </div>
        <br>
        <p>Small sips. Better habits. Stay hydrated.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='mascot'>🐢</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>Meet your hydration buddy!</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Let's set up your daily water goal.</p>",
        unsafe_allow_html=True
    )

    if st.button("Get Started", use_container_width=True):
        navigate(2)


# =====================================================
# SCREEN 2: AGE SELECTION
# =====================================================

def screen_2():

    header(
        2,
        "How old are you?",
        "We'll use this to suggest your daily water goal."
    )

    age_group = st.selectbox(
        "Choose your age group",
        [
            "Children (4–8)",
            "Teens (9–13)",
            "Adults (14–64)",
            "Seniors (65+)"
        ],
        index=None,
        placeholder="Select your age group"
    )

    if st.button("Continue", use_container_width=True):

        if age_group is None:
            st.warning("Please select your age group.")

        else:

            goals = {
                "Children (4–8)": 1200,
                "Teens (9–13)": 1700,
                "Adults (14–64)": 2250,
                "Seniors (65+)": 1850
            }

            st.session_state.age_group = age_group
            st.session_state.suggested_goal = goals[age_group]
            st.session_state.goal = goals[age_group]

            navigate(3)


# =====================================================
# SCREEN 3: SUGGESTED GOAL
# =====================================================

def screen_3():

    header(
        3,
        "Your suggested goal",
        "Here's your recommended daily target."
    )

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:50px;">💧</div>
            <p class="small-label">SUGGESTED DAILY INTAKE</p>
            <div class="big-number">
                {st.session_state.suggested_goal:,} ml
            </div>
            <p>{st.session_state.age_group}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "This is a general suggested target. "
        "Individual hydration needs can vary."
    )

    navigation_buttons(2, 4)


# =====================================================
# SCREEN 4: CUSTOM GOAL
# =====================================================

def screen_4():

    header(
        4,
        "Customise your goal",
        "You can adjust your daily target here."
    )

    goal = st.number_input(
        "Daily water goal (ml)",
        min_value=250,
        max_value=5000,
        value=st.session_state.goal,
        step=250,
        key="custom_goal_input"
    )

    st.caption(
        f"Suggested target: {st.session_state.suggested_goal:,} ml"
    )

    if st.button("Save My Goal", use_container_width=True):

        st.session_state.goal = goal
        navigate(5)

    if st.button("Use Suggested Goal", use_container_width=True):

        st.session_state.goal = st.session_state.suggested_goal
        navigate(5)

    if st.button("← Back", use_container_width=True):
        navigate(3)


# =====================================================
# SCREEN 5: HOME DASHBOARD
# =====================================================

def screen_5():

    header(
        5,
        "Your Dashboard",
        "Here's how your hydration is going today."
    )

    percentage = show_progress()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        mascot, message = mascot_message()

        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div class="mascot">{mascot}</div>
                <h3>Your Buddy</h3>
                <p>{message}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <h3>Today's Goal</h3>
                <div style="font-size:42px;">🎯</div>
                <div class="big-number">
                    {st.session_state.goal:,}
                </div>
                <p>ml per day</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("What would you like to do?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💧 Log Water", use_container_width=True):
            navigate(6)

    with col2:
        if st.button("📊 View Progress", use_container_width=True):
            navigate(8)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⚙️ Settings", use_container_width=True):
            navigate(11)

    with col2:
        if st.button("🔄 Reset Progress", use_container_width=True):
            navigate(9)


# =====================================================
# SCREEN 6: LOG WATER
# =====================================================

def screen_6():

    header(
        6,
        "Log Your Water",
        "How much water have you just had?"
    )

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <p class="small-label">CURRENT INTAKE</p>
            <div class="big-number">
                {st.session_state.total_water:,} ml
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Quick Add")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("+250 ml", use_container_width=True):
            st.session_state.total_water += 250
            st.session_state.last_logged = 250
            navigate(7)

    with col2:

        if st.button("+500 ml", use_container_width=True):
            st.session_state.total_water += 500
            st.session_state.last_logged = 500
            navigate(7)

    st.divider()

    custom_amount = st.number_input(
        "Enter another amount (ml)",
        min_value=0,
        max_value=3000,
        value=0,
        step=50,
        key="water_custom_input"
    )

    if st.button("Add Water", use_container_width=True):

        if custom_amount > 0:

            st.session_state.total_water += custom_amount
            st.session_state.last_logged = custom_amount

            navigate(7)

        else:
            st.warning("Please enter an amount greater than zero.")

    if st.button("← Back to Dashboard", use_container_width=True):
        navigate(5)


# =====================================================
# SCREEN 7: LOGGING CONFIRMATION
# =====================================================

def screen_7():

    header(
        7,
        "Water Logged!",
        "Your water intake has been updated."
    )

    st.markdown("""
    <div class="hero">
        <div style="font-size:75px;">💧</div>
        <h2>Nice one!</h2>
        <p>Your water intake has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <p class="small-label">YOU JUST ADDED</p>
            <div class="big-number">
                +{st.session_state.last_logged:,} ml
            </div>
            <p>Total intake: {st.session_state.total_water:,} ml</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Back to Dashboard", use_container_width=True):
        navigate(5)

    if st.button("Log More Water", use_container_width=True):
        navigate(6)


# =====================================================
# SCREEN 8: PROGRESS DETAILS
# =====================================================

def screen_8():

    header(
        8,
        "Your Progress",
        "A closer look at today's hydration."
    )

    percentage = show_progress()

    st.subheader("Daily Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Consumed",
            f"{st.session_state.total_water:,} ml"
        )

    with col2:
        st.metric(
            "Daily Target",
            f"{st.session_state.goal:,} ml"
        )

    remaining = max(
        st.session_state.goal - st.session_state.total_water,
        0
    )

    st.metric("Water Remaining", f"{remaining:,} ml")

    if percentage >= 1:
        st.success("You've completed your daily goal!")

    elif percentage >= 0.5:
        st.info("You're doing well. Keep it up!")

    else:
        st.info("Keep logging your water intake throughout the day.")

    if st.button("← Back to Dashboard", use_container_width=True):
        navigate(5)


# =====================================================
# SCREEN 9: RESET PROGRESS
# =====================================================

def screen_9():

    header(
        9,
        "Reset Progress",
        "Do you want to clear today's water intake?"
    )

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:55px;">🔄</div>
            <h3>Current Progress</h3>
            <div class="big-number">
                {st.session_state.total_water:,} ml
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "Resetting will clear your current daily water intake."
    )

    if st.button("Continue to Reset", use_container_width=True):
        navigate(10)

    if st.button("Cancel", use_container_width=True):
        navigate(5)


# =====================================================
# SCREEN 10: RESET CONFIRMATION
# =====================================================

def screen_10():

    header(
        10,
        "Confirm Reset",
        "Are you sure you want to reset your progress?"
    )

    st.markdown(
        "<div class='mascot'>🐢</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>Start fresh?</h3>",
        unsafe_allow_html=True
    )

    st.write(
        "Your current water intake will be set back to zero."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Yes, Reset", use_container_width=True):

            st.session_state.total_water = 0
            st.session_state.last_logged = 0

            navigate(5)

    with col2:

        if st.button("Cancel", use_container_width=True):
            navigate(5)


# =====================================================
# SCREEN 11: SETTINGS
# =====================================================

def screen_11():

    header(
        11,
        "Settings",
        "Manage your WaterBuddy preferences."
    )

    st.subheader("Your Profile")

    st.markdown(
        f"""
        <div class="card">
            <p class="small-label">AGE GROUP</p>
            <h3>{st.session_state.age_group}</h3>
            <p class="small-label">DAILY WATER GOAL</p>
            <div class="big-number">
                {st.session_state.goal:,} ml
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Change Water Goal", use_container_width=True):
        navigate(4)

    st.divider()

    if st.button("Reminder Preferences", use_container_width=True):
        navigate(12)

    if st.button("Back to Dashboard", use_container_width=True):
        navigate(5)


# =====================================================
# SCREEN 12: REMINDER PREFERENCES
# =====================================================

def screen_12():

    header(
        12,
        "Reminder Preferences",
        "Choose how often you want hydration reminders."
    )

    reminders = st.toggle(
        "Enable reminders",
        value=st.session_state.reminders
    )

    reminder_time = st.selectbox(
        "Reminder frequency",
        [
            "Every 1 hour",
            "Every 2 hours",
            "Every 3 hours",
            "Every 4 hours"
        ],
        index=[
            "Every 1 hour",
            "Every 2 hours",
            "Every 3 hours",
            "Every 4 hours"
        ].index(st.session_state.reminder_time)
        if st.session_state.reminder_time in [
            "Every 1 hour",
            "Every 2 hours",
            "Every 3 hours",
            "Every 4 hours"
        ] else 1
    )

    if st.button("Save Preferences", use_container_width=True):

        st.session_state.reminders = reminders
        st.session_state.reminder_time = reminder_time

        st.success("Preferences saved!")

    if st.button("Preview Reminder", use_container_width=True):
        navigate(13)

    if st.button("← Back to Settings", use_container_width=True):
        navigate(11)


# =====================================================
# SCREEN 13: REMINDER NOTIFICATION
# =====================================================

def screen_13():

    header(
        13,
        "Reminder Notification",
        "Here's how your hydration reminder will look."
    )

    if st.session_state.reminders:

        st.markdown("""
        <div class="hero">
            <div style="font-size:65px;">💧</div>
            <h2>Time for a Water Break!</h2>
            <p>Take a moment to drink some water.</p>
            <div class="mascot">🐢</div>
            <h3>Your Buddy is waiting!</h3>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            f"Reminder frequency: {st.session_state.reminder_time}"
        )

    else:

        st.warning("Your reminders are currently disabled.")

    if st.button("Back to Reminder Settings", use_container_width=True):
        navigate(12)

    if st.button("Return to Dashboard", use_container_width=True):
        navigate(5)


# =====================================================
# SCREEN ROUTING
# =====================================================

screens = {
    1: screen_1,
    2: screen_2,
    3: screen_3,
    4: screen_4,
    5: screen_5,
    6: screen_6,
    7: screen_7,
    8: screen_8,
    9: screen_9,
    10: screen_10,
    11: screen_11,
    12: screen_12,
    13: screen_13
}

# Display the selected screen
screens[st.session_state.page]()