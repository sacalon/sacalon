# Contributing to Sacalon

Thank you for your interest in contributing to **Sacalon**! This project is an evolving programming language, and every contribution — from bug reports to new standard-library modules — helps shape its future.

---

## 🧭 Project Philosophy

Sacalon aims to be a general purpose and open source programming language designed to build optimal, maintainable, reliable, and efficient software. Please keep these principles in mind:

* Prioritize simplicity over unnecessary complexity
* Cross-platform compatibility is essential
* Code must be readable, testable, and well-documented

---

## 📝 How to Contribute

### 1. Fork and Clone

Begin by forking the repository and cloning your fork:

```bash
git clone https://github.com/sacalon/sacalon.git
```

### 2. Create a Feature Branch

For each new feature or bug fix, create a separate branch:

```bash
git checkout -b feature/my-feature
```

### 3. Coding Style

* All C++ code must target **C++17 or newer**.
* Use meaningful, consistent naming conventions.
* Document all functions, classes, and modules.

### 4. Tests
If you changes the core compiler(`src/core`) you should test your changes with codes in `tests` folder. First ensure you installed `pytest`, and run follwing command(s) in base folder of repository:
```
$ make clean # for windows: make clean-windows
$ make # this command rebuild sacalon compiler
# make tests
```
All tests should passed.
### 5. Commit Messages

Commit messages should be clear and descriptive:

```
fix: resolve memory leak in lexer
docs: update README for build system
```

### 6. Pull Requests

* Ensure that the project builds and tests successfully before submitting a PR.
* For major changes, discuss them in an Issue before implementing.
* PR descriptions should concisely explain the changes made.

---

## 🐛 Bug Reports

If you encounter a bug:

1. Open a **Bug Report** using the template in Issues.
2. Include your OS, compiler version, error output, and minimal reproducible example.

---

## 💡 Feature Proposals

For new features:

* Create an Issue before starting implementation.
* Include a brief discussion of the design, API, and how it interacts with the rest of the language.

---

## 🔌 Standard Library (salivan)

When contributing a new module (e.g., a web server):

* Its structure should follow existing `salivan` modules.
* External dependencies must be minimal.
* Behavior must be validated on Linux, Windows, and macOS.

---

## 🤝 Communication

For questions, architectural discussions, and coordination, use Issues or Discussions.
For large proposed features, open an Issue with the `enhancement` label.

---

## ❤️ Thank You

We greatly appreciate your interest in improving Sacalon. Every contribution — even a small one — matters.