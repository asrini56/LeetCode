class Solution:
    def angleClock(self, hour: int, minutes: int, seconds: int = 0, return_larger: bool = False) -> float:
        """
        Calculates the angle between the hour and minute hands,
        accounting for continuous movement from seconds, with an option
        to return the larger (reflex) angle.
        """
        # Minute hand position (degrees per minute + degrees per second)
        minute_angle = (minutes + seconds / 60.0) * 6
        
        # Hour hand position (30°/hr + 0.5°/min + (30/3600)°/sec)
        hour_angle = (hour % 12) * 30 + (minutes / 60.0) * 30 + (seconds / 3600.0) * 30
        
        # Absolute difference between the two hands
        diff = abs(hour_angle - minute_angle)
        
        # Return either the smaller or larger angle
        if return_larger:
            return max(diff, 360 - diff)
        else:
            return min(diff, 360 - diff)
