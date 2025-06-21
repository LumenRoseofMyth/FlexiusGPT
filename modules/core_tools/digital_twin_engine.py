class DigitalTwin:
    def __init__(self, user_profile):
        self.state = {
            'phys': user_profile.get('phys_state', {}),
            'psych': user_profile.get('psych_state', {}),
            'social': user_profile.get('social_state', {}),
        }

    def update(self, feedback, session_outcome, context):
        # Continuously update state with new feedback, session data, and context
        self.state['phys'].update(feedback.to_dict())
        self.state['psych']['mood'] = feedback.mood
        # Add more behavioral/context integration as needed

    def risk_score(self):
        # Predict risk of injury/burnout based on composite state
        if self.state['phys'].get('fatigue', 0) > 8 or self.state['psych'].get('mood', 5) < 3:
            return "high"
        return "low"

    def suggest_nudge(self):
        if self.risk_score() == "high":
            return "Recommend deload/rest week, mental health check-in, or motivational intervention."
        return "Continue adaptive progression."
