import json
import base64
import cgi
import io
import cv2
import numpy as np


def lambda_handler(event, context):
    if 'body' not in event:
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "no body",
        }),
    }

    event['body'] = base64.b64decode(event['body'])
    
    # Decode multipart form-data
    fp = io.BytesIO(event['body'])
    pdict = cgi.parse_header(event['headers']['Content-Type'])[1]
    if 'boundary' in pdict:
        pdict['boundary'] = pdict['boundary'].encode('utf-8')
    pdict['CONTENT-LENGTH'] = len(event['body'])
    form_data = cgi.parse_multipart(fp, pdict)
    

    if '' not in form_data:
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "no file",
        }),
    }

    # Load face detection cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Load image
    np_img = np.frombuffer(form_data[''][0], dtype=np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Create return image
    output_img = cv2.imencode('.png',img)[1]
    output_img = base64.b64encode(output_img).decode('utf-8')

    return {
        "statusCode": 200,
        "body": output_img,
        "isBase64Encoded": True,
        "headers": {
            "Content-Type": "image/png"
        }
    }
