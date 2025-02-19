import sys
import requests

# Force UTF-8 encoding (Windows fix)
sys.stdout.reconfigure(encoding='utf-8')

# API Endpoint
API_URL = "http://127.0.0.1:8000/ratings/students/"

def fetch_students(output_format="json"):
    headers = {"Accept": "application/json"} if output_format == "json" else {"Accept": "text/html"}

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()

        if output_format == "json":
            students = response.json()
            print("\n📢 Student List (JSON Response):")
            for student in students:
                print(f" - ID: {student['id']}, Username: {student['username']}, Email: {student['email']}")

        elif output_format == "html":
            with open("students.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            print("\n✅ HTML saved as 'students.html'. Open it in your browser.")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching students: {e}")

if __name__ == "__main__":
    print("\n🔹 Student API Command Line Tool 🔹")
    print("1. Fetch as JSON (default)")
    print("2. Fetch as HTML (save to file)")

    # Debug input handling
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        print(f"\n[DEBUG] You entered: {choice} (Type: {type(choice)})")  # Debugging line

        if choice == "2":
            fetch_students(output_format="html")
        elif choice == "1":
            fetch_students(output_format="json")
        else:
            print("\n❌ Invalid choice. Please enter '1' or '2'.")
    except EOFError:
        print("\n❌ Input error: EOF detected.")
    except KeyboardInterrupt:
        print("\n❌ Input error: Script interrupted.")
