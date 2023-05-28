import os
import json
import webbrowser
import requests

def load_templates():
    templates = {}
    template_file = "templates.json"

    if os.path.exists(template_file):
        with open(template_file, "r") as file:
            templates = json.load(file)

    return templates

def create_file():
    print("Welcome to FileCreator!")
    print("-------------------------------")
    print("Create a new file with a custom name, extension, and location.")
    print()

    templates = load_templates()

    print("Select your option:")
    print("1. Python (PY)")
    print("2. JavaScript (JS)")

    option = input("Enter your option: ")

    if option == "1":
        file_extension = "PY"
    elif option == "2":
        file_extension = "JS"
    else:
        print("Invalid option!")
        return

    template = templates.get(file_extension)

    if not template:
        print(f"No template found for file extension '{file_extension}'")
        return

    file_content = template["content"]

    file_name = input("Enter the file name: ")  # Get the desired file name from the user

    use_bot_token = input("Do you want to provide a Discord bot token? (Y/N): ")
    if use_bot_token.upper() == "Y":
        bot_token = input("Enter your Discord bot token: ")
        file_content = file_content.replace("{BOT_TOKEN}", bot_token)
    else:
        file_content = file_content.replace("'{BOT_TOKEN}'", "None")

    current_directory = os.getcwd()
    created_files_folder = os.path.join(current_directory, "Created Files", file_extension)

    if not os.path.exists(created_files_folder):
        os.makedirs(created_files_folder)
        print(f"Created Files folder created at: {created_files_folder}")

    full_file_path = os.path.join(created_files_folder, f"{file_name}.{file_extension.lower()}")

    try:
        with open(full_file_path, "w") as file:
            file.write(file_content)  # Write the content to the file

        print(f"File '{full_file_path}' created successfully!")

        file_folder_path = os.path.dirname(os.path.abspath(full_file_path))
        file_folder_url = "file://" + file_folder_path.replace("\\", "/")
        webbrowser.open(file_folder_url)
    except Exception as e:
        print(f"Error occurred while creating the file: {str(e)}")


def check_latest_version():
    latest_release_url = "https://api.github.com/repos/your_username/your_repository/releases/latest"

    try:
        response = requests.get(latest_release_url)
        if response.status_code == 200:
            release_info = json.loads(response.text)
            latest_version = release_info["tag_name"]

            return latest_version
        else:
            print("Failed to retrieve latest version information.")
    except requests.exceptions.RequestException:
        print("Error occurred while checking the latest version.")

    return None

def compare_versions(current_version, latest_version):
    if current_version != latest_version:
        print("A new version is available!")
        print(f"Current version: {current_version}")
        print(f"Latest version: {latest_version}")
        print("Please update your code.")
    else:
        print("You are using the latest version.")

def main():
    current_version = "1.0"  # Your current version number
    latest_version = check_latest_version()

    if latest_version:
        compare_versions(current_version, latest_version)

    # Rest of your code

# Call the main function
main()

# Call the create_file function to create a file
create_file()






