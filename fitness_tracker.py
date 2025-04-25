from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import List, Dict
import pandas as pd
import json
import os

@dataclass
class Workout:
    date: date
    activity_type: str
    duration: int  # in minutes
    calories_burned: int
    notes: str = ""
    
    # Add methods to convert date to/from string for JSON serialization
    def to_dict(self):
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data
    
    @staticmethod
    def from_dict(data):
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        return Workout(**data)

@dataclass
class Goal:
    target_type: str
    target_value: int
    start_date: date
    end_date: date
    description: str = ""
    
    # Add methods to convert dates to/from string for JSON serialization
    def to_dict(self):
        data = asdict(self)
        data['start_date'] = self.start_date.isoformat()
        data['end_date'] = self.end_date.isoformat()
        return data
    
    @staticmethod
    def from_dict(data):
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        return Goal(**data)

class FitnessTracker:
    def __init__(self):
        self.workouts: List[Workout] = []
        self.goals: List[Goal] = []
        self.data_file = "fitness_data.json"
        self.load_data()
    
    def save_data(self):
        """Save workouts and goals to JSON file"""
        data = {
            'workouts': [workout.to_dict() for workout in self.workouts],
            'goals': [goal.to_dict() for goal in self.goals]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)
    
    def load_data(self):
        """Load workouts and goals from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.workouts = [Workout.from_dict(w) for w in data.get('workouts', [])]
                self.goals = [Goal.from_dict(g) for g in data.get('goals', [])]
            except Exception as e:
                print(f"Error loading data: {e}")
                self.workouts = []
                self.goals = []
    
    def add_workout(self, workout: Workout) -> None:
        self.workouts.append(workout)
        self.save_data()
    
    def add_goal(self, goal: Goal) -> None:
        self.goals.append(goal)
        self.save_data()
    
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