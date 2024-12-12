async function fetchPosts() {
    try {
        const response = await fetch('/api/posts/');
        const posts = await response.json();

        const postsContainer = document.getElementById('posts-container');
        postsContainer.innerHTML = posts.map(post => `
            <div class="post">
                <h2><a href="/post.html?post_id=${post.id}">${post.title}</a></h2>
                <div class="post-meta">
                    By ${post.author} on ${new Date(post.created_at).toLocaleDateString()}
                </div>
                <p>${post.content.substring(0, 200)}${post.content.length > 200 ? '...' : ''}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error fetching posts:', error);
    }
}

// Load posts when the page loads
document.addEventListener('DOMContentLoaded', fetchPosts);
