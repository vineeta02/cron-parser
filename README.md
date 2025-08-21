# cron-parser

A Python utility to parse cron expressions and expand them into lists of possible values for each field.

---

## Features

- Supports `*`, ranges (e.g., `10-20`), steps (e.g., `*/15`, `1-10/2`), and comma-separated lists (e.g., `1,5,10`).
- Handles day-of-week (`0–7`) and month/day-of-month ranges.
- Returns empty lists for out-of-range values instead of raising errors.
- Includes unit tests using `pytest`.

---

## Installation

1. **Clone this repository:**

```bash
git clone https://github.com/vineeta02/cron-parser.git
cd CronParser
```
2. **Create a virtual environment:**

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
python3 -m pip install pytest
```

## Usage
## Run CronParser from the command line
`python3 CronParser.py "*/15 0 1,15 * 1-5 /usr/bin/find"`

This will print the expanded values for each cron field.

## Running Tests
Run unit tests using pytest:

```bash
pytest -v Test_CronParser.py
```

## Examples
Input argument - `*/15 0 1,15 * 1-5 /usr/bin/find`
| Expression     | Expanded Values           |
|----------------|----------------------------|
| minute         | 0 15 30 45                 |
| hour           | 0                          |
| day of month   | 1 15                       |
| month          | 1 2 3 4 5 6 7 8 9 10 11 12 |
| day of week    | 1 2 3 4 5                  |
| command        | /usr/bin/find              |
    
