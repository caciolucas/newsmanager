from django.db import transaction
from django.utils import timezone

from news.models import NewsPost
from newsmanager.celery import app

#! NOTE: Para simplicidade, poderíamos somente filtrar na viewset os posts com published_at <= now
#! e status = "scheduled", mas para fins de demonstração, vamos criar uma task que faz essa verificação


#! NOTE: Poderia trigar a task com celery ETA, mas poderia acumular muitas tasks agendadas em memória


@app.task
def publish_pending_news():
    now = timezone.now()
    pending_news = NewsPost.objects.filter(
        published_at__lte=now, status=NewsPost.SCHEDULED
    )
    count = pending_news.count()
    pending_news.update(status=NewsPost.PUBLISHED)
    return {"message": "News published successfully", "count": count}


@app.task
def test_task():
    return {"message": "Test task executed successfully"}
