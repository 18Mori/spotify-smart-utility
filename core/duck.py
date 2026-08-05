import logging, os, threading, pythoncom
from pycaw.pycaw import AudioUtilities

# Configure logger instance for this module
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
CONFIG_FILE = os.path.join(os.path.dirname(BASE_DIR), "ignored_apps.txt") # defines the path to the configuration file for ignored apps

def excluded_apps():
    ignored = set() # Read ignored apps from the configuration file
    if os.path.exists(CONFIG_FILE): # Check if the configuration file exists
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8")  as f:
                for line in f:
                    line = line.strip().lower()
                    # Ignore empty lines and comment lines starting with '#'
                    if line and not line.startswith("#"):
                        ignored.add(line)
            logger.info("Loaded ignored apps from %s: %s", CONFIG_FILE, ", ".join(ignored))
        except Exception as e:
            logger.warning("Could not read %s: %s", CONFIG_FILE, e)
    else:
        logger.warning("Configuration file %s not found. No apps will be ignored.", CONFIG_FILE)
    return ignored # Return the set of ignored app names

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
        
    spot_initial_vol = 1.0  # tracks the normal volume
    ducked = False
    
    logger.info("Monitoring audio sessions...")
    
    try:
        while not stop_event.is_set():
            sessions = get_audio_sessions() # gets all audio sessions
            spot_session = None
            apps_trigger_active = []  # List to track other apps playing audio
            # Loop through (Inspect) all audio sessions to find Spotify and check for other active audio
            for session in sessions:
                try:
                    if session.Process:
                        process_name = session.Process.name().lower()
                        """Check if the session is Spotify or another app playing audio -- it's important to check for other apps first to avoid ducking Spotify when it's the only one playing. It's the key to avoid a feedback loop where Spotify ducks itself."""
                        if "spotify.exe" in process_name:
                            spot_session = session
                        elif process_name in excluded_apps():
                            continue  # Skip ignored apps
                        elif session.State == 1: # Active session audio -- actively playing
                            is_ignored = any(ignored_app in process_name for ignored_app in excluded_apps()) # Check if the process name contains any ignored app names
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
                        print(f"Audio detected from [{app_name}]. Spotify ducked to 15%.")
                            
                    elif not apps_trigger_active and ducked:
                        # Restore original volume
                        volume_control.SetMasterVolume(spot_initial_vol, None)
                        ducked = False
                        logger.info("Spotify volume restored to %.0f%%.", spot_initial_vol * 100)
                        print(f"Spotify volume restored to {spot_initial_vol * 100:.0f}%.")
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