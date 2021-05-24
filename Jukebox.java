/*
Now that we have that out of the way, we'll outline the basic system components.
• Jukebox
• CD
• Song
• Artist
• Playlist
• Display (displays details on the screen)
Now, let’s break this down further and think about the possible actions.
• Playlist creation (includes add, delete, and shuffle)
• CD selector
• Song selector
• Queuing up a song
• Get next song from playlist
A user also can be introduced:
• Adding
• Deleting
• Credit information
*/

public class CD {
}
 
public class CDPlayer {
    private Playlist p;
    private CD c;
 
    public Playlist getPlaylist() {
        return p;
    }
 
    public void setPlaylist(Playlist p) {
        this.p = p;
    }
 
    public CD getCD() {
        return c;
    }
 
    public void setCD(CD c) {
        this.c = c;
    }
 
    public CDPlayer(Playlist p) {
        this.p = p;
    }
 
    public CDPlayer(CD c, Playlist p) {
        // TODO
    }
 
    public CDPlayer(CD c) {
        this.c = c;
    }
 
    public void playTrack(MySong s) {
        // TODO
    }
}
 
public class JukeBox {
    private CDPlayer cdPlayer;
    private User user;
    private Set<CD> cdCollection;
    private TrackSelector ts;
 
    public JukeBox(CDPlayer cdPlayer, User user, Set<CD> cdCollection,
            TrackSelector ts) { // TODO
 
    }
 
    public MySong getCurrentTrack() {
        return ts.getCurrentSong();
    }
 
    public void processOneUser(User u) {
        this.user = u;
    }
}
 
public class Playlist {
    private MySong track;
    private Queue<MySong> queue;
 
    public Playlist(MySong track, Queue<MySong> queue) { // TODO
 
    }
 
    public MySong getNextTrackToPlay() {
        return queue.peek();
    }
 
    public void queueUpTrack(MySong s) {
        queue.add(s);
    }
}
 
public class Song {
    private String songName;
}
 
public class TrackSelector {
    private MySong currentSong;
 
    public TrackSelector(MySong s) {
        currentSong = s;
    }
 
    public void setTrack(MySong s) {
        currentSong = s;
    }
 
    public MySong getCurrentSong() {
        return currentSong;
    }
}
 
public class User {
    private String name;
 
    public String getName() {
        return name;
    }
 
    public void setName(String name) {
        this.name = name;
    }
 
    public long getID() {
        return ID;
    }
 
    public void setID(long iD) {
        ID = iD;
    }
 
    private long ID;
 
    public User(String name, long iD) { // TODO
 
    }
 
    public User getUser() {
        return this;
    }
 
    public User addUser(String name, long iD) {// TODO
        return null;
    }
}
