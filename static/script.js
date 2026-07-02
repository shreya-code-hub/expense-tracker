document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------
    // 1. Dark Mode Setup
    // ----------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Check local storage or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        document.body.classList.add('dark-mode');
        if (themeIcon) themeIcon.className = 'bi bi-sun-fill';
    } else {
        document.body.classList.remove('dark-mode');
        if (themeIcon) themeIcon.className = 'bi bi-moon-fill';
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            if (themeIcon) {
                themeIcon.className = isDark ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
            }
            
            // Re-render or update charts to match current mode colors
            updateChartThemes(isDark);
        });
    }

    // ----------------------------
    // 2. Chart.js Implementation
    // ----------------------------
    const chartsDataEl = document.getElementById('charts-data');
    let categoryChart = null;
    let monthlyChart = null;

    function getChartThemeColors(isDark) {
        return {
            text: isDark ? '#94a3b8' : '#64748b',
            grid: isDark ? '#1f2937' : '#e2e8f0',
            border: isDark ? '#1f2937' : '#e2e8f0'
        };
    }

    function initCharts() {
        if (!chartsDataEl) return;

        // Parse data from template
        const categories = JSON.parse(chartsDataEl.getAttribute('data-categories') || '[]');
        const categoryAmounts = JSON.parse(chartsDataEl.getAttribute('data-category-amounts') || '[]');
        const months = JSON.parse(chartsDataEl.getAttribute('data-months') || '[]');
        const monthlyAmounts = JSON.parse(chartsDataEl.getAttribute('data-monthly-amounts') || '[]');

        const isDark = document.body.classList.contains('dark-mode');
        const colors = getChartThemeColors(isDark);

        // A nice modern color palette
        const palette = [
            '#6366f1', // Indigo
            '#10b981', // Emerald
            '#f59e0b', // Amber
            '#ef4444', // Rose
            '#3b82f6', // Blue
            '#8b5cf6', // Purple
            '#ec4899', // Pink
            '#14b8a6'  // Teal
        ];

        // --- Category spending Pie/Doughnut Chart ---
        const pieCtx = document.getElementById('categoryPieChart');
        if (pieCtx && categories.length > 0) {
            categoryChart = new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: categories,
                    datasets: [{
                        data: categoryAmounts,
                        backgroundColor: palette.slice(0, categories.length),
                        borderWidth: isDark ? 2 : 1,
                        borderColor: isDark ? '#111827' : '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: colors.text,
                                font: {
                                    family: 'Inter',
                                    size: 12
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return ` ${context.label}: ₹${context.raw.toFixed(2)}`;
                                }
                            }
                        }
                    },
                    cutout: '65%'
                }
            });
        }

        // --- Monthly trends Bar Chart ---
        const barCtx = document.getElementById('monthlyBarChart');
        if (barCtx && months.length > 0) {
            monthlyChart = new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Spending',
                        data: monthlyAmounts,
                        backgroundColor: '#6366f1',
                        borderRadius: 8,
                        hoverBackgroundColor: '#4f46e5'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return ` Spending: ₹${context.raw.toFixed(2)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: colors.text,
                                font: {
                                    family: 'Inter'
                                }
                            }
                        },
                        y: {
                            grid: {
                                color: colors.grid
                            },
                            border: {
                                dash: [5, 5]
                            },
                            ticks: {
                                color: colors.text,
                                font: {
                                    family: 'Inter'
                                },
                                callback: function(value) {
                                    return '₹' + value;
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    function updateChartThemes(isDark) {
        const colors = getChartThemeColors(isDark);

        if (categoryChart) {
            categoryChart.options.plugins.legend.labels.color = colors.text;
            categoryChart.data.datasets[0].borderColor = isDark ? '#111827' : '#ffffff';
            categoryChart.update();
        }

        if (monthlyChart) {
            monthlyChart.options.scales.x.ticks.color = colors.text;
            monthlyChart.options.scales.y.ticks.color = colors.text;
            monthlyChart.options.scales.y.grid.color = colors.grid;
            monthlyChart.update();
        }
    }

    // ----------------------------
    // 3. Interactive Animated Canvas Background
    // ----------------------------
    function initBackgroundAnimation() {
        const canvas = document.getElementById('bg-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        
        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });
        
        const isDarkTheme = () => document.body.classList.contains('dark-mode');
        
        // Icon classes
        class FloatingIcon {
            constructor(type, x, y) {
                this.type = type;
                this.x = x;
                this.y = y;
                this.size = Math.random() * 25 + 25; // 25px - 50px
                this.speedX = (Math.random() - 0.5) * 0.15;
                this.speedY = -(Math.random() * 0.15 + 0.1); // drift upwards
                this.rotation = Math.random() * Math.PI * 2;
                this.rotSpeed = (Math.random() - 0.5) * 0.003;
                this.pulseSpeed = Math.random() * 0.01 + 0.005;
                this.pulseTime = Math.random() * Math.PI * 2;
                this.opacity = Math.random() * 0.4 + 0.6; // multiplier
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                this.rotation += this.rotSpeed;
                this.pulseTime += this.pulseSpeed;
                
                // Wrap around edges
                if (this.y < -this.size) {
                    this.y = height + this.size;
                    this.x = Math.random() * width;
                }
                if (this.x < -this.size) this.x = width + this.size;
                if (this.x > width + this.size) this.x = -this.size;
            }
            
            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate(this.rotation);
                
                const isDark = true;
                const baseOpacity = 0.08;
                // Add soft pulse animation to opacity
                const pulseOpacity = baseOpacity * (1 + Math.sin(this.pulseTime) * 0.3) * this.opacity;
                
                // Choose color: green (emerald) or blue (indigo)
                const colorHash = (this.type.charCodeAt(0) % 2 === 0);
                if (colorHash) {
                    ctx.strokeStyle = `rgba(16, 185, 129, ${pulseOpacity})`; // Emerald green
                    ctx.shadowColor = `rgba(16, 185, 129, ${isDark ? 0.3 : 0.05})`;
                } else {
                    ctx.strokeStyle = `rgba(99, 102, 241, ${pulseOpacity})`; // Indigo blue
                    ctx.shadowColor = `rgba(99, 102, 241, ${isDark ? 0.3 : 0.05})`;
                }
                
                ctx.lineWidth = 1.5;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                
                if (isDark) {
                    ctx.shadowBlur = 10;
                } else {
                    ctx.shadowBlur = 0;
                }
                
                ctx.beginPath();
                
                const size = this.size;
                switch (this.type) {
                    case 'wallet':
                        ctx.strokeRect(-size/2, -size/3, size, size*0.7);
                        ctx.beginPath();
                        ctx.arc(size/2, 0, size*0.2, -Math.PI/2, Math.PI/2);
                        ctx.stroke();
                        break;
                    case 'coin':
                        ctx.arc(0, 0, size/2, 0, Math.PI*2);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.arc(0, 0, size/3, 0, Math.PI*2);
                        ctx.stroke();
                        break;
                    case 'card':
                        ctx.strokeRect(-size/2, -size/3, size, size*0.6);
                        ctx.beginPath();
                        ctx.moveTo(-size/2, -size/6);
                        ctx.lineTo(size/2, -size/6);
                        ctx.stroke();
                        break;
                    case 'bill':
                        ctx.strokeRect(-size/2, -size/3, size, size*0.6);
                        ctx.beginPath();
                        ctx.arc(0, 0, size/4, 0, Math.PI*2);
                        ctx.stroke();
                        break;
                    case 'pie':
                        ctx.arc(0, 0, size/2, 0, Math.PI*2);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(0, 0);
                        ctx.lineTo(0, -size/2);
                        ctx.moveTo(0, 0);
                        ctx.lineTo(size/2 * Math.cos(Math.PI/4), size/2 * Math.sin(Math.PI/4));
                        ctx.stroke();
                        break;
                    case 'bar':
                        ctx.strokeRect(-size/2, size/6, size*0.25, -size*0.4);
                        ctx.strokeRect(-size/6, size/6, size*0.25, -size*0.7);
                        ctx.strokeRect(size/6, size/6, size*0.25, -size*0.5);
                        break;
                    case 'line':
                        ctx.moveTo(-size/2, size/4);
                        ctx.lineTo(-size/6, -size/6);
                        ctx.lineTo(size/6, size/10);
                        ctx.lineTo(size/2, -size/3);
                        ctx.stroke();
                        break;
                }
                ctx.restore();
            }
        }
        
        // Particle class
        class Particle {
            constructor() {
                this.reset();
                this.y = Math.random() * height;
            }
            
            reset() {
                this.x = Math.random() * width;
                this.y = height + Math.random() * 20;
                this.size = Math.random() * 2 + 1;
                this.speedX = (Math.random() - 0.5) * 0.1;
                this.speedY = -(Math.random() * 0.2 + 0.15);
                this.alpha = Math.random() * 0.5 + 0.1;
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.y < -10 || this.x < -10 || this.x > width + 10) {
                    this.reset();
                }
            }
            
            draw() {
                const color = `rgba(16, 185, 129, ${this.alpha * 0.3})`;
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
                ctx.fill();
            }
        }
        
        // Spawn icons
        const iconTypes = ['wallet', 'coin', 'card', 'bill', 'pie', 'bar', 'line'];
        const numIcons = 12;
        const icons = [];
        for (let i = 0; i < numIcons; i++) {
            const type = iconTypes[i % iconTypes.length];
            icons.push(new FloatingIcon(type, Math.random() * width, Math.random() * height));
        }
        
        // Spawn particles
        const numParticles = 40;
        const particles = [];
        for (let i = 0; i < numParticles; i++) {
            particles.push(new Particle());
        }
        
        // Animation Loop
        function animate() {
            ctx.clearRect(0, 0, width, height);
            
            // Draw particles
            for (let p of particles) {
                p.update();
                p.draw();
            }
            
            // Draw floating icons
            for (let icon of icons) {
                icon.update();
                icon.draw();
            }
            
            requestAnimationFrame(animate);
        }
        
        animate();
    }

    // Run charts init and background animation
    initBackgroundAnimation();
    initCharts();
});
