import json
import os
from datetime import datetime

import click
import requests
from icalendar import Calendar, Event

CONFIG_FILE = "canvas_config.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        if not config["domain"].startswith("https://"):
            config["domain"] = "https://" + config["domain"]
        return config
    except FileNotFoundError:
        click.echo("Configuration file not found. Please run 'canvas configure' first.")
        exit(1)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def fetch_all_pages(url, headers, params=None):
    all_results = []
    page = 1
    per_page = 50

    while True:
        if params is None:
            params = {}
        params.update({"page": page, "per_page": per_page})
        response = requests.get(url, headers=headers, params=params)
        results = response.json()

        if not results:
            break

        all_results.extend(results)
        page += 1

    return all_results


@click.group()
def main():
    pass


@main.command("configure")
@click.option("--api_key", prompt="Canvas API key")
@click.option(
    "--domain", prompt="Canvas domain (e.g., yourinstitution.instructure.com)"
)
def configure(api_key, domain):
    config = {"api_key": api_key, "domain": domain}
    save_config(config)
    click.echo("Configuration saved.")


@main.command("reconfigure")
def reconfigure():
    configure()


@main.group("fetch")
def fetch():
    pass


@fetch.command("assignments")
@click.argument("course_id", nargs=-1, type=str)
@click.option("-e", "--export", is_flag=True, help="Export assignments to an .ics file")
def fetch_assignments(course_id, export):
    config = load_config()

    headers = {"Authorization": f"Bearer {config['api_key']}"}

    url_courses = f"{config['domain']}/api/v1/courses"
    response_courses = requests.get(url_courses, headers=headers)
    courses = response_courses.json()

    if export:
        cal = Calendar()

    for course in courses:
        if "name" not in course:
            continue

        current_course_id = course["id"]
        course_name = course["name"]

        if not course_id or str(current_course_id) in ",".join(course_id).split(","):
            url_assignments = (
                f"{config['domain']}/api/v1/courses/{current_course_id}/assignments"
            )
            course_assignments = fetch_all_pages(url_assignments, headers)

            click.echo(f"\n{course_name}:")

            for assignment in course_assignments:
                click.echo(f"{assignment['name']} - Due: {assignment['due_at']}")

                if export:
                    event = Event()
                    event.add("summary", f"{course_name}: {assignment['name']}")
                    if assignment["due_at"] is not None:
                        due_at = datetime.fromisoformat(
                            assignment["due_at"].rstrip("Z")
                        )
                    else:
                        # You can either skip the assignment or set a default value
                        continue  # This skips the current assignment

                    event.add("dtstart", due_at)
                    cal.add_component(event)

    if export:
        with open("canvas_assignments.ics", "wb") as f:
            f.write(cal.to_ical())
        click.echo("Assignments exported to canvas_assignments.ics")


@fetch.command("grades")
@click.argument("course_id", nargs=-1, type=str)
@click.option("-e", "--export", is_flag=True, help="Export grades to a .csv file")
def fetch_grades(course_id, export):
    config = load_config()
    headers = {"Authorization": f"Bearer {config['api_key']}"}

    url_courses = f"{config['domain']}/api/v1/courses"
    response_courses = requests.get(url_courses, headers=headers)
    courses = response_courses.json()

    grades = []

    for course in courses:
        current_course_id = course["id"]
        if not course_id or str(current_course_id) in ",".join(course_id).split(","):
            course_name = course.get("name", "No name")
            url_assignments = (
                f"{config['domain']}/api/v1/courses/{current_course_id}/assignments"
            )
            course_assignments = fetch_all_pages(url_assignments, headers)

            click.echo(f"\n{course_name}:")

            for assignment in course_assignments:
                url_submission = f"{config['domain']}/api/v1/courses/{current_course_id}/assignments/{assignment['id']}/submissions/self"
                response_submission = requests.get(url_submission, headers=headers)
                submission = response_submission.json()
                score = submission.get("score", "Not graded yet")
                total_score = assignment.get("points_possible", "N/A")
                click.echo(f"{assignment['name']} - Score: {score} / {total_score}")

                if export:
                    grades.append(
                        {
                            "course_id": course_id,
                            "course_name": course_name,
                            "assignment_id": assignment["id"],
                            "assignment_name": assignment["name"],
                            "score": f"{score} / {total_score}",
                        }
                    )

    if export:
        import csv

        with open("canvas_grades.csv", "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "course_id",
                "course_name",
                "assignment_id",
                "assignment_name",
                "score",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(grades)
        click.echo("Grades exported to canvas_grades.csv")


if __name__ == "__main__":
    main()
