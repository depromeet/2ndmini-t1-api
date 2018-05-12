import os
import boto3
import json
import datetime
from operator import itemgetter
from botocore.vendored import requests

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)


def lambda_handler(event, context):

    # bucket name & file
    bucket = os.environ.get('BUCKET')
    key = os.environ.get('KEY_FILE')
    
    
    # nickname
    try:
        nickname = event["nickname"]
        score = event["score"]
        stage = event["stage"]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        if nickname == "" or score == "" or stage == "":
            return {"error":"Require nickname, score, stage"}
        
    except Exception as e:
        print(e)
        raise(e)
        
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        json_data = json.loads(data['Body'].read().decode('utf-8'))
        
        """
        Test dummy data
        """
        # json_data["data"].append({
        #     "nickname":"동혁",
        #     "score":310,
        #     "stage":1
        # })
        
        # json_data["data"].append({
        #     "nickname":"상철",
        #     "score": 1400,
        #     "stage":1
        # })
        # json_data["data"].append({
        #     "nickname":"진주",
        #     "score": 2400,
        #     "stage":2
        # })
        # json_data["data"].append({
        #     "nickname":"병규",
        #     "score": 1100,
        #     "stage":1
        # })
        # json_data["data"].append({
        #     "nickname":"명준",
        #     "score": 400,
        #     "stage":1
        # })
        """
        End Test dummy data
        """
        
        # if exist, update score data
        try:
            exist_user = next((item for item in json_data["data"] if item["nickname"] == nickname))
            if exist_user and exist_user["score"] < score:
                exist_user["score"] = score
                print("update score")
                
        except:
            # else: append data
            json_data["data"].append({
                "nickname":nickname,
                "score":score,
                "stage":stage
            })
            
            
        # update score dashboard and S3 upload
        json_data["timestamp"] = timestamp
        
        try:
            s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(json_data))

        except Exception as e:
            print(e)
            raise(e)
        
        # Order by score
        res_data = sorted(json_data["data"], key=itemgetter('score'), reverse=True)
        
        # response 5 data
        return {
            "timestamp":timestamp,
            "data":res_data[:5]
        }
    
    except Exception as e:
        print(e)
        raise e
    
    
