from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from relays.models import Message, Server


@login_required
@permission_required('relays.basic_access')
def index(request):

    context = {
        "servers": Server.objects.all().order_by("-users")
    }
    try:
        # AA 4.x
        return render(request, 'relays/index-bs5.html', context)
    except TemplateDoesNotExist:
        # AA 3.x
        return render(request, 'relays/index.html', context)


@login_required
@permission_required("bountyboard.basic_access")
def server(request: WSGIRequest, server: int) -> HttpResponse:
    """
    A relayed Server
    :param request:
    :return:
    """
    context = {}
    context['server'] = Server.objects.get(server=server)

    try:
        # AA 4.x
        return render(request, "relays/server-bs5.html", context)
    except TemplateDoesNotExist:
        # AA 3.x
        return render(request, "relays/server.html", context)


@login_required
@permission_required('relays.basic_access')
def server_messages(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # is_ajax
        server_id = request.GET.get('server_id', None)
    else:
        server_id = None

    server_messages_qs = Message.objects.filter(
        channel__server_id=server_id
    ).values(
        'timestamp',
        'channel__name',
        'author_nick',
        'content',
    )

    return JsonResponse({"server_messages": list(server_messages_qs)})
