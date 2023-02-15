## AWS SAM Faces API

This project is an API to detect forward facing faces in an image.
It uses OpenCV and Rekognition for detection. 

![aws-sam-rekognition](https://user-images.githubusercontent.com/35927536/217338082-51c88cd9-3e72-4640-adab-491c88d09e66.png)

### Deployment
This application is designed to be deployed using the SAM CLI.<br/>
For more information on how to use `sam deploy` see the [aws-sam-cli repositry](https://github.com/aws/aws-sam-cli).

### API
POST /faces<br/>
send the binary image in the body and it will be returned with rectangles arround the faces.<br/>
There is an example of how to post to the api using a react app [here](https://github.com/dan-mba/react-postpic).


## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
