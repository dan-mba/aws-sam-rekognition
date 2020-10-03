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

    body = base64.b64decode(event['body'])
    
    # Load face detection cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Load image
    np_img = np.frombuffer(body, dtype=np.uint8)
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
