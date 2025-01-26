# Contributing to eHealth System

Thank you for your interest in contributing to the eHealth System project! We welcome contributions from everyone. Follow these guidelines to help us maintain quality and consistency across the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Setup](#project-setup)
3. [Contributing Workflow](#contributing-workflow)
4. [Coding Guidelines](#coding-guidelines)
5. [Testing Your Changes](#testing-your-changes)
6. [Pull Request Guidelines](#pull-request-guidelines)
7. [Contact](#contact)

## Getting Started

1. Fork the repository from GitHub:
   ```bash
   git clone https://github.com/your-username/ehealth-system.git
   cd ehealth-system
   ```

2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Project Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations and start the server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. **Create a superuser to access the admin panel:**
   ```bash
   python manage.py createsuperuser
   ```

## Contributing Workflow

1. **Make changes locally:**
   - Implement new features or fix bugs.
   - Follow the coding guidelines.

2. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Added new feature description"
   ```

3. **Push changes to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a pull request (PR) to the `main` branch:**
   - Describe the changes you have made.
   - Link any relevant issues.
   - Request a review from the maintainers.

## Coding Guidelines

- Follow PEP 8 for Python code style.
- Use meaningful variable and function names.
- Keep your code modular and reusable.
- Ensure docstrings are added for functions and classes.
- Avoid committing large or unrelated changes in a single PR.

## Testing Your Changes

Before submitting your changes, run tests to ensure no functionality is broken:

```bash
python manage.py test
```

If adding new features, please include relevant tests.

## Pull Request Guidelines

- Provide a clear title and description.
- Reference related issues if applicable.
- Ensure your code passes all existing tests.
- Keep the pull request focused on one issue at a time.

## Contact

If you have any questions, feel free to reach out by opening an issue on GitHub or contacting the project maintainers.

Happy contributing!

