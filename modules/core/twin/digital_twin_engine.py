import statistics
from datetime import datetime


class DigitalTwin:
    def __init__(self, user_profile):
        self.state = {
            'phys': user_profile.get('phys_state', {}),
            'psych': user_profile.get('psych_state', {}),
            'social': user_profile.get('social_state', {}),
        }

    def update(self, feedback, session_outcome, context, metric=None):
        """Update state with feedback, session data, and optional metrics."""
        # Continuously update state with new feedback, session data, and context
        phys_fb = feedback.to_dict() if hasattr(feedback, "to_dict") else feedback.__dict__
        self.state['phys'].update(phys_fb)
        self.state['psych']['mood'] = feedback.mood
        # Add more behavioral/context integration as needed
        if metric is not None:
            twin = self.state.setdefault('meta', {})
            # START UPGRADE_BLOCK_INIT_TWIN
            if not twin.get("coding_baseline"):
                twin["coding_baseline"] = {
                    "initial_pr_count": metric["metrics"].get("pull_requests", 0),
                    "start_date": metric["date"],
                    "average_lines_added": metric["metrics"].get("lines_added", 0),
                }
            # END
            # START UPGRADE_BLOCK_WEEKLY_DELTA
            if "coding_week_history" not in twin:
                twin["coding_week_history"] = []

            current_week_prs = metric["metrics"].get("pull_requests", 0)
            twin["coding_week_history"].append(current_week_prs)
            if len(twin["coding_week_history"]) > 2:
                twin["coding_week_delta"] = twin["coding_week_history"][-1] - twin["coding_week_history"][-2]
            # END
            # START UPGRADE_BLOCK_PEAK_FLAGGING
            lines_added = metric["metrics"].get("lines_added", 0)
            if lines_added > 1200:
                twin["peak_push_flag"] = True
            else:
                twin["peak_push_flag"] = False
            # END

            # START CODE_ANALYTICS_SIMULATION
            if metric["type"] == "coding":
                commits = metric["metrics"].get("pull_requests", 0)
                twin.setdefault("daily_commit_history", []).append(commits)
                twin["daily_commit_history"] = twin["daily_commit_history"][-7:]
                if len(twin["daily_commit_history"]) > 1:
                    twin["commit_volatility"] = statistics.stdev(
                        twin["daily_commit_history"]
                    )
                else:
                    twin["commit_volatility"] = 0.0

                commit_times = metric.get("data", {}).get("commit_times", [])
                if commit_times:
                    hrs = [datetime.fromisoformat(t).hour for t in commit_times]
                    avg_hr = sum(hrs) / len(hrs)
                    twin.setdefault("commit_hours_history", []).append(avg_hr)
                    twin["commit_hours_history"] = twin["commit_hours_history"][-7:]
                    twin["circadian_rhythm_hour"] = sum(twin["commit_hours_history"])/len(twin["commit_hours_history"])
            # END

    def risk_score(self):
        # Predict risk of injury/burnout based on composite state
        if self.state['phys'].get('fatigue', 0) > 8 or self.state['psych'].get('mood', 5) < 3:
            return "high"
        return "low"

    def suggest_nudge(self):
        if self.risk_score() == "high":
            return "Recommend deload/rest week, mental health check-in, or motivational intervention."
        return "Continue adaptive progression."

    def simulate_fatigue_risk(self) -> bool:
        """Micro-simulate mental fatigue based on mood, fatigue, and volatility."""
        twin = self.state.get("meta", {})
        volatility = twin.get("commit_volatility", 0)
        fatigue = self.state["phys"].get("fatigue", 0)
        mood = self.state["psych"].get("mood", 5)
        score = fatigue + volatility - mood
        return score > 8

