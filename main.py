import omnivox
import asyncio

async def main():
    username = input("What is your Omnivox username: ")
    password = input("What is your Omnivox password: ")
    session = await omnivox.login(username, password)
    if not session:
        return print('Login failed')

    leaSession = session.startLeaSession()
    leaSession.getAssignments()

asyncio.run(main())