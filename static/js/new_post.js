async function handlePostSubmit(event) {
    event.preventDefault();

    const formData = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        content: document.getElementById('content').value
    };

    try {
        const response = await fetch('/api/posts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const post = await response.json();
            // Redirect to the post detail page
            window.location.href = `/post.html?post_id=${post.id}`;
        }
    } catch (error) {
        console.error('Error creating post:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('post-form').addEventListener('submit', handlePostSubmit);
});
