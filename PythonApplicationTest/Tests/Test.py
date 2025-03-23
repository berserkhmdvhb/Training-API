import asyncio
from datetime import datetime
'''
async def get_data():
    print("Fetching data...")
    await asyncio.sleep(3)  # Simulating delay
    print("Data received!")
    return "Success"


async def main():
    #tm_start = datetime.now()
    print("Start")
    #tm_pre_req = datetime.now()
    result = await get_data()    # Simulating delay (without await will be unexpected behavior)
    #tm_post_req = datetime.now()
    print("End\n")
    #print(f'Start Time: {tm_start}\nPre Req Time: {tm_pre_req}\nPost Req Time:{tm_post_req}\nDuration:{tm_post_req - tm_st art}')

asyncio.run(main())
'''

##############################################

from pydantic import BaseModel

# A model that accepts only certain fields
class UserInDB(BaseModel):
    username: str
    hashed_password: str

# Simulated incoming data that has an extra field "password"
incoming_data = {
    "username": "alice",
    "password": "plain-text-pass",
    "hashed_password": "supersecret123"
}

# Try to create the model with extra data
user = UserInDB(**incoming_data)

print(user)