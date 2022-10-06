
class DatachangeHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def __init__(self):
        super()
        self.subscribed_val = 0

    def datachange_notification(self, node, val, data):
        # instead of just printing this, we need to send it to the frontend somehow
        self.subscribed_val = val
        print("New data change event", node, self.subscribed_val)

    def event_notification(self, event):
        print("New event", event)
