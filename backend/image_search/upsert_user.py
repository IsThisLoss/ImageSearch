import asyncio
import getpass
import sys

from . import db
from . import auth


async def upsert_user(username: str, raw_password: str):
    hashed_password = auth.get_password_hash(raw_password)
    user_db = db.get_db().users
    await user_db.put(username, hashed_password)


async def main():
    if len(sys.argv) != 2 or not sys.argv[1]:
        print('Wrong usage, expected one positional argument: USERNAME')
        exit(1)
    username = sys.argv[1]
    raw_password = getpass.getpass()
    if not raw_password:
        print('Empty password, do nothing')
        exit(1)
    await upsert_user(username, raw_password)
    print(f'Done')
    

if __name__ == '__main__':
    asyncio.run(main())

