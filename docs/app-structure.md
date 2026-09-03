# Fitness Tracker — App Structure

Derived from `hierarchy diagram and UI.drawio` (Page-1: hierarchy, Page-2: UI mockups).

Python Reflex web app, SQLite database.

## 1. Hierarchy

```
Fitness Tracker
├── User Management
│   ├── Register
│   ├── Login
│   └── Logout
├── Fitness Management
│   ├── Workout input
│   ├── Weight input
│   ├── Calorie input
│   └── Step input
└── Progress Management
    ├── Goal tracking
    └── History
```

All of the above read/write to **Database Management**, which holds:

- **User details**
- **Fitness records**
- **Goal records**

These feed a **Notification System**:
- Activity reminders
- Goal Achievement Alerts

## 2. Pages (from UI mockups)

### 2.1 Login
- Fields: Username, Password
- Action: Login button
- Link: "Don't have an account? Sign Up" → Register

### 2.2 Register
- Fields: Name, Date of Birth (Day / Month / Year), Gender, Weight, Height, Email
- Action: Register button

### 2.3 Profile / Account
- Displays: profile picture, Username, Date of Birth, Gender, Weight, Height
- Logout link
- Navigation to: Account Settings, Add Fitness Data, Progress Tracker, Fitness Goals

### 2.4 Fitness Goals (Goals Overview)
- Daily Steps — slider, "x / y steps reached", steps left
- Workout Duration — slider, "x / y workouts duration", duration left
- Weight Goal — slider, current weight, weight left to lose
- Calories Burn — slider, "x / y kcal", calories left to burn
- Progress Summary — pie chart

### 2.5 Add Fitness Data
Four input panels, each with its own Save button:
- **Workout**: Workout Type (dropdown), Duration (minutes), Date
- **Weight**: Weight (kg), Date
- **Calories**: Calories Consumed (kcal), Calories Burned (kcal), Date
- **Steps**: Step Count, Date

### 2.6 History
Tables:
- Workout History — Date, Workout Type, Duration
- Steps History — Date, Steps, Daily Goal
- Weight History — Date, Weight (kg), Change
- Calories History — Date, Calories Consumed, Calories Burned

### 2.7 Goals (setting goals)
Mirrors the Add Fitness Data layout — one panel per goal type, each with a Save button:
- Daily Workout Duration
- Weight
- Daily Calories
- Daily Steps

## 3. Data entities implied by the above

These are the entities the database design (next step) needs to cover:

- **User** — identity + profile (name, DOB, gender, weight, height, email, username, password)
- **Workout record** — type, duration, date
- **Weight record** — weight, date
- **Calorie record** — consumed, burned, date
- **Step record** — step count, date
- **Goal** — per goal type (steps, workout duration, weight, calories), target value, current progress
- **Notification** — activity reminders, goal achievement alerts
