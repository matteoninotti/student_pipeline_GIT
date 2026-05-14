# Copilot Instructions: Student Pipeline

## Running the Project

### Main Commands
The pipeline is executed via CLI commands from `main.py`:

```bash
python main.py generate    # Generate random student data (creates CSV)
python main.py validate    # Validate data and generate JSON of valid records
python main.py report      # Calculate and display course statistics
python main.py all         # Run full pipeline (not yet implemented)
```

### Project Initialization
- All commands automatically create necessary working directories: `data/{input,output,backup}` and `report/`
- The project path is defined in `state.py` (currently hardcoded, not using environment variables)

## Architecture

### Data Pipeline Flow
1. **Generate Phase** (`gen_students.py`)
   - `Corso` class loads configuration from `config.json` (student count, grade range, subjects)
   - `Studente` class represents individual students
   - Random data generated via Faker library (Italian locale)
   - Intentionally creates invalid records (e.g., impossible grades) for validation testing

2. **ETL Phase** (`ETL.py`)
   - Reformats student objects to flatten nested subject grades
   - Writes CSV with one column per subject
   - Validates records (currently checking grade ranges and email format)
   - Separates valid from invalid records
   - Outputs valid records as JSON for analysis

3. **Statistics Phase** (`calc_stats.py`)
   - `Stats_calculator` processes validated JSON
   - Calculates course-wide statistics (mean, median, std dev, min/max per subject)
   - Calculates per-student statistics (individual averages)
   - Top 5 students calculation (currently incomplete)

### Key Classes
- **`Corso`** - Manages course configuration (subjects, grade bounds, student count)
- **`Studente`** - Represents a single student with conversion to/from dict
- **`ETL`** - Handles data transformation, validation, and CSV/JSON I/O
- **`Stats_calculator`** - Computes all statistical measures
- **`CLI`** - Command orchestration (generates → validates → reports)

### Module Dependencies
```
main.py
├── logic/gen_students.py (Corso, Studente)
├── logic/ETL.py
├── logic/calc_stats.py
└── state.py (paths)
```

## Key Conventions

### Language & Naming
- Code comments and variable names use Italian (e.g., `materie` for subjects, `voti` for grades)
- Internal variables often abbreviated: `subj` (subject), `stdev` (standard deviation)

### Data Management
- CSV fieldnames generated dynamically from subject list: `["id", "nome", "cognome", "data_nascita", "email", *subjects]`
- JSON output follows same flattened structure (grades unpacked from nested `voti` dict)
- All subject grades are parsed as strings from CSV, must be cast to int for calculations

### Path Handling
- Filenames include timestamps: `studenti_{YYYYMMDD_HHMMSS}.csv`
- Output paths hardcoded via `PROJECT_PATH` variable (set in `state.py`)
- Current setup has path inconsistency: `state.py` references both `student_pipeline/` and `student_pipeline_GIT/`

### Validation
- Invalid records mixed into generation intentionally (for testing)
- Validation checks: grade range (voto_min to voto_max per config), email format
- Valid/invalid records split during ETL phase
- Scartati (discarded) records cleaned up separately

## Configuration

The `config.json` file controls:
- `numero_studenti` - Total students to generate
- `voto_min` / `voto_max` - Valid grade bounds
- `materie` - List of subject names
- `classe` - Class identifier string

Example:
```json
{
  "numero_studenti": 27,
  "voto_min": 15,
  "voto_max": 30,
  "materie": ["Fondamenti DB", "Fondamenti coding", "Linux server", "JAVAAAA"],
  "classe": "ITS ACA 25-27"
}
```

## Known Issues & TODOs

- `requirements.txt` is empty (dependencies not listed: faker, likely others)
- `main.py` CLI class has global state management that could be refactored
- `all()` command not yet implemented
- `delete()` command not yet implemented
- Top 5 students calculation in `calc_stats.py` is incomplete
- `state.py` has path inconsistency (DATA_PATH points to wrong location)
- No test framework set up (intentional invalid records suggest unit tests were planned)
- CLI initialization uses global `curso` variable (not ideal)

## Development Setup

### VS Code Configuration
- Debugger configured in `.vscode/launch.json` for both `main.py` and current file
- Set `PYTHONPATH` to workspace for imports

### Virtual Environment
- Standard Python venv pattern (see `.gitignore`)
- No `poetry.lock` or `uv.lock` (simple pip setup expected)

### Ignored Paths
- Output data: `data/{backup,output,input/*.csv}`
- Reports: `report/` directory
- `__pycache__/` and `.pyc` files
- `.DS_Store` (macOS)
