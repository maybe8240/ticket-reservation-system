

class SearchTicket():
    def __init__(self, raw_tickets):
        self.tickets = []
        self.raw_tickets = raw_tickets
        self.__parse()

    def __parse(self):
        for ticket in self.raw_tickets:
            temp_ticket = {}
            temp_ticket['name'] = ticket['name']
            temp_ticket['company'] = ticket['company_name']
            temp_ticket['depart_date_time'] = ticket['depart_date'] + ' ' + ticket['depart_time']
            temp_ticket['arrive_date_time'] = ticket['arrive_date'] + ' ' + ticket['arrive_time']
            temp_ticket['depart_airport'] = ticket['depart_airport']
            temp_ticket['arrive_airport'] = ticket['arrive_airport']

            temp_ticket['third_class_pric'] = 'Economy: ' + str(ticket['third_class_price']) + 'CAD'
            temp_ticket['second_class_pric'] = 'Business: ' + str(ticket['second_class_price']) + 'CAD'
            temp_ticket['first_class_pric'] = 'First-class: ' + str(ticket['first_class_price']) + 'CAD'

            temp_ticket['depart_city'] = ticket['depart_city']
            temp_ticket['arrive_city'] = ticket['arrive_city']
            temp_ticket['first_class_num'] = str(ticket['first_class_num']) + 'tickets'
            temp_ticket['second_class_num'] = str(ticket['second_class_num']) + 'tickets'
            temp_ticket['third_class_num'] = str(ticket['third_class_num']) + 'tickets'
            self.tickets.append(temp_ticket)
