import asyncio
import os
import sys
from datetime import datetime, timezone
from telethon import TelegramClient, functions, types
from colorama import init, Fore, Style
from tqdm import tqdm
from config_handler import get_credentials

init(autoreset=True)

G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
B = Style.BRIGHT

def draw_logo():
    logo = f"""
{G}{B}          __      __  ____   _____  _____   
{G}{B}          \ \    / / / __ \ |_   _||  __ \  
{G}{B}           \ \  / / | |  | |  | |  | |  | | 
{G}{B}            \ \/ /  | |  | |  | |  | |  | | 
{G}{B}             \  /   | |__| | _| |_ | |__| | 
{G}{B}    ______    \/____ \____/ |_____||_____/  _______ 
{G}{B}   /  ____|  |__   __| / \    |  \/  |  |  __ \ 
{G}{B}   \___ \       | |   / ^ \   | \  / |  | |__) |
{G}{B}    ____) |     | |  / ___ \  | |\/| |  |  ___/ 
{G}{B}   |______/     |_| /_/   \_\ |_|  |_|  |_|     
    """
    print(logo)
    print(f"{G}{B} [>] VERSION: 3.4 | CODENAME: TABULA RASA")
    print(f"{G}{B} [>] KERNEL: STABLE DATA MODIFICATION ENGINE")
    print(f"{G}{B} " + "-"*52 + "\n")

async def run_voidstamp():
    creds = get_credentials()
    
    async with TelegramClient('void_session', creds['api_id'], creds['api_hash']) as client:
        os.system('cls' if os.name == 'nt' else 'clear')
        draw_logo()
        
        raw_date = input(f"{G}[INPUT_DATE_NODE]> (DD/MM/YYYY): ")
        try:
            target_date = datetime.strptime(raw_date, "%d/%m/%Y").replace(tzinfo=timezone.utc)
            current_limit = datetime.now(timezone.utc)
        except ValueError:
            print(f"{R}[ABORT] INVALID_TEMPORAL_DATA")
            return

        print(f"\n{Y}[TARGET_SELECTION]:")
        print(f"{G} 1. VIDEO_ROUNDS")
        print(f"{G} 2. VOICE_DATA")
        print(f"{G} 3. TEXT_TRAFFIC")
        print(f"{G} 4. FULL_ERASURE")
        print(f"{G} 5. INACTIVE_NODES (30+ DAYS)")
        
        mode = input(f"\n{G}[SELECT_TARGET]> ")

        print(f"\n{G}[SYSTEM] FETCHING DIALOGS...")
        dialogs = await client.get_dialogs()
        
        print(f"{G}[SYSTEM] INITIALIZING DATA OVERWRITE...\n")
        
        for dialog in tqdm(dialogs, desc=f"{G}TOTAL_PROGRESS", unit="chat", bar_format="{l_bar}{bar}{r_bar}", colour="green"):
            try:
                if mode == '5':
                    if dialog.date and (current_limit - dialog.date).days > 30:
                        try:
                            await client.delete_dialog(dialog.id, revoke=True)
                        except Exception:
                            continue
                    continue

                if dialog.is_channel and not (getattr(dialog.entity, 'creator', False) or getattr(dialog.entity, 'admin_rights', None)):
                    continue

                payload = []
                async for msg in client.iter_messages(dialog.id, offset_date=current_limit):
                    if msg.date < target_date:
                        break
                    
                    if not msg.out:
                        continue

                    match = False
                    if mode == '1':
                        if msg.video and getattr(msg.video, 'round_message', False):
                            match = True
                    elif mode == '2':
                        if msg.voice:
                            match = True
                    elif mode == '3':
                        if msg.text and not msg.media:
                            match = True
                    elif mode == '4':
                        match = True

                    if match:
                        payload.append(msg.id)

                if payload:
                    await client.delete_messages(dialog.id, payload, revoke=True)
                    await asyncio.sleep(0.2)

            except Exception:
                continue

        print(f"\n{G}{B}[SUCCESS] VOIDSTAMP COMPLETE. ALL TRACES NULLIFIED.")

if __name__ == '__main__':
    try:
        asyncio.run(run_voidstamp())
    except KeyboardInterrupt:
        print(f"\n{R}[HALT] EMERGENCY DISCONNECT.")
