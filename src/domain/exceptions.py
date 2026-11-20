class DomainError(Exception): pass`n`nclass ValidationError(DomainError): pass`n`nclass EntityNotFoundError(DomainError): pass
