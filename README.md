# Canvas CLI

A command-line tool for managing your Canvas courses, fetching assignments, and grades.

## Installation

To install the Canvas CLI, run the following command:

```bash
pip install canvas-cli
```

## Configuration

Before using the Canvas CLI, you'll need to configure it with your Canvas API key and domain. To do this, run the following command and follow the prompts:

```bash
canvas configure
```

You can reconfigure the Canvas API key and domain at any time by running:

```bash
canvas reconfigure
```

## Usage

### Fetch Assignments

To fetch assignments for all your Canvas courses, run:

```bash
canvas fetch assignments
```

To fetch assignments for a specific course, provide the course ID:

```bash
canvas fetch assignments <course_id>
```

To export the assignments to an `.ics` file, add the `-e` or `--export` flag:

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

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

