const arrows = document.querySelectorAll('.arrow');
const exit_buttons = document.querySelectorAll('.exit-button');
exit_buttons.forEach(button => {
    button.addEventListener('click', () => {
        const shown_sidebar = document.querySelector('.shown');
        shown_sidebar.classList.remove('shown');
        
        arrows.forEach(arrow => {
            arrow.classList.remove('hidden');
        })
    });
});

// Beginners start here
const beginners_start_here_button = document.getElementById('beginners-start-here');
const beginners_start_here_sidebar = document.getElementById('beginners-start-here-sidebar');
const bsh_progress_bar = document.getElementById('bsh-progress'); // Progress bar
const bsh_checkboxes = document.querySelectorAll('.bsh-checkbox'); // Checkboxes for each module
const num_bsh_modules = bsh_checkboxes.length;
let bsh_modules_completed = 0; // Number of checkboxes checked
let bsh_completed_count = document.getElementById('bsh-completed-count'); // Text

beginners_start_here_button.addEventListener('click', () => {
    beginners_start_here_sidebar.classList.add('shown');
    arrows.forEach(arrow => {
        arrow.classList.add('hidden');
    })
});

bsh_checkboxes.forEach(bsh_checkbox => {
    bsh_checkbox.addEventListener('click', () => {
        if (bsh_checkbox.checked) {
            bsh_modules_completed++;
            bsh_progress_bar.value++;
        } else {
            bsh_modules_completed--;
            bsh_progress_bar.value--;
        }
        bsh_completed_count.textContent = "(" + String(bsh_modules_completed) + "/" + String(num_bsh_modules) + ")";
    });
});




