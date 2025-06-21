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
        self.state['phys'].update(feedback.to_dict())
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
            # START SPEC004_VOLATILITY
            hist = twin.setdefault("coding_metrics_history", [])
            hist.append(metric["metrics"])
            values = [m.get("lines_added", 0) for m in hist[-7:]]
            if values:
                avg = sum(values) / len(values)
                twin["volatility"] = (sum((v - avg) ** 2 for v in values) / len(values)) ** 0.5
            # END
            # START SPEC004_CIRCADIAN
            hour = metric.get("hour")
            if hour is not None:
                hours = twin.setdefault("activity_hours", [])
                hours.append(hour)
                if len(hours) > 50:
                    hours.pop(0)
                buckets = {}
                for h in hours:
                    b = h // 6
                    buckets[b] = buckets.get(b, 0) + 1
                twin["circadian_peak"] = max(buckets, key=buckets.get)
            # END
            # START SPEC004_BURNOUT
            if twin.get("volatility", 0) > 300 or twin.get("peak_push_flag"):
                twin["burnout_risk"] = "high"
            else:
                twin["burnout_risk"] = "low"
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
