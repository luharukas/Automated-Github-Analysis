import requests
import time
import yaml
import os


header={"Authorization":"Bearer"+os.environ.get('GITHUB_TOKEN')}

language_mapper={
     'cpp':'c++',
     'c':'c',
     'cs': 'C#',
     'go':'go',
     'java':'java',
     'js':'js',
     'php':'php',
     'py':'python',
     'ipynb':'python',
     'rb':'ruby',
     'rs':'rust',
     'swift':'swift',
     'md':'markdown',
     'tet':'latex',
     'sol':'sol',
     'kts':'kotlin',
}

class userInfo:
    def __init__(self,url) -> None:
        self.url=url
        self.username=url.split("/")[-1]
        self.repos=[]
        

    def repo_length(self):
        return len(self.repos)
    
    def repos(self):
        return self.repos
    
    def repo_name(self):
        return [repo["name"] for repo in self.repos]
    
    def get_user_repositories(self):
    # Extract username from the GitHub URL
    # API endpoint to retrieve user repositories
        api_url = f"https://api.github.com/users/{self.username}/repos"
        try:
            response = requests.get(api_url,headers=header)
            response.raise_for_status()  # Raise an exception if the request fails
            self.repos=response.json()
            return True
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False
        

    def get_repository_content(self,repository):
        # API endpoint to retrieve repository contents
        api_url = f"https://api.github.com/repos/{self.username}/{repository}/contents"

        overall_code=""

        try:
            response = requests.get(api_url,headers=header)
            response.raise_for_status()  # Raise an exception if the request fails
            files = response.json()

            for file in files:
                if file["type"] == "file":
                    extension=file['name'].split(".")[-1]
                    if extension in language_mapper.keys():
                            file_content = requests.get(file["download_url"]).text
                            if extension=="ipynb":
                                with open('temp/temp.ipynb','w') as fp:
                                    fp.write(file_content)
                                    fp.close()
                                from src.utils import convert_ipynb_to_py
                                convert_ipynb_to_py("temp/temp.ipynb","temp/temp.py")
                                with open('temp/temp.py') as fp:
                                    file_content=fp.read()

                            if file_content:
                                overall_code=overall_code+f"File: {file['name']} of programming language :{language_mapper[extension]}\n-------"
                                overall_code=overall_code+f"{file_content}"+"\n"
                                overall_code+="-----\n\n\n"
                            

                elif (file['type']=='dir') and (not file["name"].startswith(".")) and (self.is_valid_directory(file["name"])):
                        overall_code+=self.get_files_from_directory(file["name"], repository)

            return overall_code
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_files_from_directory(self,directory, repository):
        api_url = f"https://api.github.com/repos/{self.username}/{repository}/contents/{directory}"
        overall_code_dir=""
        try:
            response = requests.get(api_url,headers=header)
            response.raise_for_status()
            files = response.json()

            for file in files:
                if file["type"] == "file":
                    extension=file['name'].split(".")[-1]
                    if extension in language_mapper.keys():
                        file_content = requests.get(file["download_url"]).text
                        if extension=="ipynb":
                            with open('temp/temp.ipynb','w') as fp:
                                fp.write(file_content)
                                fp.close()
                            from src.utils import convert_ipynb_to_py
                            convert_ipynb_to_py("temp/temp.ipynb","temp/temp.py")
                            with open('temp/temp.py') as fp:
                                file_content=fp.read()
                        
                        if file_content:
                            overall_code_dir+=f"File: {file['name']} of programming language :{language_mapper[extension]}\n-------"
                            overall_code_dir+=f"{file_content}"+"\n"
                            overall_code_dir+="-----\n\n\n"

            return overall_code_dir
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def is_valid_file(filename):
        # Add conditions to skip certain files based on their filename or extension
        # For example, to skip binary files or intermediate/cache files
        invalid_extensions = ['exe', 'dll', 'bin',"cache","log","pyc",]
        if any(filename.lower().endswith(ext) for ext in invalid_extensions):
            return False
        return True

    @staticmethod
    def is_valid_directory(directory):
        # Add conditions to skip certain directories based on their name or path
        # For example, to skip hidden directories or virtual environment directories
        invalid_directories = ['.git', '.venv', '__pycache__','venv',".cache", ".git", ".vscode","virtualenv","env","log"]
        if any(dir_name.lower() == directory.lower() or directory.lower().startswith(dir_name.lower() + "/") for dir_name in invalid_directories):
            return False
        return True

            