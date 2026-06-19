from ninja import Router
from ..shemas.user_shemas import TicketSchemaIn, TicketSchemaOut, TicketStatusOut, TicketStatusIn, TicketCommentOut, TicketCommentIn, UserIN, UserOut
from ..services.user_service import TicketService, TicketServiceComments, RegisterServices
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

router = Router()

@router.post('tickets', response=TicketSchemaOut, auth=JWTAuth())
def create_ticket(request, payload: TicketSchemaIn):
    return TicketService.create_ticket(payload,request)

@router.get('tickets/', response=list[TicketSchemaOut], auth=JWTAuth())
@paginate
def list_tickets(request, status: str = None, search: str = None, priority: str = None):
    return TicketService.list_tickets(request, status, search, priority)

@router.get("tickets/{reference}", response=TicketSchemaOut, auth=JWTAuth())
def get_by_reference(request, reference: str):
    return TicketService.get_by_reference(reference,request.user)

@router.patch("tickets/{reference}/status", response=TicketStatusOut, auth=JWTAuth())
def update_ticket(request, reference: str, payload:TicketStatusIn):
    return TicketService.update_ticket(payload, reference, request.user)

#Tickets Comments routes ------>

@router.post('/tickets/{reference}/comments', response=TicketCommentOut, auth=JWTAuth())
def post_comments(request, payload: TicketCommentIn, reference: str):
    return TicketServiceComments.post_comment(reference, payload, request.user)

@router.get('/tickets/{reference}/comments', response=list[TicketCommentOut], auth=JWTAuth())
def list_comments(request, reference: str):
    return TicketServiceComments.list_comment(reference)

#Register route ------>

@router.post("register", response=UserOut)
def register_user(request, payload: UserIN):
    return RegisterServices.register(payload)