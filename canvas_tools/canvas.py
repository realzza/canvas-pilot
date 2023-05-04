import os
import json
from canvasapi import Canvas
from icalendar import Calendar, Event
import click

CONFIG_FILE = "canvas_config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    if not config["domain"].startswith("https://"):
        config["domain"] = "https://" + config["domain"]
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

@click.group()
def main():
    pass

@main.command("configure")
@click.option("--api_key", prompt="Canvas API key")
@click.option("--domain", prompt="Canvas domain (e.g., yourinstitution.instructure.com)")
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
@click.argument("course_id", nargs=-1, type=int)
@click.option("-e", "--export", is_flag=True, help="Export assignments to an .ics file")
def fetch_assignments(course_id, export):
    config = load_config()
    canvas = Canvas(config["domain"], config["api_key"])
    courses = canvas.get_courses(enrollment_term_id="current")
    
    if export:
        cal = Calendar()
    
    for course in courses:
        if not course_id or course.id in course_id:
            assignments = course.get_assignments()
            click.echo(f"\n{course.attributes['name']}:")

            for assignment in assignments:
                click.echo(f"{assignment.name} - Due: {assignment.due_at}")

                if export:
                    event = Event()
                    event.add("summary", f"{course.attributes['name']}: {assignment.name}")
                    event.add("dtstart", assignment.due_at)
                    cal.add_component(event)
    
    if export:
        with open("canvas_assignments.ics", "wb") as f:
            f.write(cal.to_ical())
        click.echo("Assignments exported to canvas_assignments.ics")

@fetch.command("grades")
@click.argument("course_id", nargs=-1, type=int)
@click.option("-e", "--export", is_flag=True, help="Export grades to a .csv file")
def fetch_grades(course_id, export):
    config = load_config()
    canvas = Canvas(config["domain"], config["api_key"])
    courses = canvas.get_courses(enrollment_term_id="current")
    grades = []

    for course in courses:
        if not course_id or course.id in course_id:
            assignments = course.get_assignments()
            click.echo(f"\n{course.attributes['name']}:")

            for assignment in assignments:
                submission = assignment.get_submission(canvas.get_user("self"))
                score = submission.get("score", "Not graded yet")
                click.echo(f"{assignment.name} - Score: {score}")

                if export:
                    grades.append({
                        "course_id": course.id,
                        "course_name": course.attributes['name'],
                        "assignment_id": assignment.id,
                        "assignment_name": assignment.name,
                        "score": score
                    })

    if export:
        import csv
        with open("canvas_grades.csv", "w", newline='', encoding='utf-8') as f:
            fieldnames = ["course_id", "course_name", "assignment_id", "assignment_name", "score"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(grades)
        click.echo("Grades exported to canvas_grades.csv")

if __name__ == "__main__":
    main()

