from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Agent, AgentRun
from app.schemas.all_schemas import AgentResponse, AgentRunRequest, AgentRunResponse
from app.services.agent_orchestrator import execute_agent
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/agents", tags=["AI Autonomous Agents"])


@router.get("", response_model=List[AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Agent))
    return res.scalars().all()


@router.post("/{name}/run", response_model=AgentRunResponse)
async def run_agent_task(
    name: str,
    req: AgentRunRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        run = await execute_agent(db, agent_name=name, input_payload=req.input_payload)
        return {
            "run_id": run.id,
            "agent_name": name,
            "status": run.status,
            "output_payload": run.output_payload,
            "error_message": run.error_message,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
