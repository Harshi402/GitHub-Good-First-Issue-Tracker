# GitHub-Good-First-Issue-Tracker
# Technologies Used: Python, API Integration, Version Control: Git, Web Framework: Streamlit, Database: MongoDB.

https://github.com/user-attachments/assets/f0694546-1db3-4647-901b-fee75f3119e7

# How to view the website:
1. Clone the repository
2. Open it in preferably replit and then in the shell run command "streamlit run streamlit_app.py"
3. You don't need to keep delete database file.

Intention to create: Facilitate beginner-friendly open-source contributions through a streamlined Streamlit web application providing easy navigation and visualization, promoting community engagement and skill development in software development.
Utilized the GitHubAPI to fetch issues labeled as ”good-first-issue” with Python requests. Stored the processed data in MongoDB for efficient querying and retrieval.

I have created this project in replit as it provides easy connection to libraries of python. It has two major processes
Data Retrieval and Processing: This part fetches GitHub issues labeled as "good-first-issue", stores them in MongoDB, and provides functionality to retrieve and process this data.
Streamlit Application: This part creates a Streamlit web application to display the fetched data with pagination support.
My Streamlit application connects to MongoDB to retrieve the data and then displays it in a paginated manner. The application allows users to navigate through different pages of issues and provides basic information about each issue, including the repository name, the commit name, current status. Its a completely clickable webpage. 
