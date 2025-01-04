import CourseBuilder
import ScheduleMaker
import requests, re
from colorama import just_fix_windows_console
from colorama import init
from colorama import Fore, Back, Style

just_fix_windows_console()
init(autoreset=True)

CURRICULUM_ENDPOINT = "https://www.udemy.com/api-2.0/course-landing-components/???/me/?components=curriculum_context"


def get_course_id_and_title(website_url):
    response = requests.get(website_url)
    pattern_id = r'/(\d+)_'
    pattern_title = r'<meta name="title" content="([^"]+)">'

    course_id = re.search(pattern_id, response.text).group(1)
    course_title = re.search(pattern_title, response.text).group(1)

    return course_id, course_title


def is_valid_url(website_url: str) -> tuple[bool, bool]:
    # https://www.udemy.com/course-dashboard-redirect/?course_id=1406344
    pattern_with_id = r'https://www.udemy.com/course-dashboard-redirect/\?course_id=\d+'
    # https://www.udemy.com/course/javascript-beginners-complete-tutorial/
    pattern_with_course_link = r'https://www.udemy.com/course/[^/]+/'

    return bool(re.match(pattern_with_id, website_url)), bool(re.match(pattern_with_course_link, website_url))


def get_course_detail(course_detail, endpoint_url):
    response = requests.get(endpoint_url)
    response.raise_for_status()
    data = response.json()
    sections = data['curriculum_context']['data']['sections']
    for section in sections:
        section_name = section['title']
        lectures = []
        for lecture in section['items']:
            lectures.append(lecture)
        course_detail[section_name] = lectures


if __name__ == "__main__":
    WEBSITE_URL = input("Enter the course URL: ").strip()

    url_is_valid = is_valid_url(WEBSITE_URL)

    if not url_is_valid[0] and not url_is_valid[1]:
        print(Fore.RED + "Invalid URL.")
        raise Exception("Invalid URL.")

    if url_is_valid[1]:
        print("Getting course ID and title...")
        try:
            course_id, course_title = get_course_id_and_title(WEBSITE_URL)
            print(course_id, course_title, sep="\n")
        except:
            print(Fore.RED + "Invalid URL.")
            raise Exception("Invalid URL.")

    if url_is_valid[0]:
        print("Getting course ID and title...")
        try:
            course_id = WEBSITE_URL.split("=")[1]
            endpoint_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title"
            response = requests.get(endpoint_url)

            if response.status_code != 200:
                print(Fore.RED + "Invalid URL.")
                raise Exception("Invalid URL.")
            else:
                course_title = response.json()['title']
                print(course_id, course_title, sep="\n")
        except:
            print(Fore.RED + "Invalid URL.")
            raise Exception("Invalid URL.")

    endpoint_url = CURRICULUM_ENDPOINT.replace("???", str(course_id))
    print(Fore.GREEN + "Getting course detail...")
    course_detail = {}
    get_course_detail(course_detail, endpoint_url)

    print(Fore.GREEN + "Building course...")
    course_builder = CourseBuilder.CourseBuilder(course_id, course_title, course_detail)
    course_builder.build()
    # course_builder.export_to_txt()

    print(Fore.MAGENTA +
        "Building schedule...")
    schedule_maker = ScheduleMaker.Schedule(course_builder)
    schedule_maker.get_user_input()
    schedule_maker.build()

    print(Fore.GREEN + "Done.")
    print(f"The schedule has been exported to a text file: {course_id}_schedule.txt")
