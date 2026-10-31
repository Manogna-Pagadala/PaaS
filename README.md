# Serverless Face Recognition System Using AWS Lambda

A serverless face recognition application built using **AWS Lambda, Amazon S3, Amazon DynamoDB, Docker, and Python**. The system processes uploaded videos, identifies student faces, retrieves corresponding student information, and generates CSV results automatically.

The application uses an event-driven architecture where uploading a video to an S3 bucket triggers an AWS Lambda function, eliminating the need to manage dedicated application servers.

## Overview

The system automates face recognition and student information retrieval from uploaded MP4 videos.

When a video is uploaded, the application:

1. Detects the new video through an Amazon S3 event notification.
2. Invokes an AWS Lambda function packaged as a Docker container.
3. Downloads the video and extracts frames using FFmpeg.
4. Identifies faces by comparing them against stored face encodings.
5. Retrieves the corresponding student information from DynamoDB.
6. Generates a CSV file containing the identified student's details.
7. Uploads the CSV result to an S3 output bucket.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application and Lambda function logic |
| AWS Lambda | Serverless video processing and face recognition |
| Amazon S3 | Video input and CSV output storage |
| Amazon DynamoDB | Student information storage |
| Amazon ECR | Docker container image registry |
| Docker | Packaging the Lambda function and its dependencies |
| boto3 | AWS service interactions |
| FFmpeg | Extracting frames from uploaded videos |
| face_recognition | Identifying faces using known face encodings |

## System Architecture

The application follows an event-driven processing workflow:

```text
          Video Upload (MP4)
                  |
                  v
          Amazon S3 Input Bucket
                  |
                  | ObjectCreated Event
                  v
             AWS Lambda
          (Docker Image in ECR)
                  |
                  v
          Download Input Video
                  |
                  v
          Extract Frames (FFmpeg)
                  |
                  v
          Face Recognition
                  |
                  v
          Identify Student Name
                  |
                  v
             DynamoDB
       Retrieve Student Details
                  |
                  v
          Generate CSV Result
                  |
                  v
          Amazon S3 Output Bucket
```

## Key Features

### 1. Event-Driven Video Processing

The application uses Amazon S3 event notifications to invoke AWS Lambda whenever a new video is uploaded to the input bucket.

Each upload initiates processing without requiring a continuously running application server.

### 2. Containerized AWS Lambda Deployment

The face recognition function is packaged as a Docker image containing the Python runtime, application code, face encodings, and required dependencies.

The container image is stored in Amazon Elastic Container Registry (ECR) and deployed as an AWS Lambda function.

### 3. Video Frame Extraction and Face Recognition

The Lambda function downloads uploaded MP4 videos to temporary storage and uses FFmpeg to extract frames.

Extracted frames are analyzed using the Python `face_recognition` library, which compares detected faces against a set of known face encodings.

### 4. Student Information Retrieval

After identifying a student, the application queries a DynamoDB table to retrieve the corresponding student record.

Student information includes fields such as:

- Name
- Student ID
- Major
- Year

The retrieved information is used to generate a CSV result containing the student's name, major, and year.

### 5. Automatic Result Storage

The generated CSV file is uploaded to a designated Amazon S3 output bucket, where it can be retrieved after processing.

### 6. Serverless Scaling

AWS Lambda manages function execution and scaling based on incoming requests and service concurrency limits.

This removes the need to implement custom EC2 instance scaling or maintain dedicated processing servers.

## Implementation Details

### Dockerfile

The Dockerfile packages the Python-based Lambda function and its dependencies, including:

- AWS Lambda Runtime Interface Client
- boto3
- face_recognition
- FFmpeg
- Known face encodings
- Application handler code

The resulting image is pushed to Amazon ECR for deployment.

### handler.py

The Lambda handler implements the main processing workflow:

1. Receives the S3 object creation event.
2. Extracts the source bucket name and uploaded video key.
3. Downloads the video from S3.
4. Extracts frames using FFmpeg.
5. Performs face recognition against known encodings.
6. Retrieves matching student information from DynamoDB.
7. Generates a CSV result.
8. Uploads the CSV to the output S3 bucket.

### upload_data.py

This script loads student information from a JSON file into DynamoDB.

Each student record contains fields such as name, ID, major, and year. The script uses boto3's `put_item` operation to insert records into the DynamoDB table.

## Setup and Deployment

### Prerequisites

- Python
- Docker Desktop
- AWS account with access to Lambda, S3, DynamoDB, and ECR
- AWS CLI configured with appropriate credentials
- Student information JSON file
- Known face encodings required by the recognition model

### Step 1: Configure Amazon S3

Create two S3 buckets:

- **Input bucket:** Stores uploaded MP4 videos.
- **Output bucket:** Stores generated CSV results.

### Step 2: Configure DynamoDB

Create a DynamoDB table named `student1` and populate it with student records using the data upload script.

```bash
python upload_data.py
```

### Step 3: Build the Docker Image

Build the container image containing the Lambda function and its dependencies.

```bash
docker build -t face-recognition-lambda .
```

### Step 4: Push the Image to Amazon ECR

Create an ECR repository, authenticate Docker with ECR, and tag the image using the repository URI.

```bash
docker tag face-recognition-lambda:latest <ecr-repository-uri>:latest

docker push <ecr-repository-uri>:latest
```

Replace `<ecr-repository-uri>` with your Amazon ECR repository URI.

### Step 5: Deploy AWS Lambda

Create an AWS Lambda function using the container image stored in ECR.

Configure the function with the necessary IAM permissions for accessing S3 and DynamoDB.

### Step 6: Configure the S3 Trigger

Add an S3 event notification to invoke the Lambda function when a new object is created in the input bucket.

### Step 7: Run the Application

Upload an MP4 video to the input bucket or run the workload generator with the configured bucket names.

The Lambda function automatically processes the video and writes the CSV result to the output bucket.

## Testing

The application was tested using video uploads to verify the complete processing workflow.

Testing included:

- Confirming that input and output S3 buckets were initially empty.
- Uploading test videos to the input bucket.
- Verifying that S3 object creation events invoked the Lambda function.
- Checking the face recognition and DynamoDB lookup workflow.
- Confirming that CSV results were generated in the output bucket.

Two test cases were documented, producing CSV output files such as `Test_0.csv` and `Test_1.csv`.

## Project Outcome

The project demonstrates how AWS managed services can be combined to build an event-driven video processing application.

It covers containerized serverless deployment, event-triggered execution, object storage integration, facial recognition, and NoSQL database access without requiring dedicated application servers.

## Technologies Used

`Python` · `AWS Lambda` · `Amazon S3` · `Amazon DynamoDB` · `Amazon ECR` · `Docker` · `boto3` · `FFmpeg` · `face_recognition`
