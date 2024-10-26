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


const paragraph = document.querySelector('p');
paragraph.classList.add('paragraph-style');

function updateResultsList(results) {
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';
    results.forEach(result => {
        let element;
        if (result.type === 'main-header') {
            element = document.createElement('h2');
            element.textContent = result.content;
        } else if (result.type === 'sub-header1') {
            element = document.createElement('h3');
            element.textContent = result.content;
        } else if (result.type === 'paragraph') {
            element = document.createElement('p');
            element.textContent = result.content;
            element.classList.add('paragraph-style'); 
        }
        resultsList.appendChild(element);
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