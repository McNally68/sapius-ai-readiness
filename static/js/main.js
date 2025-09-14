// Main JavaScript for AIReady Assessment Platform

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active class to current navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Progress indication for assessment form
    const assessmentForm = document.getElementById('assessmentForm');
    if (assessmentForm) {
        const sections = assessmentForm.querySelectorAll('.form-section');
        const progressBar = createProgressBar(sections.length);
        
        if (progressBar) {
            assessmentForm.insertBefore(progressBar, assessmentForm.firstChild);
            updateProgress();
            
            // Listen for changes in radio buttons
            assessmentForm.addEventListener('change', updateProgress);
        }
    }

    function createProgressBar(totalSections) {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container';
        progressContainer.style.position = 'fixed';
        progressContainer.style.top = '0';
        progressContainer.style.zIndex = '100';
        progressContainer.innerHTML = `
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text">
                    <span id="progressText">0% Complete</span>
                </div>
            </div>
        `;
        return progressContainer;
    }

    function updateProgress() {
        const assessmentForm = document.getElementById('assessmentForm');
        if (!assessmentForm) return;
        
        const allQuestions = assessmentForm.querySelectorAll('.question-group');
        const answeredQuestions = assessmentForm.querySelectorAll('.question-group input:checked');
        
        const progress = (answeredQuestions.length / allQuestions.length) * 100;
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        if (progressFill && progressText) {
            progressFill.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '% Complete';
        }
    }

    // Add CSS for progress bar if it doesn't exist
    const progressStyles = `
        .progress-container {
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .progress-bar-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .progress-bar {
            flex: 1;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            transition: width 0.3s ease;
            width: 0%;
        }
        
        .progress-text {
            font-size: 0.875rem;
            font-weight: 600;
            color: #495057;
            min-width: 100px;
        }
        
        .form-section {
            margin-bottom: 2rem;
        }
        
        .question-group {
            margin-bottom: 1.5rem;
        }
        
        .radio-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .radio-option {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .radio-option:hover {
            background-color: #f8f9fa;
        }
        
        .radio-custom {
            width: 20px;
            height: 20px;
            border: 2px solid #dee2e6;
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
        }
        
        .radio-option input[type="radio"]:checked + .radio-custom {
            border-color: #4CAF50;
        }
        
        .radio-option input[type="radio"]:checked + .radio-custom::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 10px;
            height: 10px;
            background: #4CAF50;
            border-radius: 50%;
        }
        
        .radio-option input[type="radio"] {
            display: none;
        }
        
        .error {
            border-color: #dc3545 !important;
        }
    `;
    
    // Add styles to head if they don't exist
    if (!document.getElementById('dynamic-styles')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'dynamic-styles';
        styleSheet.textContent = progressStyles;
        document.head.appendChild(styleSheet);
    }
});