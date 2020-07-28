from datetime import datetime


class MyOrder():
    def __init__(self, raw_order):
        self.order = []
        self.raw_order = raw_order
        self.__parse()

    def __parse(self):
        for order in self.raw_order:
            temp_order = {}
            temp_order['order_id'] = order['order_id']
            temp_order['order_time'] = datetime.fromtimestamp(order['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            temp_order['ticket_type'] = order['ticket_type']
            temp_order['route'] = order['route']
            temp_order['depart_time'] = order['depart_time']
            temp_order['status'] = order['order_status']
            self.order.append(temp_order)


class ManageOrder():
    def __init__(self, raw_order):
        self.order = []
        self.raw_order = raw_order
        self.__parse()

    def __parse(self):
        for order in self.raw_order:
            temp_order = {}
            temp_order['order_id'] = order['order_id']
            temp_order['order_time'] = datetime.fromtimestamp(order['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            temp_order['ticket_type'] = order['ticket_type']
            temp_order['route'] = order['route']
            temp_order['depart_time'] = order['depart_time']
            temp_order['status'] = order['order_status']
            temp_order['uname'] = order['uname']
            temp_order['email'] = order['email']
            temp_order['id_card'] = order['id_card']
            self.order.append(temp_order)
