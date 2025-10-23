import time
import requests
import os
import json
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import cv2 as cv
import uuid
# token = "1000.780f99c9e12d989c5cd51ec3a5304448.f70032f5653c35e215dd0c8b776101b4"
# url1 = "https://accounts.zoho.in/oauth/v2/token?grant_type=authorization_code&client_id=1000.HXW46KJBW0PAQ5V0FXI422KCD2RF2A&client_secret=81e2a7b73552a4df1518d7140bb8a53141a79b260b&code="+token
# myobj1 = {'somekey': 'somevalue'}
# x = requests.post(url1, json = myobj1)
# print(x.json())
# if "refresh_token" in x.json():
#     refresh_token = x.json()["refresh_token"]
#     print("Refresh Token:", refresh_token)  
while True:  # <-- loop continuously
    try:
        refresh_token = "1000.254511476b2ff69e88275cf68a32eb75.3e41f070a3c87d4b026e5bafaa826a5d"
        url = "https://accounts.zoho.in/oauth/v2/token?refresh_token="+refresh_token+"&client_id=1000.HXW46KJBW0PAQ5V0FXI422KCD2RF2A&client_secret=81e2a7b73552a4df1518d7140bb8a53141a79b260b&grant_type=refresh_token"
        myobj = {'somekey': 'somevalue'}
        x = requests.post(url, json = myobj)
        if "access_token" in x.json():
            access_token = x.json()["access_token"]
        api_headers = {
            "Authorization": "Zoho-oauthtoken "+access_token
        }
        report_response = requests.get("https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report", headers=api_headers)
        var = report_response.json()
        if "data" in var:
            for record in var["data"]:
                if "ID" in record:
                    id = record["ID"]
                    im = record["upload_Image"]
                    image_response = requests.get("https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report/"+id+"/upload_Image/download", headers=api_headers)
                    img = Image.open(BytesIO(image_response.content))
                    random_name = str(uuid.uuid4()) + ".jpg"
                    # ############### Analysing ##################
                    model = YOLO("yolo11n.pt")
                    vid = img
                    result = model(vid)
                    arr_frame = result[0].plot()
                    cv.imwrite(random_name, arr_frame)

                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    ############### Uploading ##################
                    up_refresh_token = "1000.0ec80a6e0bf93bfa7b8397d8d7d5f08c.5b3714b167919f0e2c24b74f808d90db"
                    url2 = "https://accounts.zoho.in/oauth/v2/token?refresh_token="+up_refresh_token+"&client_id=1000.HXW46KJBW0PAQ5V0FXI422KCD2RF2A&client_secret=81e2a7b73552a4df1518d7140bb8a53141a79b260b&grant_type=refresh_token"
                    myobj2 = {'somekey': 'somevalue'}
                    xy = requests.post(url2, json = myobj2)
                    if "access_token" in xy.json():
                        up_access_token = xy.json()["access_token"]
                    api_headers1 = {
                        "Authorization": "Zoho-oauthtoken "+up_access_token
                    }
                    path = os.path.join("D:\\Training", random_name)
                    print("Uploading Image from path:", path)
                    parameters = {
                        "skip_workflow": "[\"schedules\",\"form_workflow\"]"
                    }

                    file_path = path

                    with open(file_path, 'rb') as file:
                        files = {'file': file}

                        try:
                            response = requests.post("https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report/"+id+"/Detected_Image/upload", headers=api_headers1, files=files, params=parameters)
                        except:
                            print("Exception while making the API request.")
    except:
        print("Exception while making the API request.")

    # Wait a few seconds before checking again
    time.sleep(10)
