import numpy as np

def workload_score(tasks_count, hours_worked, deadline_pressure, complexity_factor, skill_level_factor, w1=1.0, w2=1.0, w3=1.0, w4=1.0):
    return (
        tasks_count * w1 +
        hours_worked * w2 +
        deadline_pressure * w3 +
        complexity_factor * w4
    ) / max(skill_level_factor, 1)
