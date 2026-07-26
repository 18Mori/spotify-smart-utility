import time
from pycaw.pycaw import AudioUtilities

def get_audio_sessions():
    return AudioUtilities.GetAllSessions()

def monitor_audio():
    spot_initial_vol = 1.0  # tracks the normal volume
    ducked = False
    
    print("Monitoring audio sessions...")
    
    while True:
        sessions = get_audio_sessions() # listens fr all audio sessions
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
                
        time.sleep(0.5) # Poll every 0.5 seconds to reduce CPU usage

if __name__ == "__main__":
  monitor_audio()