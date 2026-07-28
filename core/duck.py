import time, threading
from pycaw.pycaw import AudioUtilities

def get_audio_sessions():
    return AudioUtilities.GetAllSessions()

def restore_volume(initial_vol):
    # Restore Spotify volume to the initial volume on exit
    try:
        for session in get_audio_sessions():
            if session.Process and "spotify.exe" in session.Process.name().lower():
                volume_control = session.SimpleAudioVolume
                volume_control.SetMasterVolume(initial_vol, None)
                print(f"Spotify volume restored to {initial_vol}.")
                break
    except Exception as e:
        print(f"Error restoring volume on exit: {e}")

def monitor_audio(stop_event=None):
    spot_initial_vol = 1.0  # tracks the normal volume
    ducked = False
    
    print("Monitoring audio sessions...")
    
    try:
        while not (stop_event and stop_event.is_set()):
            sessions = get_audio_sessions() # gets all audio sessions
            spot_session = None
            other_active_audio = False
            # Loop through all audio sessions to find Spotify and check for other active audio
            for session in sessions:
                if session.Process:
                    process_name = session.Process.name().lower()
                    # Check if the session is Spotify or another app playing audio -- it's important to check for other apps first to avoid ducking Spotify when it's the only one playing. It's the key to avoid a feedback loop where Spotify ducks itself.
                    if "spotify.exe" in process_name:
                        spot_session = session
                    elif session.State == 1: # Active session audio --
                        other_active_audio = True

            if spot_session:
                volume_control = spot_session.SimpleAudioVolume
                
                if other_active_audio and not ducked:
                    # Save current volume and duck it to 15%
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
                    
            if stop_event:
                if stop_event.is_set(): # Check if the stop event is set to exit the loop
                    break
                else:
                    time.sleep(0.5)  # it breaks out immediately when the event is set rather than waiting out the sleep timer
    except KeyboardInterrupt:
        print("\nAudio monitoring STOPPED...!")
        
    finally:
        if ducked:
            restore_volume(spot_initial_vol) # Restore Spotify volume to the initial volume on exit

if __name__ == "__main__":
    monitor_audio()
    
    stop_event = threading.Event()