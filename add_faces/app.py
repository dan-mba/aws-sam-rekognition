import json
import base64
import cv2
import numpy as np
import boto3
from botocore.exceptions import ClientError

client = boto3.client('rekognition')

def lambda_handler(event, context):
    if 'body' not in event:
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "no body",
        }),
    }

    try:
        img_bytes = event['body']
        img_decoded = base64.b64decode(img_bytes)

        # Load image
        np_img = np.frombuffer(img_decoded, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        faces = client.detect_faces(
            Image={
                'Bytes': img_bytes
            }
        )

        return {
            "statusCode": "200",
            "body": json.dumps(faces)
        }

        # Draw rectangle around the faces TODO update for Rekognition
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Create return image
        output_img = cv2.imencode('.png',img)[1]
        output_img = base64.b64encode(output_img).decode('utf-8')
    except ClientError as error:
        return {
            "statusCode": "200",
            "body": json.dumps(error.response['Error'])
        }
    except Exception as error:
        return {
            "statusCode": "200",
            "body": json.dumps({
                "message": str(error)
            })
        }

    return {
        "statusCode": 200,
        "body": output_img,
        "isBase64Encoded": True,
        "headers": {
            "Content-Type": "image/png"
        }
    }
