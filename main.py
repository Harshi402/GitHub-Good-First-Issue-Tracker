import json
import logging
import os
import requests
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

gh_token = os.environ['GITHUB_TOKEN']
mongo_password = os.environ['MONGO_PASSWORD']


def time_track(start, name):
  #function for time tracking- for github client thing
  elapsed = time.time() - start  #current time - start time
  log.info(f"{name} took {elapsed}\n\n")


def get_github_client_headers(token):
  headers = {
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {token}",
      "X-GitHub-Api-Version": "2022-11-28"
  }
  return headers


def get_issues_from_github(token, page=1):
  start_time = time.time()
  url = f"https://api.github.com/search/issues?q=is:issue+label:good-first-issue+state:open&per_page=100&page={page}"
  #max per page 100

  gh_headers = get_github_client_headers(token)

  response = requests.get(url, headers=gh_headers)

  print(f"Recieved {response.status_code} for url {response.url}")
  results = response.json()
  time_track(start_time, "GitHub API")
  return results


def insert_into_file(file_name, results):
  start_time = time.time()
  with open(file_name, "w") as f:
    json.dump(results, f)
    time_track(start_time, f"Insert into file {file_name}")


def insert_into_database(mongo_client, results):
  start_time = time.time()

  db = mongo_client["github_issues"]
  issues_collection = db["issues"]
  issues_collection.insert_many(results)

  time_track(start_time, "Insert into MongoDB ")


def find_good_first_issues(labels):
  #it is an array and we want the object where name is gfi
  for label in labels:
    if label.get("name") == "good-first-issue":
      label_url = label.get("url").replace("https://api.github.com/repos/",
                                           "https://github.com/")
      label_name = label.get("name")
      return {"label_name": label_name, "label_url": label_url}
  return {"label_name": "", "label_url": ""}


def process_json(json_file):
  start_time = time.time()
  with open(json_file, "r") as f:
    data = json.load(f)

  result_data = []  #arraylist

  for item in data.get("items", []):
    issue_title = item.get("title", "")
    repo_name = item.get("repository_url",
                         "").replace("https://api.github.com/repos/", "")
    issue_url = item.get("html_url", "")
    label_info = find_good_first_issues(item.get("labels", []))
    state = item.get("state", "")
    locked = item.get("locked", False)
    result_entry = {
        "repo_name": repo_name,
        "issue_title": issue_title,
        "issue_url": issue_url,
        "label_name": label_info["label_name"],
        "label_url": label_info["label_url"],
        "state": state,
        "locked": locked
    }
    result_data.append(result_entry)
  time_track(start_time, f"Processed {json_file}")
  return result_data


def main():
  start_time = time.time()
  # mongo_uri = MongoClient(
  #     f"mongodb+srv://TrialH23:{mongo_password}@cluster0.a48kdir.mongodb.net/?retryWrites=true&w=majority"
  # )

  # get issues from github and insert into a json file
  # for page_number in range(1, 4):
  #   issues_from_github = get_issues_from_github(token=gh_token,
  #                                               page=page_number)
  #   #key called as items -> array with multiple jsons inside it
  #   #that many objects in it (javascript) we need length of this array

  #   print(f"Length of result 'item' = {len(issues_from_github['items'])}")
  #   insert_into_file(f"results_{page_number}.json", issues_from_github)
  #   time.sleep(10)

  #   #Process each results_<page_number>.json file and store data in separate files
  # for page_number in range(1, 4):
  #   new_results_json = process_json(f"results_{page_number}.json")
  #   insert_into_file(f"new_results_{page_number}.json", new_results_json)
  #   insert_into_database(mongo_uri, new_results_json)
  #   time.sleep(1)

  time_track(start_time, "Total execution time")


if __name__ == "__main__":
  main()
