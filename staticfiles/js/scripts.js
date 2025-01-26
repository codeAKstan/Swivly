const signupButton = document.getElementById('signup-btn');
const dropdown = document.querySelector('.signup-dropdown');

signupButton.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('active');
});

document.addEventListener('click', () => {
    dropdown.classList.remove('active');
});