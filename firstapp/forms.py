from mongodbforms import DocumentForm
from models import CreateAccount

class CreateAccountForm(DocumentForm):
    class Meta:
        document = CreateAccount
        fields = ['firstName', 'lastName', 'phoneNum', 'ssn', 'address',  'email', 'userName', 'password', 'verification']