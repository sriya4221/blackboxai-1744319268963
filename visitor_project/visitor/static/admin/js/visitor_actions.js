function approveVisitor(visitorId) {
    if (confirm('Are you sure you want to approve this visitor?')) {
        fetch(`/visitor/approve/${visitorId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function rejectVisitor(visitorId) {
    if (confirm('Are you sure you want to reject this visitor?')) {
        fetch(`/visitor/reject/${visitorId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function blockVisitor(visitorId) {
    if (confirm('Are you sure you want to block this visitor?')) {
        fetch(`/visitor/block/${visitorId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
