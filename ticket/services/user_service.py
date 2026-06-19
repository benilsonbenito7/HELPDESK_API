import datetime
import random
from ..models import Ticket, TicketComment
from django.db.models import Q
from django.shortcuts import  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..utils.permissions import get_user_role
from ninja.errors import HttpError

class TicketService:

    @staticmethod
    def generate_reference():
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H:%M:%S")
        rand = random.randint(1000, 9999)
        return f"TCKT-{timestamp}-{rand}"

    @staticmethod
    def create_ticket(payload, request):
        data = payload.model_dump()
        key = [
                "erro",
                "falha",
                "bug",
                "crítico",
                "indisponível",
                "não funciona"
        ]
        data["status"] = Ticket.Status.OPEN
        data["priority"] = Ticket.Priority.MEDIUM
        data["user"] = request.user
        
        titulo = data["title"].lower()
        if any(word in titulo for word in key):
            data["priority"] = Ticket.Priority.HIGH
            
        data["reference"] = TicketService.generate_reference()

        return Ticket.objects.create(**data)
    
    @staticmethod
    def list_tickets(request, status: str = None, search: str = None, priority: str =None):
        
        role = get_user_role(request.user)
        
        if role in ["admin", "support"]:
            ticket = Ticket.objects.all()
        else:
            ticket = Ticket.objects.filter(user=request.user)

        ticket = ticket.order_by("-pk")

        if status:
            ticket = ticket.filter(status=status)
            
        if search:
            ticket = ticket.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(name__icontains=search))
        
        if priority:
            ticket = ticket.filter(priority=priority.upper())
    
        return ticket
    
    @staticmethod
    def get_by_reference(reference: str, user):
        ticket = get_object_or_404(Ticket, reference=reference)
        
        if user.groups.filter(name__in=["admin", "support"]).exists():
            return ticket

        if ticket.user != user:
            raise HttpError(403,"Not allowed")
    
        return ticket
    
    @staticmethod
    def update_ticket(payload, reference, user):
        ticket = get_object_or_404(Ticket, reference=reference)

        if not user.groups.filter(name__in=["admin", "support"]).exists():
            raise HttpError(403,"Not allowed")

        ticket.status = payload.status
        ticket.save()

        return ticket

class TicketServiceComments:
    
    @staticmethod
    def post_comment(reference: str, payload, user):
        ticket = get_object_or_404(Ticket, reference=reference)
        if not user.groups.filter(name__in=["admin", "support"]).exists() and ticket.user != user:
            raise HttpError(403,"Not allowed")

        comment = TicketComment.objects.create(
            ticket = ticket,
            author = payload.author,
            message = payload.message
        )
        return comment
    
    @staticmethod
    def list_comment(reference: str = None):
        ticket = get_object_or_404(Ticket, reference=reference)
        return ticket.comments.all()


class RegisterServices:
    
    @staticmethod
    def register(payload):
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password
        )
        return user