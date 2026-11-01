class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        """
        1. Minute Hand Position
        - A clock has 360° and 60 minutes on the dial.
        - Each minute represents: 360° / 60 = 6° per minute.
        - Minute Angle = minutes * 6
        
        2. Hour Hand Position
        - A clock has 12 hours on the dial, so each hour represents: 360° / 12 = 30° per hour.
        - The hour hand also moves slightly as minutes pass (it covers 30° in 60 minutes, which is 0.5° per minute).
        - Hour Angle = (hour % 12) * 30 + minutes * 0.5
        
        3. Finding the Smaller Angle
        - Calculate the absolute difference between the two angles: diff = abs(hour_angle - minute_angle)
        - The smaller angle is the minimum of diff and 360 - diff.
        """
        minute_angle = minutes * 6
        hour_angle = (hour % 12) * 30 + minutes * 0.5
        
        diff = abs(hour_angle - minute_angle)
        
        return min(diff, 360 - diff)
