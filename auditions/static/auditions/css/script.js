// Add transforming effects to list items
document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.classList.add('animated');
    });
    item.addEventListener('mouseout', () => {
        item.classList.remove('animated');
    });
});