async function getPostId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('post_id');
}

async function fetchPost() {
    const postId = await getPostId();
    if (!postId) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch(`/api/posts/${postId}`);
        const post = await response.json();

        const postContainer = document.getElementById('post-container');
        postContainer.innerHTML = `
            <h1>${post.title}</h1>
            <div class="post-meta">
                By ${post.author} on ${new Date(post.created_at).toLocaleDateString()}
            </div>
            <div class="post-content">
                ${post.content}
            </div>
        `;

        // Display comments
        const commentsContainer = document.getElementById('comments-container');
        if (post.comments && post.comments.length > 0) {
            commentsContainer.innerHTML = post.comments.map(comment => `
                <div class="comment">
                    <div class="comment-meta">
                        By ${comment.author} on ${new Date(comment.created_at).toLocaleDateString()}
                    </div>
                    <div class="comment-content">
                        ${comment.content}
                    </div>
                </div>
            `).join('');
        } else {
            commentsContainer.innerHTML = '<p>No comments yet.</p>';
        }
    } catch (error) {
        console.error('Error fetching post:', error);
    }
}

async function handleCommentSubmit(event) {
    event.preventDefault();
    const postId = await getPostId();

    const formData = {
        author: document.getElementById('author').value,
        content: document.getElementById('content').value
    };

    try {
        const response = await fetch(`/api/posts/${postId}/comments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            // Refresh the page to show the new comment
            window.location.reload();
        }
    } catch (error) {
        console.error('Error posting comment:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchPost);
document.getElementById('comment-form').addEventListener('submit', handleCommentSubmit);
