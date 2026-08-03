import threading
import pythoncom
from pycaw.pycaw import AudioUtilities

def get_audio_sessions():
    # fetches all active audio sessions
    try:
        return AudioUtilities.GetAllSessions()
    except Exception as e:
        print(f"Error fetching audio sessions: {e}")
        return []

def restore_volume(initial_vol):
    # Restore Spotify volume to the initial volume on exit
    try:
        for session in get_audio_sessions():
            if session.Process and "spotify.exe" in session.Process.name().lower():
                session.SimpleAudioVolume.SetMasterVolume(initial_vol, None)
                print(f"Spotify volume restored to {initial_vol * 100:.0f}% on exit.")
                break
    except Exception as e:
        print(f"Error restoring volume on exit: {e}")

def monitor_audio(stop_event=None):
    # Initialize COM library for this specific thread
    pythoncom.CoInitialize()
    
    if stop_event is None:
        stop_event = threading.Event()
        
    spot_initial_vol = 1.0  # tracks the normal volume
    ducked = False
    
    print("Monitoring audio sessions...")
    
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
                        elif session.State == 1: # Active session audio -- actively playing
                            apps_trigger_active.append(session.Process.name())
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
                        print(f"Audio detected from [{app_name}]. Spotify ducked to 15%.")
                            
                    elif not apps_trigger_active and ducked:
                        # Restore original volume
                        volume_control.SetMasterVolume(spot_initial_vol, None)
                        ducked = False
                        print(f"Spotify volume restored to {spot_initial_vol * 100:.0f}%.")
                except Exception as e:
                    print(f"Error adjusting Spotify volume: {e}")
                    
            if stop_event.wait(timeout=0.5): # Wait for 0.5 seconds or until the stop_event is set -- checks for stop signal
                break
    except KeyboardInterrupt:
        print("\nAudio monitoring STOPPED...!")
        
    finally:
        if ducked:
            restore_volume(spot_initial_vol) # Restore Spotify volume to the initial volume on exit
            # Clean up COM resources on thread exit
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    monitor_audio()