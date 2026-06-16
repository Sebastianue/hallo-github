# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## Project overview

`hallo-github` is a personal starter project ("Mein erstes Projekt auf GitHub" —
*My first project on GitHub*). As of this writing it is essentially a blank
slate: there is no application code, build tooling, or test suite yet.

Current contents:

- `README.md` — one-line project description (in German).
- `LICENSE` — GNU General Public License v3.0 (GPLv3).
- `CLAUDE.md` — this file.

## Repository state

This is an early-stage repository with a single commit. Because there is no
source code yet, **do not invent or assume** a build system, framework, package
manager, or directory layout. There are currently no commands to build, run,
lint, or test.

When code is introduced, update this file to document:

- The language(s) and runtime(s) chosen.
- How to install dependencies, build, run, and test.
- The directory structure and where key modules live.
- Any project-specific conventions (formatting, naming, commit style).

## Licensing

The project is licensed under **GPLv3**. Keep this in mind when adding code:

- New source files should be compatible with GPLv3.
- Be cautious about pulling in dependencies under incompatible licenses.
- Preserve the existing `LICENSE` file.

## Conventions

- The README is written in German; match the existing language when editing
  user-facing docs unless asked otherwise.
- Keep changes small and focused, with clear, descriptive commit messages.

## Git workflow

- Default branch: `master`.
- Develop on a feature branch, commit with descriptive messages, and push with
  `git push -u origin <branch-name>`.
- Do not create pull requests unless explicitly requested.
