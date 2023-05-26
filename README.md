# Canvas Pilot

![PyPI](https://img.shields.io/pypi/v/canvas_pilot?color=df)&nbsp;
![GitHub](https://img.shields.io/github/license/realzza/canvas-pilot?color=%23FFB6C1)&nbsp;
![GitHub last commit](https://img.shields.io/github/last-commit/realzza/canvas-pilot?color=orange)&nbsp;
[![CodeFactor](https://www.codefactor.io/repository/github/realzza/canvas-pilot/badge)](https://www.codefactor.io/repository/github/realzza/canvas-pilot)&nbsp;
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/canvas-pilot)

A command-line tool for managing your Canvas courses, fetching assignments, and grades.

## Installation

To install the Canvas CLI, run the following command:

```bash
pip install canvas-pilot
```

## Configuration

Before using the Canvas CLI, you'll need to configure it with your Canvas API key and domain.

### Retrieving your Canvas API Key

To retrieve your Canvas API key, follow these steps:

1. Log in to your Canvas account.
2. Click on "Account" in the left-hand side menu.
3. Click on "Settings" from the dropdown.
4. Scroll down to the "Approved Integrations" section and click on "+ New Access Token".
5. In the pop-up window, optionally enter a purpose for the token and set its expiry date.
6. Click on "Generate Token".
7. Copy the token displayed in the "Token" field. This is your Canvas API key.

**Important:** Keep your API key safe and secure, like you would with a password. Don't share it with anyone.

### Getting your Canvas Domain

Your Canvas domain is the URL you use to access Canvas. For example, if you access Canvas by navigating to `https://canvas.<yourinstitution>.com`, then your Canvas domain is `canvas.<yourinstitution>.com`.

Once you have your API key and domain, run the following command and follow the prompts to configure the Canvas CLI:

```bash
canvas configure
```

You can reconfigure the Canvas API key and domain at any time by running `canvas configure` again. You will be prompted to update your keys.

## Usage

### Fetch Courses

To fetch the list of your Canvas courses, run:

```bash
canvas fetch courses
```

### Fetch Assignments

To fetch assignments for all your Canvas courses, run:

```bash
canvas fetch assignments
```

To fetch assignments for a specific course, provide the course ID:

```bash
canvas fetch assignments <course_id>
```

To export the assignments/exams deadlines to an `.ics` file, add the `-e` or `--export` flag:

```bash
canvas fetch assignments --export
```

### Fetch Grades

To fetch grades for all your Canvas courses, run:

```bash
canvas fetch grades
```

To fetch grades for a specific course, provide the course ID:

```bash
canvas fetch grades <course_id>
```

To export the grades to a `.csv` file, add the `-e` or `--export` flag:

```bash
canvas fetch grades --export
```

### Help

To display help information for the command-line interface and its subcommands, run:

```bash
canvas --help
```

## Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the Canvas CLI, please open an issue or submit a pull request.

## License

This project is licensed under the GPLv3+ License. See the [LICENSE](LICENSE) file for details.
