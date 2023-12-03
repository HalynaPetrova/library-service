from rest_framework import routers

from book.views import BookViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("books", BookViewSet)


urlpatterns = router.urls

app_name = "book"
