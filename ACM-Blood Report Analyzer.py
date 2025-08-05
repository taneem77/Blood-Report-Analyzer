import csv
import os

CSV_FILE = "Blood Report Details(CSV).csv"
MAX_FILE_SIZE = 5 * 1024 * 1024

reference_ranges = {
    "Hemoglobin": (12, 16),
    "HDL Cholesterol": (40, 60),
    "Total Protein": (6.0, 8.3),
    "Albumin": (3.5, 5.0),
    "Globulin": (2.0, 3.5),
    "C-Reactive Protein": (0, 3),
    "Urea": (10, 40),
    "Creatinine": (0.6, 1.2),
    "Uric Acid": (3.5, 7.2),
    "Blood Glucose Level": (70, 99),
}

health_advice = {
    "Hemoglobin": {
        "low": ("May cause fatigue or weakness.", "Eat iron-rich foods like spinach, lentils, and red meat."),
        "high": ("Could indicate dehydration or a blood disorder.", "Drink enough water and avoid smoking."),
    },
    "HDL Cholesterol": {
        "low": ("Increases risk of heart disease.", "Exercise regularly and consume healthy fats like olive oil, nuts."),
        "high": ("Generally good but very high levels may rarely cause inflammation.", "Maintain a balanced diet."),
    },
    "Total Protein": {
        "low": ("May suggest liver or kidney issues.", "Eat dairy, lean meats, and legumes."),
        "high": ("Could mean chronic inflammation or infections.", "Avoid high-protein supplements if unnecessary."),
    },
    "Albumin": {
        "low": ("May be a sign of liver or kidney disease.", "Increase protein intake through eggs, fish."),
        "high": ("Rare; may indicate dehydration.", "Stay well-hydrated."),
    },
    "Globulin": {
        "low": ("Could mean immune deficiency.", "Eat whole grains and fresh fruits."),
        "high": ("Could suggest chronic infections.", "Get regular health checkups."),
    },
    "C-Reactive Protein": {
        "high": ("Indicates inflammation or infection.", "Include anti-inflammatory foods like turmeric and berries."),
        "low": ("Good; low inflammation.", "Maintain a healthy lifestyle."),
    },
    "Urea": {
        "low": ("May be due to liver problems.", "Include moderate protein in diet."),
        "high": ("Could indicate kidney issues.", "Stay hydrated and reduce protein overload."),
    },
    "Creatinine": {
        "low": ("Possible liver/muscle issues.", "Exercise and protein balance can help."),
        "high": ("May mean kidney dysfunction.", "Drink water and avoid creatine supplements."),
    },
    "Uric Acid": {
        "low": ("Uncommon, but could indicate liver/kidney issues.", "Eat a well-rounded diet."),
        "high": ("Can cause gout or joint pain.", "Avoid red meat, sugary drinks."),
    },
    "Blood Glucose Level": {
        "low": ("Leads to hypoglycemia — dizziness, sweating.", "Eat small frequent meals, include fruits."),
        "high": ("Risk of diabetes.", "Limit sugar intake, increase fiber and walk daily."),
    }
}

sample_data = [
    {"Test Name": "Hemoglobin", "Value": "13.5"},
    {"Test Name": "HDL Cholesterol", "Value": "45"},
    {"Test Name": "Total Protein", "Value": "7.5"},
    {"Test Name": "Albumin", "Value": "4.2"},
    {"Test Name": "Globulin", "Value": "3.0"},
    {"Test Name": "C-Reactive Protein", "Value": "1.5"},
    {"Test Name": "Urea", "Value": "35"},
    {"Test Name": "Creatinine", "Value": "1.0"},
    {"Test Name": "Uric Acid", "Value": "6.8"},
    {"Test Name": "Blood Glucose Level", "Value": "92"},
]

def create_sample_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Test Name", "Value"])
            writer.writeheader()
            writer.writerows(sample_data)
        print(f"Sample blood report CSV created: '{CSV_FILE}'.")

def analyze_blood_report(csv_path):
    result = "\n Blood Report Analysis:\n"
    if not os.path.exists(csv_path):
        print("Error: CSV file not found.")
        return
    if os.path.getsize(csv_path) > MAX_FILE_SIZE:
        print("Error: CSV file too large. Must be under 5MB.")
        return

    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                test = row['Test Name'].strip()
                try:
                    value = float(row['Value'])
                except ValueError:
                    result += f"{test}: ❌ Invalid value.\n"
                    continue

                if test in reference_ranges:
                    low, high = reference_ranges[test]
                    if value < low:
                        risk, tip = health_advice.get(test, {}).get("low", ("", ""))
                        result += f"{test}: 🔻 Low. {risk} Tip: {tip}\n"
                    elif value > high:
                        risk, tip = health_advice.get(test, {}).get("high", ("", ""))
                        result += f"{test}: 🔺 High. {risk} Tip: {tip}\n"
                    else:
                        result += f"{test}: ✅ Normal. Keep it up!\n"
                else:
                    result += f"{test}: ❓ Unknown test.\n"
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")

# Main Logic
create_sample_csv()


file_path = input("Upload your blood report (PDF or Word doc): ")
if not file_path.lower().endswith(('.pdf', '.doc', '.docx')):
    print(" Please upload a valid PDF or Word document.")
else:
    print(" File received. Analyzing data from internal CSV...")
    analyze_blood_report(CSV_FILE)
