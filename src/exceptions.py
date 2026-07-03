class MarketMockError(Exception):
    """Служи като базова грешка за целия проект."""
    pass

class InsufficientFundsError(MarketMockError):
    """Хвърли грешка, когато няма достатъчно пари за покупка."""
    
    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        self.message = f"Нямаш достатъчно пари! Трябват ти {required:.2f}, а имаш само {available:.2f}."
        super().__init__(self.message)

class InvalidDataError(MarketMockError):
    """Хвърли грешка, когато редът в данните е счупен."""
    
    def __init__(self, row: dict, reason: str):
        self.row = row
        self.reason = reason
        self.message = f"Счупени данни: {reason}. Редът е: {row}"
        super().__init__(self.message)