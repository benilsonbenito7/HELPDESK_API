from ninja.orm import ModelSchema
from ..models import Ticket, TicketComment
from ninja import Schema, Field
from pydantic import EmailStr

class TicketSchemaIn(Schema):
    email: EmailStr
    title: str
    description: str

class TicketSchemaOut(ModelSchema):
    class Meta:
        model = Ticket
        fields = "__all__"

#Schemas status ------>

class TicketStatusOut(ModelSchema):
    class Meta:
        model = Ticket
        fields = ("status",)
        
class TicketStatusIn(Schema):
    status : Ticket.Status

#Schemas comments ------>

class TicketCommentOut(ModelSchema):
    ticket_reference: str = Field(None)
    
    class Meta:
        model = TicketComment
        fields = ["id", "author", "message", "created_at"]
        
    @staticmethod
    def resolve_ticket_reference(obj):
        return obj.ticket.reference
        
class TicketCommentIn(ModelSchema):
    class Meta:
        model = TicketComment
        fields = ["author", "message"]

#Schemas USER ------>

class UserIN(Schema):
    username: str
    email: str
    password: str

class UserOut(Schema):
    id: int
    username: str
    email: str