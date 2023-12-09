from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PlaylistCreationRequest:
    user_id: str
    name: str
    description: str
    public: bool

    def to_payload(self) -> dict:
        return {k: v for k, v in self.to_dict() if k != "user_id"}
