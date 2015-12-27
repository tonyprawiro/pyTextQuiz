# pyTextQuiz
A very simple text-based quiz engine

Usage: `$ python quiz-engine.py QUIZNAME`

E.g: `$ python quiz-engine.py MATHGRADE6`

This is a very simple quiz engine that is supposed to be run from terminal.

Works with multiple choice questions (single or multiple correct answers), fill-in-the-blank, or simple question-answer types of quiz.

Before starting a session, you have to choose how many questions you would like to add in the session, and what is your targeted timing (default 2 minutes or 120 seconds per question).

You also need to prepare two text files, questions and keys files.

The questions file is the pool of the quiz questions. The quiz engine will show the questions in random sequence on every session. This is an example:

```
QUESTION 1

What is the name of Mickey Mouse's dog pet ?

A. Goofie
B. Pluto
C. Whiskey
D. Spot

---
QUESTION 2

Donald Duck is a _____. No wonder he swims well.

---
```

The keys file is the answers. All questions must be answered for, otherwise the session won't start.

```
1:B
2:duck
```

Both of these files need to follow a certain format which is very simple. In this repository I have included a sample question-key sets which is `MATHGRADE6`.

For the evaluation, the engine does only stripping and uppercasing. So, make sure that the answers are short and concise. Multiple choice or keyword-based answers work best. Long sentences and essays definitely are not ideal for this quiz engine.

At the end of a quiz session, a very simple assessment is shown which tells you how many correct and incorrect questions were there, and write them to a text file. The correct answer for those that you answered incorrectly isn't shown. This is done on purpose, because by not showing the correct answer, you are forced to go back to your reference material and find the correct answer. This way, you will cover more ground and will be better prepared for the real quiz.