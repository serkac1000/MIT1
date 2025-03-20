// Global variables to store project data
let currentProject = null;
let projectFileName = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();
    
    // Setup form inputs
    setupFileInput();
    
    // Setup form submissions
    setupFormHandlers();
    
    // Setup button handlers
    setupButtonHandlers();
});

// Setup custom file input to show selected filename
function setupFileInput() {
    const fileInput = document.getElementById('aia-file');
    const fileLabel = document.querySelector('.custom-file-label');
    
    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            fileLabel.textContent = this.files[0].name;
        } else {
            fileLabel.textContent = 'Choose file...';
        }
    });
}

// Setup form submission handlers
function setupFormHandlers() {
    // Upload form submission
    const uploadForm = document.getElementById('upload-form');
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('aia-file');
        if (fileInput.files.length === 0) {
            showError('Please select a file to upload');
            return;
        }
        
        const file = fileInput.files[0];
        if (!file.name.toLowerCase().endsWith('.aia')) {
            showError('Please select a valid .aia file');
            return;
        }
        
        uploadProject(file);
    });
}

// Setup button click handlers
function setupButtonHandlers() {
    // Back button
    document.getElementById('back-btn').addEventListener('click', function() {
        showSection('upload-section');
    });
    
    // Compile button
    document.getElementById('compile-btn').addEventListener('click', function() {
        if (!currentProject) {
            showError('No project loaded. Please upload a project first.');
            return;
        }
        
        compileProject();
    });
    
    // Retry button
    document.getElementById('retry-btn').addEventListener('click', function() {
        showSection('project-info-section');
    });
    
    // Download button - will be handled after compilation completes
}

// Upload project file
function uploadProject(file) {
    showLoading('Uploading and analyzing your project...');
    
    const formData = new FormData();
    formData.append('file', file);
    projectFileName = file.name;
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error uploading file');
            });
        }
        return response.json();
    })
    .then(data => {
        hideLoading();
        if (data.success) {
            currentProject = data.project_info;
            // Store filename in currentProject
            if (!currentProject.filename) {
                currentProject.filename = projectFileName;
            }
            displayProjectInfo(currentProject);
            showSection('project-info-section');
        } else {
            showError(data.error || 'Unknown error occurred');
        }
    })
    .catch(error => {
        hideLoading();
        showError(error.message || 'Error uploading file');
    });
}

// Display project information
function displayProjectInfo(project) {
    document.getElementById('project-name').textContent = project.projectName || 'Unknown';
    document.getElementById('project-screens').textContent = project.screens.join(', ') || 'None';
    document.getElementById('project-components').textContent = project.components.join(', ') || 'None';
    document.getElementById('project-version').textContent = project.version || 'Unknown';
    
    // Display missing components info if available
    if (project.missing_components && project.missing_components.length > 0) {
        // Find project-details to add missing components section
        const projectDetails = document.querySelector('.project-details');
        
        // Check if we already have a missing components section
        let missingComponentsRow = document.getElementById('missing-components-row');
        if (!missingComponentsRow) {
            // Create it if it doesn't exist
            missingComponentsRow = document.createElement('div');
            missingComponentsRow.id = 'missing-components-row';
            missingComponentsRow.className = 'row';
            missingComponentsRow.innerHTML = `
                <div class="col-md-4 font-weight-bold text-danger">Missing Components:</div>
                <div class="col-md-8 text-danger" id="missing-components-list"></div>
            `;
            projectDetails.appendChild(missingComponentsRow);
        }
        
        // Populate the missing components list
        const missingComponentsList = document.getElementById('missing-components-list');
        const missingComponentsText = project.missing_components.map(item => 
            `${item.component} (in ${item.screen})`
        ).join(', ');
        
        missingComponentsList.textContent = missingComponentsText;
        
        // Add a warning message
        let warningMessage = document.getElementById('missing-components-warning');
        if (!warningMessage) {
            warningMessage = document.createElement('div');
            warningMessage.id = 'missing-components-warning';
            warningMessage.className = 'alert alert-warning mt-3';
            warningMessage.innerHTML = `
                <strong>Warning:</strong> Some components are referenced in your blocks but not added to your screens.
                <p>Your app may not work correctly without these components. Consider adding them in MIT App Inventor before using the compiled app.</p>
            `;
            projectDetails.after(warningMessage);
        }
    } else {
        // Remove missing components sections if they exist but there are no missing components
        const missingComponentsRow = document.getElementById('missing-components-row');
        if (missingComponentsRow) {
            missingComponentsRow.remove();
        }
        
        const warningMessage = document.getElementById('missing-components-warning');
        if (warningMessage) {
            warningMessage.remove();
        }
    }
}

// Compile the project
function compileProject() {
    showSection('compilation-section');
    updateCompilationProgress(10, 'Initializing compilation...');
    
    // Add compilation options
    const compilationOptions = {
        projectName: currentProject.projectName,
        filename: currentProject.filename || projectFileName,
        target: document.getElementById('compilation-target').value,
        optimize: document.getElementById('optimize-apk').checked,
        components: currentProject.components || [],
        screens: currentProject.screens || [],
        version: currentProject.version || ''
    };
    
    // Add missing components info if available
    if (currentProject.missing_components && currentProject.missing_components.length > 0) {
        compilationOptions.missing_components = currentProject.missing_components;
    }
    
    // Update progress for visual feedback
    updateCompilationProgress(25, 'Processing project files...');
    setTimeout(() => updateCompilationProgress(40, 'Converting blocks to code...'), 1000);
    setTimeout(() => updateCompilationProgress(60, 'Building Android project...'), 2000);
    setTimeout(() => updateCompilationProgress(75, 'Compiling APK...'), 3000);
    setTimeout(() => updateCompilationProgress(90, 'Finalizing package...'), 4000);
    
    // Send compilation request
    setTimeout(() => {
        fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(compilationOptions)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Error during compilation');
                });
            }
            
            // Handle successful compilation
            updateCompilationProgress(100, 'Compilation completed successfully!');
            
            // Show compilation result
            document.getElementById('compilation-result').classList.remove('d-none');
            
            return response.blob();
        })
        .then(blob => {
            // Create a download URL for the APK
            const url = window.URL.createObjectURL(blob);
            const downloadBtn = document.getElementById('download-btn');
            
            // Clear previous event listeners
            const newDownloadBtn = downloadBtn.cloneNode(true);
            downloadBtn.parentNode.replaceChild(newDownloadBtn, downloadBtn);
            
            // Update download button to trigger download
            newDownloadBtn.addEventListener('click', function() {
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `${currentProject.projectName}.apk`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            });
        })
        .catch(error => {
            // Handle compilation error
            updateCompilationProgress(0, 'Compilation failed');
            document.getElementById('error-details').textContent = error.message || 'Unknown error occurred';
            document.getElementById('compilation-error').classList.remove('d-none');
        });
    }, 5000);
}

// Update the compilation progress
function updateCompilationProgress(percentage, message) {
    const progressBar = document.getElementById('compilation-progress');
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute('aria-valuenow', percentage);
    
    const log = document.getElementById('compilation-log');
    const logEntry = document.createElement('p');
    logEntry.innerHTML = `<span class="text-muted">[${new Date().toLocaleTimeString()}]</span> ${message}`;
    log.appendChild(logEntry);
    log.scrollTop = log.scrollHeight;
}

// Show loading modal
function showLoading(message) {
    const loadingMessage = document.getElementById('loading-message');
    loadingMessage.textContent = message || 'Loading...';
    $('#loadingModal').modal('show');
}

// Hide loading modal
function hideLoading() {
    $('#loadingModal').modal('hide');
}

// Show error message
function showError(message) {
    alert(message);
}

// Show a specific section and hide others
function showSection(sectionId) {
    const sections = ['upload-section', 'project-info-section', 'compilation-section'];
    sections.forEach(section => {
        const element = document.getElementById(section);
        if (section === sectionId) {
            element.classList.remove('d-none');
        } else {
            element.classList.add('d-none');
        }
    });
    
    // Reset states for compilation section
    if (sectionId === 'compilation-section') {
        document.getElementById('compilation-progress').style.width = '0%';
        document.getElementById('compilation-log').innerHTML = '<p>Starting compilation process...</p>';
        document.getElementById('compilation-result').classList.add('d-none');
        document.getElementById('compilation-error').classList.add('d-none');
    }
}
