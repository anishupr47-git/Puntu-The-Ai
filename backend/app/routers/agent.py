from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import AgentRequest, AgentResponse
from ..services.agent_router import route_skill, handle_skill
from ..models import ModuleLog


router = APIRouter()


@router.post('/route', response_model=AgentResponse)
async def route(req: AgentRequest, db: Session = Depends(get_db)):
    skill = route_skill(req.message, req.skill, req.mode)
    result = await handle_skill(skill, req.message, req.context, db=db)

    log = ModuleLog(
        user_id=req.user_id,
        module=skill,
        input={'message': req.message, 'mode': req.mode},
        output={'result': result} if isinstance(result, dict) else {'text': str(result)},
    )
    db.add(log)
    db.commit()

    return AgentResponse(skill=skill, result=result)
