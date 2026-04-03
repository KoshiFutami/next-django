"""ドメイン例外（インフラやフレームワークに依存しない）。"""


class DomainError(Exception):
    """ドメインルール違反の基底。"""


class DomainValidationError(DomainError):
    """入力や状態が不変条件を満たさない。"""


class EmailAlreadyRegisteredError(DomainError):
    """同じメールアドレスで既に利用者が登録されている。"""


class HandleAlreadyRegisteredError(DomainError):
    """同じハンドルで既に利用者が登録されている。"""
