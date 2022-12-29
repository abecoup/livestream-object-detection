"""
Raw Data Format:
    {
        'people_crosswalk_count': Decimal('3'), 
        'alert_id': Decimal('7'), 
        'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image75.jpg', 
        'epoch_timestamp': '1669134397'
    }

"""

"""
"""
class Alert:
    """
    """
    def __init__(self, raw_data):
        #print("Raw Data:", raw_data)
        self.people_count = int(raw_data['people_crosswalk_count'])
        self.alert_id = int(raw_data['alert_id'])
        self.image = raw_data['image_url']
        self.epoch_timestamp = int(raw_data['epoch_timestamp'])
    
    """
    """
    def print_alert(self):
        print("Detected People Count:", self.people_count)
        print("Alert ID:", self.alert_id)
        print("Image URL:", self.image)
        print("Epoch Timestamp:", self.epoch_timestamp)