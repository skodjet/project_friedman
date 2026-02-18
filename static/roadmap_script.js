const beginners_start_here_button = document.getElementById('beginners-start-here');
const beginners_start_here_sidebar = document.getElementById('beginners-start-here-sidebar');
const exit_buttons = document.querySelectorAll('.exit-button');
const arrows = document.querySelectorAll('.arrow');

beginners_start_here_button.addEventListener('click', () => {
    beginners_start_here_sidebar.classList.add('shown');
    arrows.forEach(arrow => {
        arrow.classList.add('hidden');
    })
});

// Setup for exit buttons
exit_buttons.forEach(button => {
    button.addEventListener('click', () => {
        const shown_sidebar = document.querySelector('.shown');
        shown_sidebar.classList.remove('shown');
        
        arrows.forEach(arrow => {
            arrow.classList.remove('hidden');
        })
    });
});





