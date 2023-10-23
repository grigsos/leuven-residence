import requests
import json

def lambda_handler(event, context):
    api_url = "https://afspraak.leuven.be/qmaticwebbooking/rest/schedule/branches/31109068d9785b4c0f07ec342d4040756b1cb8953dd8ba9315f3ab25c560514e"
    service_id = "b1f4b813c698415d092deff4293eec7d7e649b4116888e28120b03af2e249729"
    custom_slot_length = 15
    date = "2023-10-31"
    num_of_entries = 10
    date_list = []
    result_1 = make_api_call(api_url, service_id, custom_slot_length, date, "dates")

    print(result_1)

    if type(result_1)!=int:
        for index, day in enumerate(result_1):
            if index < num_of_entries:
                date_list.append(day["date"])
            else:
                break
    else:
        print("Error: Failed to retrieve data for the first API call.")
        return {
            "statusCode": 500,
            "body": "Error: Failed to retrieve data for the first API call."
        }
    
    all_timeslots = []
    for index, date_in_list in enumerate(date_list):
        timeslot_api = make_api_call(api_url, service_id, custom_slot_length, date_in_list, "times")
        for secondary_index, timeslot in enumerate(timeslot_api):
            all_timeslots.append(timeslot)
            if len(all_timeslots) >= 10:
                break
        if len(all_timeslots) >= 10:
            break

    print(all_timeslots)
    return {
        "statusCode": 200,
        "body": json.dumps(all_timeslots)
    }

def make_api_call(api_url, service_id, custom_slot_length, date, request_type):
    if request_type == "dates":
        url = f"{api_url}/dates;servicePublicId={service_id};customSlotLength={custom_slot_length}"
    elif request_type == "times":
        url = f"{api_url}/dates/{date}/times;servicePublicId={service_id};customSlotLength={custom_slot_length}"
    else:
        return None

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

if __name__ == "__main__":
    lambda_handler(None, None)