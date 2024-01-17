import requests, json, statistics, os
from pprint import pprint
from tqdm import tqdm
from jinja2 import Template

def get_data(url, headers=None):
    response = requests.get(url, headers=headers)
    temp = json.loads(response.text)
    return temp


def post_data(url, file_path):
  url = url 
  try:
        with open(file_path, 'rb') as file:
            # Define any headers or authentication information as needed
            headers = HEADERS
            # Make a POST request to the server
            print(url, HEADERS)
            response = requests.post(url, data=file, headers=headers)

            if response.status_code == 201:
                print(f"Successfully posted {file_path} to the server.")
            else:
                print(f"Failed to post {file_path}. Status code: {response.status_code}")
                # print(response.headers)
                # print(response.con)
  except Exception as e:
        print(f"Error while posting {file_path}: {str(e)}")

def send_files():
    # Check if the local directory exists
    if not os.path.exists(LOCAL_DIR) or not os.path.isdir(LOCAL_DIR):
        print(f"Local directory '{LOCAL_DIR}' does not exist.")
        return

    # Iterate through the files in the directory
    for root, _, files in os.walk(LOCAL_DIR):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                post_data(URL, file_path)

def get_average(url, headers):
  url = url + f"&category={CATEGORY}&category={CATEGORY_ID}&date=ge{START}&date=le{END}&code=85354-9"
  print("Getting data from: "+url)
  data = get_data(url, headers)["entry"]
  records = {}
  for entry in tqdm(data): 
    datetimeentry = entry['resource']['effectiveDateTime']
    records[datetimeentry] = {
      entry['resource']['component'][0]['code']['coding'][0]['code']:entry['resource']['component'][0]['valueQuantity']['value'],
      entry['resource']['component'][1]['code']['coding'][0]['code']:entry['resource']['component'][1]['valueQuantity']['value'],
      "id":f"{entry['resource']['resourceType']}/{entry['resource']['id']}"
      }
  return calculate_averages(records), data

def calculate_averages(data):
  # Initialize a dictionary to store the averages
  averages = {}

  timestamps = []  # Initialize a list to store timestamps
  references = []
  # Iterate through the outer dictionary
  for timestamp, inner_dict in data.items():
      timestamps.append(timestamp)  # Add the timestamp to the list
      references.append(inner_dict.pop("id"))
      # Iterate through the inner dictionary
      for key, value in inner_dict.items():
          if key in averages:
              averages[key].append(value)
          else:
              averages[key] = [value]

  # Calculate the averages using the statistics.mean function
  for key, values in averages.items():
      averages[key] = statistics.mean(values)

  # Create the final result dictionary
  result = {'averages': averages, 'timestamps': timestamps, 'references': references}

  return result

def prepare_average_post(averages, data):
  inp = {
    'id': f"{PATIENT_ID}: {CATEGORY_ID}"+START+END,
    'category': CATEGORY,
    'category_code': CATEGORY_ID,
    'patient_id': PATIENT_ID,
    'start_date': START,
    'end_date': END,
    'observations': averages['references'],
    'sys_pressure': round(averages['averages']['8480-6'], 0),
    'dia_pressure': round(averages['averages']['8462-4'], 0),
    'count': len(averages['timestamps']),
  }
  template = open("template.txt", "r")
  template = template.read()
  template = Template(template)
  rendered = json.loads(template.render(inp))
  for pos, value in enumerate(rendered['component']):
      rendered['component'][pos]['valueQuantity']['value'] = int(float(rendered['component'][pos]['valueQuantity']['value']))
  return rendered

def send_average():
  averages, data = get_average(URL, HEADERS)
  # print(averages)
  json_str = prepare_average_post(averages, data)
  json.dump(json_str, open("output.json", "w"))
  try:
    headers = HEADERS
    # Make a POST request to the server
    print(URL, HEADERS)
    response = requests.post(URL, data=json.dumps(json_str), headers=headers)
    if response.status_code == 201:
              print(f"Successfully posted averages to the server.")
    else:
        print(f"Failed to post averages. Status code: {response.status_code}")
        
  except Exception as e:
        print(f"Error while posting averages: {str(e)}")

if __name__ == "__main__":
  ### Configuration information, please 
  PATIENT_ID = 14769
  URL = f"https://api.logicahealth.org/CardXHTNMG/open/Observation?patient={PATIENT_ID}"
  CATEGORY = "vital-signs"
  CATEGORY_ID = 310858007
  START = '2024-01-01'
  END = '2024-01-08'
  HEADERS = {'Content-Type':"application/json"} #{'Ocp-Apim-Subscription-Key':'76104a687e5e497e9466f660bdd30e7f', 'Content-Type':"application/json"}
  LOCAL_DIR = 'smbp_observation'
  ### Uncomment (remove #, add it back in to turn off) line below to send all files in the smbp_observation folder to the server at the patient_id.
  # send_files()

  ### Uncomment the lines below to pull all data records for the defined time frame and calculate average blood pressure
  send_average()
  
    