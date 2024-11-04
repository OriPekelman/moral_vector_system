class MoralAbstractModel:
    def __init__(self):
        self.duties = {
            "perfect": [
                "honesty", "non_harm", "keep_promises", "respect_rights",
                "justice", "non_stealing", "truthfulness", "avoid_exploitation",
                "non_manipulation", "no_false_testimony"
            ],
            "imperfect": [
                "self_improvement", "help_others", "charity", "develop_talents",
                "promote_welfare", "environmental_care", "fairness", "education",
                "community_support", "personal_growth"
            ]
        }

    def get_all_duties(self):
        return self.duties["perfect"] + self.duties["imperfect"]
