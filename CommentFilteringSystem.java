/*
This follows composite design pattern - postfilter is implemented by diff filters
Discuss about hashmap and trie implementation for word search.
Also have seperate class for comment
*/
interface PostFilter {
    boolean isAgoodPost(Post post);
}

public class HTMLScriptFilterAction implements PostFilter {
    @Override
    public boolean isAGoodPost(Post post) {
        System.out.println("the post does not contain any html script tag");
        return true;
    }
}

public class RudeWordsFilterAction implements PostFilter {
    @Override
    public boolean isAGoodPost(Post post) {
        System.out.println("The post does not contain rude words");
        return true;
    }
}

public class RudeWordsFilterAction2 implements PostFilter {
    @Override
    public boolean isAGoodPost(Post post) {
        System.out.println("Rude Action 2 didn't find any problem with this post");
        return true;
    }
}

public class PostFilterComposite implements PostFilter {
    private List<PostFilter> filters;

    public PostFilterComposite(List<PostFilter> filters) {
        this.filters = filters;
    }

    public void addPostFilter(PostFilter filter){
        this.filters.add(filter);
    }

    public void removePostFilter(PostFilter filter) {
        this.filters.remove(filter);
    }

    @Override
    public boolean isAGoodPost(Post post) {
        for (PostFilter filter : filters) {
            boolean aGoodPost = filter.isAGoodPost(post);
            if(!aGoodPost) return false;
        }
        return true;
    }
}

public class Post {
    // Omitted content for simplicity
}

public class Comment {
    public string desc;
    public Comment(string desc) {
        this.desc = desc;
    }

    public List<string> GetAsArray() {
        var res = new List<string>();
        var arr = desc.Split(" ");
        foreach(var item in arr) 
            res.Add(item);
    }
}

public class CommentFiltering {

    private PostFilter filterEngine;

    public void addFilter(PostFilter filter) {
        this.filterEngine = filter;
    }

    public boolean filterPost(Post post) {
         return filterEngine.isAGoodPost(post);
    }
    
    public List<Comment> comments;
    public Filter filter;
    public CommentsFiltering() {
        comments = new List<Comment>();
    }

    public void AddComment(Comment c){
        comments.Add(c);
    }

    public void RemoveComment(Comment c){
        comments.Remove(c);
    }

    public static void main(String[] args) {
        CommentFiltering commentFiltering = new CommentFiltering();
        PostFilterComposite mainFilter = new PostFilterComposite();
        PostFilterComposite rudeFilterComposite = new PostFilterComposite();
        rudeFilterComposite.addPostFilter(new RudeWordsFilterAction());
        rudeFilterComposite.addPostFilter(new RudeWordsFilterAction2());
        mainFilter.addPostFilter(rudeFilterComposite);
        mainFilter.addPostFilter(new HTMLScriptFilterAction());
        commentFiltering.addFilter(mainFilter);
        boolean isGoodPost = commentFiltering.filterPost(new Post());
        System.out.println("IsAGoodPost:" + isGoodPost);
    }
}
