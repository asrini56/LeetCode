from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Union, FrozenSet

@dataclass(frozen=True)
class SlotPolicy:
    start_hour: int
    end_hour: int
    holidays: FrozenSet[date]
    slot_minutes: int = 60

    def slots_for_day(self, day: date) -> List[datetime]:
        """Generates valid 1-hour time slots for a given day, excluding weekends and holidays."""
        if day.weekday() >= 5 or day in self.holidays:
            return []
        cur = datetime.combine(day, time(self.start_hour))
        end = datetime.combine(day, time(self.end_hour))
        step = timedelta(minutes=self.slot_minutes)
        out = []
        while cur + step <= end:
            out.append(cur)
            cur += step
        return out

@dataclass(frozen=True)
class InspectionRecord:
    vehicle_id: str
    inspection_slot: datetime
    next_renewal_due: date

def schedule_vehicles(vehicle_ids: List[str], days: List[date], policy: SlotPolicy) -> Dict[str, datetime]:
    """Distributes vehicles evenly across available slots using a round-robin queue approach."""
    day_slots = {day: policy.slots_for_day(day) for day in days}
    
    # Flatten available slots into per-day queues
    queues = {d: list(slots) for d, slots in day_slots.items() if slots}
    schedule = {}
    active_days = list(queues)
    
    if not active_days:
        raise ValueError("No active working days available for scheduling.")

    i = 0
    for vehicle in vehicle_ids:
        if not active_days:
            raise ValueError("Capacity overflow: Not enough slots available for all vehicles.")
        
        day = active_days[i % len(active_days)]
        schedule[vehicle] = queues[day].pop(0)
        
        # If a day's queue is empty, remove it from active rotation
        if not queues[day]:
            active_days.remove(day)
            i = 0  # Reset index safely
        else:
            i += 1
            
    return schedule

def schedule_vehicles_with_recurrence(
    vehicle_ids: List[str], 
    days: List[date], 
    policy: SlotPolicy
) -> Dict[str, InspectionRecord]:
    """Wraps the scheduler to attach 6-month recurrence tracking to each inspection."""
    base_schedule = schedule_vehicles(vehicle_ids, days, policy)
    extended_schedule = {}
    
    for vehicle, slot_dt in base_schedule.items():
        # Compute 6-month renewal anniversary (approx 182 days)
        renewal_date = (slot_dt + timedelta(days=182)).date()
        extended_schedule[vehicle] = InspectionRecord(
            vehicle_id=vehicle,
            inspection_slot=slot_dt,
            next_renewal_due=renewal_date
        )
        
    return extended_schedule

# ==========================================
# Demonstration & Dynamic Configuration Test
# ==========================================
if __name__ == "__main__":
    # 1. Setup planning window (1 work week: Monday to Friday)
    start_date = date(2026, 6, 1)
    days = [start_date + timedelta(days=i) for i in range(5)]
    
    # 2. Define fleet and holidays
    vehicles = [f"V-{i:03d}" for i in range(1, 16)] # 15 vehicles
    holidays = frozenset([date(2026, 6, 3)])          # Closed holiday on Wednesday

    print("=== Test 1: Original Config (Hours: 10:00 to 16:00) ===")
    policy_v1 = SlotPolicy(start_hour=10, end_hour=16, holidays=holidays)
    schedule_v1 = schedule_vehicles_with_recurrence(vehicles, days, policy_v1)
    
    for v_id, record in list(schedule_v1.items()[:3]):
        print(f"Vehicle {v_id} -> Inspection: {record.inspection_slot.strftime('%Y-%m-%d %H:%M')} | Renewal Due: {record.next_renewal_due}")

    print("\n=== Test 2: Updated Config (Interviewer changes hours to 11:00 to 15:00) ===")
    # Instantiating a new frozen policy object with updated working hours
    policy_v2 = SlotPolicy(start_hour=11, end_hour=15, holidays=holidays)
    schedule_v2 = schedule_vehicles_with_recurrence(vehicles, days, policy_v2)
    
    for v_id, record in list(schedule_v2.items()[:3]):
        print(f"Vehicle {v_id} -> Inspection: {record.inspection_slot.strftime('%Y-%m-%d %H:%M')} | Renewal Due: {record.next_renewal_due}")
