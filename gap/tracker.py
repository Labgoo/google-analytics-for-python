__author__ = 'minhtule'

from request import *


class Tracker(object):
    """

    """

    def __init__(self, tracking_id, visitor):
        self.__tracking_id = tracking_id
        self.__visitor = visitor
        self.__debug_enabled = False

    @property
    def tracking_id(self):
        return self.__tracking_id

    @property
    def client_id(self):
        return self.__visitor.id

    @property
    def visitor(self):
        return self.__visitor

    @property
    def debug_enabled(self):
        return self.__debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, value):
        self.__debug_enabled = value

    @property
    def original_request_ip(self):
        return self.visitor.ip_address

    @property
    def original_request_user_agent(self):
        return self.visitor.user_agent

    @property
    def original_request_language(self):
        return self.visitor.language

    # Public method
    def send_page(self, hostname=None, path=None, title=None):
        PageTrackingRequest(
            self,
            document_hostname=hostname if hostname else self.visitor.document_host,
            document_path=path if path else self.visitor.document_path.document_host,
            document_title=title
        ).send()

    def send_transaction(self, transaction_id, transaction_affiliation=None, transaction_revenue=None, transaction_shipping=None, transaction_tax=None, currency_code=None):
        TransactionTrackingRequest(
            self,
            transaction_id,
            transaction_affiliation=transaction_affiliation,
            transaction_revenue=transaction_revenue,
            transaction_shipping=transaction_shipping,
            transaction_tax=transaction_tax,
            currency_code=currency_code
        ).send()

    def send_item(self, transaction_id, item_name, item_price=None, item_quantity=None, item_code=None, item_category=None, currency_code=None):
        ItemTrackingRequest(
            self,
            transaction_id,
            item_name,
            item_price=item_price,
            item_quantity=item_quantity,
            item_code=item_code,
            item_category=item_category,
            currency_code=currency_code
        ).send()


class CustomVariable(object):
    @property
    def index(self):
        return self.__index

    @property
    def value(self):
        return self.__value

    def __init__(self, index, value):
        self.__index = index
        self.__value = value