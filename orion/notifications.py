from notifications.models import Notification


def get_notificacoes_nao_lidas(user):
    notificacoes_nao_lidas = Notification.objects.unread().filter(recipient = user)
    #quantidade = notificacoes_nao_lidas.count()
    return notificacoes_nao_lidas

def get_numero_notificacoes_nao_lidas(user):
    return get_notificacoes_nao_lidas(user).count()