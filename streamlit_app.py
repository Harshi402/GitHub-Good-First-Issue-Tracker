import streamlit as st
from pymongo.mongo_client import MongoClient
import os
import time

st.set_page_config(
    page_title="GitHub Good-First-Issue Tracker",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'first_load' not in st.session_state:
    st.session_state.first_load = True

if st.session_state.first_load:
    st.session_state.first_load = False 
    
# load mongodb password from secrets
mongo_password = os.environ['MONGO_PASSWORD']

# MongoDB Configuration

mongo_uri = f"mongodb+srv://TrialH23:{mongo_password}@cluster0.a48kdir.mongodb.net/?retryWrites=true&w=majority"
database_name = "github_issues"
colllection_name = "issues"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[colllection_name]


# load the data from MongoDB
def load_data(page_size, page_number):
  #page size - 20
  skip_value = page_size * (page_number - 1)
  return list(collection.find().skip(skip_value).limit(page_size))


# "repo_name": "kelvins/algorithms-and-data-structures",
#     "issue_title": "Translate Python algorithms and comments to English. ",
#     "issue_url": "https://github.com/kelvins/algorithms-and-data-structures/issues/183",
#     "label_name": "good-first-issue",
#     "label_url": "https://github.com/kelvins/algorithms-and-data-structures/labels/good-first-issue",
#     "state": "open",
#     "locked": false


# Display data
def display_data(record):
  issue_title = record["issue_title"]
  repo_name = record["repo_name"]
  issue_url = record["issue_url"]
  label_name = record["label_name"]
  label_url = record["label_url"]

  st.markdown(f"##{issue_title}")
  st.link_button(repo_name, f"https://github.com/{repo_name}", type="primary")
  st.markdown(f"**Issue Url** : {issue_url}")

  st.link_button(label_name, label_url)

  state_indicator = "🟢" if record["state"] == "open" else "🔴"
  locked_indicator = "True" if record["locked"] else "False"

  st.write(f"**Status:** {state_indicator} | **Locked:** {locked_indicator}")

  st.markdown("---")


# Streamlit App
def main():
  total_records = collection.count_documents({})
  st.sidebar.title("Navigation")
  st.sidebar.radio("Go to", ["Issues", "Repos"])

  st.title("_GitHub_ :blue[_Good-First-Issues_]")
  #pagination settings
  page_size = 20
  mx = int(total_records/page_size)
  st.sidebar.title("Page Number")
  page_number = st.sidebar.number_input("Select Page", min_value=1,value=1,max_value=mx)
  #loader while fetching data
  
  st.sidebar.write(f"Total Records: {total_records}")

  with st.spinner("Loading..."):
    st.toast('Your request is processing!')
    time.sleep(5)

  #load data from MongoDB
  data = load_data(page_size, page_number)

  for record in data:
    display_data(record)


if __name__ == "__main__":
  main()
