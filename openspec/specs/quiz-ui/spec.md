## ADDED Requirements

### Requirement: Exam selection screen
The webapp SHALL display a landing page listing all available exams, one per professor.

#### Scenario: Landing page shows all exams
- **WHEN** a student opens the webapp
- **THEN** the landing page displays a card or button for each available exam (one per JSON file in `data/`)

#### Scenario: Exam names are human-readable
- **WHEN** exam options are displayed
- **THEN** each exam shows the professor name in a readable format (e.g., "Malusà" not "malusa")

### Requirement: Configurable quiz length
The webapp SHALL allow the student to choose how many questions to include in a quiz session before starting.

#### Scenario: Student selects number of questions
- **WHEN** a student selects an exam
- **THEN** the app presents an option to choose the number of questions (e.g., 10, 20, 30, or all)

#### Scenario: Requested number exceeds available questions
- **WHEN** the student selects a number greater than the total available questions for that exam
- **THEN** the quiz includes all available questions

### Requirement: Randomized question order
The webapp SHALL present questions in a different random order for each quiz session.

#### Scenario: Questions are shuffled each session
- **WHEN** a quiz session starts
- **THEN** the selected questions are presented in a random order (Fisher-Yates shuffle), different from the canonical JSON order

### Requirement: Randomized alternative order
The webapp SHALL shuffle the order of alternatives within each question for each session.

#### Scenario: Alternatives are shuffled per question
- **WHEN** a question is displayed to the student
- **THEN** the 4 alternatives are shown in a random order, and the correct answer index is remapped accordingly

### Requirement: Per-question immediate feedback
The webapp SHALL show whether the selected answer is correct or wrong immediately after the student answers.

#### Scenario: Student selects the correct answer
- **WHEN** the student selects the correct alternative
- **THEN** the app immediately shows a "correct" visual indicator (e.g., green highlight)

#### Scenario: Student selects a wrong answer
- **WHEN** the student selects an incorrect alternative
- **THEN** the app immediately shows which answer was wrong (e.g., red highlight) and highlights the correct answer (e.g., green highlight)

### Requirement: Final score display
The webapp SHALL show a summary score at the end of a quiz session.

#### Scenario: Quiz completed
- **WHEN** the student answers the last question
- **THEN** the app displays the total score (e.g., "18/20 correct") and offers options to retry the same exam or go back to exam selection

### Requirement: Mobile-friendly layout
The webapp SHALL be responsive and usable on mobile devices.

#### Scenario: Quiz on a mobile screen
- **WHEN** a student opens the webapp on a phone (viewport width < 768px)
- **THEN** all UI elements (exam cards, questions, alternatives, score) are readable and tappable without horizontal scrolling

### Requirement: Exams are strictly separated
The webapp SHALL NOT mix questions from different exams/professors in a single quiz session.

#### Scenario: Quiz contains only questions from selected exam
- **WHEN** a student starts a quiz for a specific exam
- **THEN** all questions in that session come exclusively from that exam's JSON file
