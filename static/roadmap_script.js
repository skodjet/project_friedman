const beginners_start_here_button = document.getElementById('beginners-start-here');
const beginners_start_here_sidebar = document.getElementById('beginners-start-here-sidebar');
const exit_buttons = document.querySelectorAll('.exit-button');

beginners_start_here_button.addEventListener('click', () => {
    beginners_start_here_sidebar.classList.toggle('shown');
});

// Setup for exit buttons
exit_buttons.forEach(button => {
    button.addEventListener('click', () => {
        const shown_sidebar = document.querySelector('.shown');
        shown_sidebar.classList.toggle('shown');
    });
});



