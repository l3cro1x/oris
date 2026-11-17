from datetime import datetime


class Task:
    def __init__(self, text: str, deadline_str: str | None = None):
        self._text = text
        self.deadline_dt = None

        if deadline_str:
            formats = ["%Y-%m-%d_%H:%M", "%d.%m.%Y_%H:%M"]
            for fmt in formats:
                try:
                    self.deadline_dt = datetime.strptime(deadline_str, fmt)
                    break
                except ValueError:
                    continue
            if not self.deadline_dt:
                print(f"Warning: Could not parse deadline string '{deadline_str}'")
    def task_text(self) -> str:
        return self._text
    def left(self) -> str:
        if not self.deadline_dt:
            return "No deadline"
        now = datetime.now()
        if now > self.deadline_dt:
            return "Expired"
        time_left = self.deadline_dt - now
        days = time_left.days
        hours = time_left.seconds // 3600
        remainder = time_left.seconds % 3600
        minutes = remainder // 60
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        return f"{hours}h {minutes}m"
