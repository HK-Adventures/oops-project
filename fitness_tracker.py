from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Dict
import pandas as pd

@dataclass
class Workout:
    date: date
    activity_type: str
    duration: int  # in minutes
    calories_burned: int
    notes: str = ""

@dataclass
class Goal:
    target_type: str  # "calories", "duration", "workouts"
    target_value: int
    start_date: date
    end_date: date
    description: str = ""

class FitnessTracker:
    def __init__(self):
        self.workouts: List[Workout] = []
        self.goals: List[Goal] = []
    
    def add_workout(self, workout: Workout) -> None:
        self.workouts.append(workout)
    
    def add_goal(self, goal: Goal) -> None:
        self.goals.append(goal)
    
    def get_workouts_by_date_range(self, start_date: date, end_date: date) -> List[Workout]:
        return [
            workout for workout in self.workouts
            if start_date <= workout.date <= end_date
        ]
    
    def get_total_calories_burned(self, start_date: date, end_date: date) -> int:
        workouts = self.get_workouts_by_date_range(start_date, end_date)
        return sum(workout.calories_burned for workout in workouts)
    
    def get_total_duration(self, start_date: date, end_date: date) -> int:
        workouts = self.get_workouts_by_date_range(start_date, end_date)
        return sum(workout.duration for workout in workouts)
    
    def get_workout_summary(self) -> pd.DataFrame:
        if not self.workouts:
            return pd.DataFrame(columns=['Date', 'Activity', 'Duration (mins)', 'Calories Burned', 'Notes'])
        
        return pd.DataFrame([
            {
                'Date': workout.date,
                'Activity': workout.activity_type,
                'Duration (mins)': workout.duration,
                'Calories Burned': workout.calories_burned,
                'Notes': workout.notes
            }
            for workout in sorted(self.workouts, key=lambda x: x.date, reverse=True)
        ])
    
    def get_goals_summary(self) -> pd.DataFrame:
        if not self.goals:
            return pd.DataFrame(columns=['Target Type', 'Target Value', 'Start Date', 'End Date', 'Description'])
        
        return pd.DataFrame([
            {
                'Target Type': goal.target_type,
                'Target Value': goal.target_value,
                'Start Date': goal.start_date,
                'End Date': goal.end_date,
                'Description': goal.description
            }
            for goal in self.goals
        ])
    
    def calculate_goal_progress(self, goal: Goal) -> float:
        if goal.target_type == "calories":
            actual = self.get_total_calories_burned(goal.start_date, goal.end_date)
        elif goal.target_type == "duration":
            actual = self.get_total_duration(goal.start_date, goal.end_date)
        elif goal.target_type == "workouts":
            actual = len(self.get_workouts_by_date_range(goal.start_date, goal.end_date))
        else:
            return 0.0
        
        return min((actual / goal.target_value) * 100, 100) 