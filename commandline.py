import requests
import getpass

# Global variable to track login status
access_token = None
refresh_token = None

def login_cli(api_url):
    global access_token, refresh_token
    username = input("Enter username: ")
    password = input("Enter password: ")  # Hides password input

    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]
            print(f"\n Login successful! Welcome, {data['username']}")
            return True
        else:
            print("\n Error:", data.get("error", "Unknown error"))
            return False
    except requests.exceptions.RequestException as e:
        print("\n Failed to connect to the server:", str(e))


def logout_cli():
    global access_token, refresh_token
    if access_token:
        access_token = None
        refresh_token = None
        print("\n Successfully logged out.")
    else:
        print("\n You are not logged in.")


def register_cli():
    api_url = "http://127.0.0.1:8000/register/"
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 201:
            print(f"\n Registration successful! Welcome, {username}")
            return True
        else:
            print("\n Error:", data.get("error", "Unknown error"))
            return False

    except requests.exceptions.RequestException as e:
        print("\n Failed to connect to the server:", str(e))


def view_cli():
    api_url = "http://127.0.0.1:8000/professors_ratings/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        ratings = response.json()

        # Iterate through each professor's rating
        for rating in ratings:
            professor_name = rating.get('professor_name', 'Unknown')
            professor_id = rating.get('professor_id', 'N/A')
            average_rating = rating.get('average_rating', '0')

            # Convert to float and generate stars
            try:
                stars = "*" * int(round(float(average_rating)))
            except (ValueError, TypeError):
                stars = "No rating yet"

            print(f"The rating of Professor {professor_name} ({professor_id}) is {stars or 'No rating yet'}")

    except requests.exceptions.RequestException as e:
        print("\n Failed to connect to the server:", str(e))
    except KeyError as e:
        print(f"\n Missing expected key: {e}")
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")


def modules_cli():
    api_url = "http://127.0.0.1:8000/modules/"
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        modules = response.json()

        # Print table header
        print("\n Module List:\n" + "="*60)
        print(f"{'Code':<6}{'Name':<30}{'Year':<6}{'Semester':<10}{'Taught by'}")
        print("-"*60)

        # Track the previous module code to know when to add dashed lines
        prev_code = None

        for module in modules:
            module_code = module.get('module_code', 'N/A')
            name = module.get('name', 'N/A')
            year = module.get('year', 'N/A')
            semester = module.get('semester', 'N/A')
            professors = module.get('professors', [])
            if prev_code and prev_code != module_code:
                print("-"*60)
            print(f"{module_code:<6}{name:<30}{year:<6}{semester:<10}{professors[0] if professors else 'No professors assigned'}")

            for prof in professors[1:]:
                print(f"{'':<6}{'':<30}{'':<6}{'':<10}{prof}")

            prev_code = module_code

        print("="*60)

    except requests.exceptions.RequestException as e:
        print("\n Failed to connect to the server:", str(e))
    except KeyError as e:
        print(f"\n Missing expected key: {e}")
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")


def professor_avg_cli(professor_id, module_code):
    api_url = f"http://127.0.0.1:8000/professor_avg/professor/{professor_id}/module/{module_code}/"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        avg_rating= response.json()

        professor_name = avg_rating.get('name')
        professor_id = avg_rating.get('professor_id')
        module_name = avg_rating.get('module_name')
        avg_rating = avg_rating.get('average_rating_stars')


        print(f"The rating of Professor {professor_name} ({professor_id}) in module{module_name} is {avg_rating or 'No rating yet'}")

    except requests.exceptions.RequestException as e:
        print("\n Failed to connect to the server:", str(e))




def rate_cli(professor_id, module_code, year, semester, rating):
    global access_token  

    if not access_token:
        print("\n Error: You must log in first.")
        return

    api_url = "http://127.0.0.1:8000/rating/"
    payload = {
        "professor_id": professor_id,
        "module_code": module_code,
        "year": year,
        "semester": semester,
        "rating": rating,
    }

    headers = {
        "Authorization": f"Bearer {access_token}", 
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("\n Rating Submitted Successfully!")
        print(f" Professor: {data.get('professor', 'N/A')}")
        print(f" Module: {data.get('module', 'N/A')}")
        print(f" Rating Given: {data.get('rating', 'N/A')}/5")

    except requests.exceptions.HTTPError as e:
        print(f"\n HTTP Error: {e}")
        print(f" Response Content: {response.text}")  
    except requests.exceptions.RequestException as e:
        print(f"\n Request Failed: {e}")

    

if __name__ == "__main__":
    print("\n Student API Command Line Tool")
    session_obj = requests.Session()
    logged_in = False
    while True:
        
        prompt = "(logged in) > " if logged_in else "> "  
        command = input(prompt).strip().split()

        if len(command) == 0:
            continue  # Ignore empty inputs

        if command[0] == "list":
            modules_cli()

        elif command[0] == "login" and len(command) == 2:
            if command[1] == "http://127.0.0.1:8000/login/":
                logged_in = login_cli(command[1])
                print()
        
        elif command[0] == "logout":
            logout_cli()
            logged_in = False
        
        elif command[0] =="register":
            register_cli()
        elif command[0] == "view":
            view_cli()
        elif command[0] == "average" and len(command) == 3:
            professor_avg_cli(command[1], command[2])
        elif command[0] == "rate" and len(command) == 6 :
            rate_cli(command[1], command[2], command[3], command[4], command[5])
        else:
            print("\n Invalid command. Available commands: 'list', 'login <url>', 'logout'")
