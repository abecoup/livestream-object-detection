"""
Raw Data Format:
    {
        'report': [
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image7.jpg', 
                'epoch_timestamp': '1669133966', 
                'alert_id': Decimal('7')
            }, 
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image295.jpg', 
                'epoch_timestamp': '1669133502', 
                'alert_id': Decimal('2')
            }, 
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image9.jpg', 
                'epoch_timestamp': '1669133839', 
                'alert_id': Decimal('9')
            }, 
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image6.jpg', 
                'epoch_timestamp': '1669133962', 
                'alert_id': Decimal('6')
            }, 
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image10.jpg', 
                'epoch_timestamp': '1669133843', 
                'alert_id': Decimal('1')
            }, 
            {
                'people_crosswalk_count': Decimal('1'), 
                'image_url': 'https://crosswalk-frames2.s3.us-east-1.amazonaws.com/image5.jpg', 
                'epoch_timestamp': '1669133959', 
                'alert_id': Decimal('5')
            }
        ], 
        'report_id': Decimal('3')
    }
"""

from model.alert import Alert
import datetime

"""
"""
class Report:
    """
    """
    def __init__(self, raw_data):
        self.report_id = int(raw_data['report_id'])
        self.alerts = self.get_raw_alerts(raw_data['report'])
        self.epoch_timestamps = self.get_epoch_timestamps()
        self.start_time = self.convert_datetime(self.epoch_timestamps[0])
        self.end_time = self.convert_datetime(self.epoch_timestamps[len(self.epoch_timestamps)-1])
        self.report_image = self.alerts[0].image
        self.total_people_count = self.get_total_count()

    """
    """
    def get_raw_alerts(self, raw_data):
        alert_list = []
        for alert in raw_data:
            new_alert = Alert(alert)
            alert_list.append(new_alert)
        alert_list.sort(key=lambda x: x.epoch_timestamp)
        return alert_list

    """
    """
    def get_epoch_timestamps(self):
        epoch_timestamp_list = []
        for alert in self.alerts:
            epoch_timestamp_list.append(alert.epoch_timestamp)
        epoch_timestamp_list.sort()
        return epoch_timestamp_list

    """
    """
    def convert_datetime(self, epoch_time):
        date_time = datetime.datetime.fromtimestamp(epoch_time)
        return date_time

    """
    """
    def get_total_count(self):
        total_count = 0
        for alert in self.alerts:
            total_count = total_count + alert.people_count
        return total_count

    """
    """
    def print_report(self):
        print("Report ID:", self.report_id)
        print("Alerts:", self.alerts)
        print("Epoch Timestamps:", self.epoch_timestamps)
        print("Report Start:", self.start_time)
        print("Report End:", self.end_time)
        print("Report Image:", self.report_image)
        print("Total People Count:", self.total_people_count)
