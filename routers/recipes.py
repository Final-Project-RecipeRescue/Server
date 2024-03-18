from fastapi import APIRouter

router = APIRouter(prefix='/drones')
# drone_service = DronesService(collection_drones)

@router.get("/")
async def get_drones():
    # drones = await drone_service.get_all()
    # if not drones:
    #     raise HTTPException(status_code=404, detail="No missions found")
    # return drones
    return

# Endpoint to get all drones by availability status
@router.get("/findByStatus/{status}")
async def get_drones_by_status(status):
    # drones = await drone_service.get_drones_by_status(status)
    # if not drones:
    #     raise HTTPException(status_code=404, detail=f"No drones found with status {status}")
    # return drones
    return
