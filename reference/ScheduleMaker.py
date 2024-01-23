import datetime, math
from CourseBuilder import CourseBuilder, Lecture

PAUSING_BUFFER_RATIO = 1.5  # a 1 hour lecture will take 1.5 hours to complete with the pausing buffer

class Schedule:
    def __init__(self, course):
        self.course: CourseBuilder = course
        self.days_until_completion = -1
        self.hours_per_day = -1
        self.start_date = None
        self.pausing_buffer = False
        self.video_speed = 1.0

    def get_user_input(self):
        """ Get user input for days until completion, hours per day, and start date. """
        prompt = "(1) Do you want to finish the course in a specific number of days or (2) spend a specific number of hours per day until completion? (days/hours): "
        while True:
            try:
                choice = int(input(prompt))
                if choice == 1:
                    self.days_until_completion = int(input("Enter the number of days until completion: "))
                    break
                elif choice == 2:
                    self.hours_per_day = int(input("Enter the number of hours per day: "))
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        while True:
            try:
                start_date = input("Enter the start date (YYYY-MM-DD): (Blank for tomorrow)")
                if start_date == "":
                    self.start_date = datetime.date.today() + datetime.timedelta(days=1)
                else:
                    self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date. Please enter a valid date in the format YYYY-MM-DD.")

        self.pausing_buffer = input("Do you want to add a pausing buffer? (y/n): ").lower() == 'y'
        self.video_speed = float(input("Enter the video speed (1.0 for normal speed): Eg. 1.25, 1.5, 1.75, 2.0: "))

        print("Thank you. We will now build the schedule.")

    def build(self):
        """ Build the schedule based on the user input. """
        if self.days_until_completion != -1:
            self.build_by_days()
        else:
            self.build_by_hours()

    def build_by_days(self):
        """ Build the schedule based on the number of days until completion. """
        lectures_per_section = self.course.sections_and_lectures

        # Calculate the number of seconds per day, factor in the video speed
        seconds_per_day = (self.course.total_duration_seconds / self.days_until_completion / self.video_speed) * PAUSING_BUFFER_RATIO if self.pausing_buffer else self.course.total_duration_seconds / self.days_until_completion / self.video_speed

        lectures_per_day = {}
        current_day = 1
        date = self.start_date
        cumulative_seconds = 0
        day_format = lambda x, y: f"Day {x} ({y.strftime('%Y-%m-%d')})"
        lectures_per_day[day_format(current_day, date)] = []
        for section in lectures_per_section:
            for lecture in lectures_per_section[section]:
                lecture_duration = lecture.duration_seconds
                if self.pausing_buffer:
                    lecture_duration *= PAUSING_BUFFER_RATIO
                cumulative_seconds += lecture_duration / self.video_speed

                lectures_per_day[day_format(current_day, date)].append(lecture)
                
                if cumulative_seconds >= seconds_per_day:
                    cumulative_seconds = 0
                    current_day += 1
                    date = self.start_date + datetime.timedelta(days=current_day - 1)
                    lectures_per_day[day_format(current_day, date)] = []

        self.export_to_txt(lectures_per_day)

    def build_by_hours(self):
        """ Build the schedule based on the number of hours per day. """
        lectures_per_section = self.course.sections_and_lectures

        seconds_per_day = self.hours_per_day * 3600
        lectures_per_day = {}
        current_day = 1
        date = self.start_date
        cumulative_seconds = 0
        day_format = lambda x, y: f"Day {x} ({y.strftime('%Y-%m-%d')})"
        lectures_per_day[day_format(current_day, date)] = []

        for section in lectures_per_section:
            for lecture in lectures_per_section[section]:
                lecture_duration = lecture.duration_seconds
                if self.pausing_buffer:
                    lecture_duration *= PAUSING_BUFFER_RATIO
                cumulative_seconds += lecture_duration / self.video_speed

                lectures_per_day[day_format(current_day, date)].append(lecture)
                
                if cumulative_seconds >= seconds_per_day:
                    cumulative_seconds = 0
                    current_day += 1
                    date = self.start_date + datetime.timedelta(days=current_day - 1)
                    lectures_per_day[day_format(current_day, date)] = []

        self.export_to_txt(lectures_per_day)

    def export_to_txt(self, lectures_per_day):
        """ Export the schedule to a text file. """
        with open(f"{self.course.id}_schedule.txt", "w") as file:
            file.write(f"{self.course.title} Schedule\n")
            file.write(
                f"Total duration: {self.course.total_duration_seconds // 3600}:"
                f"{self.course.total_duration_seconds % 3600 // 60:02} (hh:mm)\n"
            )
            if self.days_until_completion != -1:
                file.write(f"Days until completion: {self.days_until_completion}\n")
                if self.pausing_buffer:
                    file.write(
                        f"To complete the course in {self.days_until_completion} days, you will need to spend about "
                        f"{round(self.course.total_duration_seconds / self.days_until_completion / 3600 * PAUSING_BUFFER_RATIO, 2)} hours per day.\n")
                else:
                    file.write(f"To complete the course in {self.days_until_completion} days, you will need to spend about {round(self.course.total_duration_seconds / self.days_until_completion / 3600, 2)} hours per day.\n")
            else:
                file.write(f"Hours per day: {self.hours_per_day}\n")
                file.write(f"If you spend {self.hours_per_day} hours per day, you will complete the course in {len(lectures_per_day)} days.\n")
            file.write(f"Start date: {self.start_date.strftime('%Y-%m-%d')}\n")
            file.write(f"Pausing buffer: {self.pausing_buffer}\n")
            file.write(f"Video speed: {self.video_speed}\n\n")

            for day in lectures_per_day:
                file.write(f"{day}\n")
                file.write("*-" * 20 + "\n")
                for lecture in lectures_per_day[day]:
                    file.write(f"{lecture.title} - {lecture.duration_seconds // 60}:{lecture.duration_seconds % 60:02} ({lecture.lecture_type.value})\n")
                file.write("\n")


