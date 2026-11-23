"""
===============================================================================
MUSIC PLAYER — CLASS BLUEPRINT
===============================================================================
1. Domain Models
   - Song (frozen dataclass)
       Attributes: song_id: str, title: str, artist: str, duration_sec: int
   - Playlist (dataclass)
       Attributes: playlist_id: str, name: str, songs: List[Song]
       Methods:    add_song(song), remove_song(song_id)

2. Strategy Pattern — Playback Ordering
   - PlaybackStrategy (ABC)
       Methods:    get_next_index(current_index, total_tracks),
                   get_prev_index(current_index, total_tracks)
   - SequentialStrategy (PlaybackStrategy)
       Methods:    get_next_index(...), get_prev_index(...)
   - RepeatAllStrategy (PlaybackStrategy)
       Methods:    get_next_index(...), get_prev_index(...)
   - RepeatOneStrategy (PlaybackStrategy)
       Methods:    get_next_index(...), get_prev_index(...)
   - ShuffleStrategy (PlaybackStrategy)
       Attributes: _history: List[int]
       Methods:    get_next_index(...), get_prev_index(...)

3. Queue Manager
   - PlaybackQueue
       Attributes: _tracks: List[Song], _current_index: int, _strategy: PlaybackStrategy
       Properties: current_song -> Optional[Song]
       Methods:    load(songs, start_index), add_next(song), set_strategy(strategy),
                   advance_next() -> Optional[Song], advance_prev() -> Optional[Song]

4. Observer Pattern — Event Listeners
   - PlayerObserver (ABC)
       Methods:    on_track_changed(song), on_state_changed(state_name)
   - RecentlyPlayedTracker (PlayerObserver)
       Attributes: recent_songs: List[Song], _max_size: int
       Methods:    on_track_changed(song), on_state_changed(state_name)

5. State Pattern — Playback Lifecycle
   - PlayerState (ABC)
       Properties: name -> str
       Methods:    play(player), pause(player), stop(player)
   - IdleState / PlayingState / PausedState (PlayerState)
       Methods:    play(player), pause(player), stop(player)

6. Facade — MusicPlayer
   - MusicPlayer
       Attributes: queue: PlaybackQueue, _state: PlayerState,
                   _observers: List[PlayerObserver], position_sec: int
       Methods:    add_observer(observer), set_state(new_state),
                   notify_track_changed(), load_playlist(playlist, auto_play),
                   set_playback_mode(strategy), play(), pause(), stop(),
                   next_track(), prev_track(), seek(seconds)
===============================================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
import random


# --- 1. Core Domain Models ---

@dataclass(frozen=True)
class Song:
    song_id: str
    title: str
    artist: str
    duration_sec: int


@dataclass
class Playlist:
    playlist_id: str
    name: str
    songs: List[Song] = field(default_factory=list)

    def add_song(self, song: Song) -> None:
        self.songs.append(song)

    def remove_song(self, song_id: str) -> None:
        self.songs = [s for s in self.songs if s.song_id != song_id]


# --- 2. Strategy Pattern: Playback Ordering ---

class PlaybackStrategy(ABC):
    @abstractmethod
    def get_next_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        pass

    @abstractmethod
    def get_prev_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        pass


class SequentialStrategy(PlaybackStrategy):
    def get_next_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        if current_index + 1 < total_tracks:
            return current_index + 1
        return None  # Reached end of queue

    def get_prev_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        return max(0, current_index - 1) if total_tracks > 0 else None


class RepeatAllStrategy(PlaybackStrategy):
    def get_next_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        if total_tracks == 0:
            return None
        return (current_index + 1) % total_tracks

    def get_prev_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        if total_tracks == 0:
            return None
        return (current_index - 1 + total_tracks) % total_tracks


class RepeatOneStrategy(PlaybackStrategy):
    def get_next_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        return current_index if total_tracks > 0 else None

    def get_prev_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        return current_index if total_tracks > 0 else None


class ShuffleStrategy(PlaybackStrategy):
    # Follow-up: How do you make Shuffle feel "fair" (no repeats until all songs play)?
    # Instead of random.choice() on every next(), pre-generate a Fisher-Yates shuffled
    # permutation of indices [0..N-1] inside ShuffleStrategy and advance a pointer
    # through it (maintaining a history stack for previous()).
    def __init__(self) -> None:
        self._history: List[int] = []

    def get_next_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        if total_tracks == 0:
            return None
        if total_tracks == 1:
            return 0
        self._history.append(current_index)
        candidates = [i for i in range(total_tracks) if i != current_index]
        return random.choice(candidates)

    def get_prev_index(self, current_index: int, total_tracks: int) -> Optional[int]:
        if self._history:
            return self._history.pop()
        return current_index if total_tracks > 0 else None


# --- 3. Queue Manager ---

class PlaybackQueue:
    def __init__(self, strategy: Optional[PlaybackStrategy] = None) -> None:
        self._tracks: List[Song] = []
        self._current_index: int = -1
        self._strategy: PlaybackStrategy = strategy or SequentialStrategy()

    def load(self, songs: List[Song], start_index: int = 0) -> None:
        if not songs:
            raise ValueError("Cannot load an empty track list.")
        if not (0 <= start_index < len(songs)):
            raise IndexError("Invalid start index.")
        # Follow-up: How do you handle a playlist being edited while it's playing?
        # PlaybackQueue.load() copies the song list (list(songs)), decoupling the
        # active session queue from background playlist mutations so deleting a song
        # from a saved playlist doesn't corrupt current_index mid-playback.
        self._tracks = list(songs)
        self._current_index = start_index

    def add_next(self, song: Song) -> None:
        if not self._tracks:
            self._tracks = [song]
            self._current_index = 0
        else:
            self._tracks.insert(self._current_index + 1, song)

    def set_strategy(self, strategy: PlaybackStrategy) -> None:
        self._strategy = strategy

    @property
    def current_song(self) -> Optional[Song]:
        if 0 <= self._current_index < len(self._tracks):
            return self._tracks[self._current_index]
        return None

    def advance_next(self) -> Optional[Song]:
        next_idx = self._strategy.get_next_index(self._current_index, len(self._tracks))
        if next_idx is None:
            return None
        self._current_index = next_idx
        return self.current_song

    def advance_prev(self) -> Optional[Song]:
        prev_idx = self._strategy.get_prev_index(self._current_index, len(self._tracks))
        if prev_idx is None:
            return None
        self._current_index = prev_idx
        return self.current_song


# --- 4. Observer Pattern: Event Listeners ---

class PlayerObserver(ABC):
    @abstractmethod
    def on_track_changed(self, song: Optional[Song]) -> None:
        pass

    @abstractmethod
    def on_state_changed(self, state_name: str) -> None:
        pass


class RecentlyPlayedTracker(PlayerObserver):
    def __init__(self, max_size: int = 50) -> None:
        self.recent_songs: List[Song] = []
        self._max_size = max_size

    def on_track_changed(self, song: Optional[Song]) -> None:
        if song:
            self.recent_songs = [s for s in self.recent_songs if s.song_id != song.song_id]
            self.recent_songs.insert(0, song)
            self.recent_songs = self.recent_songs[:self._max_size]

    def on_state_changed(self, state_name: str) -> None:
        pass


# --- 5. State Pattern: Playback Lifecycle ---

class PlayerState(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def play(self, player: "MusicPlayer") -> None:
        pass

    @abstractmethod
    def pause(self, player: "MusicPlayer") -> None:
        pass

    @abstractmethod
    def stop(self, player: "MusicPlayer") -> None:
        pass


class IdleState(PlayerState):
    @property
    def name(self) -> str:
        return "IDLE"

    def play(self, player: "MusicPlayer") -> None:
        if not player.queue.current_song:
            raise RuntimeError("No song loaded in queue.")
        player.set_state(PlayingState())
        player.notify_track_changed()

    def pause(self, player: "MusicPlayer") -> None:
        pass  # No-op when idle

    def stop(self, player: "MusicPlayer") -> None:
        pass  # Already idle


class PlayingState(PlayerState):
    @property
    def name(self) -> str:
        return "PLAYING"

    def play(self, player: "MusicPlayer") -> None:
        pass  # Already playing

    def pause(self, player: "MusicPlayer") -> None:
        player.set_state(PausedState())

    def stop(self, player: "MusicPlayer") -> None:
        player.position_sec = 0
        player.set_state(IdleState())


class PausedState(PlayerState):
    @property
    def name(self) -> str:
        return "PAUSED"

    def play(self, player: "MusicPlayer") -> None:
        player.set_state(PlayingState())

    def pause(self, player: "MusicPlayer") -> None:
        pass  # Already paused

    def stop(self, player: "MusicPlayer") -> None:
        player.position_sec = 0
        player.set_state(IdleState())


# --- 6. Facade: MusicPlayer ---

class MusicPlayer:
    def __init__(self) -> None:
        self.queue = PlaybackQueue()
        self._state: PlayerState = IdleState()
        self._observers: List[PlayerObserver] = []
        self.position_sec: int = 0

    def add_observer(self, observer: PlayerObserver) -> None:
        self._observers.append(observer)

    def set_state(self, new_state: PlayerState) -> None:
        self._state = new_state
        for obs in self._observers:
            obs.on_state_changed(new_state.name)

    def notify_track_changed(self) -> None:
        for obs in self._observers:
            obs.on_track_changed(self.queue.current_song)

    def load_playlist(self, playlist: Playlist, auto_play: bool = True) -> None:
        self.queue.load(playlist.songs, start_index=0)
        self.position_sec = 0
        if auto_play:
            self._state = PlayingState()
            self.notify_track_changed()
            self.set_state(self._state)

    def set_playback_mode(self, strategy: PlaybackStrategy) -> None:
        self.queue.set_strategy(strategy)

    def play(self) -> None:
        self._state.play(self)

    def pause(self) -> None:
        self._state.pause(self)

    def stop(self) -> None:
        self._state.stop(self)

    def next_track(self) -> None:
        next_song = self.queue.advance_next()
        self.position_sec = 0
        if next_song is None:
            self.set_state(IdleState())
        else:
            self.notify_track_changed()
            if self._state.name != "PLAYING":
                self.set_state(PlayingState())

    def prev_track(self) -> None:
        if self.position_sec > 3:
            # Standard UX: restart current track if > 3s elapsed
            self.position_sec = 0
            return
        prev_song = self.queue.advance_prev()
        self.position_sec = 0
        if prev_song:
            self.notify_track_changed()

    def seek(self, seconds: int) -> None:
        song = self.queue.current_song
        if not song:
            raise RuntimeError("No active track to seek.")
        if not (0 <= seconds <= song.duration_sec):
            raise ValueError("Seek position out of bounds.")
        self.position_sec = seconds
