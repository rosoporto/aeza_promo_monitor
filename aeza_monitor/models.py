from dataclasses import asdict, dataclass


@dataclass
class PromoData:
    found: bool
    location: str | None = None
    name: str | None = None
    plan_code: str | None = None
    price: str | None = None
    cpu: str | None = None
    ram: str | None = None
    disk: str | None = None
    bandwidth: str | None = None
    ipv4: str | None = None
    ipv6: str | None = None
    order_link: str | None = None
    reason: str | None = None

    def signature(self) -> tuple[str | None, str | None, str | None]:
        return (self.location, self.plan_code, self.price)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict | None) -> "PromoData | None":
        if not data:
            return None
        return cls(**data)


@dataclass
class NotificationState:
    last_notified: PromoData | None = None

    def to_dict(self) -> dict:
        return {
            "last_notified": self.last_notified.to_dict() if self.last_notified else None,
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "NotificationState":
        if not data:
            return cls()
        return cls(last_notified=PromoData.from_dict(data.get("last_notified")))
