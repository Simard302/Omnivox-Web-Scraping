import asyncio
from OmnivoxSession import OmnivoxSession

async def main():
    username = input("What is your Omnivox username: ")
    password = input("What is your Omnivox password: ")
    session = OmnivoxSession("jac", username, password)
    session = await session.login()
    if not session:
        return print('Login failed')

    #session.getClassNameList()
    leaSession = session.startLeaSession()
    leaSession.getAssignments()

asyncio.run(main())