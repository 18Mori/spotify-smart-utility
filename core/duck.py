import logging, os, threading, pythoncom
from pycaw.pycaw import AudioUtilities
from core.config import ConfigManager

# Configure logger instance for this module
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
CONFIG_FILE = os.path.join(os.path.dirname(BASE_DIR), "ignored_apps.txt") # defines the path to the configuration file for ignored apps


def get_audio_sessions():
    # fetches all active audio sessions
    try:
        return AudioUtilities.GetAllSessions()
    except Exception as e:
        logger.error("Error fetching audio sessions: %s", e)
        return []


def restore_volume(initial_vol):
    # Restore Spotify volume to the initial volume on exit
    try:
        for session in get_audio_sessions():
            if session.Process and "spotify.exe" in session.Process.name().lower():
                session.SimpleAudioVolume.SetMasterVolume(initial_vol, None)
                logger.info("Spotify volume restored to %.0f%% on exit.", initial_vol * 100)
                break
    except Exception as e:
        logger.error("Error restoring volume on exit: %s", e)

def monitor_audio(stop_event=None):
    # Initialize COM library for this specific thread
    pythoncom.CoInitialize()
    
    if stop_event is None:
        stop_event = threading.Event()
        
    config_manager = ConfigManager() # Initialize the ConfigManager to manage ignored apps
        
    spot_initial_vol = 1.0  # tracks the normal volume
    ducked = False
    
    logger.info("Monitoring audio sessions...")
    
    try:
        while not stop_event.is_set():
            ignored_apps = config_manager.load_ignored_apps() # Load the list of ignored apps from the configuration file (auto reloads if file changes)
            
            sessions = get_audio_sessions() # gets all audio sessions
            spot_session = None
            apps_trigger_active = []  # List to track other apps playing audio
            # Loop through (Inspect) all audio sessions to find Spotify and check for other active audio
            for session in sessions:
                try:
                    if session.Process:
                        process_name = session.Process.name().lower()
                        if "spotify.exe" in process_name:
                            spot_session = session
                        elif process_name in ignored_apps:
                            continue  # Skip ignored apps
                        elif session.State == 1: # Active session audio -- actively playing
                            is_ignored = any(ignored_app in process_name for ignored_app in ignored_apps) # Check if the process name contains any ignored app names
                            if not is_ignored:
                                apps_trigger_active.append(process_name)
                except Exception:
                    continue

            if spot_session:
                try:
                    volume_control = spot_session.SimpleAudioVolume
                    current_vol = volume_control.GetMasterVolume()
                    
                    if apps_trigger_active and not ducked:
                        if current_vol > 0.15:  # it only ducks, if the current volume is above 15%
                            spot_initial_vol = current_vol
                        
                        volume_control.SetMasterVolume(0.15, None)
                        ducked = True
                        app_name = ", ".join(set(apps_trigger_active))
                        logger.info("Audio detected from [%s]. Spotify ducked to 15%%.", app_name)
                            
                    elif not apps_trigger_active and ducked:
                        # Restore original volume
                        volume_control.SetMasterVolume(spot_initial_vol, None)
                        ducked = False
                        logger.info("Spotify volume restored to %.0f%%.", spot_initial_vol * 100)
                except Exception as e:
                    logger.error("Error adjusting Spotify volume: %s", e)
                    
            if stop_event.wait(timeout=0.5): # Wait for 0.5 seconds or until the stop_event is set -- checks for stop signal
                break
    except KeyboardInterrupt:
        logger.info("Audio monitoring STOPPED...!")
        
    finally:
        if ducked:
            restore_volume(spot_initial_vol) # Restore Spotify volume to the initial volume on exit
            # Clean up COM resources on thread exit
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    monitor_audio()