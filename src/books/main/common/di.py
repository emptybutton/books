from dishka import AnyOf, Provider, Scope, provide
from in_memory_db import InMemoryDb

from books.application.create_book import CreateBook
from books.application.create_chapter import CreateChapter
from books.application.delete_book import DeleteBook
from books.application.delete_chapter import DeleteChapter
from books.application.edit_chapter import EditChapter
from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.book_views import BookViews
from books.application.ports.books import Books
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.application.ports.user_views import UserViews
from books.application.ports.users import Users
from books.application.sign_in import SignIn
from books.application.sign_out import SignOut
from books.application.sign_up import SignUp
from books.application.view_book_with_name import ViewBookWithName
from books.application.view_chapter import ViewChapter
from books.application.view_current_user import ViewCurrentUser
from books.application.view_user_with_name import ViewUserWithName
from books.entities.auth.password import PasswordHashes
from books.infrastructure.adapters.access_token_signing import (
    AccessTokenSigningToHS256JWT,
)
from books.infrastructure.adapters.books import InMemoryDbBooks
from books.infrastructure.adapters.clock import LocalHostClock
from books.infrastructure.adapters.map import MapToInMemoryDb
from books.infrastructure.adapters.password_hashes import (
    Pbkdf2HmacPasswordHashes,
)
from books.infrastructure.adapters.transaction import in_memory_db_transaction
from books.infrastructure.adapters.users import InMemoryDbUsers
from books.infrastructure.typenv.envs import Envs
from books.presentation.adapters.book_views import (
    BookSchemasAndChapterSchemasFromInMemoryDbAsBookViews,
)
from books.presentation.adapters.user_views import (
    UserSchemasFromInMemoryDbAsUserViews,
)
from books.presentation.fastapi.schemas.output import (
    BookSchema,
    ChapterSchema,
    UserSchema,
)


class CommonProvider(Provider):
    provide_envs = provide(source=Envs.load, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_db(self) -> InMemoryDb:
        db = InMemoryDb()
        db._snapshots = list()
        return db

    @provide(scope=Scope.APP)
    def provide_access_token_signing(
        self, envs: Envs
    ) -> AnyOf[AccessTokenSigningToHS256JWT, AccessTokenSigning[str]]:
        return AccessTokenSigningToHS256JWT(secret=envs.jwt_secret)

    provide_books = provide(
        InMemoryDbBooks,
        provides=AnyOf[InMemoryDbBooks, Books],
        scope=Scope.APP,
    )

    provide_users = provide(
        InMemoryDbUsers,
        provides=AnyOf[InMemoryDbUsers, Users],
        scope=Scope.APP,
    )

    provide_clock = provide(
        LocalHostClock,
        provides=AnyOf[LocalHostClock, Clock],
        scope=Scope.APP,
    )

    provide_map = provide(
        MapToInMemoryDb,
        provides=AnyOf[Map, MapToInMemoryDb],
        scope=Scope.APP,
    )

    @provide(scope=Scope.REQUEST)
    def provide_transaction(self, db: InMemoryDb) -> Transaction:
        return in_memory_db_transaction([db])

    provide_user_views = provide(
        UserSchemasFromInMemoryDbAsUserViews,
        provides=AnyOf[
            UserSchemasFromInMemoryDbAsUserViews, UserViews[UserSchema | None]
        ],
        scope=Scope.APP,
    )

    provide_book_views = provide(
        BookSchemasAndChapterSchemasFromInMemoryDbAsBookViews,
        provides=AnyOf[
            BookSchemasAndChapterSchemasFromInMemoryDbAsBookViews,
            BookViews[BookSchema | None, ChapterSchema | None],
        ],
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    def provide_password_hashes(self) -> AnyOf[
        Pbkdf2HmacPasswordHashes, PasswordHashes
    ]:
        return Pbkdf2HmacPasswordHashes(
            salt_lenght=32, iterations=10_000, hash_lenght=128
        )

    provide_create_book = provide(CreateBook[str], scope=Scope.REQUEST)
    provide_create_chapter = provide(CreateChapter[str], scope=Scope.REQUEST)
    provide_delete_book = provide(DeleteBook[str], scope=Scope.REQUEST)
    provide_delete_chapter = provide(DeleteChapter[str], scope=Scope.REQUEST)
    provide_edit_chapter = provide(EditChapter[str], scope=Scope.REQUEST)
    provide_sign_in = provide(SignIn[str], scope=Scope.REQUEST)
    provide_sign_out = provide(SignOut[str], scope=Scope.REQUEST)
    provide_sign_up = provide(SignUp[str], scope=Scope.REQUEST)
    provide_view_book_with_name = provide(
        ViewBookWithName[BookSchema | None, ChapterSchema | None],
        scope=Scope.REQUEST,
    )
    provide_view_chapter = provide(
        ViewChapter[BookSchema | None, ChapterSchema | None],
        scope=Scope.REQUEST,
    )
    provide_view_current_user = provide(
        ViewCurrentUser[str, UserSchema | None],
        scope=Scope.REQUEST,
    )
    provide_view_user_with_name = provide(
        ViewUserWithName[str, UserSchema | None],
        scope=Scope.REQUEST,
    )
