class MultiModalFeedback:
    def __init__(self, pain=0, fatigue=0, mood=0, **kwargs):
        self.pain = pain
        self.fatigue = fatigue
        self.mood = mood
        # Accept arbitrary future signals
        for k, v in kwargs.items():
            setattr(self, k, v)

    def is_critical(self):
        return self.pain > 7 or self.fatigue > 7 or self.mood < 3
