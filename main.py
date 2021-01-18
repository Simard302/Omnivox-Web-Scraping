import omnivox
import asyncio

async def main():
    username = input("What is your Omnivox username: ")
    password = input("What is your Omnivox password: ")
    session = await omnivox.login(username, password)
    if not session:
        return print('Login failed')

    #session.getClassNameList()
    leaSession = session.startLeaSession()
    leaSession.getAssignments()

class Omnivox:
    async def startSession(self, username, password):
        session = await omnivox.login(username, password)
        if not session:
            print('Login failed')
            return False
        return session

asyncio.run(main())