

class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return 'An application error occurred'


class ToClientException(ApplicationException):
    ...


class CommitError(ApplicationException):
    @property
    def message(self):
        return 'Error while trying commit'


class RollbackError(ApplicationException):
    @property
    def message(self):
        return 'Error while trying rollback'


class RepoError(ApplicationException):
    error: str

    @property
    def message(self) -> str:
        return f'Repository error: {self.error}'
