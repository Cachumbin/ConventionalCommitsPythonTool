# Conventional Commits Python Tool

## Introduction

The Conventional Commits Python Tool provides a graphical interface using tkinter for generating Git commit messages following the Conventional Commits specification. It allows users to select commit type, scope, message, body, and breaking change footer, and then generates the formatted commit message for copying to the clipboard.

## Requirements

To run the `app.pyw` file, ensure the following:

- Python 3.x installed on your system.
- Dependencies: `tkinter`, `json`. (Included with Python)

## Usage

1. **Launching the Application**:

   - Run `app.pyw` to launch the application.

2. **Commit Message Generation**:

   - **Type**: Select the type of commit (e.g., `feat`, `fix`, `docs`).
   - **Scope**: Optional scope. It specifies where the changes have been made.
   - **Breaking Change**: Check if the commit includes a breaking change.
   - **Message**: Enter a concise commit message.
   - **Body**: Optional. Enter additional details about the commit.
   - **Breaking Change Footer**: Optional. Enter details about breaking changes.
   - Click on "Generate Commit Message" to create the formatted commit message.

3. **Project Templates Management**:

   - Switch to the "Projects" tab to manage project templates:
     - Create new project templates.
     - Add scopes to existing project templates.
     - Delete scopes from existing project templates.

4. **Copying Commit Message**:
   - The generated commit message will be displayed and copied to the clipboard automatically to paste on git.
   - Example of the message:
   ```bash
   git commit -m "feat(Header): Automatic scrolling when clicking a button" -m "Added the function that scrolls to the section of each button"
   ```

## Conventional Commits

The full documentation of Conventional Commits where are specified all the caracteristics of the commit is in their oficcial [website](https://www.conventionalcommits.org/en/v1.0.0/).
