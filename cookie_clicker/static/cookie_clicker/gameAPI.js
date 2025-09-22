// my-second-django-project/cookie_clicker/static/cookie_clicker/gameAPI.js

// CSRF token utility po sir
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export class GameAPI {
    constructor() {
        this.csrftoken = getCookie('csrftoken');
    }

    async sendAction(url, method = 'POST') {
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrftoken,
                },
                body: JSON.stringify({}) 
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || response.statusText);
            }

            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            alert('Network or server error: ' + error.message);
            throw error; 
        }
    }
}