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
            const checked = checkbox.checked;
            if (checked) {
                modules_completed++;
                progress_bar.value++;
            } else {
                modules_completed--;
                progress_bar.value--;
            }
            completed_count.textContent = "(" + String(modules_completed) + "/" + String(num_modules) + ")";

            // Send information about completed lesson to Flask
            const c_id = checkbox.id;
            fetch('/update-progress', {
                method: 'POST', 
                body: JSON.stringify({lesson_id: c_id, status: checked}), 
                headers: {'Content-Type': 'application/json'}
            });
        });
    });
}


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
setup_sidebar(document.getElementById('beginners-start-here-button'), document.getElementById('beginners-start-here-sidebar'), 
              document.getElementById('bsh-progress'), document.querySelectorAll('.bsh-checkbox'), document.getElementById('bsh-completed-count'));

// Basic chords
setup_sidebar(document.getElementById('basic-chords-button'), document.getElementById('basic-chords-sidebar'), 
              document.getElementById('bc-progress'), document.querySelectorAll('.bc-checkbox'), document.getElementById('bc-completed-count'));

// Picking 1
setup_sidebar(document.getElementById('picking-1-button'), document.getElementById('picking-1-sidebar'), 
              document.getElementById('pck1-progress'), document.querySelectorAll('.pck1-checkbox'), document.getElementById('pck1-completed-count'));

// Articulation
setup_sidebar(document.getElementById('artc-button'), document.getElementById('artc-sidebar'), 
              document.getElementById('artc-progress'), document.querySelectorAll('.artc-checkbox'), document.getElementById('artc-completed-count'));

// Advanced picking
setup_sidebar(document.getElementById('picking-2-button'), document.getElementById('picking-2-sidebar'), 
              document.getElementById('pck2-progress'), document.querySelectorAll('.pck2-checkbox'), document.getElementById('pck2-completed-count'));





