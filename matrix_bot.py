import os
import asyncio
from dotenv import load_dotenv
from nio import AsyncClient, RoomMessageText, RoomCreateError

# Load environment variables from .env file
load_dotenv()

# Matrix configuration
homeserver = os.getenv("MATRIX_HOMESERVER")
access_token = os.getenv("MATRIX_ACCESS_TOKEN")
room_ids = os.getenv("MATRIX_ROOM_IDS")

if not all([homeserver, access_token, room_ids]):
    raise ValueError("MATRIX_HOMESERVER, MATRIX_ACCESS_TOKEN, and MATRIX_ROOM_IDS must be set in the .env file")

# Split the room_ids into a list
room_ids = room_ids.split(',')

class MatrixBot:
    def __init__(self, homeserver, access_token, room_ids):
        self.homeserver = homeserver
        self.access_token = access_token
        self.room_ids = room_ids
        self.client = AsyncClient(homeserver, access_token=access_token)

    async def join_room(self, room_id):
        try:
            await self.client.join(room_id)
            print(f"Joined room {room_id}")
        except Exception as e:
            print(f"Failed to join room {room_id}: {e}")

    async def invite_new_user(self, room_id, event):
        if event.sender == self.client.user_id:
            return

        username = event.sender
        display_name = await self.get_display_name(username)
        if display_name:
            username_parts = display_name.split()
            first_name = username_parts[0]
            last_initial = username_parts[1][0] if len(username_parts) > 1 else ''
            new_username = f"{first_name.lower()}-{last_initial.lower()}" if last_initial else first_name.lower()
        else:
            new_username = username.split(":")[0].split("_")[1]

        print(f"Creating new user with username: {new_username}")
        new_password = generate_password()

        # Create user using the existing authentik-creation-workflow.py functionality
        create_user_result = os.system(f"python3 authentik-creation-workflow.py create {new_username}")

        if create_user_result != 0:
            print(f"Failed to create user {new_username}")
            return

        try:
            # Create a new room to message the user
            response = await self.client.room_create(
                invite=[username],
                name="Welcome Room",
                topic="Your IrregularChat account information"
            )
            welcome_room_id = response.room_id

            # Send the account information to the user in the new room
            welcome_message = f"""
            Welcome to IrregularChat!

            Your account has been created with the following credentials:
            Username: {new_username}
            Password: {new_password}

            You can login at https://sso.irregularchat.com/
            """
            await self.client.room_send(
                room_id=welcome_room_id,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": welcome_message}
            )
            print(f"Sent welcome message to {username} in room {welcome_room_id}")
        except RoomCreateError as e:
            print(f"Failed to create room to message user: {e}")

    async def get_display_name(self, user_id):
        try:
            response = await self.client.get_displayname(user_id)
            return response.displayname
        except Exception as e:
            print(f"Failed to get display name for user {user_id}: {e}")
            return None

    async def main(self):
        for room_id in self.room_ids:
            await self.join_room(room_id)

        @self.client.event_callback(RoomMessageText)
        async def on_message(room: Room, event: RoomMessageText):
            await self.invite_new_user(room.room_id, event)

        await self.client.sync_forever(timeout=30000, full_state=True)

async def run_bot():
    bot = MatrixBot(
        homeserver=homeserver,
        access_token=access_token,
        room_ids=room_ids
    )
    while True:
        try:
            await bot.main()
        except Exception as e:
            print(f"Bot encountered an error: {e}. Restarting...")
            await asyncio.sleep(5)  # Wait for a few seconds before restarting

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run_bot())