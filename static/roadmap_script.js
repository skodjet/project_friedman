// Sidebar exit button functionality
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
// const beginners_start_here_button = document.getElementById('beginners-start-here');
// const beginners_start_here_sidebar = document.getElementById('beginners-start-here-sidebar');
// const bsh_progress_bar = document.getElementById('bsh-progress'); // Progress bar
// const bsh_checkboxes = document.querySelectorAll('.bsh-checkbox'); // Checkboxes for each module
// const num_bsh_modules = bsh_checkboxes.length;
// let bsh_modules_completed = 0; // Number of checkboxes checked
// let bsh_completed_count = document.getElementById('bsh-completed-count'); // Text

// beginners_start_here_button.addEventListener('click', () => {
//     beginners_start_here_sidebar.classList.add('shown');
//     arrows.forEach(arrow => {
//         arrow.classList.add('hidden');
//     })
// });

// bsh_checkboxes.forEach(bsh_checkbox => {
//     bsh_checkbox.addEventListener('click', () => {
//         if (bsh_checkbox.checked) {
//             bsh_modules_completed++;
//             bsh_progress_bar.value++;
//         } else {
//             bsh_modules_completed--;
//             bsh_progress_bar.value--;
//         }
//         bsh_completed_count.textContent = "(" + String(bsh_modules_completed) + "/" + String(num_bsh_modules) + ")";
//     });
// });


// Functionality for showing sidebar
// completed count = <p> element of how many modules are completed
function setup_sidebar(button, sidebar, progress_bar, checkboxes, completed_count) {
    const num_modules = checkboxes.length;
    let modules_completed = 0; // Number of checkboxes checked

    // Show sidebar and hide arrows
    button.addEventListener('click', () => {
        sidebar.classList.add('shown');
        arrows.forEach(arrow => {
            arrow.classList.add('hidden');
        })
    });

    // Checkboxes and progress bar functionality
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', () => {
            if (checkbox.checked) {
                modules_completed++;
                progress_bar.value++;
            } else {
                modules_completed--;
                progress_bar.value--;
            }
            completed_count.textContent = "(" + String(modules_completed) + "/" + String(num_modules) + ")";
        });
    });
}

// Beginners start here
setup_sidebar(document.getElementById('beginners-start-here-button'), document.getElementById('beginners-start-here-sidebar'), 
              document.getElementById('bsh-progress'), document.querySelectorAll('.bsh-checkbox'), document.getElementById('bsh-completed-count'));

// Basic chords
setup_sidebar(document.getElementById('basic-chords-button'), document.getElementById('basic-chords-sidebar'), 
              document.getElementById('bc-progress'), document.querySelectorAll('.bc-checkbox'), document.getElementById('bc-completed-count'));

// Picking 1
setup_sidebar(document.getElementById('picking-1-button'), document.getElementById('picking-1-sidebar'), 
              document.getElementById('pck1-progress'), document.querySelectorAll('.pck1-checkbox'), document.getElementById('pck1-completed-count'));




