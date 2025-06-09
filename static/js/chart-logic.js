document.addEventListener("DOMContentLoaded", function () {
    // Chart data
    const chart1Data = [                                        // histogram chart data
        { year: 2018, ad_spending_usd_m: 1.2, mobile_usd_m: 0.7, desktop_usd_m: 0.5, yoy_growth_percent: 0.12, mobile_share_percent: 0.58, desktop_share_percent: 0.42, spend_per_user_usd: 0.4 },
        { year: 2019, ad_spending_usd_m: 1.5, mobile_usd_m: 0.9, desktop_usd_m: 0.6, yoy_growth_percent: 0.25, mobile_share_percent: 0.6, desktop_share_percent: 0.4, spend_per_user_usd: 0.5 },
        { year: 2020, ad_spending_usd_m: 1.8, mobile_usd_m: 1.2, desktop_usd_m: 0.6, yoy_growth_percent: 0.2, mobile_share_percent: 0.67, desktop_share_percent: 0.33, spend_per_user_usd: 0.6 },
        { year: 2021, ad_spending_usd_m: 2.3, mobile_usd_m: 1.6, desktop_usd_m: 0.7, yoy_growth_percent: 0.28, mobile_share_percent: 0.7, desktop_share_percent: 0.3, spend_per_user_usd: 0.75 },
        { year: 2022, ad_spending_usd_m: 2.9, mobile_usd_m: 2.1, desktop_usd_m: 0.8, yoy_growth_percent: 0.26, mobile_share_percent: 0.72, desktop_share_percent: 0.28, spend_per_user_usd: 0.95 },
        { year: 2023, ad_spending_usd_m: 3.6, mobile_usd_m: 2.7, desktop_usd_m: 0.9, yoy_growth_percent: 0.24, mobile_share_percent: 0.75, desktop_share_percent: 0.25, spend_per_user_usd: 1.15 },
        { year: 2024, ad_spending_usd_m: 4.2, mobile_usd_m: 3.3, desktop_usd_m: 0.9, yoy_growth_percent: 0.17, mobile_share_percent: 0.79, desktop_share_percent: 0.21, spend_per_user_usd: 1.35 },
        { year: 2025, ad_spending_usd_m: 4.8, mobile_usd_m: 3.9, desktop_usd_m: 0.9, yoy_growth_percent: 0.14, mobile_share_percent: 0.81, desktop_share_percent: 0.19, spend_per_user_usd: 1.5 }
    ];

    const chart2Data = [                                        // histogram chart data
        { year: 2021, roi_percent: 3.2 },
        { year: 2023, roi_percent: 3.8 },
        { year: 2025, roi_percent: 4.0 }
    ];

    const chart3Data = [                                        // histogram chart data
        { platform: "Instagram", "2023": 850, "2024": 900, "2025": 950 },
        { platform: "Facebook", "2023": 650, "2024": 620, "2025": 600 },
        { platform: "TikTok", "2023": 500, "2024": 600, "2025": 700 },
        { platform: "YouTube", "2023": 400, "2024": 450, "2025": 500 },
        { platform: "Twitter/X", "2023": 150, "2024": 140, "2025": 130 }
    ];

    const chart4Data = [                                        // horizontal histogram chart data
        { age_group: "35+", male_percent: 0.03, female_percent: 0.05 },
        { age_group: "25–34", male_percent: 0.1, female_percent: 0.15 },
        { age_group: "18–24", male_percent: 0.2, female_percent: 0.25 },
        { age_group: "13–17", male_percent: 0.12, female_percent: 0.18 }
    ];

    const chart5Data = {                                        // pie chart data
        traffic_share_percent: {
            smartphones: 0.78,
            pcs_laptops: 0.18,
            tablets: 0.04,
            "4th_quarter_total": 1.2
        }
    };

    const chart6Data = [                                        // histogram chart data
        { platform: "Instagram", avg_er: 0.042, likes_comments: 0.035, clicks: 0.007 },
        { platform: "TikTok", avg_er: 0.081, likes_comments: 0.06, clicks: 0.021 },
        { platform: "Facebook", avg_er: 0.023, likes_comments: 0.018, clicks: 0.005 }
    ];

    const chart7Data = [                                        // pie chart data
        { niche: "Fashion & Beauty", percentage: 0.42 },
        { niche: "Food & Restaurants", percentage: 0.25 },
        { niche: "Travel", percentage: 0.15 },
        { niche: "Technology", percentage: 0.10 },
        { niche: "Finance", percentage: 0.08 }
    ];

    const chart8Data = [                                        // pie chart data
        { time_range: "18:00–22:00", engagement_peak: 0.45 },
        { time_range: "12:00–14:00", engagement_peak: 0.25 }
    ];

    const chart9Data = [                                        // pie chart data
        { language: "Armenian", engagement_peak: 0.65 },
        { language: "Russian", engagement_peak: 0.25 },
        { language: "English", engagement_peak: 0.10 }
    ];

    const chart10Data = [                                        // pie chart data
        { monetization_type: "Paid Posts", share: 0.45 },
        { monetization_type: "Barter", share: 0.30 },
        { monetization_type: "Affiliate", share: 0.20 },
        { monetization_type: "Others", share: 0.05 }
    ];

    const chart11Data = [                                        // histogram chart data
        { platform: "Instagram", fake_followers: 0.12, suspicious_engagement: 0.08 },
        { platform: "TikTok", fake_followers: 0.09, suspicious_engagement: 0.06 },
        { platform: "Facebook", fake_followers: 0.15, suspicious_engagement: 0.10 },
        { platform: "YouTube", fake_followers: 0.07, suspicious_engagement: 0.05 }
    ];
    const chart12Data = [                                        // histogram chart data                           
        { group: "13–17", female: 0.18, male: 0.12, urban: 0.85, rural: 0.15, top_device: 0 },
        { group: "18–24", female: 0.25, male: 0.20, urban: 0.78, rural: 0.22, top_device: 0 },
        { group: "25–34", female: 0.15, male: 0.10, urban: 0.70, rural: 0.30, top_device: 0 },
        { group: "YouTube", female: 0.07, male: 0.05, urban: 0, rural: 0, top_device: 0 }
    ];
    const chart13Data = [                                        // histogram chart data
        {
            content_type: "Reels/Short Videos",
            avg_engagement_rate: 0.081,
            reach: 0.72,
            video_completion: 0.65,
            ctr: 0.042,
            story_completion: 0
        },
        {
            content_type: "Static Posts",
            avg_engagement_rate: 0.042,
            reach: 0.58,
            video_completion: 0,
            ctr: 0.035,
            story_completion: 0
        },
        {
            content_type: "Stories",
            avg_engagement_rate: 0.038,
            reach: 0.64,
            video_completion: 0,
            ctr: 0,
            story_completion: 0.68
        },
        {
            content_type: "Live Streams",
            avg_engagement_rate: 0.065,
            reach: 0.47,
            video_completion: 0.52,
            ctr: 0.029,
            story_completion: 0
        }
    ];
    const chart14Data = [                                        // histogram chart data
        {
            group: "13–17",
            female: 0.18,
            male: 0.12,
            urban: 0.85,
            rural: 0.15,
            mobile: 0.95
        },
        {
            group: "18–24",
            female: 0.25,
            male: 0.20,
            urban: 0.78,
            rural: 0.22,
            mobile: 0.92
        },
        {
            group: "25–34",
            female: 0.15,
            male: 0.10,
            urban: 0.70,
            rural: 0.30,
            mobile: 0.83
        },
        {
            group: "Live Streams",
            female: 0.065,
            male: 0.47,
            urban: 0.52,
            rural: 0.029,
            mobile: 0
        }
    ];
    const chart15Data = [                                        // histogram chart data
        {
            tier: "Nano",
            avg_ctr: 0.052,
            conversion_rate: 0.031
        },
        {
            tier: "Micro",
            avg_ctr: 0.048,
            conversion_rate: 0.028
        },
        {
            tier: "Macro",
            avg_ctr: 0.039,
            conversion_rate: 0.022
        },
        {
            tier: "Mega",
            avg_ctr: 0.027,
            conversion_rate: 0.015
        }
    ];
    const chart16Data = [                                        // histogram chart data
        {
            year: 2018,
            instagram_reels: 8200,
            tiktok: 12500,
            youtube_shorts: 6800,
            facebook_video: 5400
        },
        {
            year: 2019,
            instagram_reels: 9700,
            tiktok: 18300,
            youtube_shorts: 8100,
            facebook_video: 6200
        },
        {
            year: 2020,
            instagram_reels: 12500,
            tiktok: 24600,
            youtube_shorts: 9900,
            facebook_video: 7800
        },
        {
            year: 2021,
            instagram_reels: 15200,
            tiktok: 31400,
            youtube_shorts: 12300,
            facebook_video: 9100
        },
        {
            year: 2022,
            instagram_reels: 18700,
            tiktok: 42800,
            youtube_shorts: 15600,
            facebook_video: 11200
        },
        {
            year: 2023,
            instagram_reels: 22400,
            tiktok: 53200,
            youtube_shorts: 19800,
            facebook_video: 13500
        },
        {
            year: 2024,
            instagram_reels: 25100,
            tiktok: 61700,
            youtube_shorts: 23400,
            facebook_video: 15200
        },
        {
            year: 2025,
            instagram_reels: 27900,
            tiktok: 68300,
            youtube_shorts: 26100,
            facebook_video: 16800
        }
    ];
    const chart17Data = [                                        // pie chart data
        { category: "Comedy", avg_vtr: 0.76 },
        { category: "Beauty Hacks", avg_vtr: 0.63 },
        { category: "Food/Travel", avg_vtr: 0.59 },
        { category: "Tech Reviews", avg_vtr: 0.52 },
        { category: "Fitness", avg_vtr: 0.48 }
    ];
    const chart18Data = [                                        // histogram chart data
        {
            duration: "15–30 sec",
            tiktok: 0.82,
            instagram: 0.78,
            youtube: 0.75
        },
        {
            duration: "30–60 sec",
            tiktok: 0.68,
            instagram: 0.62,
            youtube: 0.58
        },
        {
            duration: "1–2 min",
            tiktok: 0.45,
            instagram: 0.38,
            youtube: 0.52
        },
        {
            duration: "2–5 min",
            tiktok: 0.28,
            instagram: 0.22,
            youtube: 0.41
        }
    ];



    // Initialize charts
    function initializeCharts() {
        // Chart 1: Ad Spending Trends
        const ctx1 = document.getElementById('chart1').getContext('2d');
        const chart1 = new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: chart1Data.map(item => item.year),
                datasets: [
                    {
                        label: 'Total Ad Spending (USD M)',
                        data: chart1Data.map(item => item.ad_spending_usd_m),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Mobile Ad Spending (USD M)',
                        data: chart1Data.map(item => item.mobile_usd_m),
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Desktop Ad Spending (USD M)',
                        data: chart1Data.map(item => item.desktop_usd_m),
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'YoY Growth (%)',
                        data: chart1Data.map(item => item.yoy_growth_percent * 100),
                        backgroundColor: 'rgba(153, 102, 255, 0.7)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1,
                        type: 'line',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'USD (Millions)'
                        }
                    },
                    y1: {
                        position: 'right',
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.datasetIndex === 3) {
                                    label += context.raw.toFixed(1) + '%';
                                } else {
                                    label += '$' + context.raw.toFixed(1) + 'M';
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
        // Chart 2: ROI Over Years
        const ctx2 = document.getElementById('chart2').getContext('2d');
        const chart2 = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: chart2Data.map(item => item.year),
                datasets: [{
                    label: 'ROI (%)',
                    data: chart2Data.map(item => item.roi_percent),
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 3,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 3,
                        title: {
                            display: true,
                            text: 'ROI (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return 'ROI: ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        // Chart 3: Platform Engagement
        const ctx3 = document.getElementById('chart3').getContext('2d');
        const chart3 = new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: chart3Data.map(item => item.platform),
                datasets: [
                    {
                        label: '2023',
                        data: chart3Data.map(item => item["2023"]),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: '2024',
                        data: chart3Data.map(item => item["2024"]),
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: '2025',
                        data: chart3Data.map(item => item["2025"]),
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Users (Millions)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Platform'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.dataset.label + ': ' + context.raw + 'M users';
                            }
                        }
                    }
                }
            }
        });
        // Chart 4: Age and Gender Distribution
        const ctx4 = document.getElementById('chart4').getContext('2d');
        const chart4 = new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: chart4Data.map(item => item.age_group),
                datasets: [
                    {
                        label: 'Male (%)',
                        data: chart4Data.map(item => item.male_percent * 100),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Female (%)',
                        data: chart4Data.map(item => item.female_percent * 100),
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Age Group'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        // Chart 5: Traffic Share
        const ctx5 = document.getElementById('chart5').getContext('2d');
        const chart5 = new Chart(ctx5, {
            type: 'doughnut',
            data: {
                labels: ['Smartphones', 'PCs/Laptops', 'Tablets'],
                datasets: [{
                    data: [
                        chart5Data.traffic_share_percent.smartphones * 100,
                        chart5Data.traffic_share_percent.pcs_laptops * 100,
                        chart5Data.traffic_share_percent.tablets * 100
                    ],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(75, 192, 192, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Total Traffic Share: 120% (Multiple devices possible)',
                        position: 'bottom'
                    }
                }
            }
        });
        // Chart 6: Engagement Rates by Platform
        const ctx6 = document.getElementById('chart6').getContext('2d');
        const chart6 = new Chart(ctx6, {
            type: 'bar',
            data: {
                labels: chart6Data.map(item => item.platform),
                datasets: [
                    {
                        label: 'Average Engagement Rate',
                        data: chart6Data.map(item => item.avg_er * 100),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Likes/Comments Rate',
                        data: chart6Data.map(item => item.likes_comments * 100),
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Click Rate',
                        data: chart6Data.map(item => item.clicks * 100),
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Platform'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        // Chart 7: Niche Distribution
        const ctx7 = document.getElementById('chart7').getContext('2d');
        const chart7 = new Chart(ctx7, {
            type: 'pie',
            data: {
                labels: chart7Data.map(item => item.niche),
                datasets: [{
                    data: chart7Data.map(item => item.percentage * 100),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw.toFixed(1)}%`
                        }
                    }
                }
            }
        });
        // Chart 8: Engagement Peak by Time
        const ctx8 = document.getElementById('chart8').getContext('2d');
        const chart8 = new Chart(ctx8, {
            type: 'doughnut',
            data: {
                labels: chart8Data.map(item => item.time_range),
                datasets: [{
                    data: chart8Data.map(item => item.engagement_peak * 100),
                    backgroundColor: ['#36A2EB', '#FFCE56'],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw.toFixed(1)}%`
                        }
                    }
                }
            }
        });
        // Chart 9: Engagement by Language
        const ctx9 = document.getElementById('chart9').getContext('2d');
        const chart9 = new Chart(ctx9, {
            type: 'pie',
            data: {
                labels: chart9Data.map(item => item.language),
                datasets: [{
                    data: chart9Data.map(item => item.engagement_peak * 100),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw.toFixed(1)}%`
                        }
                    }
                }
            }
        });
        // Chart 10: Monetization Types
        const ctx10 = document.getElementById('chart10').getContext('2d');
        const chart10 = new Chart(ctx10, {
            type: 'pie',
            data: {
                labels: chart10Data.map(item => item.monetization_type),
                datasets: [{
                    data: chart10Data.map(item => item.share * 100),
                    backgroundColor: ['#4BC0C0', '#FF6384', '#FFCE56', '#36A2EB'],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw.toFixed(1)}%`
                        }
                    }
                }
            }
        });
        // Chart 11: Fake Followers vs. Suspicious Engagement
        const ctx11 = document.getElementById('chart11').getContext('2d');
        const chart11 = new Chart(ctx11, {
            type: 'bar',
            data: {
                labels: chart11Data.map(d => d.platform),
                datasets: [
                    {
                        label: 'Fake Followers (%)',
                        data: chart11Data.map(d => d.fake_followers * 100),
                        backgroundColor: '#FF6384'
                    },
                    {
                        label: 'Suspicious Engagement (%)',
                        data: chart11Data.map(d => d.suspicious_engagement * 100),
                        backgroundColor: '#36A2EB'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Percentage (%)' }
                    }
                }
            }
        });
        // Chart 12: Demographic Breakdown
        const ctx12 = document.getElementById('chart12').getContext('2d');
        const chart12 = new Chart(ctx12, {
            type: 'bar',
            data: {
                labels: chart12Data.map(d => d.group),
                datasets: [
                    {
                        label: 'Female (%)',
                        data: chart12Data.map(d => d.female * 100),
                        backgroundColor: '#FF6384'
                    },
                    {
                        label: 'Male (%)',
                        data: chart12Data.map(d => d.male * 100),
                        backgroundColor: '#36A2EB'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Percentage (%)' }
                    }
                }
            }
        });
        // Chart 13: Content Type Performance
        const ctx13 = document.getElementById('chart13').getContext('2d');
        const chart13 = new Chart(ctx13, {
            type: 'bar',
            data: {
                labels: chart13Data.map(d => d.content_type),
                datasets: [
                    {
                        label: 'Avg Engagement Rate (%)',
                        data: chart13Data.map(d => d.avg_engagement_rate * 100),
                        backgroundColor: '#FF6384'
                    },
                    {
                        label: 'Reach (%)',
                        data: chart13Data.map(d => d.reach * 100),
                        backgroundColor: '#36A2EB'
                    },
                    {
                        label: 'Video Completion (%)',
                        data: chart13Data.map(d => d.video_completion * 100),
                        backgroundColor: '#FFCE56'
                    },
                    {
                        label: 'CTR (%)',
                        data: chart13Data.map(d => d.ctr * 100),
                        backgroundColor: '#4BC0C0'
                    },
                    {
                        label: 'Story Completion (%)',
                        data: chart13Data.map(d => d.story_completion * 100),
                        backgroundColor: '#9966FF'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Percentage (%)' }
                    }
                }
            }
        });
        // Chart 14: Device Usage and Demographics
        const ctx14 = document.getElementById('chart14').getContext('2d');
        const chart14 = new Chart(ctx14, {
            type: 'bar',
            data: {
                labels: chart14Data.map(d => d.group),
                datasets: [
                    {
                        label: 'Mobile Usage (%)',
                        data: chart14Data.map(d => d.mobile * 100),
                        backgroundColor: '#36A2EB'
                    },
                    {
                        label: 'Urban (%)',
                        data: chart14Data.map(d => d.urban * 100),
                        backgroundColor: '#4BC0C0'
                    },
                    {
                        label: 'Rural (%)',
                        data: chart14Data.map(d => d.rural * 100),
                        backgroundColor: '#FFCE56'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Percentage (%)' }
                    }
                }
            }
        });
        // Chart 15: CTR and Conversion by Influencer Tier
        const ctx15 = document.getElementById('chart15').getContext('2d');
        const chart15 = new Chart(ctx15, {
            type: 'bar',
            data: {
                labels: chart15Data.map(d => d.tier),
                datasets: [
                    {
                        label: 'Avg CTR (%)',
                        data: chart15Data.map(d => d.avg_ctr * 100),
                        backgroundColor: '#36A2EB'
                    },
                    {
                        label: 'Conversion Rate (%)',
                        data: chart15Data.map(d => d.conversion_rate * 100),
                        backgroundColor: '#FF6384'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Percentage (%)' }
                    }
                }
            }
        });
        // Chart 16: Platform Growth Over Time
        const ctx16 = document.getElementById('chart16').getContext('2d');
        const chart16 = new Chart(ctx16, {
            type: 'line',
            data: {
                labels: chart16Data.map(d => d.year),
                datasets: [
                    {
                        label: 'Instagram Reels',
                        data: chart16Data.map(d => d.instagram_reels),
                        borderColor: '#36A2EB',
                        fill: false
                    },
                    {
                        label: 'TikTok',
                        data: chart16Data.map(d => d.tiktok),
                        borderColor: '#FF6384',
                        fill: false
                    },
                    {
                        label: 'YouTube Shorts',
                        data: chart16Data.map(d => d.youtube_shorts),
                        borderColor: '#FFCE56',
                        fill: false
                    },
                    {
                        label: 'Facebook Video',
                        data: chart16Data.map(d => d.facebook_video),
                        borderColor: '#4BC0C0',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Videos (K)' }
                    }
                }
            }
        });
        // Chart 17: Video Completion by Category
        const ctx17 = document.getElementById('chart17').getContext('2d');
        const chart17 = new Chart(ctx17, {
            type: 'pie',
            data: {
                labels: chart17Data.map(d => d.category),
                datasets: [{
                    data: chart17Data.map(d => d.avg_vtr * 100),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw.toFixed(1)}%`
                        }
                    }
                }
            }
        });
        // Chart 18: Platform Performance by Video Duration
        const ctx18 = document.getElementById('chart18').getContext('2d');
        const chart18 = new Chart(ctx18, {
            type: 'bar',
            data: {
                labels: chart18Data.map(d => d.duration),
                datasets: [
                    {
                        label: 'TikTok (%)',
                        data: chart18Data.map(d => d.tiktok * 100),
                        backgroundColor: '#FF6384'
                    },
                    {
                        label: 'Instagram (%)',
                        data: chart18Data.map(d => d.instagram * 100),
                        backgroundColor: '#36A2EB'
                    },
                    {
                        label: 'YouTube (%)',
                        data: chart18Data.map(d => d.youtube * 100),
                        backgroundColor: '#FFCE56'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Completion Rate (%)' }
                    }
                }
            }
        });

        return [chart1, chart2, chart3, chart4, chart5, chart6, chart7, chart8, chart9, chart10, chart11, chart12, chart13, chart14, chart15, chart16, chart17, chart18];
    }

    // Chart navigation functionality
    const chartContainers = document.querySelectorAll('.chart-container');
    const navDotsContainer = document.querySelector('.chart-navigation');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    let currentIndex = 0;
    let autoSlideInterval;
    let charts = [];

    // Create navigation dots
    chartContainers.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('nav-dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
            goToChart(index);
        });
        navDotsContainer.appendChild(dot);
    });

    const navDots = document.querySelectorAll('.nav-dot');

    function updateNavigation() {
        chartContainers.forEach((container, index) => {
            container.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
        });

        navDots.forEach((dot, index) => {
            if (index === currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    function goToChart(index) {
        if (index < 0) index = chartContainers.length - 1;
        if (index >= chartContainers.length) index = 0;

        currentIndex = index;
        updateNavigation();
        resetAutoSlide();
    }

    function nextChart() {
        goToChart(currentIndex + 1);
    }

    function prevChart() {
        goToChart(currentIndex - 1);
    }

    function startAutoSlide() {
        autoSlideInterval = setInterval(nextChart, 5000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Event listeners
    nextBtn.addEventListener('click', nextChart);
    prevBtn.addEventListener('click', prevChart);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            nextChart();
        } else if (e.key === 'ArrowLeft') {
            prevChart();
        }
    });

    // Initialize charts and navigation
    charts = initializeCharts();
    updateNavigation();
    startAutoSlide();

    // Resize charts when window resizes
    window.addEventListener('resize', function () {
        charts.forEach(chart => {
            if (chart) chart.resize();
        });
    });
});