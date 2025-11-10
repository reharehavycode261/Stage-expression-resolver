## Overview 🔮

The system recognizes handwritten equations or inequalities, parses them, and solves them using Reverse Polish Notation. It also generates steps for the resolution and graphical representations of the equations.

## How It Works 🧠

### 1. Image Processing & Character Segmentation
- The input image is processed to split individual characters using blank spaces or image contours.
<img width="100%" alt="Input" src="https://github.com/user-attachments/assets/c2d9b36c-e608-4925-96e0-fa9345e88397">

### 2. Text Recognition Using ML Model
- A **RandomForestClassifier** trained on the **MINST** dataset transcribes the segmented characters into text. Over time, the model can be improved by manually correcting outputs, allowing retraining with corrected data for better accuracy.

### 3. Equation Parsing
> Due to lack of dataset, I used `w` as the variable, `//` as `<`, and `///` as `>`
- The recognized text is parsed into an algebraic equation or inequality, such as `6w + 1 // 3` -> `6x + 1 < 3`.

### 4. Solving Using Reverse Polish Notation (RPN)
- The equation is solved using the **Reverse Polish Notation** (RPN) algorithm, which eliminates the need for parentheses and operator precedence.

### 5. Solution Output & Graphical Representation
- The solution is returned with steps, and if applicable, a graph of the equation is generated to visually represent the solution.
<img width="100%" alt="Steps" src="https://github.com/user-attachments/assets/484784b6-10c5-4a01-8934-eff50d11a004">
<img width="100%" alt="Graph" src="https://github.com/user-attachments/assets/c9b4f11d-2547-4836-9493-49b30fab34f1">


---

## How to get started ℹ️
- Create a virtual environment
```bash
python3 -m venv venv
```
- Activate the virtual environment
```bash
source venv/bin/activate
```
- Install the requirements
```bash
pip install -r requirements.txt
```
- Run the program
```bash
python3 manage.py runserver
```
