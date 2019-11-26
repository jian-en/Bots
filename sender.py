import os
import boto3
import datetime

FORMAT = '%Y-%m-%d %H:%M:%S'
client = boto3.client('sns')


def send(data, period):
    print('Sending')
    result = client.publish(TopicArn='arn:aws:sns:us-east-1:949577760398:mexico-visa',
                            Message="{} has available slots. Go and reserve!".format(data),
                            MessageAttributes={"time": {'DataType': 'String', 
                                                        'StringValue': period}})
    print(result)
    with open('sendtime', 'w') as f:
        f.write(datetime.datetime.now().strftime(FORMAT))
    

def can_send():
    if not os.path.exists('sendtime'):
        return True
    else:
        with open("sendtime", "r") as f:
            dt = f.read().strip()
        last_send_time = datetime.datetime.strptime(dt, FORMAT)
        time_delta = datetime.datetime.now() - last_send_time
        if time_delta.seconds > 3600:
            return True
        else:
            return False

def send_to_topic(data):
    now = datetime.datetime.now()
    if now.hour >= 0 and now.hour <= 8:
        period = 'nighttime'
    else:
        period = 'daytime'
    print "send..."
    if can_send():
        send(data, period)
    else:
        print "no send..."
