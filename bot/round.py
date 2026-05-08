from datetime import datetime

CATEGORIES = ["Państwo", "Miasto", "Imię", "Zwierzę", "Roślina"]


class Round:
    def __init__(self, round_number: int, letter: str):
        self.round_number = round_number
        self.letter       = letter
        # {discord_id: {category: (answer_str, is_valid, reason)}}
        self.validated_answers: dict = {}
        self.start_time = datetime.now()
        self.end_time: datetime | None = None

    def set_validated_answers(self, discord_id: str, cat_results: dict):
        """Store the fully-validated answer map for one player."""
        self.validated_answers[discord_id] = cat_results

    def calculate_points(self) -> dict[str, int]:
        points = {pid: 0 for pid in self.validated_answers}

        for category in CATEGORIES:
            bucket: dict[str, list[str]] = {}
            for pid, cat_data in self.validated_answers.items():
                entry = cat_data.get(category)
                if entry is None:
                    continue
                answer, is_valid, _ = entry
                answer = answer.strip().upper()
                if is_valid and answer:
                    bucket.setdefault(answer, []).append(pid)

            for pids in bucket.values():
                pts = 10 if len(pids) == 1 else 5
                for pid in pids:
                    points[pid] += pts

        self.end_time = datetime.now()
        return points

    def get_answer_display(self, discord_id: str, category: str) -> str:
        """Return a formatted string for a single player+category cell."""
        cat_data = self.validated_answers.get(discord_id, {})
        entry = cat_data.get(category)
        if not entry:
            return "—"
        answer, is_valid, _ = entry
        if not answer.strip():
            return "—"
        mark = "✅" if is_valid else "❌"
        return f"{answer} {mark}"
