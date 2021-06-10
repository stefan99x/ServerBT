from pydantic import BaseModel

class BodyPart(BaseModel):
    id: tes
    name: str


    def to_json(self):
        return jsonable