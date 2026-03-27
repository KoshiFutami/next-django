"""ドメイン例外（インフラやフレームワークに依存しない）。"""


class DomainError(Exception):
    """ドメインルール違反の基底。"""


class DomainValidationError(DomainError):
    """入力や状態が不変条件を満たさない。"""
