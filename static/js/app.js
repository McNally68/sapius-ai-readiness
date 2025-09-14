// AI Readiness Assessment Platform - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAnimations();
    initializeScrollEffects();
    initializeTooltips();
    
    // Page-specific initializations
    const currentPage = window.location.pathname;
    
    if (currentPage === '/assessment') {
        initializeAssessmentForm();
    } else if (currentPage.startsWith('/results/')) {
        initializeResultsPage();
    }
});

// Animation utilities
function initializeAnimations() {
    // Add fade-in animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and important elements
    const elementsToAnimate = document.querySelectorAll('.card, .feature-icon, .dimension-badge');
    elementsToAnimate.forEach(function(element) {
        observer.observe(element);
    });
}

// Scroll effects
function initializeScrollEffects() {
    let ticking = false;
    
    function updateScrollEffects() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        // Parallax effect for hero section
        const heroSection = document.querySelector('.hero-section');
        if (heroSection && scrolled < heroSection.offsetHeight) {
            heroSection.style.transform = `translateY(${rate}px)`;
        }
        
        ticking = false;
    }
    
    function requestScrollUpdate() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestScrollUpdate);
}

// Tooltip initialization
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Assessment form functionality
function initializeAssessmentForm() {
    const form = document.getElementById('assessmentForm');
    const progressBar = document.getElementById('progressBar');
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    if (!form) return;
    
    // Enhanced progress tracking
    function updateProgress() {
        const totalQuestions = document.querySelectorAll('input[type="radio"][required]').length;
        const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
        const companyFields = document.querySelectorAll('#assessmentForm input[required], #assessmentForm select[required]');
        const filledCompanyFields = Array.from(companyFields).filter(field => field.value.trim() !== '').length;
        
        const totalRequired = totalQuestions + companyFields.length;
        const totalCompleted = answeredQuestions + filledCompanyFields;
        const progress = (totalCompleted / totalRequired) * 100;
        
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
        
        // Update submit button state
        submitBtn.disabled = totalCompleted < totalRequired;
        
        if (progress === 100) {
            submitBtn.classList.add('btn-success');
            submitBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Calculate AI Readiness Score';
        }
    }
    
    // Smooth scrolling to next question
    function scrollToNextUnanswered(currentInput) {
        const currentQuestion = currentInput.closest('.question-group');
        const nextQuestion = currentQuestion.nextElementSibling;
        
        if (nextQuestion && nextQuestion.classList.contains('question-group')) {
            const nextUnanswered = nextQuestion.querySelector('input[type="radio"]:not(:checked)');
            if (nextUnanswered) {
                setTimeout(() => {
                    nextQuestion.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 100);
            }
        }
    }
    
    // Enhanced event listeners
    form.addEventListener('change', function(e) {
        updateProgress();
        
        if (e.target.type === 'radio') {
            // Add visual feedback
            const questionGroup = e.target.closest('.question-group');
            questionGroup.classList.add('answered');
            
            // Scroll to next question
            scrollToNextUnanswered(e.target);
        }
    });
    
    form.addEventListener('input', updateProgress);
    
    // Form submission with enhanced UX
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        loadingSpinner.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Calculating...';
        
        // Collect data
        const formData = new FormData(form);
        const companyInfo = {
            name: formData.get('companyName'),
            industry: formData.get('industry'),
            size: formData.get('companySize'),
            role: formData.get('role')
        };
        
        const responses = [];
        const radioInputs = document.querySelectorAll('input[type="radio"]:checked');
        
        radioInputs.forEach(function(input) {
            responses.push({
                question_id: input.name,
                score: parseInt(input.value)
            });
        });
        
        // Submit assessment
        submitAssessment(companyInfo, responses);
    });
    
    // Initial progress update
    updateProgress();
    
    // Add category navigation
    addCategoryNavigation();
}

// Submit assessment with retry logic
function submitAssessment(companyInfo, responses, retryCount = 0) {
    const maxRetries = 3;
    
    fetch('/api/submit_assessment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company_info: companyInfo,
            responses: responses
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Success - redirect to results
            window.location.href = '/results/' + data.assessment_id;
        } else {
            throw new Error(data.message || 'Assessment submission failed');
        }
    })
    .catch(error => {
        console.error('Assessment submission error:', error);
        
        if (retryCount < maxRetries) {
            // Retry after a delay
            setTimeout(() => {
                submitAssessment(companyInfo, responses, retryCount + 1);
            }, 1000 * (retryCount + 1));
        } else {
            // Show error message
            showErrorMessage('Unable to submit assessment. Please check your connection and try again.');
            resetSubmitButton();
        }
    });
}

// Add category navigation
function addCategoryNavigation() {
    const categories = document.querySelectorAll('.category-section');
    if (categories.length <= 1) return;
    
    const navContainer = document.createElement('div');
    navContainer.className = 'category-navigation sticky-top bg-white py-3 mb-4';
    navContainer.innerHTML = `
        <div class="container">
            <div class="d-flex justify-content-center flex-wrap gap-2">
                ${Array.from(categories).map((category, index) => {
                    const title = category.querySelector('.card-header h4').textContent.trim();
                    return `<button type="button" class="btn btn-outline-primary btn-sm" onclick="scrollToCategory('${category.id}')">${title}</button>`;
                }).join('')}
            </div>
        </div>
    `;
    
    const form = document.getElementById('assessmentForm');
    form.parentNode.insertBefore(navContainer, form);
}

// Scroll to category
window.scrollToCategory = function(categoryId) {
    const category = document.getElementById(categoryId);
    if (category) {
        category.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
};

// Results page functionality
function initializeResultsPage() {
    // Animate score reveal
    const scoreElement = document.querySelector('.score-circle .display-2');
    if (scoreElement) {
        const finalScore = parseFloat(scoreElement.textContent);
        animateScore(scoreElement, 0, finalScore, 1500);
    }
    
    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach((bar, index) => {
        const finalWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1.2s ease-out';
            bar.style.width = finalWidth;
        }, 300 + (index * 150));
    });
    
    // Add copy results functionality
    addCopyResultsFeature();
    
    // Add print functionality
    addPrintFeature();
}

// Animate score counting
function animateScore(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateScore(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentScore = start + (end - start) * easeOutQuart;
        
        element.textContent = currentScore.toFixed(1);
        
        if (progress < 1) {
            requestAnimationFrame(updateScore);
        } else {
            element.textContent = end.toFixed(1);
        }
    }
    
    requestAnimationFrame(updateScore);
}

// Utility functions
function showErrorMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

function resetSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Calculate AI Readiness Score';
    }
    
    if (loadingSpinner) {
        loadingSpinner.style.display = 'none';
    }
}

function addCopyResultsFeature() {
    const resultsContainer = document.querySelector('.container');
    if (!resultsContainer) return;
    
    const copyButton = document.createElement('button');
    copyButton.className = 'btn btn-outline-secondary btn-sm position-fixed';
    copyButton.style.cssText = 'bottom: 20px; left: 20px; z-index: 1000;';
    copyButton.innerHTML = '<i class="fas fa-copy me-2"></i>Copy Results';
    copyButton.title = 'Copy assessment results to clipboard';
    
    copyButton.addEventListener('click', function() {
        const resultsText = generateResultsText();
        navigator.clipboard.writeText(resultsText).then(function() {
            copyButton.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            copyButton.classList.replace('btn-outline-secondary', 'btn-success');
            
            setTimeout(() => {
                copyButton.innerHTML = '<i class="fas fa-copy me-2"></i>Copy Results';
                copyButton.classList.replace('btn-success', 'btn-outline-secondary');
            }, 2000);
        });
    });
    
    document.body.appendChild(copyButton);
}

function addPrintFeature() {
    const printButton = document.createElement('button');
    printButton.className = 'btn btn-outline-secondary btn-sm position-fixed';
    printButton.style.cssText = 'bottom: 20px; left: 180px; z-index: 1000;';
    printButton.innerHTML = '<i class="fas fa-print me-2"></i>Print';
    printButton.title = 'Print assessment results';
    
    printButton.addEventListener('click', function() {
        window.print();
    });
    
    document.body.appendChild(printButton);
}

function generateResultsText() {
    const companyName = document.querySelector('.lead').textContent;
    const overallScore = document.querySelector('.score-value .display-2').textContent;
    
    let resultsText = `AI Readiness Assessment Results\n`;
    resultsText += `Company: ${companyName}\n`;
    resultsText += `Overall Score: ${overallScore}/5.0\n\n`;
    
    // Add category scores
    const categoryCards = document.querySelectorAll('.category-score-card');
    if (categoryCards.length > 0) {
        resultsText += `Category Breakdown:\n`;
        categoryCards.forEach(card => {
            const categoryName = card.querySelector('h6').textContent;
            const score = card.querySelector('.fw-bold').textContent;
            resultsText += `- ${categoryName}: ${score}\n`;
        });
    }
    
    // Add recommendations
    const recommendations = document.querySelectorAll('.recommendation-card');
    if (recommendations.length > 0) {
        resultsText += `\nRecommendations:\n`;
        recommendations.forEach((rec, index) => {
            const title = rec.querySelector('h5').textContent;
            const description = rec.querySelector('p').textContent;
            resultsText += `${index + 1}. ${title}\n   ${description}\n`;
        });
    }
    
    return resultsText;
}

// Export functions for global use
window.AIReadinessApp = {
    scrollToCategory: window.scrollToCategory,
    submitAssessment,
    showErrorMessage,
    resetSubmitButton
};