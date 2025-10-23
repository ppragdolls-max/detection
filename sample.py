import time
import requests
import os
import uuid
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import cv2 as cv

# Load YOLO model once (avoid reloading every image)
model = YOLO("yolo11n.pt")

while True:
    try:
        # Refresh Zoho token
        refresh_token = "1000.254511476b2ff69e88275cf68a32eb75.3e41f070a3c87d4b026e5bafaa826a5d"
        url = f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id=1000.HXW46KJBW0PAQ5V0FXI422KCD2RF2A&client_secret=81e2a7b73552a4df1518d7140bb8a53141a79b260b&grant_type=refresh_token"
        x = requests.post(url)
        access_token = x.json().get("access_token")
        api_headers = {"Authorization": "Zoho-oauthtoken " + access_token}

        # Fetch records from Zoho
        report_response = requests.get(
            "https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report",
            headers=api_headers
        )
        var = report_response.json()

        if "data" in var:
            for record in var["data"]:
                if "ID" in record:
                    id = record["ID"]
                    image_response = requests.get(
                        f"https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report/{id}/upload_Image/download",
                        headers=api_headers
                    )
                    img = Image.open(BytesIO(image_response.content))
                    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)

                    # Run YOLO
                    result = model(img_cv)
                    arr_frame = result[0].plot()

                    # Save to /tmp
                    random_name = f"/tmp/{uuid.uuid4()}.jpg"
                    cv.imwrite(random_name, arr_frame)

                    # Upload processed image
                    up_refresh_token = "1000.0ec80a6e0bf93bfa7b8397d8d7d5f08c.5b3714b167919f0e2c24b74f808d90db"
                    url2 = f"https://accounts.zoho.in/oauth/v2/token?refresh_token={up_refresh_token}&client_id=1000.HXW46KJBW0PAQ5V0FXI422KCD2RF2A&client_secret=81e2a7b73552a4df1518d7140bb8a53141a79b260b&grant_type=refresh_token"
                    xy = requests.post(url2)
                    up_access_token = xy.json().get("access_token")
                    api_headers1 = {"Authorization": "Zoho-oauthtoken " + up_access_token}

                    with open(random_name, 'rb') as file:
                        files = {'file': file}
                        params = {"skip_workflow": "[\"schedules\",\"form_workflow\"]"}
                        requests.post(
                            f"https://www.zohoapis.in/creator/v2.1/data/twinpixelsstudio/detection/report/Image_Upload_Report/{id}/Detected_Image/upload",
                            headers=api_headers1,
                            files=files,
                            params=params
                        )

    except Exception as e:
        print("Error:", e)

    time.sleep(10)
