const beginners_start_here_button = document.getElementById('beginners-start-here');
const beginners_start_here_sidebar = document.getElementById('beginners-start-here-sidebar');

beginners_start_here_button.addEventListener('click', () => {
    beginners_start_here_sidebar.classList.remove('hidden');
    beginners_start_here_sidebar.classList.add('shown');
});
