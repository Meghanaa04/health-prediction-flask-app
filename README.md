# Health Prediction Application

## Overview
A Flask-based web application that manages patient records and predicts health risks based on medical parameters.

## Features
- Add Patient
- View Patients
- Edit Patient
- Delete Patient
- Reset Database
- Input Validation
- Health Risk Prediction

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- Bootstrap

## Prediction Logic
- Glucose > 140 → High Diabetes Risk
- Haemoglobin < 12 → Possible Anemia Risk
- Cholesterol > 240 → High Cholesterol Risk
- Otherwise → Healthy Range

## Validations
- Email Validation
- Future DOB Validation
- Negative Value Validation

## Run Project

```bash
pip install -r requirements.txt
python app.py
```
