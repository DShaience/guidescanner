document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('searchQuery').value;
    showSearchingEffect();
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            storedResults = data.results;
            if (!document.hidden) {
                updateResultsList(storedResults);
            }
            hideSearchingEffect();
        })
        .catch(error => {
            console.error('Error:', error);
            hideSearchingEffect();
        });
});

document.addEventListener('visibilitychange', function() {
    if (!document.hidden && storedResults) {
        updateResultsList(storedResults);
    }
});

function updateResultsList(results) {
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';
    results.forEach(result => {
        const li = document.createElement('li');
        li.textContent = result;
        resultsList.appendChild(li);
    });
}

function showSearchingEffect() {
    document.getElementById('searchButton').style.display = 'none';
    document.getElementById('searchingText').style.display = 'block';
    let dots = document.getElementById('dots');
    let dotCount = 1;
    dotInterval = setInterval(() => {
        dots.textContent = '.'.repeat(dotCount);
        dotCount = (dotCount % 3) + 1;
    }, 500);
}

function hideSearchingEffect() {
    clearInterval(dotInterval);
    document.getElementById('searchButton').style.display = 'block';
    document.getElementById('searchingText').style.display = 'none';
}