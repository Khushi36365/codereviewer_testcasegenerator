from pathlib import Path
import json

from agents.analyzer import analyze_code
from agents.scenario_generator import generate_scenarios
from agents.test_generator import generate_tests

from utils.code_parser import extract_python_code
from utils.clean_text import clean_text


def process_file(
    code: str,
    project_name: str,
    output_dir: Path = None
):
    
    # ----------------------------
    # CREATE OUTPUT FOLDER
    # ----------------------------


    if output_dir is None:
        output_dir = (
            Path("output")
            / project_name
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------
    # STEP 1: ANALYSIS
    # ----------------------------

    analysis = analyze_code(code)

    with open(
        output_dir / "analysis.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(analysis, f, indent=4)

    print(f"{project_name}: Analysis saved.")

    # ----------------------------
    # STEP 2: SCENARIOS
    # ----------------------------

    scenarios = generate_scenarios(
        code=code,
        analysis=analysis
    )

    scenarios = clean_text(scenarios)

    with open(
        output_dir / "scenarios.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            scenarios,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"{project_name}: Scenarios saved.")

    # ----------------------------
    # STEP 3: TESTS
    # ----------------------------

    tests = generate_tests(
        code=code,
        scenarios=scenarios
    )

    tests = extract_python_code(tests)

    with open(
        output_dir / "generated_test.py",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(tests)

    print(f"{project_name}: Tests saved.")

    print(f"Output saved at: {output_dir}\n")


# ----------------------------
# INPUT METHOD
# ----------------------------

print("\nChoose input method:")
print("1. Paste code")
print("2. Read from file")
print("3. Read folder")

choice = input("\nEnter choice (1/2/3): ").strip()


# ----------------------------
# OPTION 1: PASTE CODE
# ----------------------------

if choice == "1":

    print("\nPaste your code below.")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    code = "\n".join(lines)

    project_name = input(
        "\nEnter project name: "
    ).strip()

    process_file(
        code=code,
        project_name=project_name
    )


# ----------------------------
# OPTION 2: SINGLE FILE
# ----------------------------
elif choice == "2":

    file_path = input(
        "\nEnter file path: "
    ).strip()

    file_path = Path(file_path)

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        code = f.read()

    process_file(
        code=code,
        project_name=file_path.stem
    )


# ----------------------------
# OPTION 3: FOLDER
# ----------------------------
elif choice == "3":

    folder_path = input(
        "\nEnter folder path: "
    ).strip()

    folder = Path(folder_path)

    extensions = [
        "*.py",
        "*.java",
        "*.js",
        "*.cpp",
        "*.sql"
    ]

    SKIP_DIRS = {
        ".venv",
        "venv",
        "__pycache__",
        ".git",
        "node_modules",
        "dist",
        "build",
        ".env",
        ".gitignore",
        "uv.lock",
        "pyproject.toml",
        "README.md",
        ".python-version",
        "__init__.py"
    }

    code_files = []

    for ext in extensions:

        for file_path in folder.rglob(ext):

            if any(
                part in SKIP_DIRS
                for part in file_path.parts
            ):
                continue

            code_files.append(file_path)

    print(
        f"\nFound {len(code_files)} code files.\n"
    )

    project_code = ""

    for file_path in code_files:

        print(
            f"Reading: {file_path.name}"
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            project_code += (
                f"\n\n# FILE: {file_path.name}\n"
            )

            project_code += f.read()

    project_output_dir = (
        Path("output")
        / folder.name
    )

    project_output_dir.mkdir(
        parents=True,
        exist_ok=True
)

    process_file(
        code=project_code,
        project_name=folder.name,
        output_dir=project_output_dir
    )

    print("\nFolder processing completed.")


# ----------------------------
# INVALID OPTION
# ----------------------------

else:

    print("Invalid choice.")