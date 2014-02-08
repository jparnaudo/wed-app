import datetime

from google.appengine.ext import db
from google.appengine.ext.db.metadata import Property
from base_model import BaseModel
from util import dt2ts


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%d-%m-%Y"
MONTH_FORMAT = '%Y-%m'
        
class BasicInfo(BaseModel):
    title = db.StringProperty(choices=[None, "Mr", "Mrs", "Miss", "Ms", "Dr", "Prof"])
    first = db.StringProperty()
    middle = db.StringProperty()
    suffix = db.StringProperty()
    last = db.StringProperty()
    aliases = db.StringProperty()
    birthdate = db.DateProperty()
    email = db.StringProperty()
    other_email = db.StringProperty()
    phone = db.StringProperty()  # int'l code, number
    other_phone = db.StringProperty()  # int'l code, number
    country = db.StringProperty()

    def get_full_name(self):
        return self.first + " " + self.last

    def to_dict(self):
        d = db.to_dict(self)
        if self.birthdate: d["birthdate"] = d["birthdate"].strftime(DATE_FORMAT)
        return d


class IDUpload(BaseModel):
    id_type = db.StringProperty(choices=["passport", "driverslicense", "ssc", "military", "birth", "residency", "other"])
    upload = db.BlobProperty()
    number = db.StringProperty()
    issued = db.DateProperty()
    expires = db.DateProperty()
    country = db.StringProperty()
    state = db.StringProperty()

    def to_dict(self):
        d = db.to_dict(self)
        del d["upload"]
        if self.issued: d["issued"] = self.issued.strftime(DATE_FORMAT)
        if self.expires: d["expires"] = self.expires.strftime(DATE_FORMAT)
        return d

class PEPCheck(BaseModel):
    value = db.BooleanProperty()
    comment = db.TextProperty()

class Address(BaseModel):
    street_address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    zip = db.StringProperty()
    country = db.StringProperty()

class Period(BaseModel):
    start = db.DateProperty()
    end = db.DateProperty()

    def to_dict(self):
        d = db.to_dict(self)
        if self.start : d["start"] = self.start.strftime(DATE_FORMAT)
        if self.end : d["end"] = self.end.strftime(DATE_FORMAT)
        return d

class DomicileInfo(BaseModel):
    current = db.ReferenceProperty(Address)
    current_period = db.ReferenceProperty(Period)
    current_proof = db.BlobProperty()
    previous = db.ReferenceProperty(Address, collection_name='previous')
    previous_period = db.ReferenceProperty(Period, collection_name='previous')
    previous_proof = db.BlobProperty()

    def to_dict(self):
        d = db.to_dict(self)

        del d["current_proof"]
        del d["previous_proof"]

        d["current_period"] = self.current_period.to_dict()
        d["previous_period"] = self.previous_period.to_dict()

        d["current"] = self.current.to_dict()
        current_data = {"cur_" + key:value for key, value in d["current"].items()}
        d["current"] = current_data
        d["previous"] = self.previous.to_dict()
        previous_data = {"prev_" + key:value for key, value in d["previous"].items()}
        d["previous"] = previous_data

        return d
     
    @classmethod
    def new(cls):
        d = cls()
        d.current = Address().put()
        d.current_period = Period().put()
        d.previous = Address().put()
        d.previous_period = Period().put()
        d.put()
        return d

class FinancialInfo(BaseModel):
    income = db.StringProperty(choices=["salary", "self", "pension", "other"])
    other = db.StringProperty()
    employer = db.StringProperty()
    employment_type = db.StringProperty(choices=["fulltime", "home", "government", "unemployed", "parttime", "public_assistance", "retired", "student"])
    time_in_employment = db.ReferenceProperty(Period)
    phone = db.StringProperty()  # int'l code, number
    occupation = db.StringProperty()
    nature_of_business = db.StringProperty()
    annual_income = db.IntegerProperty()
    annual_income_currency = db.StringProperty()  # USD, EUR, etc
    account_usage = db.StringListProperty()  # International transfer, Bitcoin to FX, FX to Bitcoin, Transferring Bitcoin payments for goods and services into FX, Trading and Investing, Other (text box)
    regularity = db.StringProperty(choices=["daily", "weekly", "monthly", "twice", "annually"])

    def to_dict(self):
        d = db.to_dict(self)
        if self.time_in_employment.start: d["time_in_employment_start"] = self.time_in_employment.start.strftime(MONTH_FORMAT)
        if self.time_in_employment.end: d["time_in_employment_end"] = self.time_in_employment.end.strftime(MONTH_FORMAT)
        return d

    @classmethod
    def new(cls):
        f = cls()
        f.time_in_employment = Period().put()
        f.put()
        return f

class BankAccount(BaseModel):

    account_holder = db.StringProperty()
    account_number = db.StringProperty()
    sort_code = db.StringProperty()
    currency = db.StringProperty()
    bic = db.StringProperty()
    swift = db.StringProperty()
    bank_address = db.ReferenceProperty(Address, collection_name='bank')
    fedwire_or_aba = db.StringProperty()
    clearing_code = db.StringProperty()
    iban = db.StringProperty()
    recipients_full_name = db.StringProperty()
    recipients_address = db.ReferenceProperty(Address, collection_name='recipient')

    @classmethod
    def new(cls):
        ba = cls()
        ba.bank_address = Address().put()
        ba.recipients_address = Address().put()
        ba.put()
        return ba

class BitcoinInfo(BaseModel):
    bank_account1 = db.ReferenceProperty(BankAccount, collection_name='one')
    bank_account2 = db.ReferenceProperty(BankAccount, collection_name='two')
    bitcoin_addresses = db.StringListProperty()

    def to_dict(self):
        d = db.to_dict(self)
        d["bank_account1"] = self.bank_account1.to_dict()
        d["bank_account2"] = self.bank_account2.to_dict()

        d["bank_account1"]["bank_address"] = self.bank_account1.bank_address.to_dict()
        d["bank_account1"]["recipients_address"] = self.bank_account1.recipients_address.to_dict()
        d["bank_account2"]["bank_address"] = self.bank_account2.bank_address.to_dict()
        d["bank_account2"]["recipients_address"] = self.bank_account2.recipients_address.to_dict()

        if self.bitcoin_addresses:
            bitcoin_addresses = {"bitcoin_address_" + str(i + 1):d["bitcoin_addresses"][i] for i in range(0, len(d["bitcoin_addresses"]))}
        else:
            bitcoin_addresses = {"bitcoin_address_" + str(i + 1):"" for i in range(0, 6)}
        
        d["bitcoin_addresses"] = bitcoin_addresses
        

        return d

    @classmethod
    def new(cls):
        b = cls()
        b.bank_account1 = BankAccount.new()
        b.bank_account2 = BankAccount.new()
        b.put()
        return b

IN_CREATION, PENDING, APPROVED = 0,1,2
class Person(BaseModel):
    person_id = db.IntegerProperty()
    basic_info = db.ReferenceProperty(BasicInfo)
    id_upload = db.ReferenceProperty(IDUpload)
    pep_check = db.ReferenceProperty(PEPCheck)
    domicile_info = db.ReferenceProperty(DomicileInfo)
    financial_info = db.ReferenceProperty(FinancialInfo)
    bitcoin_info = db.ReferenceProperty(BitcoinInfo)
    state = db.IntegerProperty(choices=[IN_CREATION, PENDING, APPROVED])
 
    def to_dict(self):
        d = db.to_dict(self)
        d["basic_info"] = self.basic_info.to_dict()
        return d
    
    def to_dict_full(self):
        d = db.to_dict(self)
        d["basic_info"] = self.basic_info.to_dict()
        d["id_upload"] = self.id_upload.to_dict()
        d["pep_check"] = self.pep_check.to_dict()   
        d["domicile_info"] = self.domicile_info.to_dict()
        d["financial_info"] = self.financial_info.to_dict()
        d["bitcoin_info"] = self.bitcoin_info.to_dict()
        return d
    
    def approve(self):
        self.state = APPROVED 
        self.put()
    
    def set_pending(self):
        self.state = PENDING
        self.put()

    def get_state(self):
        if self.state == IN_CREATION : return "in_creation"
        elif self.state == PENDING : return "pending"
        else: return "approved"
        
    @classmethod
    def get_all(cls):
        return cls.all()

    @classmethod
    def get(cls, ts):
        return cls.all().filter("person_id =", ts).get()

    @classmethod
    def get_pending(cls):
        return cls.all().filter("state <=", PENDING)

    @classmethod
    def new(cls):
        p = cls()
        p.person_id = dt2ts(datetime.datetime.now())
        p.basic_info = BasicInfo().put()
        p.id_upload = IDUpload().put()
        p.pep_check = PEPCheck().put()
        p.domicile_info = DomicileInfo.new()
        p.financial_info = FinancialInfo.new()
        p.bitcoin_info = BitcoinInfo.new()
        p.state = IN_CREATION
        p.put()
        return p