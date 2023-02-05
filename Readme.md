![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows Terminal](https://img.shields.io/badge/Windows%20Terminal-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

![GitHub repo size](https://img.shields.io/github/repo-size/Lonely-Dark/Phoenix-Project?style=flat-square)


# Phoenix Project

This is the official repository for the Phoenix Project, a solution that allows users to delete all videos from a user's page on the social network VKontakte. 

## Getting Started

The project is written in the Python programming language. Before you start, you need to download all dependencies from the requirements.txt file and create a virtual environment. 

You also need to create a .env file in the directory, where you will store the user's token (example: `token=1234`) and the user's ID (example: `target_id=842334`). 

To get started, follow these steps:

1. Clone the repository:

`$ git clone https://github.com/Lonely-Dark/Phoenix-Project.git`

2. Navigate to the project directory:

`$ cd Phoenix-Project`

3. Create a virtual environment:

`$ python3 -m venv env`

4. Activate the virtual environment:

`$ source env/bin/activate`

5. Install dependencies:

`$ pip install -r requirements.txt`

6. Create a .env file:

`$ touch .env`

7. Open the .env file and store your token and user_id:

`$ nano .env`

Example .env:

```
token=tgerkgjkkslfkmkvm

target_id=12345
```

8. Run the project:

`$ python3 main.py`

## Contributing

Contributions are welcome! If you have any suggestions or bug reports, please create an issue in the repository.


