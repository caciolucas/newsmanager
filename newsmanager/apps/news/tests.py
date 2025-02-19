from authentication.models import User
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from news.models import NewsPost, NewsVerticals


class NewsPostViewSetTest(APITestCase):
    fixtures = [
        "test_data",
    ]

    def setUp(self):
        self.client = APIClient()

        NewsPost.objects.all().delete()
        editor_group = Group.objects.get(name="Editor")
        editor_group.permissions.set(
            Permission.objects.filter(
                codename__contains="newspost", content_type__app_label="news"
            )
        )

        # Recupera os usuários criados nas fixtures
        self.admin = User.objects.get(username="admin")
        self.editor_john = User.objects.get(username="john_editor")
        self.editor_jane = User.objects.get(username="jane_editor")
        self.regular_peter = User.objects.get(username="peter_p")
        self.regular_bruce = User.objects.get(
            username="bruce_w"
        )  # Possui inscrição ativa no plano “Jota Info”

        # Recupera algumas verticais
        self.vertical_tributos = NewsVerticals.objects.get(
            pk="defce85b-2216-4dbc-a8a8-055369ba431c"
        )
        self.vertical_energia = NewsVerticals.objects.get(
            pk="6d576e3e-ce74-4ae7-8378-aebc0ba43965"
        )
        self.vertical_poder = NewsVerticals.objects.get(
            pk="5b27c185-d8a2-4f68-93c7-61950308dbe0"
        )

        # Cria notícias para teste:

        # Notícia criada pelo editor John – associada a “Tributos”
        self.news_post_editor = NewsPost.objects.create(
            title="Post by John",
            sub_title="Subtítulo John",
            content="Conteúdo do post do John",
            author=self.editor_john,
            published_at=timezone.now(),
        )
        self.news_post_editor.verticals.add(self.vertical_tributos)
        self.news_post_editor.tags.set(
            ["dolore"]
        )  # considerando que o campo espera lista de strings

        # Notícia criada pelo editor Jane – associada a “Poder” (não está na inscrição do Bruce)
        self.news_post_editor2 = NewsPost.objects.create(
            title="Post by Jane",
            sub_title="Subtítulo Jane",
            content="Conteúdo do post da Jane",
            author=self.editor_jane,
            published_at=timezone.now(),
        )
        self.news_post_editor2.verticals.add(self.vertical_poder)
        self.news_post_editor2.tags.set(["mollit"])

        # Notícia criada pelo admin – associada a “Energia”
        self.news_post_admin = NewsPost.objects.create(
            title="Admin Post",
            sub_title="Subtítulo Admin",
            content="Conteúdo do post do admin",
            author=self.admin,
            published_at=timezone.now(),
        )
        self.news_post_admin.verticals.add(self.vertical_energia)
        self.news_post_admin.tags.set(["consectetur"])

    # ---------------------------
    # Testes de list e retrieve
    # ---------------------------
    def test_list_newsposts_regular_user(self):
        """
        Usuário regular deve ver somente as notícias cuja vertical esteja ativa
        na inscrição (no exemplo, o Bruce tem inscrição para “Tributos” e “Energia”).
        """
        self.client.force_authenticate(user=self.regular_bruce)
        url = reverse("news-posts-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Espera-se que o Bruce veja a notícia do John (Tributos) e a do Admin (Energia)
        data = response.data["results"]

        self.assertEqual(len(data), 2)
        titles = [item["title"] for item in data]

        self.assertIn("Post by John", titles)
        self.assertIn("Admin Post", titles)
        self.assertNotIn("Post by Jane", titles)

    def test_retrieve_newspost_regular_user_allowed(self):
        """
        Usuário regular consegue recuperar uma notícia cuja vertical esteja ativa na inscrição.
        """
        self.client.force_authenticate(user=self.regular_bruce)
        url = reverse("news-posts-detail", args=[self.news_post_admin.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Admin Post")

    def test_retrieve_newspost_regular_user_forbidden(self):
        """
        Usuário regular não consegue recuperar uma notícia cuja vertical não esteja ativa na inscrição.
        """
        self.client.force_authenticate(user=self.regular_bruce)
        url = reverse("news-posts-detail", args=[self.news_post_editor2.pk])
        response = self.client.get(url)
        # Notícia não disponível para o usuário regular, pois não corresponde à inscrição ativa
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_unauthenticated(self):
        """
        Usuário não autenticado não deve acessar a listagem.
        """
        self.client.force_authenticate(user=None)
        url = reverse("news-posts-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------
    # Testes de criação
    # ---------------------------
    def test_create_newspost_admin(self):
        """
        Usuário admin pode criar uma notícia.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("news-posts-list")
        data = {
            "title": "Admin created post",
            "sub_title": "Subtítulo do post do admin",
            "content": "Conteúdo do post criado pelo admin",
            "tags": ["admin", "news"],
            "published_at": timezone.now().isoformat(),
            "verticals": [self.vertical_energia.pk],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # O autor deve ser automaticamente definido como o usuário autenticado (admin)
        self.assertEqual(response.data["author"]["id"], str(self.admin.pk))

    def test_create_newspost_editor(self):
        """
        Usuário editor pode criar uma notícia (o autor será definido automaticamente).
        """
        self.client.force_authenticate(user=self.editor_john)
        url = reverse("news-posts-list")
        data = {
            "title": "Editor created post",
            "sub_title": "Subtítulo do post do editor",
            "content": "Conteúdo do post criado pelo editor",
            "tags": ["editor", "news"],
            "published_at": timezone.now().isoformat(),
            "verticals": [self.vertical_tributos.pk],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"]["id"], str(self.editor_john.pk))

    def test_create_newspost_regular_user_forbidden(self):
        """
        Usuário regular, sem a permissão "news.add_newspost", não pode criar uma notícia.
        """
        self.client.force_authenticate(user=self.regular_peter)
        url = reverse("news-posts-list")
        data = {
            "title": "Regular user post",
            "sub_title": "Subtítulo do post do regular",
            "content": "Conteúdo do post criado pelo regular",
            "tags": ["regular"],
            "published_at": timezone.now().isoformat(),
            "verticals": [self.vertical_energia.pk],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------------
    # Testes de atualização (update/patch)
    # ---------------------------
    def test_update_newspost_editor_own(self):
        """
        Usuário editor pode atualizar sua própria notícia.
        """
        self.client.force_authenticate(user=self.editor_john)
        url = reverse("news-posts-detail", args=[self.news_post_editor.pk])
        data = {
            "title": "Updated title by John",
            "sub_title": self.news_post_editor.sub_title,
            "content": "Conteúdo atualizado do post do John",
            "tags": ["updated", "john"],
            "published_at": self.news_post_editor.published_at.isoformat(),
            "verticals": [self.vertical_tributos.pk],
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated title by John")

    def test_update_newspost_editor_not_owner(self):
        """
        Usuário editor não pode atualizar notícia de outro editor.
        """
        self.client.force_authenticate(user=self.editor_john)
        url = reverse("news-posts-detail", args=[self.news_post_editor2.pk])
        data = {
            "title": "Tentativa de update malicioso",
            "sub_title": self.news_post_editor2.sub_title,
            "content": self.news_post_editor2.content,
            "tags": ["malicious"],
            "published_at": self.news_post_editor2.published_at.isoformat(),
            "verticals": [self.vertical_poder.pk],
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_newspost_admin(self):
        """
        Usuário admin pode atualizar qualquer notícia.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("news-posts-detail", args=[self.news_post_editor2.pk])
        data = {
            "title": "Admin updated title",
            "sub_title": self.news_post_editor2.sub_title,
            "content": "Conteúdo atualizado pelo admin",
            "tags": ["admin", "update"],
            "published_at": self.news_post_editor2.published_at.isoformat(),
            "verticals": [self.vertical_poder.pk],
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Admin updated title")

    # ---------------------------
    # Testes de deleção
    # ---------------------------
    def test_delete_newspost_editor_own(self):
        """
        Usuário editor pode deletar sua própria notícia.
        """
        self.client.force_authenticate(user=self.editor_jane)
        url = reverse("news-posts-detail", args=[self.news_post_editor2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_newspost_editor_not_owner(self):
        """
        Usuário editor não pode deletar notícia de outro editor.
        """
        self.client.force_authenticate(user=self.editor_john)
        url = reverse("news-posts-detail", args=[self.news_post_editor2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_newspost_admin(self):
        """
        Usuário admin pode deletar qualquer notícia.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse("news-posts-detail", args=[self.news_post_editor.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
