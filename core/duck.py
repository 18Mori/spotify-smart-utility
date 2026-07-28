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
                print(f"Spotify volume restored to {initial_vol * 100:.0f}%.")
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
            other_active_audio = False
            # Loop through (Inspect) all audio sessions to find Spotify and check for other active audio
            for session in sessions:
                try:
                    if session.Process:
                        process_name = session.Process.name().lower()
                        """Check if the session is Spotify or another app playing audio -- it's important to check for other apps first to avoid ducking Spotify when it's the only one playing. It's the key to avoid a feedback loop where Spotify ducks itself."""
                        if "spotify.exe" in process_name:
                            spot_session = session
                        elif session.State == 1: # Active session audio -- actively playing
                            other_active_audio = True
                except Exception:
                    continue

            if spot_session:
                try:
                    volume_control = spot_session.SimpleAudioVolume
                    
                    if other_active_audio and not ducked:
                        spot_initial_vol = volume_control.GetMasterVolume()
                        # Ensure we don't accidentally save an already ducked state as normal.
                        if spot_initial_vol > 0.0: 
                            volume_control.SetMasterVolume(0.15, None)
                            ducked = True
                            print("Spotify ducked to 15%.")
                            
                    elif not other_active_audio and ducked:
                        # Restore original volume
                        volume_control.SetMasterVolume(spot_initial_vol, None)
                        ducked = False
                        print("Spotify volume restored.")
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