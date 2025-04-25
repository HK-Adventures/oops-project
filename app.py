import streamlit as st
import plotly.express as px
from datetime import datetime, date, timedelta
from fitness_tracker import FitnessTracker, Workout, Goal

class FitnessApp:
    def __init__(self):
        # Initialize tracker without session state
        self.tracker = FitnessTracker()
        
    def run(self):
        st.title("🏃‍♂️ Fitness Tracker")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigate",
            ["Dashboard", "Log Workout", "Set Goals"]
        )
        
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Log Workout":
            self.log_workout()
        else:
            self.set_goals()
    
    def show_dashboard(self):
        st.header("Fitness Dashboard")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", date.today())
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        workouts = self.tracker.get_workouts_by_date_range(start_date, end_date)
        
        with col1:
            st.metric("Total Workouts", len(workouts))
        with col2:
            st.metric("Total Minutes", self.tracker.get_total_duration(start_date, end_date))
        with col3:
            st.metric("Calories Burned", self.tracker.get_total_calories_burned(start_date, end_date))
        
        # Workout history
        st.subheader("Recent Workouts")
        workout_df = self.tracker.get_workout_summary()
        if not workout_df.empty:
            st.dataframe(workout_df, use_container_width=True)
            
            # Activity distribution chart
            fig = px.pie(workout_df, names='Activity', title='Workout Distribution')
            st.plotly_chart(fig)
        else:
            st.info("No workouts logged yet. Start by adding a workout!")
        
        # Goals progress
        st.subheader("Goals Progress")
        goals_df = self.tracker.get_goals_summary()
        if not goals_df.empty:
            for _, goal in goals_df.iterrows():
                goal_obj = Goal(
                    target_type=goal['Target Type'],
                    target_value=goal['Target Value'],
                    start_date=goal['Start Date'],
                    end_date=goal['End Date'],
                    description=goal['Description']
                )
                progress = self.tracker.calculate_goal_progress(goal_obj)
                st.write(f"**{goal['Description']}**")
                st.progress(progress / 100)
                st.write(f"Progress: {progress:.1f}%")
        else:
            st.info("No goals set yet. Add some goals to track your progress!")
    
    def log_workout(self):
        st.header("Log New Workout")
        
        with st.form("workout_form"):
            workout_date = st.date_input("Workout Date", date.today())
            activity_type = st.selectbox(
                "Activity Type",
                ["Running", "Cycling", "Swimming", "Weight Training", "Yoga", "Other"]
            )
            duration = st.number_input("Duration (minutes)", min_value=1, value=30)
            calories = st.number_input("Calories Burned", min_value=0, value=100)
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Log Workout")
            
            if submitted:
                workout = Workout(
                    date=workout_date,
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    notes=notes
                )
                self.tracker.add_workout(workout)
                st.success("Workout logged successfully!")
    
    def set_goals(self):
        st.header("Set Fitness Goals")
        
        with st.form("goal_form"):
            target_type = st.selectbox(
                "Goal Type",
                ["calories", "duration", "workouts"]
            )
            target_value = st.number_input(
                "Target Value",
                min_value=1,
                help="Calories, minutes, or number of workouts"
            )
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            description = st.text_input(
                "Goal Description",
                help="e.g., 'Burn 5000 calories this month'"
            )
            
            submitted = st.form_submit_button("Set Goal")
            
            if submitted:
                if end_date <= start_date:
                    st.error("End date must be after start date!")
                else:
                    goal = Goal(
                        target_type=target_type,
                        target_value=target_value,
                        start_date=start_date,
                        end_date=end_date,
                        description=description
                    )
                    self.tracker.add_goal(goal)
                    st.success("Goal set successfully!")

if __name__ == "__main__":
    app = FitnessApp()
    app.run() 