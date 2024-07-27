document.getElementById('qa-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const question = document.getElementById('question').value;
    const context = document.getElementById('context').value;

    console.log("Submitting request:", { question, context }); // Debugging line

    try {
        const response = await fetch('http://127.0.0.1:8000/qa/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question, context })
        });

        console.log("Response status:", response.status); // Debugging line

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response data:", data); // Debugging line
        document.getElementById('answer').textContent = data.answer || 'No answer found';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('answer').textContent = 'An error occurred. Please try again.';
    }
});
